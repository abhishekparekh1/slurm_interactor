from flask import Flask
from flask import request
from flask import jsonify
from flask import abort
import subprocess
from error import InvalidUsage
app = Flask(__name__)


@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

@app.route('/drain_node')
def drain_node():
    proc =  subprocess.Popen('ansible-playbook -i /home/prateek/slurm_interactor/inventory/hosts /home/prateek/slurm_interactor/roles/common/tasks/drain-node.yml', stdout=subprocess.PIPE,stderr=subprocess.STDOUT, shell=True)
    out = proc.communicate()
    out = out[0]
    for line in out.split("\n"):
        if "failed=" in line:
            failure_string = line.split("failed=")[1]
            num_of_failures = int(failure_string[0])
            if num_of_failures > 0:
                abort(500, out)
        if "item=" in line:
            node_name=line.split("=")[2].replace(")","")
    return node_name

@app.route('/resume_node')
def resume_node():
    hostname = request.args.get('hostname')
    if not hostname:
        raise InvalidUsage('Hostname is Null', status_code=500)
    query_string = 'ansible-playbook -i /home/prateek/slurm_interactor/inventory/hosts --extra-vars compute="'+hostname+'" /home/prateek/slurm_interactor/roles/common/tasks/resume-compute.yml'
    proc =  subprocess.Popen(query_string, stdout=subprocess.PIPE,stderr=subprocess.STDOUT, shell=True)
    out = proc.communicate()
    return out

if __name__ == '__main__':
    app.run(host='10.227.119.160')
