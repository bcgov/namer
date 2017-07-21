node{
    stage('build') {
        echo "Building..."
        openshiftBuild bldCfg: 'namer', showBuildLogs: 'true', waitTime: 3600000
        openshiftTag destStream: 'namer', verbose: 'true', destTag: 'stable', srcStream: 'namer', srcTag: 'latest'
        openshiftBuild bldCfg: 'namer-dev', showBuildLogs: 'true', waitTime: 3600000
        openshiftTag destStream: 'namer', verbose: 'true', destTag: '$BUILD_ID', srcStream: 'namer-dev', srcTag: 'latest'
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
