
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import re
import psutil
import time
from conf import *
# from rapl import *


# 降低机器的cpu频率
def down_cpufreq():
	# 命令行中要运行的语句
	down_cpufreq_cmd = "echo \"powersave\" | sudo tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor"
	# 执行以上命令，并且返回结果
	textlist = os.popen(down_cpufreq_cmd).readlines()
	# 异常处理,读取到的文件应该总是一行，进行基本的判断
	for text in textlist:
		print("降低机器频率结果为：" + text)

# 提高机器的cpu频率
def up_cpufreq():
	# 命令行中要运行的语句
	up_cpufreq_cmd = "echo \"performance\" | sudo tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor"
	# 执行以上命令，并且返回结果
	textlist = os.popen(up_cpufreq_cmd).readlines()
	# 异常处理,读取到的文件应该总是一行，进行基本的判断
	for text in textlist:
		print("升高机器频率结果为：" + text)

# 获取cpu利用率
def get_cpu_usage():
	# 命令行中要运行的语句
	cpu_usage_cmd = "kubectl describe node " + node_name + " | grep \"cpuUse\""
	# 执行以上命令，并且返回结果
	cpu_usage = os.popen(cpu_usage_cmd).readlines()
	# 异常处理,读取到的文件应该总是一行，进行基本的判断
	if len(cpu_usage)==0:
		return ""
	return cpu_usage[0].strip().split('=')[1]

# 获取cpu目前所处的状态
def get_cpu_state(node):
	# 命令行中要运行的语句
	cpu_usage_cmd = "kubectl describe node " + node + " | grep \"cpuState\""
	# 执行以上命令，并且返回结果
	cpu_usage = os.popen(cpu_usage_cmd).readlines()
	# 异常处理,读取到的文件应该总是一行，进行基本的判断
	if len(cpu_usage)==0:
		return ""
	return cpu_usage[0].strip().split('=')[1]

if __name__ == "__main__":
	cpu_usage = get_cpu_usage()
	cpu_state = get_cpu_state(node_name)
	print("当前节点的cpu状态为：",cpu_state)
	print("当前节点的cpu利用率为：",cpu_usage)
	if(cpu_state == "powersave"):
		print("当前节点为关闭节点，无需迁移")
		sys.exit()
	if(float(cpu_usage) < threshold_cpu_usage):
		print("cpu利用率足够小，停止迁移")
		# 在此处停留几秒在查询结果，因为更改状态以及状态更新需要时间
		down_cpufreq()
	else:
		# 获取node列表
		get_node_cmd = "kubectl get nodes | grep \" Ready\" "
		# 执行以上命令，并且返回结果
		textlist = os.popen(get_node_cmd).readlines()
		# 异常处理,读取到的文件应该总是一行，进行基本的判断
		node_powersave = []
		for text in textlist:
			node = text.strip().split()[0]
			node_state = get_cpu_state(node)
			print(node + "的状态为：",node_state)
			if(node_state == "powersave"):
				node_powersave.append(node)
		
		print("以下节点的状态为powersave，可以向上调度任务")
		for a in node_powersave:
			print(a)
		
		# 获取当前节点运行的pod信息
		get_pod_cmd = "kubectl describe node " + node_name + " | grep \"default\""
		# 执行以上命令，并且返回结果
		pod_list = os.popen(get_pod_cmd).readlines()
		# 异常处理,读取到的文件应该总是一行，进行基本的判断
		num_pod = len(pod_list)
		if(num_pod != 0):
			print(f"{node_name} 节点上的pod {pod_list[0].split()[1]}需要被迁移走，应该迁移到{node_powersave[0]} 上")
		else:
			print(f"{node_name} 节点上没有pod未完成运行")
			
			



