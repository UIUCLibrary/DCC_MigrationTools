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
}

node {
    stage("Generating Documentation"){
        unstash 'pysource'
        sh '$TOX docs'
        tar -czvf DCC_MigrationToolsDocs.tar.gz .tox/docs/tmp/html/
        archiveArtifacts artifacts: 'DCC_MigrationToolsDocs.tar.gz'
    }
    stage("Packaging source"){
        sh '$PYTHON3 setup.py sdist'
        archiveArtifacts artifacts: 'dist/*.tar.gz'
        
    }
}