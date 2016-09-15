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
    try {
        stage("Generating Documentation"){
            sh '$PYTHON3 -m virtualenv venv_doc'
            sh 'source venv_doc/bin/activate'
            sh 'pip install Sphinx'

            unstash 'pysource'
            // sh '$TOX docs'
            sh '$PYTHON3 setup.py build_sphinx'
            dir('docs/build'){
                stash includes: '**', name: 'sphinx_docs'
            }
        }

        stage("Packaging Documentation"){
            unstash 'sphinx_docs'
            sh 'tar -czvf DCC_MigrationToolsDocs.tar.gz html'
            archiveArtifacts artifacts: 'DCC_MigrationToolsDocs.tar.gz'
            //dir('.tox/docs/tmp/'){
            //    sh 'tar -czvf DCC_MigrationToolsDocs.tar.gz html'
            //    archiveArtifacts artifacts: 'DCC_MigrationToolsDocs.tar.gz'
            //}
            sh 'deactivate'
            sh 'rmvirtualenv venv_doc'
        }

    } catch(error) {
        echo 'Unable to generate Sphinx documentation'
    }
}

node {

    stage("Packaging source"){
        unstash 'pysource'
        sh '$PYTHON3 setup.py sdist'
        archiveArtifacts artifacts: 'dist/*.tar.gz'
        
    }
}