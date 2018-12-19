import io
import os
import sys
import json
import time
import yaml
import subprocess
from pathlib import Path
from slackclient import SlackClient
from kubernetes import client, config

class SlackBot(object):

    def __init__(self, config=None):
        self.config = config
        self.token = config['slack_token']
        self.slack_client = SlackClient(self.token)
        self.bot_name = config['bot_name']
        self.bot_id = self.get_bot_id()
        
        self.respond_to = ['help',
                           'help-private',
                           'rules',
                           'suggest',
                           'grafana-screenshot',
                           'eod-report',
                           'schedule',
                           'list',
                           'assign<name>',
                           'prometheus']
        
        self.prometheus_subcommands = ['cpu','memory','io','filesystem','http']
        
        self.help_msg = '```\n'
        for answer in self.respond_to:
            self.help_msg += f'{answer}\n'
        self.help_msg += '```'
        
        self.graph_urls = {}
        self.graph_shortcuts = '```\n'
        for name, url in config['graph_urls'].items():
            self.graph_urls[name] = url
            self.graph_shortcuts += name + "\n"
        self.graph_shortcuts += '```'
        self.query = {
            'cpu' : {
                'node' : 'node_cpu_seconds_total',
                'container' : 'container_cpu_usage_seconds_total'
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
            'count' : 'http_request_duration_seconds_count'},
            'filesystem' : {
            'total' : 'node_filesystem_size_bytes{fstype=~"ext4|vfat"}',
            'free'  : 'node_filesystem_free_bytes{fstype=~"ext4|vfat"}',
            'active' : 'node_filesystem_size_bytes{fstype=~"ext4|vfat"} - node_filesystem_free_bytes{fstype=~"ext4|vfat"}'
            },
            'sum' : 'sum',
            'avg' : 'avg',
            'rate' : 'rate',
            'irate' : 'irate'
        }

    from ._start import start
    from ._getBotId import get_bot_id
    from ._respond import respond
    from ._respondk8s import respondk8s
    from ._respondcpu import respondCpu
    from ._onMessage import on_message
    from ._upload import cmdline, prepare_dir, generate_and_upload_graph
    

    
            
    
    
            
    
    