
# coding: utf-8

# In[1]:


import os
from subprocess import PIPE, Popen


def cmdline(command):
    process = Popen(
        args=command,
        stdout=PIPE,
        shell=True
    )
    return process.communicate()[0]
os.environ['KUBECONFIG'] = <path to kubeconfig>

os.system('kubectl --namespace <namespace> port-forward <pod-name> 9090 &')

print(cmdline("ls"))

