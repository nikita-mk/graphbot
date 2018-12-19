import os
from slackclient import SlackClient
from kubernetes import client, config
from kubernetes.client.rest import ApiException
import yaml
import subprocess
import json

def respond(self, channel, text,listt=[], upload=False,cpu=False,k8s=False):
        # self.slack_client.api_call(
        #     'chat.postMessage',
        #     channel=channel,
        #     text=text,
        #     )
        if upload:
            for graph_name, url in self.graph_urls.items():
                self.generate_and_upload_graph(graph_name, url, channel)
        if cpu:
            self.respondCpu(channel)
        if k8s:
            self.respondk8s(channel,listt)
        # if prometheus:
        #     self.respondPrometheus(channel)