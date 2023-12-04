package nodemetric

import (
	"context"
	"encoding/csv"
	"fmt"
	"log"
	"os"
	time "time"

	v1 "github.com/prometheus/client_golang/api/prometheus/v1"
	"github.com/prometheus/common/model"

	"lstio-monitor/client"
)

// 获取节点的 CPU 利用率
func getNodeCPULoad(api v1.API, nodeName string) (float64, error) {
	query := fmt.Sprintf("100 - (sum(irate(node_cpu_seconds_total{mode='idle', node='%s'}[5m])) / scalar(count(node_cpu_seconds_total{mode='idle', node='%s'}[5m]))) * 100", nodeName, nodeName)
	result, _, err := api.QueryRange(context.Background(), query, v1.Range{Start: time.Now().Add(-5 * time.Minute), End: time.Now()})
	if err != nil {
		return 0.0, err
	}

	// 计算整个时间范围的平均值
	var sum float64
	var count float64

	for _, value := range result.(model.Matrix) {
		for _, sample := range value.Values {
			sum += float64(sample.Value)
			count++
		}
	}

	if count == 0 {
		return 0.0, fmt.Errorf("no data available for calculation")
	}

	average := sum / count

	return 100.0 - average*100.0, nil
}

func CPUMetric() {
	// 获取Prometheus监控指标客户端
	config := client.NewPrometheusConfig()
	prometheusAPI, err := config.GetPrometheusClient()
	if err != nil {
		log.Fatalf("Error creating Prometheus client: %v", err)
	}

	// 创建 CSV 文件
	csvFileName := "cpu_load.csv"
	csvFile, err := os.Create(csvFileName)
	if err != nil {
		log.Fatalf("Error creating CSV file: %v", err)
	}
	defer csvFile.Close()

	// 创建 CSV 写入器
	csvWriter := csv.NewWriter(csvFile)
	defer csvWriter.Flush()

	// 写入 CSV 表头
	if err := csvWriter.Write([]string{"Timestamp", "CPU_Load"}); err != nil {
		log.Fatalf("Error writing CSV header: %v", err)
	}

	// 获取节点的 CPU 利用率
	nodeName := "slave-node3"
	// 开始时间
	startTime := time.Now()

	// 定期查询 CPU 利用率：每5秒获取一次指标数据
	for range time.Tick(5 * time.Second) {
		cpuLoad, err := getNodeCPULoad(prometheusAPI, nodeName)
		if err != nil {
			if err != nil {
				log.Fatalf("Error getting CPU load for node %s: %v", nodeName, err)
			}
			continue
		}

		// 计算经过的时间
		elapsedTime := time.Since(startTime).Seconds()
		record := []string{fmt.Sprintf("%f", elapsedTime), fmt.Sprintf("%f", cpuLoad)}

		// 写入 CSV 记录
		if err := csvWriter.Write(record); err != nil {
			log.Printf("Error writing CSV record: %v", err)
			continue
		}

		// 手动刷新 CSV 写入器以确保数据写入文件
		csvWriter.Flush()
		log.Printf("CPU load for node %s: %f%%", nodeName, cpuLoad)
	}
}
