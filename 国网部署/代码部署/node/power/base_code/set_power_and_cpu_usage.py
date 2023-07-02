#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import re
import psutil
import time
import requests
import json
from conf import *

server_power = 0
server_usage = -1

# 通过接口获取服务器功率
def get_power_http(node):
		global server_power
		url = "http://192.168.1.14:8079/kube/v1/api/all/eer"
		mydata = {}  # 字典格式，推荐使用，它会自动帮你按照k-v拼接url
		res = requests.post(url=url, data=mydata)
		power_dic = json.loads(res.text)
		server_power = power_dic['data'][0]['nodes'][node]


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

# 获取cpu目前所处的状态
def get_cpu_state():
	global cpu_state
	# 命令行中要运行的语句
	cpu_state_cmd = "cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor"
	# 执行以上命令，并且返回结果
	cpu_state = os.popen(cpu_state_cmd).readlines()[0].strip()

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


if __name__ == "__main__":
	print("执行前查看信息")
	print(server_power)
	print(server_usage)
	# i = 1
	# j = 2
	# k = 0
	# state_list = ["ondemand", "performance", "powersave"]
	while True:
		get_power_http(node_name)
		# read_power_tool()
		read_server_usage()
		get_cpu_state()
		print("执行后查看信息")
		print(server_power)
		print(server_usage)
		print(cpu_state)
		# i+=1
		# j+=1
		# k+=1
		
		# server_power = i
		# server_usage = j
		# cpu_state = state_list[k%3]

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

		cmd_state = "kubectl label nodes "+ node_name + " cpuState=" + str(cpu_state) + " --overwrite"
		# 执行以上命令，并且返回结果
		textlist = os.popen(cmd_state).readlines()
		# 异常处理,读取到的文件应该总是一行，进行基本的判断
		for text in textlist:
			print(text)


		time.sleep(0.5)
