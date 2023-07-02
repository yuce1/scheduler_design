package main

import (
	"log"
	// "math/rand"
	"fmt"
	"os/exec"

	// "strconv"
	// "strings"
	"bytes"

	extender "k8s.io/kube-scheduler/extender/v1"
)

// It'd better to only define one custom priority per extender
// as current extender interface only supports one single weight mapped to one extender
// and also it returns HostPriorityList, rather than []HostPriorityList

const (
	// lucky priority gives a random [0, extender.MaxPriority] score
	// currently extender.MaxPriority is 10
	luckyPrioMsg = "pod %v/%v is lucky to get score %v on node %v\n"
)

// it's webhooked to pkg/scheduler/core/generic_scheduler.go#prioritizeNodes()
// you can't see existing scores calculated so far by default scheduler
// instead, scores output by this function will be added back to default scheduler
func prioritize(args extender.ExtenderArgs) *extender.HostPriorityList {
	log.Printf("--------+++++++++prioritize++++++++++++-------------------")
	pod := args.Pod
	nodes := args.Nodes.Items

	is_all_capping := true
	//进行一轮筛选，判断是否有节点 没有处于 powersave状态
	for _, node := range nodes {
		cap_state := node.ObjectMeta.Labels["capState"]
		if cap_state != "capping" {
			is_all_capping = false
			break
		}
	}

	hostPriorityList := make(extender.HostPriorityList, len(nodes))
	//全都处于powersave状态，随机选择一个节点，给该节点打分为10，并且调整该节点的cpu频率为performance
	if is_all_capping {
		for i, node := range nodes {
			cap_state := node.ObjectMeta.Labels["capState"]

			log.Printf("节点%v的cpu状态为:%v", node.Name, cap_state)
			if i == 0 {
				score := int64(10)
				log.Printf(luckyPrioMsg, pod.Name, pod.Namespace, score, node.Name)
				hostPriorityList[i] = extender.HostPriority{
					Host:  node.Name,
					Score: score,
				}
				log.Printf("节点%v被选取", node.Name)
				run_cmd := "kubectl label nodes " + node.Name + " capNeedSetState=uncapping --overwrite"
				log.Printf("需要执行命令：%v", run_cmd)
				cmd := exec.Command("kubectl", "label", "nodes", node.Name, "capNeedSetState=uncapping", "--overwrite")

				var out bytes.Buffer
				var stderr bytes.Buffer
				cmd.Stdout = &out
				cmd.Stderr = &stderr
				err := cmd.Run()
				if err != nil {
					fmt.Println(fmt.Sprint(err) + ": " + stderr.String())
				}
				fmt.Println("Result: " + out.String())

			} else {
				score := int64(0)
				log.Printf(luckyPrioMsg, pod.Name, pod.Namespace, score, node.Name)
				hostPriorityList[i] = extender.HostPriority{
					Host:  node.Name,
					Score: score,
				}
			}

		}
	} else {
		for i, node := range nodes {
			cap_state := node.ObjectMeta.Labels["capState"]

			log.Printf("节点%v的cpu状态为:%v", node.Name, cap_state)
			if cap_state != "capping" {
				score := int64(10)
				log.Printf(luckyPrioMsg, pod.Name, pod.Namespace, score, node.Name)
				hostPriorityList[i] = extender.HostPriority{
					Host:  node.Name,
					Score: score,
				}
			} else {
				score := int64(0)
				log.Printf(luckyPrioMsg, pod.Name, pod.Namespace, score, node.Name)
				hostPriorityList[i] = extender.HostPriority{
					Host:  node.Name,
					Score: score,
				}
			}

		}
	}

	log.Printf("   ")

	return &hostPriorityList
}
