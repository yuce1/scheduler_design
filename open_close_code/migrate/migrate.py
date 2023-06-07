#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import string
import subprocess
import json
import requests
import re
from conf import *



class node:
	node_name = ""
	status = ""
	role = ""
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
	close_node_list = []
	get_node_cmd = "kubectl get nodes | grep \" Ready\""
	# 执行以上命令，并且返回结果
	textlist = os.popen(get_node_cmd).readlines()
	# 异常处理,读取到的文件应该总是一行，进行基本的判断
	num_node = len(textlist)
	if(num_node<=close_node_num):
		print(f"关闭 {close_node_num} 个结点之后，集群节点将全部被关闭！")
		sys.exit()
	else:
		i = 0
		mp = {}
		
		while(i<num_node):
			inf_list = textlist[i].strip().split()
			node_name = inf_list[0]
			status = inf_list[1]
			role = inf_list[2]
			print(node_name)
			print(status)
			print(role)
			node_list.append(node_name)
			if(status == "Ready" and role != "master"):
				run_node = get_run_pod_num(node_name)
				if(len(mp) < close_node_num):
					mp[node_name] = run_node
				else:
					mp[node_name] = run_node
					maxK = ""
					maxV = 0
					for key,value in mp.items():
						if(int(value) > maxV):
							maxV = int(value)
							maxK = key
					del mp[maxK]
					print(maxK + "节点上元素较多\n")
					node_list.remove(maxK)
				
			i = i+1

		print(f"需要关闭的 {close_node_num} 个节点是：")
		for key,value in mp.items():
			print(key + " ")
			node_list.remove(key)

		# 此时任务还没有完成，开始进行迁移
		# 此处考虑轮询
		# mp中是要关闭的节点
		print("目前处于可用的节点为：")
		for nd in node_list:
			print(nd + " ")
		
		for key,value in mp.items():
			print(key + " ")
			node_list.remove(key)

		
