pipeline {
  agent any

  environment {
    DOCKERHUB_CREDS = 'dockerhub-cred'                 // Jenkins credentials ID for Docker Hub
    IMAGE_NAME      = "srikandala/python-falsk-test"  // Docker image name
    HOST_PORT       = "8081"                           // Port on host
    CONTAINER_PORT  = "8000"                           // Port inside container
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
          echo "Cleaning up any existing python-static-* containers..."
          docker ps -a --filter "name=python-static-" -q | xargs -r docker rm -f

          echo "Starting new container for this build..."
          docker run -d --name python-static-${env.BUILD_NUMBER} \\
            -p ${HOST_PORT}:${CONTAINER_PORT} \\
            ${IMAGE_NAME}:${BUILD_NUMBER}

          sleep 3

          echo "Hitting http://localhost:${HOST_PORT}/"
          curl -sSf http://localhost:${HOST_PORT}/ | head -n 5 || (echo "Main page check failed" && exit 1)

          echo "Hitting http://localhost:${HOST_PORT}/health"
          curl -sSf http://localhost:${HOST_PORT}/health || (echo "Health check failed" && exit 1)
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
