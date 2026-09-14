# -*- coding: utf-8 -*-
"""申报书标题格式处理工具(可复用)
对已生成内容的申报书,应用阜阳师范大创的标题格式规范:
- 一级标题(一、二、三): 母版不变
- 二级标题((一)(二)): 宋体小四加粗 + 首行缩进2字符 + 1.5倍行距
- 三级标题(1. 2. 3.): 宋体小四加粗 + 首行缩进2字符 + 1.5倍行距
- 四级标题(研究内容X): 宋体小四不加粗 + 首行缩进2字符 + 1.5倍行距
- 正文: 宋体小四 + 首行缩进2字符 + 1.5倍行距
用法: python format_apply.py <输入.docx> [输出.docx]
"""
import sys, re
from docx import Document
from docx.shared import Pt
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

# 正文所在的表格行(阜阳师范母版: 行17-21)
BODY_ROWS = [17, 18, 19, 20, 21]

def set_indent(paragraph, chars=2):
    pPr = paragraph._p.get_or_add_pPr()
    ind = pPr.find(qn('w:ind'))
    if ind is None:
        ind = OxmlElement('w:ind')
        pPr.append(ind)
    ind.set(qn('w:firstLineChars'), str(chars * 100))
    ind.set(qn('w:firstLine'), str(int(chars * 240)))

def is_h2(txt):
    return bool(re.match(r'^[（(][一二三四五六七八九十]+[）)]', txt))

def is_h3(txt):
    """三级标题: '1. 标题' 或 '1. 小标题:正文'"""
    return bool(re.match(r'^[1-9]\.', txt))

def is_h4(txt):
    """四级标题: '研究内容一:xxx' 或 '研究内容一:xxx:正文'"""
    return bool(re.match(r'^研究内容[一二三四五]', txt))

def is_subhead_paragraph(txt):
    """分点段落(正文里的'1. xxx:yyy'或'(1) xxx:yyy'): 只加粗编号+小标题部分"""
    # 数字. 小标题:描述
    if re.match(r'^\d+\.\s*[^：:]+[：:]\s*\S', txt):
        return True
    # (数字) 小标题:描述
    if re.match(r'^[（(]\d+[）)]\s*[^：:]+[：:]\s*\S', txt):
        return True
    return False

def apply_format(input_path, output_path=None):
    output_path = output_path or input_path
    doc = Document(input_path)
    MT = doc.tables[1]

    for row_id in BODY_ROWS:
        cell = MT.cell(row_id, 0)
        ps = cell.paragraphs

        # 第一个段落是一级标题(母版原有),跳过
        new_items = []  # (text, kind, body_subhead) — body_subhead: 子标题部分(用于部分加粗)
        for i in range(1, len(ps)):
            txt = ps[i].text.strip()
            if not txt:
                continue

            if is_h2(txt):
                new_items.append((txt, 'h2', None))
            elif is_h3(txt):
                # 三级标题: "1. 标题" 或 "1. 小标题:正文"
                m = re.match(r'^([1-9]\.\s*[^。]+。)(.*)$', txt)
                if m:
                    new_items.append((m.group(1).strip(), 'h3', None))
                    if m.group(2).strip():
                        new_items.append((m.group(2).strip(), 'body', None))
                else:
                    new_items.append((txt, 'h3', None))
            elif is_h4(txt):
                m = re.match(r'^(研究内容[一二三四五][:：][^。]+。)(.*)$', txt)
                if m:
                    new_items.append((m.group(1).strip(), 'h4', None))
                    if m.group(2).strip():
                        new_items.append((m.group(2).strip(), 'body', None))
                else:
                    new_items.append((txt, 'h4', None))
            elif is_subhead_paragraph(txt):
                # 分点段落: 编号+小标题:描述 → 加粗标题部分
                m = re.match(r'^(\d+\.\s*[^：:]+[：:]\s*)(.*)$', txt)
                if not m:
                    m = re.match(r'^([（(]\d+[）)]\s*[^：:]+[：:]\s*)(.*)$', txt)
                if m:
                    new_items.append((m.group(1).strip(), 'subhead', m.group(2).strip()))
                else:
                    new_items.append((txt, 'body', None))
            else:
                new_items.append((txt, 'body', None))

        # 删除第一个段落(一级标题)之后的所有段落
        tc = cell._tc
        p_elements = tc.findall(qn('w:p'))
        for pe in p_elements[1:]:
            tc.remove(pe)

        # 重新追加格式化段落
        for item in new_items:
            text = item[0]; kind = item[1]
            body_sub = item[2] if len(item) > 2 else None

            p_el = OxmlElement('w:p')
            tc.append(p_el)
            p = cell.paragraphs[-1]
            p.paragraph_format.line_spacing = 1.5
            set_indent(p, 2)

            if kind == 'subhead':
                # 分点段落: 加粗子标题 + 不加粗描述(两个 run)
                if text:
                    r1 = p.add_run(text)
                    r1.font.name = '宋体'; r1._element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')
                    r1.font.size = Pt(12); r1.bold = True
                if body_sub:
                    r2 = p.add_run(body_sub)
                    r2.font.name = '宋体'; r2._element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')
                    r2.font.size = Pt(12); r2.bold = False
            else:
                r = p.add_run(text)
                r.font.name = '宋体'; r._element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')
                r.font.size = Pt(12); r.bold = (kind in ('h2', 'h3'))

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
