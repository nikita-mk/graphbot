# Slack bot - Documentation

## Zookeeper & Kafka
Documented already

## Configure Prometheus to monitor kafka
	
**Configure values.yaml**
```
storageClass : "gp2"

alertmanagerFiles:
    alertmanager.yml:
    global: 
        slack_api_url: 'https://hooks.slack.com/services/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'

    receivers:
    - name: 'slack-notifications'
        slack_configs:
        - channel: '#general'
        send_resolved: true
        text: 'You need to look into this!!!'

    route:
        group_wait: 10s
        group_interval: 1m
        receiver: 'slack-notifications'
        repeat_interval: 1m
        group_by: [alertname, datacenter, app]

serverFiles:
  alerts: 
    groups:
      - name: Instances
        rules:
          - alert: InstanceDown
            expr: up == 0
            for: 1m
            labels:
              severity: page
            annotations:
              description: '{{ $labels.instance }} of job {{ $labels.job }} has been down for more than 1 minutes.'
              summary: 'Instance {{ $labels.instance }} down'
  rules: {}	



  prometheus.yml:
    rule_files:
      - /etc/config/rules
      - /etc/config/alerts

    scrape_configs:
      - job_name: prometheus
        static_configs:
          - targets:
            - localhost:9090
 ```
**Install Helm**

`helm init --tiller-namespace=kafka-confluent-5`

**Deploy Prometheus**

`helm install stable/prometheus --name prometheus --namespace kafka-confluent-5 --values d.yaml   //deploy`

*Cleanup*

`helm del --purge prometheus ` 					

## Monitoring Kafka which uses Zookeeper
Query for metrics and graph representation 
	
`kubectl -n <namespace> port-forward <prometheus_pod_name> 9090`

