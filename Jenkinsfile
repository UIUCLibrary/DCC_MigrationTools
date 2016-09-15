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
        // sh '$TOX docs'
        sh '$PYTHON3 setup.py build_sphinx'
        dir('docs/build/'){
            stash includes: '**', name: 'sphinx_docs'
        }
    }
}
node {
    stage("Packaging Documentation"){
        unstash 'sphinx_docs'
        sh 'tar -czvf DCC_MigrationToolsDocs.tar.gz html'
        archiveArtifacts artifacts: 'DCC_MigrationToolsDocs.tar.gz'
        //dir('.tox/docs/tmp/'){
        //    sh 'tar -czvf DCC_MigrationToolsDocs.tar.gz html'
        //    archiveArtifacts artifacts: 'DCC_MigrationToolsDocs.tar.gz'
        //}
    }

    stage("Packaging source"){
        unstash 'pysource'
        sh '$PYTHON3 setup.py sdist'
        archiveArtifacts artifacts: 'dist/*.tar.gz'
        
    }
}