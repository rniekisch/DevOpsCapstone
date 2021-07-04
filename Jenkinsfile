node('master') {
    
    def newImage

    stage('Checkout Git Repository') {
        checkout scm
    }
    /*
    stage('Build docker image') {
        newImage = docker.build("rniekisch/capstone_app")
    }

    stage('Push docker image') {
        withDockerRegistry([url: "", credentialsId: "dockerhub"]) {
            newImage.push("BUILD_${env.BUILD_NUMBER}")
            newImage.push("latest")
        }
    }
    */
    stage('Deploy to Kubernetes cluster') {
        def path = pwd
        echo "Path: $path"
        def text = readFile file: "${WORKSPACE}/Jenkinsfile"
        //def text = readFile file: "${WORKSPACE}/kubernetes/deployment.yaml.tmp"
        ////text = text.replaceAll("<IMAGE>", "rniekisch/capstone_app:BUILD_${env.BUILD_NUMBER}")
        //text = text.replaceAll("<IMAGE>", "rniekisch/capstone_app:latest")
        //writeFile file: "${WORKSPACE}/kubernetes/deployment.yaml", text: text            
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
