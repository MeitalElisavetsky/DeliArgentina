pipeline {
    agent {
        kubernetes {
            label 'ez-joy-friends'
            idleMinutes 5
            yamlFile 'build-pod.yaml'
            defaultContainer 'ez-docker-helm-build'
        }
    }

    environment {
        APP_NAME = "deli-argentina"
        DOCKER_IMAGE = "meitalle/deli-argentina-img" // Docker Hub registry
        HELM_CHART_NAME = "meitalchart"
        GITLAB_TOKEN = credentials('meital-gitlab-cred') // Reference the GitLab token credential ID
        DOCKERHUB_TOKEN = credentials('meital-docker-cred') // Reference the Docker Hub token credential ID
        PROJECT_ID = '55457838'
        GITLAB_URL = 'https://gitlab.com'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    // Build and tag Docker image for feature branches
                    dockerImage = docker.build("${DOCKER_IMAGE}:latest", "--no-cache .")
                }
            }
        }

        stage('Tests') {
            steps {
                script {
                    sh 'docker-compose -f docker-compose.yaml up -d'
                    sh 'docker-compose -f docker-compose.yaml run tests'
                    sh 'docker-compose -f docker-compose.yaml down'
                }
            }
        }

        stage ('Push Docker image') {
            when {
                branch 'main'
            }
            steps {
                script {
                    docker.withRegistry('https://registry.hub.docker.com', 'meital-dockerhub-cred' ) {
                        dockerImage.push("latest")
                    }
                }
            }
        }


        stages {
            stage('Build Helm Chart') {
                steps {
                    sh 'helm lint $HELM_CHART_NAME'
                    sh 'helm package $HELM_CHART_NAME'
                }
            }
        }

        stage('Push Helm Package to DockerHub') {
            when {
                branch 'main'
            }
            steps {
                script {
                    withCredentials([string(credentialsId: 'meital-docker-cred', variable: 'DOCKERHUB_TOKEN')]) {
                        // Push the Helm chart to DockerHub
                        sh "helm push $HELM_CHART_NAME*.tgz oci://index.docker.io/meitalle"
                    }
                }
            }
        }



        stage('Create Merge Request') {
            when {
                not {
                    branch 'main'
                }
            }
            steps {
                script {
                    withCredentials([string(credentialsId: 'meital-gitlab-api', variable: 'GITLAB_API_TOKEN')]) {
                        def response = sh(script: """
                        curl -s -o response.json -w "%{http_code}" --header "PRIVATE-TOKEN: ${GITLAB_API_TOKEN}" -X POST "${GITLAB_URL}/api/v4/projects/${PROJECT_ID}/merge_requests" \
                        --form "source_branch=${env.BRANCH_NAME}" \
                        --form "target_branch=main" \
                        --form "title=MR from ${env.BRANCH_NAME} into main" \
                        --form "remove_source_branch=false"
                        """, returnStdout: true).trim()
                        if (response.startsWith("20")) {
                            echo "Merge request created successfully."
                        } else {
                            echo "Failed to create merge request. Response Code: ${response}"
                            def jsonResponse = readJSON file: 'response.json'
                            echo "Error message: ${jsonResponse.message}"
                            error "Merge request creation failed."
                        }
                    }
                }
            }
        }
    }

    post {
        always {
            cleanWs()
        }
    }
}

