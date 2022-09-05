pipeline {
  agent any
  stages {
    stage('Log Tool Versions') {
      steps {
        sh '''python --version
docker --version
git --version'''
      }
    }

  }
}