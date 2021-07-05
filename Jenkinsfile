node('master') {
    
    def newImage
    def commitId

    stage('Checkout Git Repository') {
        checkout scm
        commitId = sh(returnStdout: true, script: "git log -n 1 --pretty=format:'%h'").trim()
        echo ("CommitId: $commitId")
    }
	
    stage('Lint Dockerfile') {
	sh('docker run --rm -i hadolint/hadolint < Dockerfile')
    }

    stage('Build docker image') {
        newImage = docker.build("rniekisch/capstone_app")
    }

    stage('Security Scan') {
	sh('trivy image rniekisch/capstone_app')
    }
	
    stage('Lint app') {
    	docker.image('rniekisch/capstone_app:latest').inside() {
	    withEnv(['PYLINTHOME=.']) {
                sh "pylint --disable=R,C,W1203 --output-format=parseable app.py"
            }
	}
    }
	
    stage('Push docker image') {
        withDockerRegistry([url: "", credentialsId: "dockerhub"]) {
            newImage.push("${commitId}")
            newImage.push("latest")
        }
    }

    stage('Deploy to Kubernetes cluster') {
        def text = readFile(file: 'kubernetes/deployment.yaml.tmp')
        text = text.replaceAll("<IMAGE>", "rniekisch/capstone_app:${commitId}")
        writeFile file: "${WORKSPACE}/kubernetes/deployment.yaml", text: text            
        echo "Kubernetes Deployment:\n$text"

        withAWS(credentials: 'aws', region: 'us-west-2') {
            sh "aws eks --region us-west-2 update-kubeconfig --name capstone-cluster"
            sh "kubectl config use-context arn:aws:eks:us-west-2:443372179821:cluster/capstone-cluster"
            sh "kubectl apply -f kubernetes/deployment.yaml"
            sh "kubectl get nodes"
            sh "kubectl get deployments"
            sh "kubectl get pod -o wide"
            sh "kubectl get service/capstone-service"
        }
    }

}
