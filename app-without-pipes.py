from flask import Flask
from flask import request
from flask import jsonify
from playbook_handler import Runner
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
    become_user_password = '123'
    run_data={
        'user_id': 0
    }
    runner = Runner(
        hostnames='192.168.122.204',
        playbook='roles/common/tasks/drain-node.yml',
        private_key_file='/root/.ssh/id_rsa',
        run_data=run_data,
        become_pass=become_user_password
    )
    stats = runner.run()
    
    print stats


@app.route('/resume_node')
def resume_node():
    become_user_password = '123'
    run_data={
        'user_id': 0,
     }
    runner = Runner(
        hostnames='192.168.122.204',
        playbook='roles/common/tasks/resume-node.yml',
        private_key_file='/root/.ssh/id_rsa',
        run_data=run_data,
        become_pass=become_user_password
    )
    stats = runner.run()

    return stats




if __name__ == '__main__':
    app.run()
