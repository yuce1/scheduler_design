#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys


node_name = "node231"
# cpu的最大功率
max_power = 80
max_proportion = 0.3
min_proportion = 0.2
cpu_num = 1
capping_proportion = 0.25

def set_node_name(value):
    # 定义一个全局变量
    global node_name 
    node_name = value

def get_node_name():
    global node_name
    return node_name

def set_max_power(value):
    # 定义一个全局变量
    global max_power 
    max_power = value

def get_max_power():
    global max_power
    return max_power

def set_max_proportion(value):
    # 定义一个全局变量
    global max_proportion 
    max_proportion = value

def get_max_proportion():
    global max_proportion
    return max_proportion


def set_min_proportion(value):
    # 定义一个全局变量
    global max_proportion 
    max_proportion = value

def get_min_proportion():
    global max_proportion
    return max_proportion

def set_cpu_num(value):
    # 定义一个全局变量
    global cpu_num 
    cpu_num = value

def get_cpu_num():
    global cpu_num
    return cpu_num

def set_capping_proportion(value):
    # 定义一个全局变量
    global capping_proportion 
    capping_proportion = value

def get_capping_proportion():
    global capping_proportion
    return capping_proportion