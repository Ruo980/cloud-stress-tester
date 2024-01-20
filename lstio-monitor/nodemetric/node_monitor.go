package nodemetric

import (
	"context"
	"fmt"
	"github.com/prometheus/common/model"
	"lstio-monitor/client"
	"time"
)

// NodeMonitor
// @Description: 该类对外提供指定节点监控指标，包括内存使用率、CPU使用率、磁盘使用率、网络使用率。
type NodeMonitor struct {
	nodeName         string
	kubeConfig       client.KubeConfig
	prometheusConfig client.PrometheusConfig
}

// NewNodeMonitor
// @Description: 构造函数：返回一个 NodeMonitor 对象
// @return NodeMonitor
func NewNodeMonitor(nodeName string) *NodeMonitor {
	nodeMonitor := &NodeMonitor{
		nodeName:         nodeName,
		kubeConfig:       *client.NewKubeConfig(),
		prometheusConfig: *client.NewPrometheusConfig(),
	}
	return nodeMonitor
}

// GetNodeMemoryUsage
// @Description: 获取节点的当前内存使用率
// @receiver n
// @return float64
// @return error
func (n NodeMonitor) GetNodeMemoryUsage() (float64, error) {
	prometheusClient, err := n.prometheusConfig.GetPrometheusClient()
	if err != nil {
		panic(err.Error())
	}

	// 查询指定node节点的内存利用率
	query := fmt.Sprintf("(sum(node_memory_MemTotal_bytes{instance='%s'} - node_memory_MemAvailable_bytes{instance='%s'}) / sum(node_memory_MemTotal_bytes{instance='%s'}))*100", n.nodeName, n.nodeName, n.nodeName)
	value, _, err := prometheusClient.Query(context.Background(), query, time.Now())
	if err != nil {
		return 0, err
	}

	// 解析查询结果
	if vectorValue, ok := value.(model.Vector); ok {
		// 遍历样本点
		for _, sample := range vectorValue {
			// 获取内存利用率值
			memoryUtilization := float64(sample.Value)

			// 在这里，你可以将结果返回或进行其他处理
			return memoryUtilization, nil
		}
	} else {
		// 类型断言失败
		return 0, fmt.Errorf("unexpected value type, expected model.Vector")
	}

	// 如果到达这里，表示查询结果为空
	return 0, fmt.Errorf("no data found for memory usage")
}

// GetNodeCPULoad
// @Description: 获取节点的当前CPU利用率
// @receiver n
// @return float64
// @return error
func (n NodeMonitor) GetNodeCPULoad() (float64, error) {
	prometheusClient, err := n.prometheusConfig.GetPrometheusClient()
	if err != nil {
		panic(err.Error())
	}

	// 查询指定node节点的CPU利用率
	query := fmt.Sprintf("(1 - avg(rate(node_cpu_seconds_total{instance='%s',mode='idle'}[2m])) by (instance))*100", n.nodeName)
	value, _, err := prometheusClient.Query(context.Background(), query, time.Now())
	if err != nil {
		return 0, err
	}

	// 解析查询结果
	if vectorValue, ok := value.(model.Vector); ok {
		// 遍历样本点
		for _, sample := range vectorValue {
			// 获取CPU利用率值
			cpuUtilization := float64(sample.Value)

			// 在这里，你可以将结果返回或进行其他处理
			return cpuUtilization, nil
		}
	} else {
		// 类型断言失败
		return 0, fmt.Errorf("unexpected value type, expected model.Vector")
	}

	// 如果到达这里，表示查询结果为空
	return 0, fmt.Errorf("no data found for cpu load")
}

// GetNodeDiskUsage
// @Description: 获取节点的当前磁盘使用率
// @receiver n
// @return float64
// @return error
func (n NodeMonitor) GetNodeDiskUsage() (float64, error) {
	prometheusClient, err := n.prometheusConfig.GetPrometheusClient()
	if err != nil {
		panic(err.Error())
	}

	// 查询指定node节点的磁盘利用率
	query := fmt.Sprintf("(node_filesystem_size_bytes{instance='%s',fstype!='rootfs'} - node_filesystem_avail_bytes{instance='%s',fstype!='rootfs'}) / node_filesystem_size_bytes{instance='%s',fstype!='rootfs'}", n.nodeName, n.nodeName, n.nodeName)
	value, _, err := prometheusClient.Query(context.Background(), query, time.Now())
	if err != nil {
		return 0, err
	}

	// 解析查询结果
	if vectorValue, ok := value.(model.Vector); ok {
		// 遍历样本点
		for _, sample := range vectorValue {
			// 获取磁盘利用率值
			diskUtilization := float64(sample.Value)

			// 在这里，你可以将结果返回或进行其他处理
			return diskUtilization, nil
		}
	} else {
		// 类型断言失败
		return 0, fmt.Errorf("unexpected value type, expected model.Vector")
	}

	// 如果到达这里，表示查询结果为空
	return 0, fmt.Errorf("no data found for disk usage")
}

// GetNodeNetworkUsage
// @Description: 获取节点的当前网络使用率
// @receiver n
// @return float64
// @return error
func (n NodeMonitor) GetNodeNetworkUsage() (float64, error) {
	prometheusClient, err := n.prometheusConfig.GetPrometheusClient()
	if err != nil {
		panic(err.Error())
	}

	// 查询指定node节点的网络利用率
	query := fmt.Sprintf("sum(rate(node_network_receive_bytes_total{instance='%s'}[5m]))", n.nodeName)
	value, _, err := prometheusClient.Query(context.Background(), query, time.Now())
	if err != nil {
		return 0, err
	}

	// 解析查询结果
	if vectorValue, ok := value.(model.Vector); ok {
		// 遍历样本点
		for _, sample := range vectorValue {
			// 获取网络利用率值
			networkUtilization := float64(sample.Value)

			// 在这里，你可以将结果返回或进行其他处理
			return networkUtilization, nil
		}
	} else {
		// 类型断言失败
		return 0, fmt.Errorf("unexpected value type, expected model.Vector")
	}

	// 如果到达这里，表示查询结果为空
	return 0, fmt.Errorf("no data found for network usage")
}
