# -*- coding: utf-8 -*-
"""申报书标题格式处理工具(池州学院大创版)
对已生成内容的申报书,应用池州学院大创的标题格式规范:
- 字体: 仿宋(区别于阜阳的宋体)
- 一级标题(一/二/三...): 四号(14pt)加粗(按母版)
- 二级标题((一)(二)): 仿宋小四加粗 + 首行缩进2字符 + 1.5倍行距
- 三级标题(1. 2. 3.): 仿宋小四加粗 + 首行缩进2字符 + 1.5倍行距
- 阶段标题(第一阶段~第四阶段): 仿宋小四加粗 + 首行缩进2字符 + 1.5倍行距
- 正文: 仿宋小四 + 首行缩进2字符 + 1.5倍行距
- 分点段落(1. 小标题:描述): 编号+小标题加粗,描述不加粗
用法: python format_apply.py <输入.docx> [输出.docx]
"""
import sys, re
from docx import Document
from docx.shared import Pt
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

# 池州学院母版结构(4表):
#   表0: 项目编号 (不动)
#   表1: 封面信息 7×2 (不动)
#   表2: 项目信息+团队+指导教师 15×9 (不动)
#   表3: 正文 5×1 (合并单元格,本脚本处理对象)
#     行0: 一~六章正文 (要处理)
#     行1: 七、经费预算 (要处理)
#     行2-4: 八/九/十 签字栏 (不动)
BODY_CELLS = [(3, 0), (3, 1)]  # (table_idx, row_idx)

FONT = '仿宋'

def set_indent(paragraph, chars=2):
    pPr = paragraph._p.get_or_add_pPr()
    ind = pPr.find(qn('w:ind'))
    if ind is None:
        ind = OxmlElement('w:ind'); pPr.append(ind)
    ind.set(qn('w:firstLineChars'), str(chars * 100))
    ind.set(qn('w:firstLine'), str(int(chars * 240)))

def is_h2(txt):
    """二级标题: (一)(二)(三)... 或（一）（二）"""
    return bool(re.match(r'^[（(][一二三四五六七八九十]+[）)]', txt))

def is_h3(txt):
    """三级标题: 1. 标题 或 1. 小标题:正文"""
    return bool(re.match(r'^[1-9]\.', txt))

def is_stage(txt):
    """阶段标题: 第一阶段~第四阶段"""
    return bool(re.match(r'^第[一二三四]阶段', txt))

def is_subhead_paragraph(txt):
    """分点段落(1. xxx:yyy 或 (1) xxx:yyy): 加粗编号+小标题"""
    if re.match(r'^\d+\.\s*[^：:]+[：:]\s*\S', txt):
        return True
    if re.match(r'^[（(]\d+[）)]\s*[^：:]+[：:]\s*\S', txt):
        return True
    return False

def classify_para(txt):
    """分类段落"""
    if is_h2(txt):
        return 'h2', None
    elif is_h3(txt):
        # 三级标题可能和正文混在一段,如"1. 标题。正文"
        m = re.match(r'^([1-9]\.\s*[^。]+。)(.*)$', txt)
        if m:
            return 'h3_with_body', (m.group(1).strip(), m.group(2).strip())
        return 'h3', None
    elif is_stage(txt):
        return 'stage', None
    elif is_subhead_paragraph(txt):
        m = re.match(r'^(\d+\.\s*[^：:]+[：:]\s*)(.*)$', txt)
        if not m:
            m = re.match(r'^([（(]\d+[）)]\s*[^：:]+[：:]\s*)(.*)$', txt)
        if m:
            return 'subhead', (m.group(1).strip(), m.group(2).strip())
        return 'body', None
    else:
        return 'body', None

def apply_format(input_path, output_path=None):
    output_path = output_path or input_path
    doc = Document(input_path)

    for ti, ri in BODY_CELLS:
        t = doc.tables[ti]
        cell = t.cell(ri, 0)
        ps = cell.paragraphs
        tc = cell._tc

        # 第一个段落是一级标题(母版原有,如"一、项目实施的目的、意义"),跳过
        # 收集后续段落信息
        new_items = []
        for i in range(1, len(ps)):
            txt = ps[i].text.strip()
            if not txt:
                continue
            kind, extra = classify_para(txt)
            new_items.append((txt, kind, extra))

        # 删除第一个段落之后的所有段落
        p_elements = tc.findall(qn('w:p'))
        for pe in p_elements[1:]:
            tc.remove(pe)

        # 重新追加格式化段落
        for text, kind, extra in new_items:
            p_el = OxmlElement('w:p')
            tc.append(p_el)
            p = cell.paragraphs[-1]
            p.paragraph_format.line_spacing = 1.5
            set_indent(p, 2)

            if kind == 'h3_with_body':
                # 三级标题和正文拆分: 加粗标题 + 不加粗正文(两个 run)
                title, body = extra
                if title:
                    r1 = p.add_run(title)
                    r1.font.name = FONT; r1._element.rPr.rFonts.set(qn('w:eastAsia'), FONT)
                    r1.font.size = Pt(12); r1.bold = True
                if body:
                    r2 = p.add_run(body)
                    r2.font.name = FONT; r2._element.rPr.rFonts.set(qn('w:eastAsia'), FONT)
                    r2.font.size = Pt(12); r2.bold = False
            elif kind == 'subhead':
                # 分点段落: 加粗子标题 + 不加粗描述
                title, body = extra
                if title:
                    r1 = p.add_run(title)
                    r1.font.name = FONT; r1._element.rPr.rFonts.set(qn('w:eastAsia'), FONT)
                    r1.font.size = Pt(12); r1.bold = True
                if body:
                    r2 = p.add_run(body)
                    r2.font.name = FONT; r2._element.rPr.rFonts.set(qn('w:eastAsia'), FONT)
                    r2.font.size = Pt(12); r2.bold = False
            else:
                r = p.add_run(text)
                r.font.name = FONT; r._element.rPr.rFonts.set(qn('w:eastAsia'), FONT)
                r.font.size = Pt(12)
                r.bold = (kind in ('h2', 'h3', 'stage'))

    doc.save(output_path)
    return output_path

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("用法: python format_apply.py <输入.docx> [输出.docx]")
        sys.exit(1)
    inp = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else inp
    result = apply_format(inp, out)
    print(f"格式处理完成: {result}")
