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
                    sh 'pyflakes MTGProxy > test-reports/pyflakes.log || true'
                    sh 'pycodestyle --max-line-length=80 MTGProxy > test-reports/pycodestyle.log || true'
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
