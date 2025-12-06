pipeline {
  agent any

  environment {
    DOCKERHUB_CREDS = 'dockerhub-cred'                // Jenkins credentials ID
    IMAGE_NAME      = "srikandala/python-falsk-test" // Change if you want
    HOST_PORT       = "8081"                          // Port on host
    CONTAINER_PORT  = "8000"                          // Port inside container
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Build image') {
      steps {
        echo "Building Docker image: ${env.IMAGE_NAME}:${env.BUILD_NUMBER}"
        sh """
          docker build -t ${env.IMAGE_NAME}:${env.BUILD_NUMBER} .
        """
      }
    }

    stage('Test (pytest inside container)') {
      steps {
        echo "Running pytest inside Docker image"
        sh """
          docker run --rm ${IMAGE_NAME}:${BUILD_NUMBER} pytest -q
        """
      }
    }

    stage('Push Image') {
      // Only push for non-PR builds (e.g. main branch)
      when {
        not { changeRequest() }
      }
      steps {
        echo "Logging in to Docker Hub and pushing image"
        withCredentials([usernamePassword(
          credentialsId: env.DOCKERHUB_CREDS,
          usernameVariable: 'DOCKER_USER',
          passwordVariable: 'DOCKER_PASS'
        )]) {
          sh '''
            echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
            docker push ${IMAGE_NAME}:${BUILD_NUMBER}
          '''
        }
      }
    }

    stage('Run Image Locally') {
      // Only run the container as a "deployment" step for non-PR builds
      when {
        not { changeRequest() }
      }
      steps {
        echo "Running container locally on host port ${env.HOST_PORT}"
        sh """
          # Clean old container if exists
          docker rm -f python-static-${env.BUILD_NUMBER} || true

          # Run the new container
          docker run -d --name python-static-${env.BUILD_NUMBER} \
            -p ${HOST_PORT}:${CONTAINER_PORT} \
            ${IMAGE_NAME}:${BUILD_NUMBER}

          sleep 3

          echo "Hitting http://localhost:${HOST_PORT}/"
          curl -sSf http://localhost:${HOST_PORT}/ | head -n 5

          echo "Hitting http://localhost:${HOST_PORT}/health"
          curl -sSf http://localhost:${HOST_PORT}/health
        """
      }
    }
  }

  post {
    success {
      script {
        if (env.CHANGE_ID) {
          echo "✅ PR build (CHANGE_ID=${env.CHANGE_ID}) succeeded — image built and tests passed."
        } else {
          echo "✅ Non-PR build succeeded — image pushed and container running on host port ${env.HOST_PORT}."
        }
      }
    }
    failure {
      echo "❌ Pipeline failed — check console output for details."
    }
  }
}
