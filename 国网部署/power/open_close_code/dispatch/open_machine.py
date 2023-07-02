#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import subprocess
import json
import requests
import re

def open_new_mach():
	get_node_cmd = "kubectl get nodes | grep \"NotReady\""
	# 执行以上命令，并且返回结果
	textlist = os.popen(get_node_cmd).readlines()
	# 异常处理,读取到的文件应该总是一行，进行基本的判断
	if(len(textlist) == 0):
		print("集群没有关闭的节点，需对集群进行扩容，或者等待其他pod运行完毕，让出资源")
	else:
		print(f"node {textlist[0].strip().split()[0]} 需要被开启")
		openList = []
		openList.append(textlist[0].strip().split()[0])
		fileName = "/root/workspace/schedule/power/mac_open.json"
		jsonObject = {
			"powerOn": openList
		}

		with open(fileName, "w") as file:
			json.dump(jsonObject, file)
		file.close()

if __name__ == "__main__":
	get_pod_cmd = "kubectl get pods"
	# 执行以上命令，并且返回结果
	textlist = os.popen(get_pod_cmd).readlines()
	# 异常处理,读取到的文件应该总是一行，进行基本的判断
	node_num = len(textlist)-1
	if(node_num<=0):
		print("无pod运行！")
		sys.exit()
	else:
		i = 1
		isOpen = False
		while(i<=node_num):
			inf_list = textlist[i].strip().split()
			pod_name = inf_list[0]
			status = inf_list[2]
			if(status == "Pending"):
				get_pod_reason = "kubectl describe pod " + pod_name + " |grep \"Insufficient\""
				# 执行以上命令，并且返回结果
				pod_reason_list = os.popen(get_pod_reason).readlines()
				# 异常处理,读取到的文件应该总是一行，进行基本的判断
				if(len(pod_reason_list) > 0):
					print(f"pod {pod_name} 处于pending状态，并且因为资源不足无法运行，需要开启新的节点:")
					isOpen = True
				
			i = i+1
		if(isOpen):
			open_new_mach()

