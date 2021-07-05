
## Solution

The deployed application is a simple Python Flask app, showing request data like browser, referer, event and ip address.

The implemented update strategy is a rolling update.

The url for the app is: <http://a4916a6bd3db043098bb2ddaeb334ab8-317157340.us-west-2.elb.amazonaws.com>


## Infrastructure

### Kubernetes cluster

The kubernetes cluster is build with help of eksctl. The script 'infrastructure/create_cluster.sh' will run eksctl to generate a simple two node cluster with t2.medium instances. eksctl is based on cloudformation. For reference i saved the generated cloudformation json in 'infrastructure/cluster.json'.

Note that the deployment of the app is done in the jenkinsfile stage 'Deploy to Kubernetes cluster', using the config template 'kubernetes/deployment.yaml.tmp'.

### Jenkins node

I used a "devops" vagrant box on my windows host to run Jenkins, docker and kubectl.


## Jenkins Pipeline Stages

### Checkout Git repository

Thsi stage makes sure that a complete, and not sparse, git checkout is available. For this an explicit 'checkout scm' step is executed. We also retrieve the current commit id in this stage. It is later used to uniquely tag the pushed image.

### Lint Dockerfile

hadolint is used to lint the Dockerfile. The following screenshot shows a failing hadolint stage:

![Failed hadolint stage](/screenshots/hadolint_failing.png)

### Build docker image

This stage builds the docker image. Incorporating any changes of the git repository. The default tag (latest) is used here. The image gets tagged later, before it is pushed to dockerhub (see Stage 'Push docker image').

### Security Scan

The security scan of the docker image is done with trivy, the successor of the aqua microscanner (https://aquasecurity.github.io/trivy).

My first run resulted in more than 200 critical issues found in the base image python:3.7.3-stretch. Switching to python:3.9.6-slim-buster reduced the critical issue count to two. (The two issues are related to glibc).

I do not want to fix those bugs right now. But i want to monitor them. Therefore the Security Scan stage does not break the pipeline and just reports the found issues.

### Lint app

pylint is run inside the created image. If there is an error the pipline will fail. See the next screenshot for an erroneous run:

![Failed pylint stage](/screenshots/pylint_failing.png)

### Push docker image

The created image is pushed to dockerhub. It is tagged as 'latest' and also with the commit id retrieved in the 'Checkout Git repository' stage.

### Deploy to Kubernetes cluster

Now a rolling update of the Kubernetes pods is triggered. This is done by updating the image of the deployment. The image is identified by the commit_id tag. Using the 'latest' tag could lead to undefined rollouts, if the 'latest' image is concurrently updated during the rollout. Using an unique id, like the commit hash, eleminates this issue.

The update itself is done with help of the 'kubernetes/deployment.yaml.tmp' template. It contains a placeholder for the used docker image. This placeholder is replaced with the short git commit id before running 'kubectl apply'.

The effect of the rolling update can be seen here. The "old" pods get replaced by new pods running the new image:

![Rolling update](/screenshots/rolling_update.png)


## Result

Successful Pipeline:

![Successful Build](/screenshots/successful_build.png)

Website:

![Website](/screenshots/deployed_website.png)

## Additional scripts

'run_docker.sh' and 'upload_docker.sh' can be used to test and deploy the application image outise of the CI/CD process
