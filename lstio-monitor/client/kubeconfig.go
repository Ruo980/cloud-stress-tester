package client

import (
	"flag"
	"k8s.io/client-go/dynamic"
	"k8s.io/client-go/kubernetes"
	"k8s.io/client-go/rest"
	"k8s.io/client-go/tools/clientcmd"
	"k8s.io/client-go/util/homedir"
	"log"
	"path/filepath"
)

// KubeConfig
//
//	@Description: 用于获取 kubernetes 配置文件。
type KubeConfig struct {
}

// NewKubeConfig 构造函数：返回一个 KubeConfig 对象
func NewKubeConfig() KubeConfig {
	return KubeConfig{}
}

// GetKubeConfig
//
//	@Description: 获取 Kubernetes 配置。
//	@receiver k
//	@return *rest.Config
//	@return error
func (k KubeConfig) GetKubeConfig() (*rest.Config, error) {
	// 配置文件路径
	var kubeconfig *string

	// home是家目录：如果能取得家目录的值，就将家目录中默认的kubeconfig用来做默认值
	if home := homedir.HomeDir(); home != "" {
		// 如果输入了kubeconfig参数，该参数的值就是kubeconfig文件的绝对路径，
		// 如果没有输入kubeconfig参数，就用默认路径~/.kube/config
		log.Printf("home: %s", home)
		kubeconfig = flag.String("kubeconfig", filepath.Join(home, ".kube", "config"), "(optional) absolute path to the kubeconfig file")
	} else {
		// 如果取不到当前用户的家目录，我们就使用项目相对目录中的config文件作为配置文件
		log.Printf("home: %s", home)
		kubeconfig = flag.String("kubeconfig", "./config", "absolute path to the kubeconfig file")
	}
	// 使用默认路径（""）和默认配置文件（""）构建 Kubernetes 配置
	config, err := clientcmd.BuildConfigFromFlags("", *kubeconfig)
	if err != nil {
		return nil, err
	}
	return config, nil
}

// GetClientSet
//
//	@Description: 返回基于提供的配置的 Kubernetes 客户端集。
//	@receiver k
//	@return *kubernetes.Clientset
//	@return error
func (k KubeConfig) GetClientSet() (*kubernetes.Clientset, error) {
	// 获取 Kubernetes 配置
	config, err := k.GetKubeConfig()
	if err != nil {
		return nil, err
	}

	// 基于配置创建 Kubernetes 客户端集
	clientset, err := kubernetes.NewForConfig(config)
	if err != nil {
		return nil, err
	}
	return clientset, nil
}

// GetDynamicClient
//
//	@Description: 返回基于提供的配置的 Kubernetes 动态客户端。
//	@receiver k
//	@return dynamic.Interface
//	@return error
func (k KubeConfig) GetDynamicClient() (dynamic.Interface, error) {
	// 获取 Kubernetes 配置
	config, err := k.GetKubeConfig()
	if err != nil {
		return nil, err
	}

	// 基于配置创建 Kubernetes 动态客户端
	dynamicClient, err := dynamic.NewForConfig(config)
	if err != nil {
		return nil, err
	}
	return dynamicClient, nil
}
