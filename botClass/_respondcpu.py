from slackclient import SlackClient
import subprocess
import json

def respondCpu(self, channel):
    proc = subprocess.Popen(["curl", "http://localhost:9090/api/v1/query?query=(sum(rate(container_cpu_usage_seconds_total[1000m]))/sum(machine_cpu_cores)*100)"], stdout=subprocess.PIPE)
    (out, err) = proc.communicate()
    t = str(out)
    t = t[2:-1]
    json_acceptable_string = t
    d = json.loads(json_acceptable_string)
    yy = d['data']['result'][0]['value'][1]
    yy = float(yy)
    yy = float("{0:.2f}".format(yy))

    self.slack_client.api_call(
    'chat.postMessage',
    channel=channel,
    text='Your overall CPU Usage is '+str(yy)+" %",
    )