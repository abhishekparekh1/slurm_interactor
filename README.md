# Slurm-interactor

Playbooks to allow draining of nodes out of the slurm cluster and getting them back into the SLURM cluster.

## How to Run

The hosts file should contain the address of the controller node

### Draining a Node

ansible-playbook -i inventory/hosts --ask-pass <path to>/roles/common/tasks/drain-node.yml

### Resuming a node

ansible-playbook -i inventory/hosts --extra-vars "compute=name of the compute to be resumed" --ask-pass <path to>roles/common/tasks/resume-compute.yml

### Starting an API server

python app.py

### Calling API for drain Node

curl http://127.0.0.1:5000/drain_node

### Calling API for resuming a node

curl http://127.0.0.1:5000/resume_node?hostname=<host to be resumed>
