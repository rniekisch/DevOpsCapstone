node {
    def newImage

    stage('Build docker image') {
        newImage = docker.build("rniekisch/capstone_app")
    }

    stage('Push docker image') {
        withDockerRegistry([url: "", credentialsId: "dockerhub"]) {
            newImage.push("BUILD_${env.BUILD_NUMBER}")
            newImage.push("latest")
        }
    }
    
    stage('Deploy to Kubernetes cluster') {
        def text = readFile file: "kubernetes/deplyoment.yaml.tmp"
        text = text.replaceAll("<IMAGE>", "rniekisch/capstone_app:BUILD_${env.BUILD_NUMBER}")
        writeFile file: "kubernetes/deplyoment.yaml", text: text            
        echo "Kubernetes Deployment:\n$text"

        withAWS(credentials: 'aws', region: 'us-west-2') {
            sh "aws eks --region us-west-2 update-kubeconfig --name capstone-cluster"
            sh "kubectl config use-context arn:aws:eks:us-west-2:443372179821:cluster/capstone-cluster"
            sh "kubectl apply -f kubernetes/deplyoment.yaml"
            sh "kubectl get nodes"
            sh "kubectl get deployments"
            sh "kubectl get pod -o wide"
            sh "kubectl get service/capstone-service"
        }
    }

}
