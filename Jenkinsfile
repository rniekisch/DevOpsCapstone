node {
    def newImage

    stage('Build docker image') {
        newImage = docker.build("rniekisch/capstone_app")
    }

    stage('Push docker image') {
        withDockerRegistry([url: "", credentialsId: "dockerhub"]) {
            newImage.push("${env.BUILD_NUMBER}")
            newImage.push("latest")
        }
    }
}
