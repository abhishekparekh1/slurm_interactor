from flask import Flask
from flask import request
import subprocess
app = Flask(__name__)


@app.route('/')
def hello():
    return "Hello World!"

@app.route('/drain_node')
def drain_node():
    proc =  subprocess.Popen('ansible-playbook -i /root/slurm_interactor/inventory/hosts /root/slurm_interactor/roles/common/tasks/drain-node.yml', stdout=subprocess.PIPE,stderr=subprocess.STDOUT, shell=True)
    out = proc.communicate()
    out = out[0]
    for line in out.split("\n"):
        if "item=" in line:
            node_name=line.split("=")[2].replace(")","")
    return node_name

@app.route('/resume_node')
def resume_node():
    hostname = request.args.get('hostname')
    query_string = 'ansible-playbook -i inventory/hosts --extra-vars compute="'+hostname+'" /root/slurm_interactor/roles/common/tasks/resume-compute.yml'
    proc =  subprocess.Popen(query_string, stdout=subprocess.PIPE,stderr=subprocess.STDOUT, shell=True)
    out = proc.communicate()
    return out

if __name__ == '__main__':
    app.run()
