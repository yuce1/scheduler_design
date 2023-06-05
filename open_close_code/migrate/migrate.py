#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import subprocess
import json
import requests
import re
from conf import *
import heapq



class node:
	node_name = ""
	status = ""
	pod_num = 0


def get_run_pod_num(node_name):

	get_pod_num = "kubectl describe node " + node_name + "| grep \"Non-terminated Pods: \""
	pods_inf = os.popen(get_pod_num).readlines()
	if(len(pods_inf) != 1):
		print("获取运行pod个数信息失败！")
		exit(-1)
	pod_rum = pods_inf[0].strip().split('(')[1].split()[0]

	# 异常处理,读取到的文件应该总是一行，进行基本的判断
	return pod_rum


if __name__ == "__main__":
	node_list = []
	run_node_num_list = []
	close_node_list = []
	get_node_cmd = "kubectl get nodes"
	# 执行以上命令，并且返回结果
	textlist = os.popen(get_node_cmd).readlines()
	# 异常处理,读取到的文件应该总是一行，进行基本的判断
	num_node = len(textlist)-1
	if(num_node<=0):
		print("无可用节点！")
		sys.exit()
	else:
		i = 1
		while(i<=num_node):
			inf_list = textlist[i].strip().split()
			node_name = inf_list[0]
			status = inf_list[1]
			print(node_name)
			print(status)
			if(status == "Ready"):
				run_node = get_run_pod_num(node_name)
				
			i = i+1

			num = 0
			if(len(heapq) > 0 and num < close_node_num):
				print(heapq.heappop())
		
