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
	mig = []
	get_node_cmd = "kubectl get nodes | grep \" Ready\""
	# 执行以上命令，并且返回结果
	textlist = os.popen(get_node_cmd).readlines()
	# 异常处理,读取到的文件应该总是一行，进行基本的判断
	num_node = len(textlist)
	if(num_node<=close_node_num+1):
		print(f"关闭 {close_node_num} 个结点之后，集群节点将全部被关闭！master不能运行任务！")
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
			if(role == "control-plane,master"):
				node_list.remove(node_name)
			if(status == "Ready" and role != "control-plane,master"):
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
					
				
			i = i+1

		print(f"需要关闭的 {close_node_num} 个节点是：")
		for key,value in mp.items():
			print(key + " ")
			close_node_list.append(key)
			node_list.remove(key)

		# 此时任务还没有完成，开始进行迁移
		# 此处考虑轮询
		# mp中是要关闭的节点
		print("目前处于可用的节点为：")
		for nd in node_list:
			print(nd + " ")
		can_use = len(node_list)
		now = 0
		
		for key,value in mp.items():
			get_pod_cmd = "kubectl describe node " + key + " | grep \"default\""
			# 执行以上命令，并且返回结果
			pod_list = os.popen(get_pod_cmd).readlines()
			# 异常处理,读取到的文件应该总是一行，进行基本的判断
			num_node = len(pod_list)
			if(num_node != 0):
				for pod in pod_list:
					dic = {}
					print(f"{key} 节点上的pod {pod.split()[1]}需要被迁移走，应该迁移到{node_list[now%can_use]} 上")
					dic["podName"] = pod.split()[1]
					dic["nameSpace"] = pod.split()[0]
					dic["nodeName"] = node_list[now%can_use]
					mig.append(dic)
					now += 1
			else:
				print(f"{key} 节点上没有pod未完成运行")
		
		fileName = "/root/workspace/schedule/power/close_machine_migrate.json"
		jsonObject = {
			"pods": mig,
			"powerOff": close_node_list
		}

		with open(fileName, "w") as file:
			json.dump(jsonObject, file)
		file.close()

		
