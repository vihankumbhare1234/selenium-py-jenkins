pipeline {
  agent any
  environment {
    PIP_CACHE = "${env.WORKSPACE}\\.pip-cache"
    BROWSER   = "chrome" // or "firefox"
  }
  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }
    stage('Setup Python venv') {
      steps {
        powershell '''
          py -3 -m venv .venv
          . .\\.venv\\Scripts\\Activate.ps1
          python -m pip install --upgrade pip
          pip config set global.cache-dir "$env:PIP_CACHE" | Out-Null
          pip install -r requirements.txt
        '''
      }
    }
    stage('Run Tests (headless)') {
      steps {
        powershell '''
          . .\\.venv\\Scripts\\Activate.ps1
          if (-not (Test-Path reports)) { New-Item -ItemType Directory -Path reports | Out-Null }
          pytest --browser="$env:BROWSER" `
                 --junitxml=reports\\junit.xml `
                 --html=reports\\report.html --self-contained-html
        '''
      }
    }
  }
  post {
    always {
      junit testResults: 'reports/junit.xml', allowEmptyResults: true
      // Remove publishHTML below if you don't have HTML Publisher plugin
      publishHTML (target: [
        reportDir: 'reports',
        reportFiles: 'report.html',
        reportName: 'PyTest HTML Report',
        keepAll: true,
        alwaysLinkToLastBuild: true
      ])
      archiveArtifacts artifacts: 'reports/**', fingerprint: true, onlyIfSuccessful: false
    }
  }
}
