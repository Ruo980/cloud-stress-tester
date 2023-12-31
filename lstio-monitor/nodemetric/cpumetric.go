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
	// 查询 CPU 利用率：获取最近5分钟的cpu空闲率，然后使用1-空闲率得到cpu使用率，由于得到的是小数形式，为了百分形式显示因此乘以100
	query := fmt.Sprintf("(1 - avg(rate(node_cpu_seconds_total{instance='%s',mode='idle'}[5m])) by (instance))*100", nodeName)
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

func CPUMetric() {
	// 获取Prometheus监控指标客户端
	config := client.NewPrometheusConfig()
	prometheusAPI, err := config.GetPrometheusClient()
	if err != nil {
		log.Fatalf("Error creating Prometheus client: %v", err)
	}

	// 创建 CSV 文件
	csvFileName := "./dataset/cpu_load.csv"
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
	for range time.Tick(15 * time.Second) {
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
