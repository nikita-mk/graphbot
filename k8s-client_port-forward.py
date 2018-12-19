from kubernetes import client, config,watch
from kubernetes.client.rest import ApiException
import json
import os


path = input("Enter the path to the kubeconfig : ")
namespace = input("Enter the namespace : ")
os.environ['KUBECONFIG'] = path
config.load_kube_config(path)
v1 = client.CoreV1Api()

try: 
    api_response_grafana = v1.list_namespaced_pod(namespace,label_selector='app=grafana')
    dict = api_response_grafana.to_dict()
    grafana_pod_name = dict['items'][0]['metadata']['name']
    port_grafana = dict['items'][0]['spec']['containers'][0]['liveness_probe']['http_get']['port'] 
    grafana_port_forward = "kubectl -n "+namespace+" port-forward "+grafana_pod_name+" "+str(port_grafana)+" &"
    os.system(grafana_port_forward)
    
    
    api_response_prometheus = v1.list_namespaced_pod(namespace,label_selector='app=prometheus,component=server')
    dict1 = api_response_prometheus.to_dict()
    prometheus_pod_name = dict1['items'][0]['metadata']['name']
    port_prometheus = dict1['items'][0]['spec']['containers'][1]['liveness_probe']['http_get']['port']
    prometheus_port_forward = "kubectl -n "+namespace+" port-forward "+prometheus_pod_name+" "+str(port_prometheus)
    os.system(prometheus_port_forward)

    
except ApiException as e:
        print("Exception when calling CoreV1Api : %s\n" % e)
