node{
    stage('build') {
        echo "Building..."
        openshiftBuild bldCfg: 'namer', showBuildLogs: 'true'
        openshiftTag destStream: 'namer', verbose: 'true', destTag: '$BUILD_ID', srcStream: 'namer', srcTag: 'latest'
        openshiftTag destStream: 'namer', verbose: 'true', destTag: 'dev', srcStream: 'namer', srcTag: 'latest'
    }

    stage('deploy-test') {
        //input "Deploy to test?"
        //openshiftTag destStream: 'namer', verbose: 'true', destTag: 'test', srcStream: 'namer', srcTag: '$BUILD_ID'
    }

    stage('deploy-prod') {
        //input "Deploy to prod?"
        //openshiftTag destStream: 'namer', verbose: 'true', destTag: 'prod', srcStream: 'namer', srcTag: '$BUILD_ID'
    }
}