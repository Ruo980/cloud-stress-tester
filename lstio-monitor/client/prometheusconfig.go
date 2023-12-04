package client

import (
	"github.com/prometheus/client_golang/api"
	v1 "github.com/prometheus/client_golang/api/prometheus/v1"
)

// 配置Prometheus，获取Prometheus的客户端

// PrometheusConfig
//
//	@Description: 该类对外提供Prometheus客户端。
type PrometheusConfig struct {
	// 添加你的 KubeConfig 相关字段
}

// NewPrometheusConfig
//
//	@Description: 构造函数：返回一个 PrometheusConfig 对象
//	@return PrometheusConfig
func NewPrometheusConfig() PrometheusConfig {
	return PrometheusConfig{}
}

// 创建 Prometheus 监控客户端
func (p PrometheusConfig) GetPrometheusClient() (v1.API, error) {
	// 替换为你的 Prometheus 服务器地址
	config := api.Config{
		Address: "http://localhost:9090",
	}

	client, err := api.NewClient(config)
	if err != nil {
		return nil, err
	}

	return v1.NewAPI(client), nil
}