[prometheus_home_page](http://localhost:9090)

## Configure Grafana to scrape data from Prometheus
**Configure values.yaml**
```
datasources: 
    datasources.yaml:
    apiVersion: 1
    datasources:
    - name: Prometheus
        type: prometheus
        url: http://prometheus-server.kafka-confluent-5.svc.cluster.local
        access: proxy
        isDefault: true

dashboards: 
    default:
    some-dashboard:
        json: |
        $RAW_JSON
    prometheus-stats:
        gnetId: 2
        revision: 2
        datasource: Prometheus
    local-dashboard:
        url: https://example.com/repository/test.json

```
**Deploy Grafana**

`helm install -f values.yaml stable/grafana --name grafana --namespace kafka-confluent-5`

*Cleanup*

`helm del --purge grafana`


## Use Puppeteer to launch headless Chrome & take screenshots of the provided urls
Install nodejs, npm

Puppeteer Docker image : FAIL

**Code for puppeteer screenshot**

```
const puppeteer = require('puppeteer');
(async() => {
    const browser = await puppeteer.launch();
    const page = await browser.newPage();
    await page.goto('http://localhost:3000');
    await page.type('[name="username"]', process.env.UNAME)
    await page.type('[name="password"]', process.env.PWD)
    await page.click('[type="submit"]')
    await page.waitForNavigation()
    await page.screenshot({path: 'myscreenshot1.png',fullPage:true});
    const cookies = await page.cookies();
    const page1 = await browser.newPage();
    await page1.setCookie(...cookies);	
    await page1.goto('http://localhost:3000/dashboards')
    await page1.click('[class="search-item__body-title"]')
    await page1.waitForNavigation()
    await page1.screenshot({ path: 'myscreenshot2.png', fullPage: true })
    await browser.close();
})();
```

## Create Slackbot
* Create new workspace
* Create a new slack app 
  
    [slack_app_url](https://api.slack.com/apps?new_app=1)

    ![](/home/niki/Pictures/Screenshot from 2018-11-23 19-19-34.png)

* Save the credentials
  
    ![](/home/niki/Pictures/Screenshot from 2018-11-23 19-20-55.png)

* Add Incoming Webhooks
* Incoming webhooks are a simple way to post messages from external sources into Slack. They make use of normal HTTP requests with a JSON payload, which includes the message and a few other optional details. You can include message attachments to display richly-formatted messages.
    
    ![](/home/niki/Pictures/Screenshot from 2018-11-23 19-23-17.png)

    `Webhook URL : <>`
* Add description
* Install app into the workspace


	
##Slackbot code :
* We use Python
* Slackclient & k8s-python-client library
* We use the *RTM API*
The Real Time Messaging API is a WebSocket-based API that allows you to receive events from Slack in real time and send messages as users. It's sometimes referred to as simply the "RTM API".
[](https://api.slack.com/rtm)

	* connect to the channel
	* start listening to the messages
		```
        self.slack_client = SlackClient(self.token)
		```
		***connect***
		```
		self.slack_client.rtm_connect()
		``` 
		***listen for events***
		```
		events = self.slack_client.rtm_read() 
		```
		***send messages***
		```
		self.slack_client.api_call( 		
            'chat.postMessage',
            channel=channel,
            text=text,
            )
        ```
        ***upload files***
        ```
        ret = self.slack_client.api_call(		
                        "files.upload",
                        filename=filename,
                        channels=channel,
                        title=filename,
                        file=io.BytesIO(in_file.read()))
        ```
	* When message comes compare it with the options offered by the bot

	* Response -
	  *  help : display the commands
      * cpu : shows the current cpu usage percentage
	  * list : lists the graph options
      * graph : uploads a screenshot of the grafana dashboard
	  * alerts : send alerts to slack channel when something goes down

## Port-forwarding code : 

Use kubectl port-forward to forward data from Prometheus and Grafana pods to the specified ports

`kubectl -n <namespace> port-forward <pod_name> <port_name>`

## Dynamically  querying Prometheus 

* prometheus cpu usage time <>  = 100 - (avg(rate(node_cpu_seconds_total{mode="idle"}[--time--])) * 100)   done 	
* cpu usage cluster time<> = 100 - (avg(rate(node_cpu_seconds_total{mode="idle"}[--time--])) * 100)
* cpu usage namespace <name> time<> = avg(rate(container_cpu_usage_seconds_total{namespace="---"}[---]))*100
* cpu usage container <name> time<> = avg(rate(container_cpu_usage_seconds_total{pod_name="===="}[===]))*100



* memory usage ((node_memory_MemTotal_bytes -node_memory_MemFree_bytes)/node_memory_MemTotal_bytes)*100
* total memory = node_memory_MemTotal_bytes
* memory in-use = node_memory_Active_bytes
* memory free = node_memory_MemFree_byte
* container memory sum = sum(container_memory_working_set_bytes)
* container <name> memory sum = container_memory_working_set_bytes{pod_name="===="}

* io time = sum(node_disk_io_time_seconds_total)
* io read bytes = sum(node_disk_read_bytes_total)
* io written bytes = sum(node_disk_written_bytes_total)

* http requests total = sum(http_requests_total)

**Use Dictionary**
```
query = {
'cpu' : {
    'node' : 'node_cpu_seconds_total',
    'Ter' : 'container_cpu_usage_seconds_total'
},
'memory' : {
    'total' : 'node_memory_MemTotal_bytes',
    'free'  : 'node_memory_MemFree_bytes',
    'active' : 'node_memory_Active_bytes',
    'container' : 'container_memory_working_set_bytes'
},

'io' : {
'total' : 'node_disk_io_time_seconds_total',
'read_bytes' : 'node_disk_read_bytes_total',
'write_bytes' : 'node_disk_written_bytes_total'
},

'http' : {
'total' : 'http_requests_total',
'count' : 'http_request_duration_seconds_count'
}, 
}
```
**Prometheus queries**

## Execution of kubectl commands from Slack
Use Python kubernetes-client - Python client for the Kubernetes API.

**Installation**

From Source :
```
git clone --recursive https://github.com/kubernetes-client/python.git
cd python
python setup.py install
```

From PyPi directly :

```
pip install kubernetes
```

Configuration:
```
path = <kubeconfig path>
config.load_kube_config(path)
```
**kubectl create \<resource name>**

Deployment
```
with open(os.path.join(os.path.dirname(file), "deployment.yaml")) as f:
    dep = yaml.load(f)
    resp = c.create_namespaced_deployment(body=dep, namespace=namespace)
    t = str(resp.status)
    text1 = f'Deployment created. status={t}'
```
StatefulSets
```
with open(os.path.join(os.path.dirname(file), "sts.yaml")) as f:
    dep = yaml.load(f)
    try: 
        api_response = c.create_namespaced_stateful_set(namespace=namespace, body=dep)
        text1 = 'Stateful set created' + str(api_response.status)
    except ApiException as e:
        print("Exception when calling AppsV1Api->create_namespaced_stateful_set: %s\n" %e)
```
**kubectl get \<resource name>**

Namespaces
```
api_response = api_instance.list_namespace()
dict = api_response.to_dict()
for i in range(len(dict['items'])):
    text1 += dict['items'][i]['metadata']['name'] 
    text1 += '\n'
```
Pods
```
api_response= api_instance.list_namespaced_pod(namespace)
dict = api_response.to_dict()
for i in range(len(dict['items'])):
    text1 += dict['items'][i]['status']['phase'] + '\t\t' + dict['items'][i]['metadata']['name']
    text1 += '\n'
```
Services
```
api_response= api_instance.list_namespaced_service(namespace)
dict = api_response.to_dict()
for i in range(len(dict['items'])):
    text1 +=dict['items'][i]['metadata']['name'] 
    text1 += '\n'
```                    
Deployments
```
api_response = v.list_namespaced_deployment(namespace)
dict = api_response.to_dict()
for i in range(len(dict['items'])):
    text1 += dict['items'][i]['metadata']['name'] 
    text1 += '\n'
```                    
DaemonSet
```
api_response = v.list_namespaced_daemon_set(namespace)
dict = api_response.to_dict()
for i in range(len(dict['items'])):
    text1 += dict['items'][i]['metadata']['name'] 
    text1 += '\n'
```                    

**kubectl delete \<resource name>**

Deployment
```
name = 'nginx-deployment' # str | name of the Deployment
body = client.V1DeleteOptions() # V1DeleteOptions | 
try: 
    api_response = c.delete_namespaced_deployment(name, namespace, body)
    text1 = api_response
except ApiException as e:
    print("Exception when calling AppsV1Api->delete_namespaced_deployment: %s\n" % e)
```                    
Stateful-sets
```
name = 'web' # str | name of the Deployment
body = client.V1DeleteOptions() # V1DeleteOptions | 
try: 
    api_response = c.delete_namespaced_stateful_set(name, namespace, body)
    text1 = api_response
except ApiException as e:
    print("Exception when calling AppsV1Api->delete_namespaced_stateful_set: %s\n" %e)
```
**kubectl logs \<resource name>**

Pod
```
name = 'zoo-0' # str | name of the Pod
container ='zookeeper' 
text1 = api_instance.read_namespaced_pod_log(name, namespace,container=container)
text1 = '```\n' + text1 + '\n```'
```
# Next steps :


* Use Python Library to send http-requests instead of using curl via the os.system :(if 2nd is done, then no need to do)
* Use Token to directly send requests to the Prometheus server - Not working
* Move to a channel instead of direct messaging so that people can collaborate - change the configuration
* Make the interaction more user-friendly : In progress
* Generate graphs using API instead of using Puppeteer : Done using Matplotlib (find a way to upload it)
* Send reports at a particular timing	: 
* Add more alerts	:
* Port code to Go	:
* Even if command order is wrong, still try to predict it and respond to it : Use similarity metric
