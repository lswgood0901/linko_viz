import cv2
import csv
import numpy as np
import pandas as pd
import math
import json
import ast
import os
import shutil
from matplotlib import pyplot as plt
import time


def entropy(pos):
    if pos == 0 or pos == 1:
        return 0
    return -1 * pos * math.log2(pos) - 1 * (1 - pos) * math.log2(1 - pos)

datasample = pd.read_csv('1_feedback_viewedFP_caadria_이태하선생님.csv')
linkdata = datasample['link']
fpname_list = datasample['floorplan_name']
fpname_list = fpname_list.values.tolist()
event_list = datasample['event']
event_list = event_list.values.tolist()
selected_data = []

index = 0
rnlinks = []
fslinks = []
lclinks = []
rslinks = []
rsllinks = []
rclinks = []
for i in fpname_list:
    rest_list = list(filter(lambda x: fpname_list[x] == i, range(len(fpname_list))))
    if event_list[rest_list[len(rest_list)-1]] == 3:
        event_list[rest_list[0]] = 1
    elif event_list[rest_list[len(rest_list)-1]] == 2:
        event_list[rest_list[0]] = 0

for a in range(len(linkdata)):
    string_to_array = ast.literal_eval(linkdata[a])
    rnlink = []
    fslink = []
    lclink = []
    rslink = []
    rsllink = []
    rclink = []

    for b in string_to_array:
        if b[0] == "rn" and (datasample['event'][a] != 2 and datasample['event'][a] != 3):
            rnlink.append([b[1], b[2]])
        elif b[0] == "fs" and (datasample['event'][a] != 2 and datasample['event'][a] != 3):
            fslink.append([b[1], b[2]])
        elif b[0] == "lc" and (datasample['event'][a] != 2 and datasample['event'][a] != 3):
            lclink.append([b[1], b[2]])
        elif b[0] == "rs" and (datasample['event'][a] != 2 and datasample['event'][a] != 3):
            rslink.append([b[1], b[2]])
        elif b[0] == "rsl" and (datasample['event'][a] != 2 and datasample['event'][a] != 3):
            rsllink.append([b[1], b[2]])
        elif b[0] == "rc" and (datasample['event'][a] != 2 and datasample['event'][a] != 3):
            rclink.append([b[1], b[2]])
    if (datasample['event'][a] != 2 and datasample['event'][a] != 3):
        selected_data.append(event_list[a])
        rnlinks.append(rnlink)
        fslinks.append(fslink)
        lclinks.append(lclink)
        rslinks.append(rslink)
        rsllinks.append(rsllink)
        rclinks.append(rclink)
    index += 1
def appending_currentstate(anylinks):
    index = 0
    current_state = []
    for links in anylinks:
        nforeLink_pos = [0 for i in range(index)]
        nbackLink_pos = [0 for i in range(index)]
        nforeLink_entp = [0 for i in range(index)]
        nbackLink_entp = [0 for i in range(index)]
        for link in links:
            nforeLink_pos[link[0]] += 1
            nbackLink_pos[link[1]-1] += 1
        if( index == 0):
            current_state.append([0,0])
        else:
            for i in range(index):
                nforeLink_entp[i] = entropy(nforeLink_pos[i] / (index - i))
                nbackLink_entp[i] = entropy(nbackLink_pos[i] / (i + 1))
            maxlink = max(max(nbackLink_pos), max(nforeLink_pos), 1)
            current_state.append([nbackLink_pos[index-1]/maxlink, 1-nbackLink_pos[index-1]/maxlink])
        index += 1
    return current_state

def count_linknumber(anylinks):
    index = 0
    for links in anylinks:
        nforeLink_pos = [0 for i in range(index)]
        nbackLink_pos = [0 for i in range(index)]
        for link in links:
            nforeLink_pos[link[0]] += 1
            nbackLink_pos[link[1] - 1] += 1
        index += 1
    nforeLink_pos.append(0)
    nbackLink_pos.insert(0,0)
    return nforeLink_pos, nbackLink_pos

fore_rn_num, back_rn_num = count_linknumber(rnlinks)
fore_fs_num, back_fs_num = count_linknumber(fslinks)
fore_lc_num, back_lc_num = count_linknumber(lclinks)
fore_rc_num, back_rc_num = count_linknumber(rclinks)
fore_rs_num, back_rs_num = count_linknumber(rslinks)
fore_rsl_num, back_rsl_num = count_linknumber(rsllinks)

rn_cs = appending_currentstate(rnlinks)
fs_cs = appending_currentstate(fslinks)
lc_cs = appending_currentstate(lclinks)
rs_cs = appending_currentstate(rslinks)
rsl_cs = appending_currentstate(rsllinks)
rc_cs = appending_currentstate(rclinks)

fore_rncs = []
back_rncs = []
fore_fscs = []
back_fscs = []
fore_lccs = []
back_lccs = []
fore_rscs = []
back_rscs = []
fore_rslcs = []
back_rslcs = []
fore_rccs = []
back_rccs = []

