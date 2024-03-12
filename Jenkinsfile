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
        DOCKER_REGISTRY = "meitalle/deli-argentina-img" // Docker Hub registry
        HELM_CHART_PATH = "charts/deli-argentina"
        DEVELOPER_EMAIL = "meital.2012@hotmail.com"
        GITLAB_TOKEN = credentials('meital-gitlab-cred') // Reference the GitLab token credential ID
        DOCKERHUB_TOKEN = credentials('meital-docker-cred') // Reference the Docker Hub token credential ID
        PROJECT_MANAGERS_EMAIL = "project-managers@example.com"
    }

    triggers {
        gitlab(triggerOnPush: true, triggerOnMergeRequest: true, branchFilterType: 'RegexFilter', branchFilter: '^feature/.*$')
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
                    docker.build("${DOCKER_REGISTRY}/${APP_NAME}:${BRANCH_NAME}")
                }
            }
        }

        stage('Tests') {
            steps {
                script {
                    sh 'docker-compose -f docker-compose.yaml up -d'
                    sh 'docker-compose -f docker-compose.yaml run test pytest'
                    sh 'docker-compose -f docker-compose.yaml down'
                    }
                }
            }
        }

        stage('Build Helm Package') {
            steps {
                script {
                    // Package Helm chart for feature branches
                    sh "helm package --version ${BRANCH_NAME} ${HELM_CHART_PATH} -d ${WORKSPACE}/artifacts"
                }
            }
        }


        stage('Create Merge Request') {
            steps {
                script {
                    // Use GitLab API to create a merge request
                    def apiUrl = "${GITLAB_API_URL}/projects/your-project-id/merge_requests"
                    def response = sh(script: """
                        curl --request POST \
                             --header "PRIVATE-TOKEN: ${GITLAB_TOKEN}" \
                             --header "Content-Type: application/json" \
                             --data '{"source_branch": "${BRANCH_NAME}", "target_branch": "main", "title": "Merge Request for ${BRANCH_NAME}"}' \
                             ${apiUrl}
                    """, returnStatus: true, returnStdout: true)

                    if (response != 201) {
                        error "Failed to create merge request. HTTP Status: ${response}"
                    } else {
                        echo "Merge request created successfully."
                    }
                }
            }
        }
    }

    post {
        failure {
            script {
                // Email notification for failed builds
                emailext body: 'Failed build: ${BUILD_URL}', 
                          subject: "Failed Build - ${JOB_NAME} #${BUILD_NUMBER}", 
                          to: "${PROJECT_MANAGERS_EMAIL} ${DEVELOPER_EMAIL}"
            }
        }

        success {
            script {
                echo "Build succeeded. No email notification needed."
            }
        }
    }
}
