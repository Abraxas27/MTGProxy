pipeline {
    agent none
    stages {
        stage('Test') {
            agent {
                dockerfile true
            }
            steps {
                sh 'python -m pytest --verbose --junit-xml test-reports/results.xml tests/test_MTGProxy.py'
            }
            post {
                always {
                    junit 'test-reports/results.xml'
                }
            }
        }
    }
}
