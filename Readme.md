
= Solution

The deployed application is a simple Python Flask app, showing request data like browser, referer, event and ip address.

As update strategy i implemented a rolling update.

The url for the app is: http://a4916a6bd3db043098bb2ddaeb334ab8-317157340.us-west-2.elb.amazonaws.com


= Infrastructure

== Kubernetes cluster

The kubernetes cluster is build with help of eksctl. The script infrastructure/createCluster.sh will run eksctl to generate a simple two node cluster. eksctl is based on cloudformation. For reference i saved the generated cloudformation json in 'infrastructure/cluster.json'.

Note that the deployment of the app is done in the jenkinsfile, using the config yaml template 'kubernetes/deployment.yaml.tmp'.

== Jenkins node

I used a "devops" vagrant box on my windows host to run Jenkins, docker and kubectl.


= Jenkins Pipeline Stages

== Checkout Git repository

We must make sure we are working on the complete (not sparse checkout) repository. Therefore we do an explicit 'checkout scm' step. We also retrieve the current commit id in this stage. It is later used to uniquely tag the pushed image.

== Lint Dockerfile

hadolint is used to lint the Dockerfile. The following screenshot shows a failing hadolint stage:

<img>

== Build docker image

This stage builds the docker image. Incorporating any changes of the git repository. The default tag (latest) is used here. The image gets tagged later, before it is pushed to dockerhub (see Stage 'Push docker image').

== Security Scan

The security scan of the docker image is done with trivy, the successor of the aqua microscanner (https://aquasecurity.github.io/trivy).

My first run resultet in more than 200 critical issues found in the base image python:3.7.3-stretch. Switching to python:3.9.6-slim-buster reduced them to 2 criticals. Both related to the used glibc version.

I do not want to fix those bugs right now. Bu i want to monitor them. Therefore the Security Scn stage does not break the pipeline and just reports the found issues.

= Lint app

pylint is run inside the created image. If there is an error the pipline will fail. See the next screenshot for an erroneous run:

<img>

= Push docker image

The created image is pushed to dockerhub. It is tagged as 'latest' and also with the commit id retrieved in the 'Checkout Git repository' stage.


== Deploy to Kubernetes cluster

Now a rolling update of the Kubernetes pods is triggered. This is done by updating the image of the deployment. The image is identified by the commit_id tag. Using the 'latest' tag could lead to undefined rollouts if the docker hub 'latest' image is updated during the rollout. Using an unique id, like the commit hash, eleminates this issue.

The update itself is done with help of the 'kubernetes/deployment.yaml.tmp' template. It contains a placeholder for the used docker image ("<IMAGE>"). This placeholder is replaced with the short git commit id before running 'kubectl apply'.

The effect of the rolling update can be seen here. The "old" pods get replaced by new pods running the new image:

<img>


= Result

Successful Pipeline:

<img>

Website:

<img>
