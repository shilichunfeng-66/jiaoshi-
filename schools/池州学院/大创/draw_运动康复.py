# -*- coding: utf-8 -*-
"""运动康复申报书科研绘图: 5张结构化图"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle
import numpy as np

font_manager.fontManager.addfont('C:/Windows/Fonts/simhei.ttf')
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['figure.facecolor'] = 'white'

OUT = r'D:/科研文件/outputs/'
C1 = '#2E5B8A'; C2 = '#3E8E5A'; C3 = '#B8860B'; C4 = '#8B5A2B'; GREY = '#666666'

# ===== 图1 政策演进时间线 =====
fig, ax = plt.subplots(figsize=(11, 3.4), dpi=200)
ax.set_xlim(0, 11); ax.set_ylim(0, 3.4); ax.axis('off')
nodes = [
    ('2016', '《"健康中国2030"规划纲要》\n加强体医融合', C1),
    ('2019', '《健康中国行动(2019—2030年)》\n以治病为中心转向健康为中心', C2),
    ('2022', '《全民健身公共服务体系意见》\n深化体卫融合、健康关口前移', C3),
    ('2026', '《体育强国建设"十五五"规划》\n体卫融合列为重点任务', C4),
]
w = 2.4; h = 1.5; gap = 0.3
x0 = (11 - (4*w + 3*gap)) / 2
for i, (yr, txt, c) in enumerate(nodes):
    x = x0 + i*(w+gap); y = 1.1
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.05",
                 linewidth=1.4, edgecolor=c, facecolor='white'))
    ax.text(x+w/2, y+h-0.35, yr, ha='center', fontsize=12, weight='bold', color=c)
    ax.text(x+w/2, y+h/2-0.25, txt, ha='center', va='center', fontsize=8.5, color='black')
    if i < 3:
        ax.add_patch(FancyArrowPatch((x+w, y+h/2), (x+w+gap, y+h/2),
                     arrowstyle='-|>', mutation_scale=16, linewidth=1.4, color=GREY))
ax.text(5.5, 0.3, '图1 运动康复政策演进时间线', ha='center', fontsize=11.5)
plt.tight_layout(); plt.savefig(OUT+'fig_运动康复_时间线.png', bbox_inches='tight'); plt.close()

# ===== 图2 "十五五"部署三维度框架 =====
fig, ax = plt.subplots(figsize=(9, 4.2), dpi=200)
ax.set_xlim(0, 9); ax.set_ylim(0, 4.2); ax.axis('off')
ax.text(4.5, 3.8, '"十五五"规划对运动康复的部署', ha='center', fontsize=12, weight='bold')
dims = [
    ('监测阵地', '常态化国民体质监测\n非医疗运动健康干预\n面向老年人/青少年/慢病人群', C1),
    ('干预服务', '建设运动促进健康中心\n体质测定+运动能力评估\n科学健身指导综合服务', C2),
    ('人才培育', '增设运动促进健康专业\n改革社会体育指导员制度\n运动促健康志愿服务工程', C3),
]
w = 2.5; h = 2.2; gap = 0.5
x0 = (9 - (3*w + 2*gap)) / 2
for i, (title, body, c) in enumerate(dims):
    x = x0 + i*(w+gap); y = 1.0
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.05",
                 linewidth=1.4, edgecolor=c, facecolor='#F7F9FB'))
    ax.text(x+w/2, y+h-0.4, title, ha='center', fontsize=11, weight='bold', color=c)
    ax.text(x+w/2, y+h/2-0.35, body, ha='center', va='center', fontsize=8.5, color='black')
ax.text(4.5, 0.25, '图2 "十五五"规划对运动康复的部署框架', ha='center', fontsize=11.5)
plt.tight_layout(); plt.savefig(OUT+'fig_运动康复_部署框架.png', bbox_inches='tight'); plt.close()

# ===== 图3 地方实践对比 =====
fig, ax = plt.subplots(figsize=(10, 4.5), dpi=200)
ax.set_xlim(0, 10); ax.set_ylim(0, 4.5); ax.axis('off')
cols = [
    ('江苏', ['培训运动处方师2540名', '建成203个促进健康机构', '100个慢病干预试点', '年服务10多万人次'], C1),
    ('浙江', ['好社区运动健康中心', '百姓健身房迭代升级', '体质测定纳入健康体检', '运动健康融入基层治理'], C2),
    ('山东', ['体医融合产业闭环', '探索服务收费标准', '商业保险健康险产品', '场馆与医疗机构合作'], C3),
]
w = 2.8; h = 2.9; gap = 0.4
x0 = (10 - (3*w + 2*gap)) / 2
for i, (title, items, c) in enumerate(cols):
    x = x0 + i*(w+gap); y = 0.9
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.05",
                 linewidth=1.4, edgecolor=c, facecolor='white'))
    ax.text(x+w/2, y+h-0.35, title, ha='center', fontsize=11.5, weight='bold', color=c)
    for j, it in enumerate(items):
        ax.text(x+w/2, y+h-0.75-j*0.52, '· '+it, ha='center', va='center', fontsize=8.3, color='black')
ax.text(5, 0.25, '图3 苏浙鲁三省体卫融合实践对比', ha='center', fontsize=11.5)
plt.tight_layout(); plt.savefig(OUT+'fig_运动康复_地方对比.png', bbox_inches='tight'); plt.close()

# ===== 图4 关键数据展示 =====
fig, ax = plt.subplots(figsize=(9.5, 4.2), dpi=200)
ax.set_xlim(0, 9.5); ax.set_ylim(0, 4.2); ax.axis('off')
ax.text(2.4, 3.7, '江苏实践数据', ha='center', fontsize=11.5, weight='bold', color=C1)
data_left = [('2540名', '累计培训运动处方师'), ('203个', '运动促进健康服务机构'), ('10万人次', '年均运动干预服务')]
for i, (num, label) in enumerate(data_left):
    x = 0.4 + i*1.75
    ax.add_patch(FancyBboxPatch((x, 1.2), 1.6, 2.0, boxstyle="round,pad=0.05",
                 linewidth=1.2, edgecolor=C1, facecolor='#EAF1F8'))
    ax.text(x+0.8, 2.55, num, ha='center', fontsize=13, weight='bold', color=C1)
    ax.text(x+0.8, 1.8, label, ha='center', fontsize=8, color='black')
ax.text(6.9, 3.7, '2030年量化目标', ha='center', fontsize=11.5, weight='bold', color=C2)
data_right = [('4㎡', '人均体育场地面积'), ('40%', '经常锻炼人数比例'), ('7万亿', '体育产业总规模')]
for i, (num, label) in enumerate(data_right):
    x = 5.4 + i*1.45
    ax.add_patch(FancyBboxPatch((x, 1.2), 1.35, 2.0, boxstyle="round,pad=0.05",
                 linewidth=1.2, edgecolor=C2, facecolor='#EAF6EE'))
    ax.text(x+0.675, 2.55, num, ha='center', fontsize=13, weight='bold', color=C2)
    ax.text(x+0.675, 1.8, label, ha='center', fontsize=8, color='black')
ax.text(4.75, 0.3, '图4 运动康复关键数据（江苏实践 + 2030目标）', ha='center', fontsize=11.5)
plt.tight_layout(); plt.savefig(OUT+'fig_运动康复_数据.png', bbox_inches='tight'); plt.close()

# ===== 图5 发展趋势三维度框架 =====
fig, ax = plt.subplots(figsize=(9, 4.2), dpi=200)
ax.set_xlim(0, 9); ax.set_ylim(0, 4.2); ax.axis('off')
ax.text(4.5, 3.8, '运动康复未来五年发展趋势', ha='center', fontsize=12, weight='bold')
dims = [
    ('服务体系健全', '运动促进健康中心推广\n基层站点加快布点\n干预服务标准化规范化', C1),
    ('人才培养扩容', '运动处方师规模扩大\n高校增设相关专业\n交叉培养机制完善', C2),
    ('产业融合深化', '康复器材研发产业化\n智能健康监测设备\n运动健康+业态融合', C3),
]
w = 2.5; h = 2.2; gap = 0.5
x0 = (9 - (3*w + 2*gap)) / 2
for i, (title, body, c) in enumerate(dims):
    x = x0 + i*(w+gap); y = 1.0
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.05",
                 linewidth=1.4, edgecolor=c, facecolor='#F7F9FB'))
    ax.text(x+w/2, y+h-0.4, title, ha='center', fontsize=11, weight='bold', color=c)
    ax.text(x+w/2, y+h/2-0.35, body, ha='center', va='center', fontsize=8.5, color='black')
ax.text(4.5, 0.25, '图5 运动康复发展趋势三维度研判', ha='center', fontsize=11.5)
plt.tight_layout(); plt.savefig(OUT+'fig_运动康复_趋势.png', bbox_inches='tight'); plt.close()

print("5张科研图绘制完成")
import os
for f in ['fig_运动康复_时间线.png','fig_运动康复_部署框架.png','fig_运动康复_地方对比.png','fig_运动康复_数据.png','fig_运动康复_趋势.png']:
    print(f"  {f}: {os.path.getsize(OUT+f)//1024} KB")
