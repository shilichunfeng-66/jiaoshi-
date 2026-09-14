# -*- coding: utf-8 -*-
"""运动康复 Plus 版 — 组装写入新 docx
基于 v1 docx，清空表3行0，按池州学院规范写入优化内容，插入8张图。
"""
import shutil, re
from docx import Document
from docx.shared import Cm, Pt
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from docx.enum.text import WD_ALIGN_PARAGRAPH

SRC = r'D:/科研文件/schools/池州学院/大创/母版_申报书.docx'
DST = r'D:/科研文件/outputs/池州学院_大创申报书_运动康复_v3_plus.docx'
CONTENT_TXT = r'D:/科研文件/outputs/_优化正文_plus.txt'
# 项目名称(自动填写到表2信息表行0列1) — 修改此处即可更换题目
TOPIC = '\u201c十五五\u201d规划背景下运动康复的政策演进与发展趋势研究'

shutil.copy2(SRC, DST)
doc = Document(DST)
cell = doc.tables[3].cell(0, 0)
tc = cell._tc

# === 清空表3行0所有段落 ===
for p in list(tc.findall(qn('w:p'))):
    tc.remove(p)

# === 工具：构建带格式的段落 ===
FONT = '仿宋'
FONT_CAPTION = '宋体'
SZ_H1 = 28   # 四号 14pt = 28 半磅
SZ_BODY = 24 # 小四 12pt = 24 半磅
SZ_CAP = 21  # 小五 10.5pt = 21 半磅

def _set_run_fonts(rPr, font, size_half, bold=False):
    rf = OxmlElement('w:rFonts')
    rf.set(qn('w:eastAsia'), font)
    rf.set(qn('w:ascii'), 'Times New Roman')
    rf.set(qn('w:hAnsi'), 'Times New Roman')
    rPr.append(rf)
    if bold:
        b = OxmlElement('w:b'); rPr.append(b)
        bcs = OxmlElement('w:bCs'); rPr.append(bcs)
    sz = OxmlElement('w:sz'); sz.set(qn('w:val'), str(size_half)); rPr.append(sz)
    szcs = OxmlElement('w:szCs'); szcs.set(qn('w:val'), str(size_half)); rPr.append(szcs)

def _set_para_format(pPr, indent=True, line=360, space_before=120, space_after=120):
    sp = OxmlElement('w:spacing')
    sp.set(qn('w:line'), str(line)); sp.set(qn('w:lineRule'), 'auto')
    sp.set(qn('w:before'), str(space_before)); sp.set(qn('w:after'), str(space_after))
    pPr.append(sp)
    if indent:
        ind = OxmlElement('w:ind')
        ind.set(qn('w:firstLineChars'), '200')
        ind.set(qn('w:firstLine'), '480')
        pPr.append(ind)

def make_para(text, kind='body'):
    p = OxmlElement('w:p')
    pPr = OxmlElement('w:pPr'); p.append(pPr)
    if kind == 'h1':
        # 一级标题不加粗（按之前生成）或不加粗
        # 池州规范：一级标题"按母版不变"——不缩进，仿宋四号
        # 这里我加粗以便视觉清晰
        _set_para_format(pPr, indent=False, line=360, space_before=160, space_after=100)
        r = OxmlElement('w:r'); rPr = OxmlElement('w:rPr')
        _set_run_fonts(rPr, FONT, SZ_H1, bold=True)
        r.append(rPr)
        t = OxmlElement('w:t'); t.text = text; t.set(qn('xml:space'), 'preserve'); r.append(t)
        p.append(r)
    elif kind == 'caption':
        # 图注：宋体小五 居中
        jc = OxmlElement('w:jc'); jc.set(qn('w:val'), 'center'); pPr.append(jc)
        _set_para_format(pPr, indent=False, line=300, space_before=60, space_after=120)
        r = OxmlElement('w:r'); rPr = OxmlElement('w:rPr')
        _set_run_fonts(rPr, FONT_CAPTION, SZ_CAP, bold=False)
        r.append(rPr)
        t = OxmlElement('w:t'); t.text = text; t.set(qn('xml:space'), 'preserve'); r.append(t)
        p.append(r)
    elif kind == 'subhead':
        # 分点段落：编号+小标题+冒号 加粗，描述不加粗
        _set_para_format(pPr, indent=True, line=360, space_before=80, space_after=80)
        m = re.match(r'^(\d+[\.、]\s*[^：:]+[：:]\s*)(.*)$', text)
        if m:
            bold_part, rest = m.group(1), m.group(2)
            r1 = OxmlElement('w:r'); rPr1 = OxmlElement('w:rPr')
            _set_run_fonts(rPr1, FONT, SZ_BODY, bold=True)
            r1.append(rPr1)
            t1 = OxmlElement('w:t'); t1.text = bold_part; t1.set(qn('xml:space'), 'preserve'); r1.append(t1)
            p.append(r1)
            if rest:
                r2 = OxmlElement('w:r'); rPr2 = OxmlElement('w:rPr')
                _set_run_fonts(rPr2, FONT, SZ_BODY, bold=False)
                r2.append(rPr2)
                t2 = OxmlElement('w:t'); t2.text = rest; t2.set(qn('xml:space'), 'preserve'); r2.append(t2)
                p.append(r2)
        else:
            r = OxmlElement('w:r'); rPr = OxmlElement('w:rPr')
            _set_run_fonts(rPr, FONT, SZ_BODY, bold=False)
            r.append(rPr)
            t = OxmlElement('w:t'); t.text = text; t.set(qn('xml:space'), 'preserve'); r.append(t)
            p.append(r)
    else:
        # h2/h3 加粗，body 不加粗
        _set_para_format(pPr, indent=True, line=360, space_before=100, space_after=100)
        bold = (kind in ('h2', 'h3', 'stage'))
        r = OxmlElement('w:r'); rPr = OxmlElement('w:rPr')
        _set_run_fonts(rPr, FONT, SZ_BODY, bold=bold)
        r.append(rPr)
        t = OxmlElement('w:t'); t.text = text; t.set(qn('xml:space'), 'preserve'); r.append(t)
        p.append(r)
    return p

