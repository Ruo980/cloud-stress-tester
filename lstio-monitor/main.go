package main

import (
	"encoding/csv"
	"fmt"
	"lstio-monitor/envmetric"
	"os"
	"time"
)

func main() {
	// 创建 EnvMonitor 对象
	envMonitor := envmetric.NewEnvMonitor()

	// 创建 CSV 文件
	file, err := os.Create("./dataset/metric_data.csv")
	if err != nil {
		fmt.Printf("Error creating CSV file: %v\n", err)
		return
	}
	defer file.Close()

	// 创建 CSV Writer
	writer := csv.NewWriter(file)

	// 写入 CSV 表头
	headers := []string{"Timestamp", "CPU Usage", "Memory Usage", "Replicas", "User Request Rate"}
	if err := writer.Write(headers); err != nil {
		fmt.Printf("Error writing CSV header: %v\n", err)
		return
	}
	// 刷新数据到数据集中
	writer.Flush()

	// 启动 Goroutine 持续监听
	go func() {
		for {
			// 获取时间戳
			timestamp := time.Now()

			// 获取并输出 Pods 的 CPU 利用率
			cpuUsage, err := envMonitor.GetPodsCPUUsage()
			if err != nil {
				fmt.Printf("Error getting CPU usage: %v\n", err)
			}

			// 获取并输出 Pods 的内存利用率
			memoryUsage, err := envMonitor.GetPodsMemoryUsage()
			if err != nil {
				fmt.Printf("Error getting memory usage: %v\n", err)
			}

			// 获取并输出 Deployment 的可用 Pod 数量
			replicas, err := envMonitor.GetDeploymentReplicas()
			if err != nil {
				fmt.Printf("Error getting deployment replicas: %v\n", err)
			}

			// 获取并输出用户请求速率
			requestRate, err := envMonitor.GetUserRequestRate()
			if err != nil {
				fmt.Printf("Error getting user request rate: %v\n", err)
			}

			// 将指标数据直接写入CSV文件
			record := []string{
				timestamp.Format(time.RFC3339),
				fmt.Sprintf("%f", cpuUsage),
				fmt.Sprintf("%f", memoryUsage),
				fmt.Sprintf("%d", replicas),
				fmt.Sprintf("%f", requestRate),
			}
			if err := writer.Write(record); err != nil {
				fmt.Printf("Error writing CSV record: %v\n", err)
			}
			// 刷新数据到数据集中
			writer.Flush()

			// 打印当前指标数据
			fmt.Printf(
				"Timestamp: %v, CPU Usage: %f, Memory Usage: %f, Replicas: %d, User Request Rate: %f\n",
				timestamp, cpuUsage, memoryUsage, replicas, requestRate,
			)

			// 每隔一段时间执行一次
			time.Sleep(5 * time.Second)
		}
	}()

	// 防止主 Goroutine 退出
	select {}
}
