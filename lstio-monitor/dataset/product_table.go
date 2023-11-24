// Package dataset
// @Description: 将从Prometheus导出的数据CSV文件转换为图表进行可视化
package dataset

import (
	"encoding/csv"
	"fmt"
	"github.com/go-echarts/go-echarts/charts"
	"os"
	"strconv"
	"time"
)

func ProductCPUTable() {
	// 读取 CSV 文件
	file, err := os.Open("D:\\code-repository\\JetBrains\\WorkSpace\\cloud-stress-tester\\lstio-monitor\\dataset\\CPU_used\\test.csv")
	if err != nil {
		fmt.Println("Error opening file:", err)
		return
	}
	defer file.Close()

	reader := csv.NewReader(file)
	records, err := reader.ReadAll()
	if err != nil {
		fmt.Println("Error reading CSV:", err)
		return
	}

	// 解析数据
	var elapsedTimes []float64
	var cpuUtilizationData []float64

	// 解析时间和CPU利用率字段
	for _, record := range records[1:] { // 从第二行开始读取数据
		timeValue, err := time.Parse("2006-01-02 15:04:05", record[0])
		if err != nil {
			fmt.Println("Error parsing time:", err)
			return
		}
		elapsedTime := timeValue.Sub(timeValue.Truncate(time.Minute)).Minutes()
		elapsedTimes = append(elapsedTimes, elapsedTime)
		cpuUtilization, err := strconv.ParseFloat(record[1], 64)
		if err != nil {
			fmt.Println("Error parsing CPU utilization:", err)
			return
		}
		cpuUtilizationData = append(cpuUtilizationData, cpuUtilization)
	}

	// 创建折线图
	line := charts.NewLine()
	line.SetGlobalOptions(
		charts.TitleOpts{
			Title: "CPU Utilization",
		},
	)

	line.AddXAxis(elapsedTimes).AddYAxis("CPU Utilization", cpuUtilizationData)

	// 保存为 HTML 文件
	f, err := os.Create("cpu_utilization_chart.html")
	if err != nil {
		fmt.Println("Error creating HTML file:", err)
		return
	}
	line.Render(f)
}
