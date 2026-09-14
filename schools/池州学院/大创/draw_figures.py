# -*- coding: utf-8 -*-
"""护膝申报书科研绘图: 3张结构化图"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
import numpy as np

# 注册中文字体
font_manager.fontManager.addfont('C:/Windows/Fonts/simhei.ttf')
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['figure.facecolor'] = 'white'

OUT = r'D:/科研文件/outputs/'
C1 = '#2E5B8A'   # 深蓝
C2 = '#3E8E5A'   # 绿
C3 = '#B8860B'   # 暗金
C4 = '#8B5A2B'   # 棕
GREY = '#666666'

# ============ 图1 制备工艺流程图 ============
fig, ax = plt.subplots(figsize=(11, 3.2), dpi=200)
ax.set_xlim(0, 11); ax.set_ylim(0, 3.2); ax.axis('off')

steps = ['植物纤维\n筛选', '碱处理\n(NaOH)', '偶联剂\n改性', '铺层\n设计', '手糊\n浸渍', '模压\n固化', '脱模\n修整', '试样\n加工']
n = len(steps)
w = 1.05; h = 1.15; gap = 0.28
x0 = (11 - (n*w + (n-1)*gap)) / 2

for i, s in enumerate(steps):
    x = x0 + i*(w+gap)
    y = 1.0
    box = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.05",
                         linewidth=1.4, edgecolor=C1, facecolor='#EAF1F8')
    ax.add_patch(box)
    ax.text(x+w/2, y+h/2, s, ha='center', va='center', fontsize=10.5, color=C1)
    if i < n-1:
        ax.add_patch(FancyArrowPatch((x+w, y+h/2), (x+w+gap, y+h/2),
                     arrowstyle='-|>', mutation_scale=16, linewidth=1.4, color=GREY))

ax.text(5.5, 0.3, '图1 植物纤维混杂复合材料制备工艺流程', ha='center', va='center', fontsize=11.5, color='black')
plt.tight_layout()
plt.savefig(OUT + 'fig_护膝_制备工艺.png', bbox_inches='tight', facecolor='white')
plt.close()

# ============ 图2 铺层结构示意图 ============
fig, axes = plt.subplots(1, 2, figsize=(11, 3.6), dpi=200)

# 左: 层间混杂
ax = axes[0]
ax.set_xlim(0, 10); ax.set_ylim(0, 7); ax.axis('off')
ax.text(5, 6.5, '层间混杂（分层铺放）', ha='center', fontsize=11.5, weight='bold')
layers = [('纤维A（黄麻）', C3), ('纤维B（剑麻）', C2), ('纤维A（黄麻）', C3), ('纤维B（剑麻）', C2)]
for i, (label, color) in enumerate(layers):
    y = 5.2 - i*1.05
    ax.add_patch(FancyBboxPatch((2.2, y), 5.6, 0.8, boxstyle="round,pad=0.03",
                 linewidth=1.2, edgecolor=color, facecolor=color, alpha=0.35))
    ax.text(8.0, y+0.4, label, va='center', fontsize=9.5, color=color)
ax.text(5, 0.25, '（a）', ha='center', fontsize=10)

# 右: 层内交织
ax = axes[1]
ax.set_xlim(0, 10); ax.set_ylim(0, 7); ax.axis('off')
ax.text(5, 6.5, '层内交织（单层混织）', ha='center', fontsize=11.5, weight='bold')
# 交织纹理
for row in range(4):
    y = 5.2 - row*1.05
    for col in range(8):
        x = 2.2 + col*0.7
        color = C3 if (col+row) % 2 == 0 else C2
        ax.add_patch(FancyBboxPatch((x, y), 0.7, 0.8, boxstyle="round,pad=0.02",
                     linewidth=0.8, edgecolor=color, facecolor=color, alpha=0.5))
ax.text(8.2, 5.6, '纤维A（黄麻）', fontsize=9.5, color=C3)
ax.text(8.2, 4.5, '纤维B（剑麻）', fontsize=9.5, color=C2)
ax.text(5, 0.25, '（b）', ha='center', fontsize=10)

fig.suptitle('图2 混杂复合材料两种铺层结构示意', fontsize=11.5, y=0.02)
plt.tight_layout(rect=[0, 0.03, 1, 1])
plt.savefig(OUT + 'fig_护膝_铺层结构.png', bbox_inches='tight', facecolor='white')
plt.close()

# ============ 图3 混杂配比与性能关系图 ============
fig, ax = plt.subplots(figsize=(7.5, 4.5), dpi=200)
x = np.linspace(0, 1, 100)
# 混合定律(线性预测)
y_rule = 40 + 60*x
# 实测(正混杂效应, 中间凸起)
y_exp = 40 + 60*x + 28*np.sin(np.pi*x)

ax.plot(x, y_rule, '--', color=GREY, linewidth=1.8, label='混合定律预测值')
ax.plot(x, y_exp, '-', color=C1, linewidth=2.2, label='实测值')

# 填充正混杂效应区
ax.fill_between(x, y_rule, y_exp, where=(y_exp>y_rule), color=C2, alpha=0.15)
# 标注
ax.annotate('正混杂效应区\n（实测高于预测）', xy=(0.5, 96), xytext=(0.52, 88),
            fontsize=9.5, color=C2, ha='center',
            arrowprops=dict(arrowstyle='->', color=C2, lw=1.2))

ax.set_xlabel('纤维A体积分数（%）', fontsize=10.5)
ax.set_ylabel('力学性能', fontsize=10.5)
ax.set_xlim(0, 1); ax.set_ylim(30, 110)
ax.set_xticks([0, 0.25, 0.5, 0.75, 1.0])
ax.set_xticklabels(['0', '25', '50', '75', '100'])
ax.tick_params(labelsize=9.5)
ax.legend(fontsize=9.5, loc='lower right', framealpha=0.9)
ax.grid(True, linestyle=':', alpha=0.5)
ax.set_title('图3 混杂配比与力学性能关系（正混杂效应示意）', fontsize=11.5)
for spine in ['top', 'right']:
    ax.spines[spine].set_visible(False)

plt.tight_layout()
plt.savefig(OUT + 'fig_护膝_配比性能.png', bbox_inches='tight', facecolor='white')
plt.close()

print("三张科研图绘制完成")
import os
for f in ['fig_护膝_制备工艺.png', 'fig_护膝_铺层结构.png', 'fig_护膝_配比性能.png']:
    p = OUT + f
    print(f"  {f}: {os.path.getsize(p)//1024} KB")
