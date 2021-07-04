pipeline {
    agent any
    stages {
        stage('Build Docker and push Image') {
            steps {
                withDockerRegistry([url: "", credentialsId: "dockerhub"]) {
                    def newImage = docker.build("rniekisch/capstone_app:${env.BUILD_TAG}")
                    newImage.push()
                }
            }
        }
     }
}
