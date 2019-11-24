**Notes courtesy Sama Ziki**

**Paper Notes**

- Map Reduce vs. Serverless
  - Map Reduce popularity has decreased over time and so serverless will too
- What applications are good for serverless?
  - Something that has bursts of traffic
    - Auto scaling
      - If the function is triggered multiple times then it will run the function many times
  - Use it as glue in the microarchitecture servers framework
  - Simple updates to a database that can be encapsulated into a small function
  - Embarrassingly Parallel Functions
    - None of the functions interfere with any other functions (i.e. it scales perfectly)
    - Each function invocation is an independent task and never needs to communicate with other functions
  - Orchestration Functions
    - Leverages serverless functions simply to orchestrate calls to proprietary autoscaling services (such as large scale analytics)
  - Function Composition
    - Collections of functions that are composed to build applications and this need to pass along the outputs and inputs
    - Generally manipulate state in some way and are designed as event driven workflows of lambda functions stitched together via queuing systems such as SQS or object stores such as S3
    - The overheads of lambda task handling and state management explain some of the latency
    - Current FaaS solutions are attractive for simple workloads of independent tasks
- Paper criticizes serverless for not being able to handle use cases for which it was not designed
- Limitations of serverless
  - Limited lifetimes
    - After 15 minutes, function invocations are shut down by lambda infrastructure, so functions must be written assuming that state will not be recoverable across invocations
  - I/O Bottlenecks
    - Communicating with other entities across a network takes time, so computation is higher than anticipated
  - Communication Through Slow Storage
    - Lambda functions can initiate outbound network connections but they themselves are not directly network addressable in any way
  - No Specialized Hardware
    - There is no API or mechanism to access specialized hardware
  - FaaS Stymies Distributed Computing
    - Serverless functions are run on isolated VMs, separate from data, short-lived and non-addressable, so their capacity to cache state internally to service repeated requests is limited
    - This ships data to code instead of code to data
    - Memory hierarchy realities make this a bad design decision for reasons of latency, bandwidth, and cost
  - FaaS Stymies Hardware-Accelerated Software Innovation
    - No access to GPUs
    - Big data use cases leverage the use of accessing accelerators so they are hurt by this
  - FaaS Discourages Open Source Service Innovation
    - Most popular open source software cannot not run at scale in current serverless offerings
- Objections of Limitations
  - They are looking at use cases that are not what serverless was meant for or developed for
  - The experiments are not long standing so the costs that are presented are not adequate representations of the actual cost of using serverless
  - Low-Latency Prediction Serving via Batching

