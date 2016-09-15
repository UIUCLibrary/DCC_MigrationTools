node {
    stage('Pulling from Github'){
        checkout scm
        stash includes: '*', name: 'pysource'
    }
}

node {
    
    stage("Running Tox"){
        unstash 'pysource'
        sh '$TOX'
        junit '**/junit-*.xml'
    }
    stage("Generating Documentation"){
        sh '$TOX docs'
        archiveArtifacts artifacts: '.tox/docs/tmp/html/*.*'
    }
    stage("Packaging source"){
        sh '$PYTHON3 setup.py sdist'
        archiveArtifacts artifacts: 'dist/*.tar.gz'
        
    }
}