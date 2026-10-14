pipeline {
    agent any

    stages {
        stage('Install Dependencies') {
            steps {
                sh '''
                    python3 -m venv .venv
                    .venv/bin/python -m pip install --upgrade pip
                    .venv/bin/python -m pip install -r requirements.txt
                '''
            }
        }

        stage('Run API Tests') {
            steps {
                sh '.venv/bin/python -m pytest -v --html=report.html --self-contained-html'
            }
        }
    }

    post {
        always {
            publishHTML(target: [
                reportDir: '.',
                reportFiles: 'report.html',
                reportName: 'API Automation Test Report',
                keepAll: true,
                alwaysLinkToLastBuild: true,
                allowMissing: true
            ])
        }
    }
}
