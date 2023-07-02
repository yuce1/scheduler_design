#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import subprocess
import json
import requests
import re




if __name__ == "__main__":
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
		s = set(["dev","kube-system","kubernetes-dashboard","monitoring","wisdomtest1"])
		i = 1
		while(i<=num_node):
			inf_list = textlist[i].strip().split()
			node_name = inf_list[0]
			status = inf_list[1]
			print(node_name)
			print(status)

			if(node_name == "master14"):
				i = i+1
				continue

			get_pod_num = "kubectl describe node " + node_name + "| grep \"Non-terminated Pods: \""
			pods_inf = os.popen(get_pod_num).readlines()
			if(len(pods_inf) != 1):
				print("获取运行pod个数信息失败！")
				exit(-1)
			pod_rum = int(pods_inf[0].strip().split('(')[1].split()[0])

			get_node_inf = "kubectl describe node " + node_name
			# 执行以上命令，并且返回结果
			ansList = os.popen(get_node_inf).readlines()
			tol = len(ansList)
			temp =  0
			while temp<tol:
				a = re.search("Non-terminated Pods:",ansList[temp])
				if a:
					temp += 2
					ttemp = 1
					while(ttemp<=pod_rum):
						namesp = ansList[temp+ttemp].strip().split(" ")[0].strip()
						print(namesp)
						if(namesp not in s):
							break
						ttemp += 1
					if(ttemp > pod_rum):
						close_node_list.append(node_name)
					break
				temp += 1

			i = i+1
		
		if(len(close_node_list) != 0):
			print("\n以下节点上没有pod运行，需要关闭:")
			for cn in close_node_list:
				print(cn + " ")
			fileName = "/root/workspace/schedule/power/mac_close.json"
			jsonObject = {
				"powerOff": close_node_list
			}

			with open(fileName, "w") as file:
				json.dump(jsonObject, file)
			file.close()
