package main

import "lstio-monitor/nodemetric"

func main() {
	// 生成cpu指标样本数据
	nodemetric.CPUMetric()
	nodemetric.MemoryMetric()
}
