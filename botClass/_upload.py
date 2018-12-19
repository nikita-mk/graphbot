import os
from pathlib import Path
import subprocess
import time

def prepare_dir(self,dir_name):
        # Check for any images from a previous run and remove them
        files1 = os.listdir(dir_name)
        for item in files1:
            if item.endswith(".png"):
                os.remove(os.path.join(dir_name, item))
        return os.listdir(dir_name) 

def cmdline(self,command):
    process = subprocess.Popen(
        args=command,
        stdout=subprocess.PIPE,
        shell=True
    )
    return process.communicate()[0]
   
    
def generate_and_upload_graph(self, filename, url, channel):
#         Create the graph in the current directory



        cwd = Path().resolve()
        print(cwd)
        dir_name = os.path.dirname(os.path.abspath(cwd))
        dir_name = cwd
        files1 = self.prepare_dir(dir_name)
#         # Poll for new files
#         config.load_kube_config()
        
#         with open(os.path.join(dir_name, "zoo.yaml")) as f:
#             dep = yaml.load(f)
#             k8s_beta = client.ExtensionsV1beta1Api()
#             resp = k8s_beta.create_namespaced_deployment(
#                 body=dep, namespace="default")
#             print("Deployment created. status='%s'" % str(resp.status))




#         print (cmdline("cat /etc/services"))
#         print (cmdline('ls'))
#         os.system("VERSION=v8.11.4")
#         os.system("DISTRO=linux-x64")
#         os.system("sudo mkdir /usr/local/lib/nodejs")
#         os.system("sudo tar -xJvf node-$VERSION-$DISTRO.tar.xz -C /usr/local/lib/nodejs")
#         os.system("sudo mv /usr/local/lib/nodejs/node-$VERSION-$DISTRO /usr/local/lib/nodejs/node-$VERSION")
#         os.system("export NODEJS_HOME=/usr/local/lib/nodejs/node-$VERSION/bin")
#         os.system("export PATH=$NODEJS_HOME:$PATH")
#         os.system("npm install puppeteer")
        os.environ['KUBECONFIG'] = <kubeconfig path>
        os.system("node -v")
        os.system("UNAME=<username> PWD=<password> node ss2.js")
        while True:
            time.sleep(2)
            files2 = os.listdir(dir_name)
            new = [f for f in files2 if all([f not in files1, f.endswith(".png")])]
            for f in new:
                with open(f, 'rb') as in_file:
                    ret = self.slack_client.api_call(
                        "files.upload",
                        filename=filename,
                        channels=channel,
                        title=filename,
                        file=io.BytesIO(in_file.read()))
                    if 'ok' not in ret or not ret['ok']:
                        print('File upload failed %s', ret['error'])
                os.remove(f)
            break
