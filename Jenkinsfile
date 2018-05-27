pipeline {
    agent any 

    stages {
        stage('Build') { 
            steps { 
                echo "Build..."
		sh 'sudo docker login -u ${USRDOCKERHUB} -p ${PASSDOCKERHUB}'
		sh 'sudo docker build -t kbfriend:${BUILD_NUMBER} .'
		sh 'sudo docker tag kbfriend:${BUILD_NUMBER} correiabrux/kbfriend:${BUILD_NUMBER}'
		sh 'sudo docker push correiabrux/kbfriend:${BUILD_NUMBER}'
            }
        }
        stage('Test'){
            steps {
                 echo "Test"
            }
        }
        stage('Deploy') {
            steps {
                echo "Deploy"
                sh 'gcloud container clusters get-credentials cluster-1 --zone us-central1-a --project myclusterk8s'
                sh 'kubectl set image -n kbfriend deployment/kbfriend kbfriend=correiabrux/kbfriend:${BUILD_NUMBER}'
            }
        }
    }
}
