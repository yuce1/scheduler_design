#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import re
import psutil
import time
import json
import requests
from conf import *


server_power = 0
server_usage = -1


# 解析IPMI，获取整个服务器的实时功耗
def read_server_power():
	global server_power
	# 命令行中要运行的语句
	cmd1 = "ipmitool sdr elist | grep \"Power\""
	# 执行以上命令，并且返回结果
	textlist = os.popen(cmd1).readlines()
	# 异常处理,读取到的文件应该总是一行，进行基本的判断
	for text in textlist:
		a = re.match(r'^Power{2,\s}',text)
		if a:
			print(text)
	# 进行字符串处理
	temp_list = textlist[0].split("|")
	server_power = int(temp_list[-1].strip().split(" ")[0])

# 通过接口获取服务器功率
def get_power_http(node):
		global server_power
		url = "http://192.168.1.14:8079/kube/v1/api/all/eer"
		mydata = {}  # 字典格式，推荐使用，它会自动帮你按照k-v拼接url
		res = requests.post(url=url, data=mydata)
		power_dic = json.loads(res.text)
		server_power = power_dic['data'][0]['nodes'][node]


# 使用工具获取power
def read_power_tool():
	global server_power
	# 命令行中要运行的语句
	cmd1 = "s-tui -j"
	# 执行以上命令，并且返回结果
	text = os.popen(cmd1).read()
	# 异常处理,读取到的文件应该总是一行，进行基本的判断
	cpu_dict = json.loads(text)
	server_power = float(cpu_dict.get("Power")["package-0,0"]) + float(cpu_dict.get("Power")["dram,0"])

# 获取整台服务器的利用率
def read_server_usage():
	global server_usage
	server_usage = psutil.cpu_percent(interval=None)

# 获取整台服务器的利用率,执行时间较慢，弃用
def read_server_usage_old():
	global server_usage
	# 命令行中要运行的语句
	cmd1 = "sar -P ALL -u 1 5"
	# 执行以上命令，并且返回结果
	textlist = os.popen(cmd1).readlines()
	# 异常处理,读取到的文件应该总是一行，进行基本的判断
	for text in textlist:
		a = re.match(r'^Average:\s+all\s+\S+\s+',text)
		if a:
			temp_list = re.split(r'\s+', text)
			server_usage = temp_list[2]
	if server_usage == -1:
		sys.stderr.write("[ERROR] 无法获取整台服务器的CPU利用率!\n")
		exit(-1)

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


if __name__ == "__main__":
	print("执行前查看信息")
	print(server_power)
	print(server_usage)
	# i = 1
	# j = 2
	while True:
		# read_server_power()
		get_power_http(node_name)
		read_power_tool()
		read_server_usage()
		print("执行后查看信息")
		print(server_power)
		print(server_usage)
		# i+=1
		# j+=1
		# server_power = i
		# server_usage = j
		cpu_state = get_cpu_state()
		if(server_usage < cpu_th and cpu_state != "powersave"):
			print("cpu利用率低，进行频率调节，将频率调小")
			down_cpufreq()

		if(server_usage > cpu_th and cpu_state != "performance"):
			print("cpu利用率升高，进行频率调节，将频率调大")
			up_cpufreq()
		cmd_power = "kubectl label nodes "+ node_name + " power=" + str(server_power) + " --overwrite"
		# 执行以上命令，并且返回结果
		textlist = os.popen(cmd_power).readlines()
		# 异常处理,读取到的文件应该总是一行，进行基本的判断
		for text in textlist:
			print(text)

		cmd_usage = "kubectl label nodes "+ node_name + " cpuUse=" + str(server_usage) + " --overwrite"
		# 执行以上命令，并且返回结果
		textlist = os.popen(cmd_usage).readlines()
		# 异常处理,读取到的文件应该总是一行，进行基本的判断
		for text in textlist:
			print(text)


		time.sleep(0.5)
