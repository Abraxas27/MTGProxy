#!groovy​
pipeline {
    agent none
    stages {
        stage('Test') {
            agent {
                dockerfile true
            }
            steps {
                withEnv(["PYTHONPATH=$WORKSPACE/MTGProxy"]) {
                    sh 'env'
                    sh 'python -m pytest --verbose --junit-xml test-reports/results.xml tests/test_MTGProxy.py'
                    sh 'pyflakes MTGProxy > test-reports/pyflakes.log'
                }
            }
            post {
                always {
                    junit 'test-reports/results.xml'
                }
            }
        }
    }
}