def classify(text):
    t = text.strip()
    if not t: return None
    if re.match(r'^[一二三四五六七八九十]+、', t): return 'h1'
    if re.match(r'^[（(][一二三四五六七八九十]+[）)]', t): return 'h2'
    if re.match(r'^第[一二三四五六七八九十]+阶段', t): return 'stage'
    # subhead 必须先于 h3 判断(都匹配"数字+点/顿号"开头,但 subhead 含冒号)
    if re.match(r'^\d+[\.、]\s*\S+[：:]', t): return 'subhead'
    if re.match(r'^[1-9][\.、]', t): return 'h3'
    if t.startswith('图') and len(t) < 40 and re.match(r'^图[1-9]', t): return 'caption'
    return 'body'

# === 写入优化后的内容 ===
with open(CONTENT_TXT, encoding='utf-8') as f:
    lines = f.read().split('\n')

for line in lines:
    t = line.strip()
    if not t: continue
    kind = classify(t)
    if kind is None: continue
    p = make_para(t, kind)
    tc.append(p)

print(f'内容已写入，共 {len([l for l in lines if l.strip()])} 个非空行')

# 关键：先保存一次，再重新打开（让 doc2 读到的是新内容）
doc.save(DST)

# === 在图注段落前插入对应图片 ===
PIC_MAP = {
    '图1': r'D:/科研文件/outputs/fig_p1_政策演进时间线.png',
    '图2': r'D:/科研文件/outputs/fig_p2_部署框架.png',
    '图3': r'D:/科研文件/outputs/fig_p3_五项指标对比.png',
    '图4': r'D:/科研文件/outputs/fig_p4_江苏数据全景.png',
    '图5': r'D:/科研文件/outputs/fig_p5_人才供需缺口.png',
    '图6': r'D:/科研文件/outputs/fig_p6_苏浙鲁对比.png',
    '图7': r'D:/科研文件/outputs/fig_p7_技术路线.png',
    '图8': r'D:/科研文件/outputs/fig_p8_政策工具框架.png',
}

doc2 = Document(DST)
cell2 = doc2.tables[3].cell(0, 0)
tc2 = cell2._tc
all_p = list(tc2.findall(qn('w:p')))

inserted = 0
for p in all_p:
    txt = ''.join(t.text or '' for t in p.findall('.//' + qn('w:t'))).strip()
    m = re.match(r'^(图[1-8])', txt)
    if m:
        fig_key = m.group(1)
        if fig_key in PIC_MAP:
            # 在图注段前插入图片段
            pic_path = PIC_MAP[fig_key]
            # 创建图片段（用 python-docx 方便）
            tmp_p = cell2.add_paragraph()
            tmp_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            tmp_p.paragraph_format.line_spacing = 1.5
            tmp_p.paragraph_format.space_before = Pt(6)
            tmp_p.paragraph_format.space_after = Pt(2)
            tmp_p.add_run().add_picture(pic_path, width=Cm(13.5))
            new_pic_p = tmp_p._p
            cell2._tc.remove(new_pic_p)  # 从尾部移除
            p.addprevious(new_pic_p)  # 插入到图注前
            inserted += 1
            print(f'  ✓ {fig_key} 插入: {pic_path.split("/")[-1]}')

print(f'共插入 {inserted} 张图')

# === 自动填项目名称(表2信息表行0列1) ===
if TOPIC:
    t2 = doc2.tables[2]
    tr2 = t2._tbl.findall(qn('w:tr'))[0]
    tcs2 = tr2.findall(qn('w:tc'))
    if len(tcs2) >= 2:
        cell_topic = tcs2[1]
        # 找第一个段落
        ps = cell_topic.findall(qn('w:p'))
        if ps:
            p_topic = ps[0]
            r_topic = OxmlElement('w:r')
            rPr_topic = OxmlElement('w:rPr')
            rf_topic = OxmlElement('w:rFonts')
            rf_topic.set(qn('w:eastAsia'), '宋体')
            rf_topic.set(qn('w:ascii'), 'Times New Roman')
            rf_topic.set(qn('w:hAnsi'), 'Times New Roman')
            rPr_topic.append(rf_topic)
            rPr_topic.append(OxmlElement('w:b'))
            rPr_topic.append(OxmlElement('w:bCs'))
            sz_topic = OxmlElement('w:sz'); sz_topic.set(qn('w:val'), '28'); rPr_topic.append(sz_topic)
            szcs_topic = OxmlElement('w:szCs'); szcs_topic.set(qn('w:val'), '28'); rPr_topic.append(szcs_topic)
            r_topic.append(rPr_topic)
            t_topic = OxmlElement('w:t'); t_topic.text = TOPIC; t_topic.set(qn('xml:space'), 'preserve'); r_topic.append(t_topic)
            p_topic.append(r_topic)
            print(f'已自动填项目名称: {TOPIC}')

doc2.save(DST)
print(f'\n保存: {DST}')

# 验证
doc3 = Document(DST)
c = doc3.tables[3].cell(0, 0)
pics = sum(1 for p in c.paragraphs if 'pic:pic' in p._p.xml or 'blip' in p._p.xml)
caps = sum(1 for p in c.paragraphs if p.text.strip().startswith('图') and len(p.text.strip()) < 40)
print(f'验证：图片 {pics} 张，图注 {caps} 条')
