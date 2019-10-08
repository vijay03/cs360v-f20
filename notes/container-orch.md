### Swarm
* Swarm orchestrates a cluster of Docker instances
* A swarm consists of multiple Docker hosts which run in swarm mode and act as managers (to manage membership and delegation) and workers (which run [swarm services](https://docs.docker.com/engine/swarm/key-concepts/#services-and-tasks)).
* A given Docker host can be a manager, a worker, or perform both roles
* When you create a service, you define its optimal state (number of replicas, network and storage resources available to it, ports the service exposes to the outside world, and more). 
* Docker works to maintain that desired state. For instance, if a worker node becomes unavailable, Docker schedules that node’s tasks on other nodes
* Main advantage of Swarm:
    * Online updates to network config and volume config
    * Swarm will start new nodes with new config
    * Automatically stop old nodes using old config
* Node: docker instance participating in swarm
* To deploy your application to a swarm, you submit a service definition to a manager node. 
* The manager node dispatches units of work called [tasks](https://docs.docker.com/engine/swarm/key-concepts/#services-and-tasks) to worker nodes.
* Manager nodes also perform the orchestration and cluster management functions required to maintain the desired state of the swarm.
    * Manager nodes elect a single leader to conduct orchestration tasks.
    * Worker nodes receive and execute tasks dispatched from manager nodes.
    * An agent runs on each worker node and reports on the tasks assigned to it.
* A service is the definition of the tasks to execute on the manager or worker nodes
    * In the replicated services model, the swarm manager distributes a specific number of replica tasks among the nodes based upon the scale you set in the desired state.
    * For global services, the swarm runs one task for the service on every available node in the cluster.
* A **task** carries a Docker container and the commands to run inside the container. It is the atomic scheduling unit of swarm. 
    * Manager nodes assign tasks to worker nodes according to the number of replicas set in the service scale. 
    * Once a task is assigned to a node, it cannot move to another node. It can only run on the assigned node or fail.
*  Related SOSP 13 paper: Sparrow ([http://sigops.org/sosp/sosp13/papers/p69-ousterhout.pdf](http://sigops.org/sosp/sosp13/papers/p69-ousterhout.pdf))
    * Gains performance by delaying scheduling a task until the last possible moment
    * For example, will not make a decision before the moment when job has to be dispatched to a machine

### Kubernetes
* Based on internal Google system called [Borg](https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/43438.pdf)
* Started in 2014
* Kubernetes encourages the "micro-services" approach:
    * Break your application down into small services that can be deployed at different machines
    * This has higher scalability and reliability than all code running as part of one stack on a single machine
* Kubernetes basic entities:
    * Kubernetes Master
        * collection of three processes that run on a single node in your cluster, which is designated as the master node
    * Kubelet
    * Kube Proxy
* Kubernetes Pod:
    * A group of containers meant for a single purpose
    * Co-located together, share the same (external) storage
    * A pod is all the services that would have been run on the same machine if containers were not used
    * All applications within a pod have the same IP address
    * Within a pod, applications can communicate using Inter-Process Communication (IPC) or Shared Memory (as if they were on the same machine)
    * How is a pod implemented?
        * All pod containers have the same namespace (hence same IP)
        * All pod containers share the same mounted volumes
    * Applications inside a POD have to coordinate their usage of ports (since they share the same set of ports)
    * Each time a pod is started, it gets a unique ID 
        * Therefore, the ID identifies a unique instance of the pod
    * Why not just run multiple programs in a single (Docker) container?
        * Transparency. Making the containers within the pod visible to the infrastructure enables the infrastructure to provide services to those containers, such as process management and resource monitoring. This facilitates a number of conveniences for users.
        * Decoupling software dependencies. The individual containers may be versioned, rebuilt and redeployed independently. Kubernetes may even support live updates of individual containers someday.
        * Ease of use. Users don’t need to run their own process managers, worry about signal and exit-code propagation, etc.
        * Efficiency. Because the infrastructure takes on more responsibility, containers can be lighter weight.
* Kubernetes Service
    * A Kubernetes Service is an abstraction which defines a logical set of Pods and a policy by which to access them - sometimes called a micro-service
    * For Kubernetes-native applications, Kubernetes offers a simple Endpoints API that is updated whenever the set of Pods in a Service changes. 
    * For non-native applications, Kubernetes offers a virtual-IP-based bridge to Services which redirects to the backend Pods.
	
### Kubernetes vs Swarm
* Kubernetes is more sophisticated than Swarm
* Kubernetes has auto-scaling of pods based on CPU utilization
* Swarm works only with Docker, Kubernetes can work with other container services also
* Kubernetes more complex to deploy and manage compared to Swarm
* Kubernetes is reported to have better scalability (though the proof for this is not conclusive):
    * Kubernetes reported to support 150K pods on 5000 nodes. Swarm tested upto 30K containers on 1000 nodes. 
### Reading
* [https://kubernetes.io/docs/concepts/workloads/pods/pod/](https://kubernetes.io/docs/concepts/workloads/pods/pod/)
* [https://kubernetes.io/docs/concepts/services-networking/service/](https://kubernetes.io/docs/concepts/services-networking/service/)
* [https://kubernetes.io/docs/concepts/overview/components/](https://kubernetes.io/docs/concepts/overview/components/)
* https://platform9.com/blog/kubernetes-docker-swarm-compared/
* [https://docs.docker.com/engine/swarm/key-concepts/](https://docs.docker.com/engine/swarm/key-concepts/)
* [https://docs.docker.com/engine/swarm/](https://docs.docker.com/engine/swarm/)
* [https://rominirani.com/docker-swarm-tutorial-b67470cf8872](https://rominirani.com/docker-swarm-tutorial-b67470cf8872)
