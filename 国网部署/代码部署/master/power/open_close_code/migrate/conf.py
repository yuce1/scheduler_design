#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys


close_node_num = 1

def set_close_node_num(value):
	# 定义一个全局变量
	global close_node_num 
	close_node_num = value

def get_close_node_num():
	global close_node_num
	return close_node_num