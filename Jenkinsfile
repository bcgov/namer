node {
  stage('build') {
         echo "Building..."
         openshiftBuild bldCfg: 'corporate-names-registry', showBuildLogs: 'true'
         openshiftTag destStream: 'corporate-names-registry', verbose: 'true', destTag: '$BUILD_ID', srcStream: 'corporate-names-registry', srcTag: 'latest'
         openshiftTag destStream: 'corporate-names-registry', verbose: 'true', destTag: 'dev', srcStream: 'corporate-names-registry', srcTag: 'latest'
  }
  stage('deploy-test') {
      input "Deploy to test?"
      #openshiftTag destStream: 'myapp', verbose: 'true', destTag: 'test', srcStream: 'myapp', srcTag: '$BUILD_ID'
  }
  stage('deploy-prod') {
      input "Deploy to prod?"
      #openshiftTag destStream: 'myapp', verbose: 'true', destTag: 'prod', srcStream: 'myapp', srcTag: '$BUILD_ID'
  }
}