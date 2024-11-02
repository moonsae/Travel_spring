pipeline {
    agent any

    environment {
        DOCKER_HUB_CREDENTIALS = 'moonsae' // Docker Hub 자격증명 ID
        DOCKER_IMAGE = 'moonsae/tour_java'
        ORACLE_SERVER = '129.154.56.13'
        ORACLE_SSH_KEY = 'oracle-ssh-key' // Jenkins에 등록한 Oracle SSH 키 ID
    }

    stages {
        stage('Clone Repository') {
            steps {
                // GitHub에서 소스 코드 가져오기
                git branch: 'main', url: 'https://github.com/moonsae/Travel_spring.git'
            }
        }

        stage('Build WAR') {
            steps {
                // Maven을 이용해 WAR 파일 생성
                sh 'mvn clean package'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    // Docker 이미지 생성
                    dockerImage = docker.build("${DOCKER_IMAGE}:${env.BUILD_NUMBER}")
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    docker.withRegistry('https://registry.hub.docker.com', DOCKER_HUB_CREDENTIALS) {
                        // Docker Hub에 이미지 푸시
                        dockerImage.push()
                    }
                }
            }
        }

        stage('Deploy to Oracle Cloud') {
            steps {
                script {
                    sshagent([ORACLE_SSH_KEY]) {
                        sh """
                        ssh -o StrictHostKeyChecking=no ubuntu@${ORACLE_SERVER} '
                          docker pull ${DOCKER_IMAGE}:${env.BUILD_NUMBER} &&
                          docker stop my_app || true &&
                          docker rm my_app || true &&
                          docker run -d -p 8091:8080 --name my_app ${DOCKER_IMAGE}:${env.BUILD_NUMBER}
                        '
                        """
                    }
                }
            }
        }
    }
}
