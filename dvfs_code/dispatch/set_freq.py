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

# 获取cpu目前所处的状态
def get_cpu_state():
	# 命令行中要运行的语句
	cpu_state_cmd = "cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor"
	# 执行以上命令，并且返回结果
	cpu_state = os.popen(cpu_state_cmd).readlines()[0]
	# 异常处理,读取到的文件应该总是一行，进行基本的判断
	return cpu_state

# 获取标签中的cap状态，没有的话，返回空字符串
def get_cpu_need_state():
	# 命令行中要运行的语句
	cpu_need_state_cmd = "kubectl describe node " + node_name + " | grep \"cpuNeedSetState\""
	# 执行以上命令，并且返回结果
	cpu_need_state = os.popen(cpu_need_state_cmd).readlines()
	# 异常处理,读取到的文件应该总是一行，进行基本的判断
	if len(cpu_need_state)==0:
		return ""
	return cpu_need_state[0].strip().split('=')[1]

if __name__ == "__main__":
	while True:
		cpu_state = "performance"
		# cpu_state = get_cpu_state()
		print("当前cpu状态为：",cpu_state)
		cpu_need_state = "powersave"
		# cpu_need_state = get_cpu_need_state()
		print("当前需要设置的cpu状态为：",cpu_need_state)
		
		if(cpu_state != cpu_need_state):
			if(cpu_need_state == "performance"):
				print("调整服务器状态为performance")
				up_cpufreq()
				cpu_state = "performance"
			if(cpu_need_state == "powersave"):
				print("调整服务器状态为powersave")
				down_cpufreq()
				cpu_state = "powersave"
		cmd_power = "kubectl label nodes "+ node_name + " cpuState=" + str(cpu_state) + " --overwrite"
		# 执行以上命令，并且返回结果
		textlist = os.popen(cmd_power).readlines()
		# 异常处理,读取到的文件应该总是一行，进行基本的判断
		for text in textlist:
			print(text)



		time.sleep(0.5)