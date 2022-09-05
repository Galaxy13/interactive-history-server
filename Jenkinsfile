pipeline {
  agent any
  stages {
    stage('Log Tool Versions') {
      steps {
        sh '''conda --version
docker --version
git --version'''
      }
    }

  }
}