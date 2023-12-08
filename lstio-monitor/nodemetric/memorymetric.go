package nodemetric

import (
	"context"
	"encoding/csv"
	"fmt"
	v1 "github.com/prometheus/client_golang/api/prometheus/v1"
	"github.com/prometheus/common/model"
	"log"
	"lstio-monitor/client"
	"os"
	"time"
)

// 获取节点的内存使用率
func getNodeMemoryUsage(api v1.API, nodeName string) (float64, error) {
	// 查询内存使用率：获取最近5分钟的内存使用率
	query := fmt.Sprintf("(sum(node_memory_MemTotal_bytes{instance='%s'} - node_memory_MemAvailable_bytes{instance='%s'}) / sum(node_memory_MemTotal_bytes{instance='%s'}))*100", nodeName, nodeName, nodeName)
	result, _, err := api.QueryRange(
		context.Background(),
		query,
		// 设置查询的时间范围为最近5分钟，步长为15秒
		v1.Range{
			Start: time.Now().Add(-5 * time.Minute),
			End:   time.Now(),
			Step:  15 * time.Second,
		},
	)
	if err != nil {
		return 0, err
	}

	// 处理查询结果
	if result.Type() == model.ValMatrix {
		// 处理 Matrix 类型的结果
		matrix := result.(model.Matrix)
		if len(matrix) > 0 && len(matrix[0].Values) > 0 {
			// 取第一个样本点
			sample := matrix[0].Values[0]
			return float64(sample.Value), nil
		}
	}
	return 0, fmt.Errorf("unexpected result type: %s", result.Type())
}

// 内存Metric
func MemoryMetric() {
	// 获取Prometheus监控指标客户端
	config := client.NewPrometheusConfig()
	prometheusAPI, err := config.GetPrometheusClient()
	if err != nil {
		log.Fatalf("Error creating Prometheus client: %v", err)
	}

	// 创建 CSV 文件
	csvFileName := "./dataset/memory_usage.csv"
	csvFile, err := os.Create(csvFileName)
	if err != nil {
		log.Fatalf("Error creating CSV file: %v", err)
	}
	defer csvFile.Close()

	// 创建 CSV 写入器
	csvWriter := csv.NewWriter(csvFile)
	defer csvWriter.Flush()

	// 写入 CSV 表头
	if err := csvWriter.Write([]string{"Timestamp", "Memory_Usage"}); err != nil {
		log.Fatalf("Error writing CSV header: %v", err)
	}

	// 获取节点的内存使用率
	nodeName := "slave-node3"
	// 开始时间
	startTime := time.Now()

	// 定期查询内存使用率：每5秒获取一次指标数据
	for range time.Tick(15 * time.Second) {
		memoryUsage, err := getNodeMemoryUsage(prometheusAPI, nodeName)
		if err != nil {
			log.Fatalf("Error getting memory usage for node %s: %v", nodeName, err)
			continue
		}

		// 计算经过的时间
		elapsedTime := time.Since(startTime).Seconds()
		record := []string{fmt.Sprintf("%f", elapsedTime), fmt.Sprintf("%f", memoryUsage)}

		// 写入 CSV 记录
		if err := csvWriter.Write(record); err != nil {
			log.Printf("Error writing CSV record: %v", err)
			continue
		}

		// 手动刷新 CSV 写入器以确保数据写入文件
		csvWriter.Flush()
		log.Printf("Memory usage for node %s: %f%%", nodeName, memoryUsage)
	}
}
