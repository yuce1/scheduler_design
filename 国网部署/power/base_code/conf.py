#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys


node_name = "node232"

def set_node_name(value):
    # 定义一个全局变量
    global node_name 
    node_name = value

def get_node_name():
    global node_name
    return node_name