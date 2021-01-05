#!/usr/bin/python
# -*- coding: UTF-8 -*-

import csv
import time
import os


#文件存在则删除
if os.path.isfile('auto_line.py'):
    os.remove('auto_line.py')

#生成py文件
def WirtePyFile(auto_code):
    with open('auto_line.py','a+',encoding='UTF8') as file:
        file.write(auto_code)

#读取表头
file = r'ipmitool_get_sensor_2021-01-05_10593.csv'
def ReadFile(file,index):
    with open(file) as f:
        reader = csv.reader(f)
        data = [row[index] for row in reader]
    return data

#获取每个数据的index值
with open(file) as f:
        reader = csv.reader(f)
        title = [row for row in reader]
title = title[0]
cpu =[]
pch = []
mb_nic = []
fan = []
DIMMGrp_Temp = []
V = []
total = []
aoc =[]
hdd = []
def GetIndex():
    for i in title:
        try:
            if i.startswith('CPU'):
                cpu.append(title.index(i))
            if i.startswith(('PCH','System', 'Peripheral')):
                pch.append(title.index(i))
            if i.startswith('MB_NIC'):
                mb_nic.append(title.index(i))
            if i.startswith('FAN'):
                fan.append(title.index(i))
            if i.endswith('DIMMGrp'):
                DIMMGrp_Temp.append(title.index(i))
            if i.startswith(('12V', '5VCC', '3.3VCC', 'Vcpu', 'VD', '12VSB', '3.3VSB', 'P1V8_PCH', 'PVNN_PCH', 'P1V05_PCH')):
                V.append(title.index(i))
            if i.startswith('Total'):
                total.append(title.index(i))
            if i.startswith('AOC'):
                aoc.append(title.index(i))   
            if i.startswith('HDD'):
                hdd.append(title.index(i))
        except:
            pass      
    return cpu,pch,mb_nic,fan,DIMMGrp_Temp,V,total,aoc,hdd


#====================================#
#生成图标python 文件
#||||||||||||||||||||||||||||||||||||#

cpu,pch,mb_nic,fan,DIMMGrp_Temp,V,total,aoc,hdd = GetIndex()

#序列
timezone = ReadFile(file,0)

#生成头文件
code_title = """#!/usr/bin/python
# -*- coding: UTF-8 -*-
from pyecharts import options as opts
from pyecharts.charts import Bar,Line,Tab
from pyecharts.faker import Faker\n\n\n"""
WirtePyFile(code_title)


           
def LineComponent(ex_name,comp):
    #生成index的数据
    line_all = "def line_{}() -> Line:\n    c = (Line(init_opts=opts.InitOpts(width='1800px',height='800px'))" .format(str(ex_name))
    WirtePyFile(line_all)
    x_xaxis = "\n        .add_xaxis(%s)" % timezone[1:]
    WirtePyFile(x_xaxis)

    for index in comp:
        cpuall = ReadFile(file,index)
        auto_code = "\n        .add_yaxis('%s',%s,label_opts=opts.LabelOpts(),markpoint_opts=opts.MarkPointOpts(data=[opts.MarkPointItem(type_='max'),opts.MarkPointItem(type_='min')]),)" % (cpuall[0],cpuall[1:])
        WirtePyFile(auto_code)
    
    #尾部，统一的option
    opts = """\n        .set_global_opts(
                #时间轴
                datazoom_opts=opts.DataZoomOpts(),
                #标题
                title_opts=opts.TitleOpts(title="BMC Sensor"),
                #同轴提示线
                tooltip_opts=opts.TooltipOpts(trigger="axis"),
                yaxis_opts=opts.AxisOpts(
                type_="value",
                axistick_opts=opts.AxisTickOpts(is_show=True),
                splitline_opts=opts.SplitLineOpts(is_show=True),),
                xaxis_opts=opts.AxisOpts(type_="category", boundary_gap=False),)
                          .set_series_opts(label_opts=opts.LabelOpts(is_show=False),)
                )
    return c\n"""
    WirtePyFile(opts)


index_list = ["cpu","pch"",mb_nic",'fan,DIMMGrp_Temp','V','total','aoc','hdd']
LineComponent('cpu',cpu)
LineComponent('pch',pch)
LineComponent('mb_nic',mb_nic)
LineComponent('fan',fan)
LineComponent('DIMMGrp_Temp',DIMMGrp_Temp)
LineComponent('V',V)
LineComponent('total',total)
LineComponent('aoc',aoc)
LineComponent('hdd',hdd)

WirtePyFile('\ntab = Tab()')

WirtePyFile("\ntab.add(line_cpu(),'CPU')")
WirtePyFile("\ntab.add(line_pch(),'PCH')")
WirtePyFile("\ntab.add(line_mb_nic(),'MB NIC')")
WirtePyFile("\ntab.add(line_fan(),'FAN')")
WirtePyFile("\ntab.add(line_DIMMGrp_Temp(),'DIMMGrp_Temp')")
WirtePyFile("\ntab.add(line_V(),'Voltage')")
WirtePyFile("\ntab.add(line_total(),'Total')")
WirtePyFile("\ntab.add(line_aoc(),'AOC SAS')")
WirtePyFile("\ntab.add(line_hdd(),'HDD')")
#生成html文件
html_file = '\ntab.render("%s.html")' %file.split(".")[0]
WirtePyFile(html_file)

#运行python文件
cmd = r'python auto_line.py'
os.popen(cmd)