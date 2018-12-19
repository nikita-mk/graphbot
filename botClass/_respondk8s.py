import os
from slackclient import SlackClient
from kubernetes import client, config
from kubernetes.client.rest import ApiException
import yaml
import subprocess
import json

def respondk8s(self, channel,listt=[]):
    print(listt)
    
    path = <kubeconfig>
    namespace = <namespace>
    os.environ['KUBECONFIG'] = path
    config.load_kube_config(path)
    api_instance = client.CoreV1Api()
    v = client.ExtensionsV1beta1Api()
    c = client.AppsV1Api()

    text1 = ''
    try: 
        if listt[0]=='get':
            if listt[1]=='pods':
                api_response= api_instance.list_namespaced_pod(namespace)
                dict = api_response.to_dict()
                for i in range(len(dict['items'])):
                    text1 += dict['items'][i]['status']['phase'] + '\t\t' + dict['items'][i]['metadata']['name'] 
                    text1 += '\n'
            elif listt[1]=='services':
                api_response= api_instance.list_namespaced_service(namespace)
                dict = api_response.to_dict()
                for i in range(len(dict['items'])):
                    text1 +=dict['items'][i]['metadata']['name'] 
                    text1 += '\n'
            elif listt[1]=='deployments':
                api_response = v.list_namespaced_deployment(namespace)
                dict = api_response.to_dict()
                for i in range(len(dict['items'])):
                    text1 += dict['items'][i]['metadata']['name'] 
                    text1 += '\n'
            elif listt[1]=='namespaces':
                api_response = api_instance.list_namespace()
                dict = api_response.to_dict()
                for i in range(len(dict['items'])):
                    text1 += dict['items'][i]['metadata']['name'] 
                    text1 += '\n'
            elif listt[1]=='daemon_set':
                api_response = v.list_namespaced_daemon_set(namespace)
                dict = api_response.to_dict()
                for i in range(len(dict['items'])):
                    text1 += dict['items'][i]['metadata']['name'] 
                    text1 += '\n'
        elif listt[0]=='logs':
            name = 'zoo-0' # str | name of the Pod
            container ='zookeeper' 
            text1 = api_instance.read_namespaced_pod_log(name, namespace,container=container)
            text1 = '```\n' + text1 + '\n```'

        elif listt[0]=='delete':
            if listt[1] == 'deployment':
                name = 'nginx-deployment' # str | name of the Deployment
                body = client.V1DeleteOptions() # V1DeleteOptions | 
                try: 
                    api_response = c.delete_namespaced_deployment(name, namespace, body)
                    text1 = api_response
                except ApiException as e:
                    print("Exception when calling AppsV1Api->delete_namespaced_deployment: %s\n" % e)

            elif listt[1] == 'stateful-set':
                name = 'web' # str | name of the Deployment
                body = client.V1DeleteOptions() # V1DeleteOptions | 
                try: 
                    api_response = c.delete_namespaced_stateful_set(name, namespace, body)
                    text1 = api_response
                except ApiException as e:
                    print("Exception when calling AppsV1Api->delete_namespaced_stateful_set: %s\n" %e)

        elif listt[0]=='create':
            file = '/home/niki/graphbot/'
            if listt[1]=='deployment':
                with open(os.path.join(os.path.dirname(file), "deployment.yaml")) as f:
                    dep = yaml.load(f)
                    resp = c.create_namespaced_deployment(body=dep, namespace=namespace)
                    t = str(resp.status)
                    text1 = f'Deployment created. status={t}'
            elif listt[1] == 'stateful_set':
                with open(os.path.join(os.path.dirname(file), "sts.yaml")) as f:
                    dep = yaml.load(f)
                    try: 
                        api_response = c.create_namespaced_stateful_set(namespace=namespace, body=dep)
                        text1 = 'Stateful set created' + str(api_response.status)
                    except ApiException as e:
                        print("Exception when calling AppsV1Api->create_namespaced_stateful_set: %s\n" %e)
        
        self.slack_client.api_call(
        'chat.postMessage',
        channel=channel,
        text=text1,
        )

    except ApiException as e:
        print("Exception when calling CoreV1Api : %s\n" % e)
