import subprocess
import json
import os

def get_node_labels(node_name):
    # 执行 kubectl get node 命令并将结果解析为 JSON
    command = "kubectl get node -o json"
    result = subprocess.check_output(command, shell=True, text=True)
    data = json.loads(result)

    # 查找指定节点的标签信息
    for item in data["items"]:
        if item["metadata"]["name"] == node_name:
            return item["metadata"]["labels"]

    return None




if __name__ == "__main__":
	get_node_cmd = "kubectl get nodes"
	textlist = os.popen(get_node_cmd).readlines()
	# 异常处理,读取到的文件应该总是一行，进行基本的判断
	num_node = len(textlist)-1
	i = 1
	while(i<=num_node):
		inf_list = textlist[i].strip().split()
		node_name = inf_list[0]
		status = inf_list[1]
		print(node_name)
		print(status)
		if(status == "Ready"):
			# 获取节点的标签信息
			labels = get_node_labels(node_name)

			if labels:
				print(f"Node Labels for {node_name}:")
				for key, value in labels.items():
					print(f"  {key}: {value}")
			else:
				print(f"Node '{node_name}' not found.")
		i += 1