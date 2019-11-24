**11/19 Serverless:**

**Serverless Cons**

- What are the disadvantages of serverless?
  - Cost to accessing state
  - Lack of control over placement on the containers, serverless, etc.
  - Execution facing (related to the first bullet point)
  - Hard to debug (because serverless is fast running and happening on different containers)
  - Performance variance
  - Cost of startup
  - Security? (The function is only running for a limited amount of time, so security is not a big a concern because there is such a small window for attack. The problem is you are running multiple function on the same host, so there may be issues there.)

