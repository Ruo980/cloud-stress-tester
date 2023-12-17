package envmetric

import (
	"context"
	"fmt"
	"github.com/prometheus/common/model"
	"lstio-monitor/client"
	"time"

	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
)

// EnvMonitor 强化学习环境特征监控：获取当前 Pods 的平均CPU利用率、内存利用率、可用Pod数量、请求率
type EnvMonitor struct {
	deploymentName   string
	namespace        string
	kubeConfig       client.KubeConfig
	prometheusConfig client.PrometheusConfig
}

// NewEnvMonitor 构造函数：返回一个 EnvMonitor 对象
func NewEnvMonitor() *EnvMonitor {
	envMonitor := EnvMonitor{
		deploymentName:   "stress-test-web-release-deployment",
		namespace:        "lry",
		prometheusConfig: *client.NewPrometheusConfig(),
		kubeConfig:       *client.NewKubeConfig2(),
	}
	return &envMonitor
}

// GetPodsCPUUsage 获取Pods的当前平均 CPU 利用率
func (e EnvMonitor) GetPodsCPUUsage() (float64, error) {
	prometheusClient, err := e.prometheusConfig.GetPrometheusClient()
	if err != nil {
		panic(err.Error())
	}

	// 查询 CPU 利用率
	query := "avg(irate(container_cpu_usage_seconds_total{container=\"stress-test-web\"}[1m]))"
	value, _, err := prometheusClient.Query(context.Background(), query, time.Now())
	if err != nil {
		return 0, err
	}
	// 解析查询结果
	vector, ok := value.(model.Vector)
	if !ok || len(vector) == 0 {
		return 0, fmt.Errorf("CPU query result is empty or not a vector")
	}

	// 获取第一个值
	cpuUsage := float64(vector[0].Value)

	return cpuUsage, nil

}

// GetPodsMemoryUsage 获取当前所有 pods 的内存平均使用量
func (e EnvMonitor) GetPodsMemoryUsage() (float64, error) {
	prometheusClient, err := e.prometheusConfig.GetPrometheusClient()
	if err != nil {
		panic(err.Error())
	}

	// 查询 内存平均使用量
	query := "avg(irate(container_memory_usage_bytes{container=\"stress-test-web\"}[1m]))"
	value, _, err := prometheusClient.Query(context.Background(), query, time.Now())
	if err != nil {
		return 0, err
	}
	// 解析查询结果
	vector, ok := value.(model.Vector)
	if !ok || len(vector) == 0 {
		return 0, fmt.Errorf("Memory query result is empty or not a vector")
	}

	// 获取第一个值
	memoryUsage := float64(vector[0].Value)

	return memoryUsage, nil
}

// GetDeploymentReplicas 获取可用Pods的数量: 通过 Deployment 获取 replicas 属性的值
func (e EnvMonitor) GetDeploymentReplicas() (int32, error) {
	clientSet, err := e.kubeConfig.GetClientSet()
	if err != nil {
		panic(err.Error())
	}
	deployment, err := clientSet.AppsV1().Deployments(e.namespace).Get(context.TODO(), e.deploymentName, metav1.GetOptions{})
	if err != nil {
		panic(err.Error())
	}
	// 返回 Deployment 的 AvailableReplicas，即当前可用的 Pod 数量
	return deployment.Status.AvailableReplicas, nil
}

// GetUserRequestRate 获取当前所有 Pods 的请求率
func (e EnvMonitor) GetUserRequestRate() (float64, error) {
	prometheusClient, err := e.prometheusConfig.GetPrometheusClient()
	if err != nil {
		panic(err.Error())
	}
	// 查询请求率
	query := `sum(irate(istio_requests_total{destination_app="stress-test-web"}[1m]))`
	value, _, err := prometheusClient.Query(context.Background(), query, time.Now())
	if err != nil {
		return 0, err
	}

	// 解析查询结果
	vector, ok := value.(model.Vector)
	if !ok || len(vector) == 0 {
		return 0, fmt.Errorf("RequestRate query result is empty or not a vector")
	}

	// 获取第一个值
	requestRate := float64(vector[0].Value)

	return requestRate, nil

}
