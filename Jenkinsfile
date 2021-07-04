pipeline {
    agent any
    stages {
        stage('Build Docker and push Image') {
            steps {
                script {
                    withDockerRegistry([url: "", credentialsId: "dockerhub"]) {
                        def newImage = docker.build("rniekisch/capstone_app")
                        newImage.push("${env.BUILD_TAG}")
                        newImage.push("latest")
                    }
                }
            }
        }
     }
}
