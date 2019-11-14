* Kubeless
  * Kubernetes ThirdPartyResource object provides CRUD
  * Serverless function deployed using ConfigMaps
  * Controller running as a service, checks for changes to
    ThirdPartyResource
  * Kafka/Zookeeper running to handle events
  * Init container used to handle dependencies (such as runtime for function)
  * kubeless deploys the controller, Kafka to initialize
  
