* Kubeless
  * Functions are represented as Custom Resource Definitions (CRD)
  * Serverless function deployed using ConfigMaps
  * Controller running as a service, checks for changes to
    ThirdPartyResource
  * Kafka/Zookeeper running to handle events
  * Init container used to handle dependencies (such as runtime for function)
  * kubeless deploys the controller, Kafka to initialize
  * How are functions triggered?
    * Through HTTP requests
      * The container running the function has a REST wrapper
    * Through events
      * Topics created on Kafka broker
      * An event goes to a specific topic
      * Function is triggered when event is published

* Reading
  * [Kubeless
    Architecture](https://github.com/kubeless/kubeless/blob/master/docs/architecture.md)
  * [Kubernetes Custom Resources](https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/)
  * See video middle part: [Serverless on Kubernetes with Kubeless [A]
    ](https://www.youtube.com/watch?v=1QZ6x_8h8qY)
