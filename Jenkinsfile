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
            unstash 'pysource'
            echo 'Creating virtualenv for generating docs'
            sh '$PYTHON3 -m virtualenv -p $PYTHON3 venv_doc'
            echo 'Loading virtualenv'
            sh 'source venv_doc/bin/activate'
            echo 'Installing Sphinx into virtual env'
            sh 'pip install Sphinx'

            // sh '$TOX docs'
            sh 'which python'
            sh 'python setup.py build_sphinx'
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