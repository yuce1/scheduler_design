#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

# 迁移结束的阈值为50%
threshold_cpu_usage = 50

node_name = "k8s-node"

def set_node_name(value):
    # 定义一个全局变量
    global node_name 
    node_name = value

def get_node_name():
    global node_name
    return node_name
    
def set_threshold_cpu_usage(value):
    # 定义一个全局变量
    global threshold_cpu_usage 
    threshold_cpu_usage = value

def get_threshold_cpu_usage():
    global threshold_cpu_usage
    return threshold_cpu_usage