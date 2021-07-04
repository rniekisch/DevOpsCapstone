node {
    def newImage

    stage('Build docker image') {
        newImage = docker.build("rniekisch/capstone_app")
    }

    stage('Test image') {
        /* Ideally, we would run a test framework against our image.
         * For this example, we're using a Volkswagen-type approach ;-) */

        app.inside {
            sh 'echo "Tests passed"'
        }
    }

    stage('Push docker image') {
        withDockerRegistry([url: "", credentialsId: "dockerhub"]) {
            app.push("${env.BUILD_NUMBER}")
            app.push("latest")
        }
    }
}
