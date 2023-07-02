#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import subprocess
import json
import requests
import re


class node:
	node_name = ""
	status = ""
	total_cpu = 0
	total_mem = 0
	use_cpu = 0
	use_mem = 0



# 获取节点资源容量
def get_node_capacity(node_name):
	command = f"kubectl get nodes {node_name} -o json"
	process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	output, error = process.communicate()

	if process.returncode != 0:
		print("获取节点：" + node_name + f"资源容量信息执行出错: {error.decode('utf-8')}")
		return None

	# 解析命令输出的 JSON 数据
	node_info = json.loads(output)

	# 获取节点的资源容量信息
	capacity = node_info["status"]["capacity"]

	return capacity

# 获取节点可以分配的资源总量
def get_node_allocatable_resource(node_name):
	command = f"kubectl get nodes {node_name} --output=json"
	process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	output, error = process.communicate()

	if process.returncode != 0:
		print("获取节点：" + node_name + f"可使用资源总量执行出错: {error.decode('utf-8')}")
		return None

	# 解析命令输出的 JSON 数据
	node_info = json.loads(output)

	# 获取节点的资源使用量信息
	usage = node_info["status"]["allocatable"]

	return usage

def get_used_resources(node_name):
	used_resources = {}

	get_cpu_use = "kubectl describe node " + node_name + "| grep \"cpu \""
	get_mem_use = "kubectl describe node " + node_name + "| grep \"memory \""
	get_pod_num = "kubectl describe node " + node_name + "| grep \"Non-terminated Pods: \""
	# 执行以上命令，并且返回结果
	cpu_inf = os.popen(get_cpu_use).readlines()
	if(len(cpu_inf) != 1):
		print("获取cpu使用信息失败！")
		exit(-1)
	cpu_use = cpu_inf[0].strip().split()[1]
	used_resources["cpu_use"] = cpu_use
	
	mem_inf = os.popen(get_mem_use).readlines()
	if(len(mem_inf) != 2):
		print("获取mem使用信息失败！")
		exit(-1)
	mem_use = mem_inf[1].strip().split()[1]
	used_resources["mem_use"] = mem_use

	pods_inf = os.popen(get_pod_num).readlines()
	if(len(pods_inf) != 1):
		print("获取运行pod个数信息失败！")
		exit(-1)
	pod_rum = pods_inf[0].strip().split('(')[1].split()[0]
	used_resources["pod_rum"] = pod_rum

	# 异常处理,读取到的文件应该总是一行，进行基本的判断
	return used_resources


if __name__ == "__main__":
	node_list = []
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
			# 获取节点资源容量
			node_capacity = get_node_capacity(node_name)

			if node_capacity:
				print(f"节点 {node_name} 的资源容量为:")
				print(node_capacity)

			# 获取节点可分配资源总量
			node_allocatable = get_node_allocatable_resource(node_name)

			if node_allocatable:
				print(f"节点 {node_name} 的可使用资源总量为:")
				print(node_allocatable)
			

			# 获取节点的已使用资源信息
			used_resources = get_used_resources(node_name)

			if used_resources:
				print(f"节点 {node_name} 的已使用资源信息为:")
				print(used_resources)
				if(used_resources["cpu_use"] == "0" and used_resources["mem_use"] == "0"):
					close_node_list.append(node_name)

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
