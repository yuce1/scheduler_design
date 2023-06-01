#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import re
import psutil
import time
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

if __name__ == "__main__":
	print("执行前查看信息")
	print(server_power)
	print(server_usage)
	i = 1
	j = 2
	while True:
		# read_server_power()
		# read_server_usage()
		# print("执行后查看信息")
		# print(server_power)
		# print(server_usage)
		i+=1
		j+=1
		server_power = i
		server_usage = j
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