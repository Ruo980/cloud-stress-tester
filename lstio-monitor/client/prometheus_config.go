package client

import (
	"github.com/prometheus/client_golang/api"
	v1 "github.com/prometheus/client_golang/api/prometheus/v1"
)

// 配置Prometheus，获取Prometheus的客户端

var prometheusConfig *PrometheusConfig

// PrometheusConfig
//
//	@Description: 该类对外提供Prometheus客户端。
type PrometheusConfig struct {
	// 添加你的 KubeConfig 相关字段
}

// NewPrometheusConfig
//
//	@Description: 构造函数：单例模式，返回一个 PrometheusConfig 对象
//	@return PrometheusConfig
func NewPrometheusConfig() *PrometheusConfig {
	// 单例模式
	if prometheusConfig == nil {
		prometheusConfig = &PrometheusConfig{}
	}
	return prometheusConfig
}

func (p *PrometheusConfig) GetProConfig() api.Config {
	// 替换为你的 Prometheus 服务器地址
	config := api.Config{
		//Address: "http://172.31.234.111:31995",// 容器指标监控，使用istio Prometheus
		Address: "http://127.0.0.1:9090", // 集群节点监控，使用kubernetes Prometheus
	}
	return config
}

// GetPrometheusClient
//
//	@Description: 创建 Prometheus 监控客户端
//	@receiver p
//	@return v1.API
//	@return error
func (p *PrometheusConfig) GetPrometheusClient() (v1.API, error) {

	config := p.GetProConfig()

	client, err := api.NewClient(config)
	if err != nil {
		return nil, err
	}

	return v1.NewAPI(client), nil
}
