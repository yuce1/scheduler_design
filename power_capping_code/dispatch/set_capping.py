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

# 获取标签中的cap状态，没有的话，返回空字符串
def get_cap_need_state():
	# 命令行中要运行的语句
	cap_need_state_cmd = "kubectl describe node " + node_name + " | grep \"capNeedSetState\""
	# 执行以上命令，并且返回结果
	cap_need_state = os.popen(cap_need_state_cmd).readlines()
	# 异常处理,读取到的文件应该总是一行，进行基本的判断
	if len(cap_need_state)==0:
		return ""
	return cap_need_state[0].strip().split('=')[1]


if __name__ == "__main__":
	while True:
		cap_state = get_cap_state()
		print("当前capping状态为：",cap_state)
		cap_need_state = get_cap_need_state()
		print("当前需要设置的capping状态为：",cap_need_state)
		
		if(cap_state != cap_need_state):
			if(cap_need_state == "capping"):
				print("调整服务器状态为capping")
				capping()
				cap_state = "capping"
			if(cap_need_state == "uncapping"):
				print("调整服务器状态为uncapping")
				uncapping()
				cap_state = "uncapping"
		cmd_power = "kubectl label nodes "+ node_name + " capState=" + str(cap_state) + " --overwrite"
		# 执行以上命令，并且返回结果
		textlist = os.popen(cmd_power).readlines()
		# 异常处理,读取到的文件应该总是一行，进行基本的判断
		for text in textlist:
			print(text)



		time.sleep(0.5)