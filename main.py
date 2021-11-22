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

datasample = pd.read_csv('1_feedback_viewedFP_caadria_test.csv')
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
name = ['NR - Div', 'FS - Div', 'LC - Div', 'RS - Div', 'RSL - Div', 'RC - Div', 'NR - Conv', 'FS - Conv', 'LC - Conv', 'RS - Conv', 'RSL - Conv', 'RC - Conv',]
plt.rc("font", size=8)
plt.rc('ytick', labelsize=5)
plt.rc('xtick', labelsize=5)
plt.rcParams["figure.figsize"] = (14, 7.5)
plt.rcParams['axes.grid'] = True
plt.subplots_adjust(left=0.05, bottom=0.1, right=0.95, top=0.95, wspace=0.2, hspace=0.55)
x_axis = range(0, len(rs_cs))
index = 0
for i in all_fore:
    plt.subplot(2,6,index+1)
    plt.plot(x_axis, i)
    scatter_index = 0
    for l in i:
        if selected_data[scatter_index] == 1:
            plt.scatter(scatter_index, l, s = 10, c = 'r')
        scatter_index += 1
    plt.title(name[index])
    index += 1
for i in all_back:
    plt.subplot(2,6,index+1)
    plt.plot(x_axis, i)
    scatter_index = 0
    for l in i:
        if selected_data[scatter_index] == 1:
            plt.scatter(scatter_index, l, s=10, c='r')
        scatter_index += 1
    plt.title(name[index])
    index += 1
plt.show()