for i in rn_cs:
    fore_rncs.append(i[1])
    back_rncs.append(i[0])
for i in fs_cs:
    fore_fscs.append(i[1])
    back_fscs.append(i[0])
for i in lc_cs:
    fore_lccs.append(i[1])
    back_lccs.append(i[0])
for i in rs_cs:
    fore_rscs.append(i[1])
    back_rscs.append(i[0])
for i in rsl_cs:
    fore_rslcs.append(i[1])
    back_rslcs.append(i[0])
for i in rc_cs:
    fore_rccs.append(i[1])
    back_rccs.append(i[0])

all_fore = [fore_rncs, fore_fscs, fore_lccs, fore_rscs, fore_rslcs, fore_rccs]
all_back = [back_rncs, back_fscs, back_lccs, back_rscs, back_rslcs, back_rccs]
all_fore_num = [fore_rn_num, fore_fs_num, fore_lc_num, fore_rs_num, fore_rsl_num, fore_rc_num]
all_back_num = [back_rn_num, back_fs_num, back_lc_num, back_rs_num, back_rsl_num, back_rc_num]
mean_index = 0
mean_div = []
mean_conv = []

for i in range(len(rs_cs)):
    mean_array_fore = [fore_rncs[mean_index], fore_fscs[mean_index], fore_lccs[mean_index], fore_rscs[mean_index], fore_rslcs[mean_index], fore_rccs[mean_index]]
    mean_array_back = [back_rncs[mean_index], back_fscs[mean_index], back_lccs[mean_index], back_rscs[mean_index], back_rslcs[mean_index], back_rccs[mean_index]]
    mean_div.append(np.mean(mean_array_fore))
    mean_conv.append(np.mean(mean_array_back))
    mean_index += 1
print(mean_div, mean_conv)

name = ['NR - Div', 'FS - Div', 'RL - Div', 'RS - Div', 'RSL - Div', 'RC - Div', 'mean_div',
            'NR - Conv', 'FS - Conv', 'RL - Conv', 'RS - Conv', 'RSL - Conv', 'RC - Conv', 'mean_conv',
            'NR - forelinks', 'FS - forelinks', 'RL - forelinks', 'RS - forelinks', 'RSL - forelinks', 'RC - forelinks', '',
            'NR - backlinks', 'FS - backlinks', 'RL - backlinks', 'RS - backlinks', 'RSL - backlinks', 'RC - backlinks', '']
plt.rc("font", size=8)
plt.rc('ytick', labelsize=5)
plt.rc('xtick', labelsize=5)
plt.rcParams["figure.figsize"] = (14, 7.5)
plt.rcParams['axes.grid'] = True
plt.subplots_adjust(left=0.05, bottom=0.1, right=0.95, top=0.95, wspace=0.2, hspace=0.55)
x_axis = range(0, len(rs_cs))
index = 0
for i in all_fore:
    plt.subplot(4,7,index+1)
    plt.plot(x_axis, i)
    scatter_index = 0
    for l in i:
        if selected_data[scatter_index] == 1:
            plt.scatter(scatter_index, l, s = 10, c = 'r')
        scatter_index += 1
    plt.title(name[index])
    index += 1

plt.subplot(4,7,index+1)
plt.plot(x_axis, mean_div)
scatter_index = 0
for l in mean_div:
    if selected_data[scatter_index] == 1:
        plt.scatter(scatter_index, l, s = 10, c = 'r')
    scatter_index += 1
plt.title(name[index])
index += 1

for i in all_back:
    plt.subplot(4,7,index+1)
    plt.plot(x_axis, i)
    scatter_index = 0
    for l in i:
        if selected_data[scatter_index] == 1:
            plt.scatter(scatter_index, l, s=10, c='r')
        scatter_index += 1
    plt.title(name[index])
    index += 1

plt.subplot(4,7,index+1)
plt.plot(x_axis, mean_conv)
scatter_index = 0
for l in mean_conv:
    if selected_data[scatter_index] == 1:
        plt.scatter(scatter_index, l, s = 10, c = 'r')
    scatter_index += 1
plt.title(name[index])
index += 1

for i in all_fore_num:
    plt.subplot(4,7,index+1)
    plt.plot(x_axis, i)
    scatter_index=0
    for l in i:
        if selected_data[scatter_index] == 1:
            plt.scatter(scatter_index, l, s=10, c='r')
        scatter_index += 1
    plt.title(name[index])
    index += 1
index += 1
for i in all_back_num:
    plt.subplot(4,7,index+1)
    plt.plot(x_axis, i)
    scatter_index=0
    for l in i:
        if selected_data[scatter_index] == 1:
            plt.scatter(scatter_index, l, s=10, c='r')
        scatter_index += 1
    plt.title(name[index])
    index += 1
plt.show()