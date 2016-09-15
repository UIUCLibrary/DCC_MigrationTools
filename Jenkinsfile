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
    }

    stage("Packaging Documentation"){
        dir('.tox/docs/tmp/'){
            sh 'tar -czvf DCC_MigrationToolsDocs.tar.gz html'
            archiveArtifacts artifacts: 'DCC_MigrationToolsDocs.tar.gz'
        }
    }

    stage("Packaging source"){
        sh '$PYTHON3 setup.py sdist'
        archiveArtifacts artifacts: 'dist/*.tar.gz'
        
    }
}