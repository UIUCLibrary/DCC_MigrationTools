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
    stage("Generating documentation"){
        dir('docs'){
            sh 'make html'
            archiveArtifacts artifacts: 'build/html/*.*'
        }
    }
    stage("Packaging source"){
        sh '$PYTHON3 setup.py sdist'
        archiveArtifacts artifacts: 'dist/*.tar.gz'
        
    }
}