
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import re
import psutil
import time
import json
from conf import *
# from rapl import *


# 进行capping
def capping():
	print("capping操作成功！")
	# i = 0
	# while(i<cpu_num):
	# 	su1 = set_power_limit(i, ["pkg_limit_1"], int(max_power*capping_proportion*1000000))
	# 	su2 = set_time_window(i, ["pkg_limit_1"], 3000000)
	# 	su3 = set_power_limit(i, ["pkg_limit_2"], int(max_power*capping_proportion*1000000))
	# 	su4 = set_time_window(i, ["pkg_limit_2"], 3000000)
	# 	if su1 == 0 | su2 == 0 | su3 == 0 | su4 == 0:
	# 		print("capping操作失败！")
	# 	else:
	# 		print("capping操作成功！")
	# 	i = i+1

# 获取cpu利用率
def get_cpu_power():
	# 命令行中要运行的语句
	cpu_power_cmd = "kubectl describe node " + node_name + " | grep \"power=\""
	# 执行以上命令，并且返回结果
	cpu_power = os.popen(cpu_power_cmd).readlines()
	# 异常处理,读取到的文件应该总是一行，进行基本的判断
	if len(cpu_power)==0:
		return ""
	return cpu_power[0].strip().split('=')[1]

# 获取cpu目前所处的状态
def get_cap_state(node):
	# 命令行中要运行的语句
	cap_state_cmd = "kubectl describe node " + node + " | grep \"capState\""
	# 执行以上命令，并且返回结果
	cap_state = os.popen(cap_state_cmd).readlines()
	# 异常处理,读取到的文件应该总是一行，进行基本的判断
	if len(cap_state)==0:
		return ""
	return cap_state[0].strip().split('=')[1]

if __name__ == "__main__":

	i = 0
	now = 0
	while(i<num+1):
		mig = []
		power = get_cpu_power()
		cap_state = get_cap_state(node_name)
		print("当前节点的cap状态为：",cap_state)
		print("当前节点的实时功率为：",power)
		if(cap_state == "capping"):
			print("当前节点为capping状态，无需迁移")
			sys.exit()
		if(float(power) < cpu_num*max_power*max_proportion):
			print("功率足够小，停止迁移")
			sys.exit()
		else:
			if(i == num):
				break
			# 获取node列表
			get_node_cmd = "kubectl get nodes | grep \" Ready\" "
			# 执行以上命令，并且返回结果
			textlist = os.popen(get_node_cmd).readlines()
			# 异常处理,读取到的文件应该总是一行，进行基本的判断
			node_uncapping = []
			for text in textlist:
				node = text.strip().split()[0]
				node_state = get_cap_state(node)
				print(node + "的状态为：",node_state)
				if(node_state == "uncapping" and node!=node_name):
					node_uncapping.append(node)
			
			print("以下节点的状态为uncapping，可以向上调度任务")
			for a in node_uncapping:
				print(a)
			
			# 获取当前节点运行的pod信息
			get_pod_cmd = "kubectl describe node " + node_name + " | grep \"default\""
			# 执行以上命令，并且返回结果
			pod_list = os.popen(get_pod_cmd).readlines()
			# 异常处理,读取到的文件应该总是一行，进行基本的判断
			num_pod = len(pod_list)
			
			can_use = len(node_uncapping)
			
			if(num_pod != 0 and can_use != 0):
				print(f"{node_name} 节点上的pod {pod_list[0].split()[1]}需要被迁移走，应该迁移到{node_uncapping[now%can_use]} 上")
				dic = {}
				dic["podName"] = pod_list[0].split()[1]
				dic["nameSpace"] = pod_list[0].split()[0]
				dic["nodeName"] = node_uncapping[now%can_use]
				mig.append(dic)
				fileName = "/root/workspace/schedule/power/power_capping_migrate.json"
				jsonObject = {
					"pods": mig
				}

				with open(fileName, "w") as file:
					json.dump(jsonObject, file)
				file.close()
			else:
				print(f"{node_name} 节点上没有pod未完成运行")
			
			i = i+1
			now = now+1
			print("第"+str(i)+"次迁移正在进行。。。")
			time.sleep(20)
			print("第"+str(i)+"次迁移完成")
			
	
	print("经过"+str(num)+"次迁移之后仍不能满足要求，进行功率封顶")
	capping()

			
			



