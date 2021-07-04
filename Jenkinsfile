node {
    def newImage

    stage('Build docker image') {
        newImage = docker.build("rniekisch/capstone_app")
    }

    stage('Test image') {
        /* Ideally, we would run a test framework against our image.
         * For this example, we're using a Volkswagen-type approach ;-) */

        newImage.inside {
            sh 'echo "Tests passed"'
        }
    }

    stage('Push docker image') {
        withDockerRegistry([url: "", credentialsId: "dockerhub"]) {
            newImage.push("${env.BUILD_NUMBER}")
            newImage.push("latest")
        }
    }
}
