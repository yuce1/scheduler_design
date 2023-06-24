#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import re
import psutil
import time
from conf import *
# from rapl import *

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

# 进行uncapping
def uncapping():
	print("uncapping操作成功！")
	# i = 0
	# while(i<cpu_num):
	# 	su1 = set_power_limit(i, ["pkg_limit_1"], int(max_power*1000000))
	# 	su2 = set_time_window(i, ["pkg_limit_1"], 3000000)
	# 	su3 = set_power_limit(i, ["pkg_limit_2"], int(max_power*1000000))
	# 	su4 = set_time_window(i, ["pkg_limit_2"], 3000000)
	# 	if su1 == 0 | su2 == 0 | su3 == 0 | su4 == 0:
	# 		print("uncapping操作失败！")
	# 	else:
	# 		print("uncapping操作成功！")
	# 	i = i+1

# 获取标签中的cap状态，没有的话，返回空字符串
def get_cap_state():
	# 命令行中要运行的语句
	cap_state_cmd = "kubectl describe node " + node_name + " | grep \"capState\""
	# 执行以上命令，并且返回结果
	cap_state = os.popen(cap_state_cmd).readlines()
	# 异常处理,读取到的文件应该总是一行，进行基本的判断
	if len(cap_state)==0:
		return ""
	return cap_state[0].strip().split('=')[1]


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
		cap_state = get_cap_state()
		print("当前capping状态为：",cap_state)
		if(server_power > cpu_num*max_power*max_proportion and cap_state != "capping"):
			print("服务器实时功率过高，进行power capping操作")
			capping()
			cap_state = "capping"

		if(server_power < cpu_num*max_power*min_proportion and cap_state != "uncapping"):
			print("服务器实时功率较低，解除power capping")
			uncapping()
			cap_state = "uncapping"
		cmd_power = "kubectl label nodes "+ node_name + " capState=" + str(cap_state) + " --overwrite"
		# 执行以上命令，并且返回结果
		textlist = os.popen(cmd_power).readlines()
		# 异常处理,读取到的文件应该总是一行，进行基本的判断
		for text in textlist:
			print(text)



		time.sleep(0.5)