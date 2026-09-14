# -*- coding: utf-8 -*-
"""运动康复申报书 Plus 版 — 8 张数据类/技术类图片生成"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyBboxPatch
import numpy as np

font_manager.fontManager.addfont('C:/Windows/Fonts/simhei.ttf')
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['figure.facecolor'] = 'white'

OUT = 'D:/科研文件/outputs/'
C_BLUE = '#1d4ed8'
C_GREEN = '#047857'
C_ORANGE = '#b45309'
C_RED = '#b91c1c'
C_GREY = '#6b7280'
C_LIGHT = '#F7F9FB'

# ============ 图1 政策演进时间线 ============
fig, ax = plt.subplots(figsize=(11.5, 3.6), dpi=200)
ax.axis('off')
events = [
    ('2016', '《"健康中国2030"规划纲要》\n提出加强体医融合与非医疗健康干预'),
    ('2019', '《健康中国行动(2019—2030年)》\n确立以人民健康为中心的导向'),
    ('2022', '《关于构建更高水平全民健身\n公共服务体系的意见》深化体卫融合'),
    ('2026', '《体育强国建设"十五五"规划》\n运动康复纳入国家战略部署'),
]
phases = [('萌芽阶段\n竞技体育保障', 0.5, 2.0, C_GREY),
          ('探索阶段\n体医融合试点', 2.5, 4.0, C_ORANGE),
          ('深化阶段\n体卫融合国家部署', 4.5, 6.0, C_BLUE)]
for name, x0, x1, c in phases:
    ax.add_patch(plt.Rectangle((x0, 1.1), x1-x0, 0.9, facecolor=c, alpha=0.12, edgecolor=c, linewidth=1.2))
    ax.text((x0+x1)/2, 1.55, name, ha='center', va='center', fontsize=9, color=c, weight='bold')
ax.plot([0.4, 6.2], [0.95, 0.95], color='#9ca3af', linewidth=1.6, zorder=1)
for i, (yr, txt) in enumerate(events):
    x = 0.6 + i*1.85
    ax.scatter([x], [0.95], s=70, color=C_BLUE, zorder=3)
    ax.text(x, 0.55, yr, ha='center', fontsize=12, weight='bold', color=C_BLUE)
    ax.text(x, 0.12, txt, ha='center', va='top', fontsize=8.2, color='black')
ax.set_xlim(0, 6.4); ax.set_ylim(0, 2.4)
plt.tight_layout(); plt.savefig(OUT+'fig_p1_政策演进时间线.png', bbox_inches='tight'); plt.close()

# ============ 图2 "十五五"部署框架 ============
fig, ax = plt.subplots(figsize=(9.5, 4.4), dpi=200)
ax.axis('off')
ax.text(4.75, 4.05, '"十五五"规划：体卫融合部署三维度', ha='center', fontsize=12.5, weight='bold', color='black')
dims = [('监测阵地', ['常态化国民体质监测', '重点人群非医疗运动干预'], C_BLUE),
        ('干预服务', ['建设运动促进健康中心', '体质测定·运动能力评估', '科学健身指导综合服务'], C_GREEN),
        ('人才培育', ['高校增设运动促进健康专业', '培养标准·资格认证·培训体系', '体育卫健交叉培训'], C_ORANGE)]
for i, (title, items, c) in enumerate(dims):
    x = 1.0 + i*2.85
    ax.add_patch(plt.Rectangle((x-0.5, 1.5), 2.2, 2.2, facecolor=c, alpha=0.10, edgecolor=c, linewidth=1.5))
    ax.text(x+0.6, 3.35, title, ha='center', fontsize=11.5, weight='bold', color=c)
    for j, it in enumerate(items):
        ax.text(x+0.6, 2.85-j*0.5, '· '+it, ha='center', va='center', fontsize=8.4, color='black')
ax.text(4.75, 0.85, '配套机制：从业人员培养标准 · 岗位资格认证 · 慢病运动干预纳入医保 · 体医融合服务收费试点', ha='center', fontsize=8.6, color='black')
ax.text(4.75, 0.32, '呼应《全民健身计划(2026—2030年)》：AI赋能 · 运动处方精准化 · 扩大运动康复服务供给', ha='center', fontsize=8.2, color=C_GREY)
ax.set_xlim(0, 9.5); ax.set_ylim(0, 4.4)
plt.tight_layout(); plt.savefig(OUT+'fig_p2_部署框架.png', bbox_inches='tight'); plt.close()

# ============ 图3 五项指标基准vs目标 (2x2子图) ============
fig, axes = plt.subplots(2, 2, figsize=(10, 5.4), dpi=200)
indicators = [
    ('人均体育场地面积', '平方米', 3.11, 4.0, '+28.6%', '建成12.8万公顷\n新改扩建场地'),
    ('经常锻炼人数比例', '%', 38.52, 40.0, '+1.5pp', '扩大参与面\n全民健身'),
    ('国民体质优良率', '%', 30.9, 31.1, '+0.2pp', '质的提升\n叠加营养与生活方式'),
    ('体育产业总规模', '万亿元', 3.84, 7.0, '+82.3%', '近乎翻番\n朝阳→支柱性产业'),
]
for ax, (title, unit, b, t, growth, note) in zip(axes.flatten(), indicators):
    bars = ax.bar(['基准(十四五末)', '目标(2030)'], [b, t], width=0.5, color=['#9ca3af', C_BLUE], edgecolor='white')
    for r, v in zip(bars, [b, t]):
        ax.text(r.get_x()+r.get_width()/2, r.get_height()*1.04, f'{v:g}{unit}', ha='center', fontsize=10, weight='bold',
                color='black' if r.get_facecolor()==(0.6117647058823529, 0.6117647058823529, 0.6117647058823529, 1.0) else C_BLUE)
    ax.text(0.5, 0.92, f'增幅 {growth}', transform=ax.transAxes, ha='center', fontsize=10, color=C_RED, weight='bold')
    ax.text(0.5, 0.05, note, transform=ax.transAxes, ha='center', fontsize=8.4, color=C_GREY)
    ax.set_title(title, fontsize=10.5, weight='bold', color='black')
    ax.spines[['top','right']].set_visible(False)
    ax.set_ylim(0, max(b, t)*1.22)
fig.suptitle('"十五五"五项核心指标：基准值与目标值对比（数据来源：国家体育总局）', fontsize=11.5, weight='bold', y=0.995)
fig.text(0.5, 0.01, '另：获得世界冠军数量由146个转向"位居前列"，评价标尺从数量积累转向位次引领', ha='center', fontsize=8.6, color=C_GREY)
plt.tight_layout(rect=[0, 0.03, 1, 0.97]); plt.savefig(OUT+'fig_p3_五项指标对比.png', bbox_inches='tight'); plt.close()

# ============ 图4 江苏体卫融合数据全景 ============
fig, ax = plt.subplots(figsize=(10, 4.8), dpi=200)
ax.axis('off')
cards = [('2540名', '运动处方师\n(占全国一半以上)', C_BLUE),
         ('203个', '运动促进健康\n服务机构', C_BLUE),
         ('100个', '基层慢病运动\n干预试点', C_GREEN),
         ('10万+人次', '年均运动干预\n服务群众', C_GREEN),
         ('55家', '省级运动促进\n健康中心', C_ORANGE),
         ('7所', '体育医院', C_ORANGE),
         ('583个', '体重管理门诊', C_RED),
         ('37.8万人次', '体重管理累计服务', C_RED)]
for i, (num, lab, c) in enumerate(cards):
    r, col = divmod(i, 4)
    x = 1.1 + col*2.5
    y = 3.0 - r*2.4
    ax.add_patch(plt.Rectangle((x-0.55, y-0.55), 2.1, 1.7, facecolor=c, alpha=0.08, edgecolor=c, linewidth=1.4))
    ax.text(x+0.5, y+0.62, num, ha='center', fontsize=15, weight='bold', color=c)
    ax.text(x+0.5, y-0.1, lab, ha='center', va='center', fontsize=8.6, color='black')
ax.text(5.0, 4.35, '江苏省体卫融合关键数据全景', ha='center', fontsize=12.5, weight='bold', color='black')
ax.text(5.0, -0.75, '目标：到2030年累计培训运动处方师4000人次（数据来源：江苏省体育局）', ha='center', fontsize=8.6, color=C_GREY)
ax.set_xlim(0, 10); ax.set_ylim(-1.3, 4.6)
plt.tight_layout(); plt.savefig(OUT+'fig_p4_江苏数据全景.png', bbox_inches='tight'); plt.close()

# ============ 图5 人才供需缺口 ============
fig, ax = plt.subplots(figsize=(10, 4.6), dpi=200)
ax.axis('off')
ax.text(2.35, 4.2, '需求侧', ha='center', fontsize=12, weight='bold', color=C_RED)
ax.text(7.05, 4.2, '供给侧', ha='center', fontsize=12, weight='bold', color=C_BLUE)
need = [('4.3亿', '长期运动习惯人群'), ('1亿', '面临运动损伤困扰'), ('2000亿元', '2025年市场规模(预计)'), ('20万+', '专业人才缺口')]
supply = [('40—50万人', '机构年服务人数'), ('0.4人/万', '康复治疗师密度(不足发达国家1/5)'), ('18%', '运动康复资质人员占比'), ('约8000人', '运动康复专业年培养量')]
for i in range(4):
    y = 3.4 - i*0.85
    ax.text(1.15, y, need[i][0], ha='center', fontsize=13.5, weight='bold', color=C_RED)
    ax.text(3.6, y, need[i][1], ha='center', va='center', fontsize=8.8, color='black')
    ax.text(5.85, y, supply[i][0], ha='center', fontsize=13.5, weight='bold', color=C_BLUE)
    ax.text(8.3, y, supply[i][1], ha='center', va='center', fontsize=8.8, color='black')
ax.plot([4.7, 4.7], [0.6, 3.9], color='#9ca3af', linewidth=1.2, linestyle='--')
ax.text(4.7, 0.15, '供需失衡', ha='center', fontsize=9, color=C_GREY)
ax.set_xlim(0, 9.4); ax.set_ylim(-0.2, 4.6)
ax.set_title('运动康复人才供需缺口分析（数据来源：行业白皮书及公开报告）', fontsize=11, weight='bold')
plt.tight_layout(); plt.savefig(OUT+'fig_p5_人才供需缺口.png', bbox_inches='tight'); plt.close()

# ============ 图6 苏浙鲁对比 ============
fig, ax = plt.subplots(figsize=(10, 4.4), dpi=200)
ax.axis('off')
provs = [('江苏', '体卫融合服务新模式', ['2540名运动处方师', '203个服务/促进健康机构', '年服务10万+人次'], C_BLUE),
         ('浙江', '好社区运动健康中心', ['运动促进健康融入基层治理', '公共设施体育功能复合配置', '体质测定纳入健康体检'], C_GREEN),
         ('山东', '体医融合产业闭环', ['运动促进健康服务收费梳理', '商业保险慢病运动干预险', '体医融合服务阵地'], C_ORANGE)]
for i, (p, subtitle, items, c) in enumerate(provs):
    x = 0.9 + i*2.85
    ax.add_patch(plt.Rectangle((x-0.45, 0.6), 2.2, 3.3, facecolor=c, alpha=0.08, edgecolor=c, linewidth=1.5))
    ax.text(x+0.65, 3.45, p, ha='center', fontsize=14, weight='bold', color=c)
    ax.text(x+0.65, 3.0, subtitle, ha='center', fontsize=9.5, color='black')
    for j, it in enumerate(items):
        ax.text(x+0.65, 2.5-j*0.55, '· '+it, ha='center', va='center', fontsize=8.2, color='black')
ax.set_xlim(0, 9.4); ax.set_ylim(0, 4.0)
ax.set_title('苏浙鲁三省体卫融合实践对比', fontsize=11.5, weight='bold')
plt.tight_layout(); plt.savefig(OUT+'fig_p6_苏浙鲁对比.png', bbox_inches='tight'); plt.close()

# ============ 图7 技术路线 ============
fig, ax = plt.subplots(figsize=(11, 3.2), dpi=200)
ax.axis('off')
steps = [('政策文本收集', '官网/公报'), ('政策文本库建立', '清洗·时间线'), ('内容分析编码', '分析单元·编码体系'),
         ('词频·共现计量', 'Python/NVivo'), ('案例对照分析', '苏浙鲁'), ('趋势研判', '多源印证'), ('成果凝练', '论文·报告')]
n = len(steps)
for i, (t, s) in enumerate(steps):
    x = 0.45 + i*1.5
    c = C_BLUE if i in (0, 1) else (C_GREEN if i in (2, 3) else (C_ORANGE if i in (4, 5) else C_RED))
    ax.add_patch(FancyBboxPatch((x, 0.9), 1.32, 1.1, boxstyle='round,pad=0.04', facecolor=c, alpha=0.12, edgecolor=c, linewidth=1.5))
    ax.text(x+0.66, 1.55, t, ha='center', va='center', fontsize=9.3, weight='bold', color=c)
    ax.text(x+0.66, 1.12, s, ha='center', va='center', fontsize=7.6, color='black')
    if i < n-1:
        ax.annotate('', xy=(x+1.32, 1.45), xytext=(x+1.48, 1.45), arrowprops=dict(arrowstyle='-|>', color='#9ca3af', lw=1.6))
ax.text(5.5, 0.35, '政策文本分析技术路线：定性解读 + 定量支撑 + 案例验证', ha='center', fontsize=10, color=C_GREY)
ax.set_xlim(0, 11); ax.set_ylim(0, 2.4)
plt.tight_layout(); plt.savefig(OUT+'fig_p7_技术路线.png', bbox_inches='tight'); plt.close()

# ============ 图8 政策工具三维框架 ============
fig, ax = plt.subplots(figsize=(10, 4.6), dpi=200)
ax.axis('off')
ax.text(5.0, 4.2, '运动康复政策工具三维分析框架', ha='center', fontsize=12.5, weight='bold', color='black')
tools = [('供给型', ['人才培养', '资金投入', '设施建设'], C_BLUE),
         ('需求型', ['医保支付', '政府购买', '消费引导'], C_GREEN),
         ('环境型', ['标准规范', '目标规划', '部门协同'], C_ORANGE)]
for i, (t, items, c) in enumerate(tools):
    x = 1.0 + i*3.0
    ax.add_patch(plt.Rectangle((x-0.5, 0.9), 2.2, 2.7, facecolor=c, alpha=0.10, edgecolor=c, linewidth=1.5))
    ax.text(x+0.6, 3.2, t, ha='center', fontsize=11.5, weight='bold', color=c)
    for j, it in enumerate(items):
        ax.text(x+0.6, 2.65-j*0.55, '· '+it, ha='center', va='center', fontsize=9, color='black')
ax.text(5.0, 0.4, '基于 Rothwell & Zegveld 政策工具三分法，对"十五五"规划相关条款进行编码归类', ha='center', fontsize=8.6, color=C_GREY)
ax.set_xlim(0, 10); ax.set_ylim(0, 4.6)
plt.tight_layout(); plt.savefig(OUT+'fig_p8_政策工具框架.png', bbox_inches='tight'); plt.close()

print('8 张图片生成完成')
