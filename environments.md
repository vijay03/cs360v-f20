### User Environments and Exception Handling
In JOS the terms "environment" and "process" are interchangeable - they roughly have the same meaning. We introduce the term "environment" instead of the traditional term "process" in order to stress the point that JOS environments do not provide the same semantics as UNIX processes, even though they are roughly comparable.

The include file inc/env.h contains basic definitions for user environments in JOS. The kernel uses the Env data structure to keep track of each user environment. As you can see in kern/env.c, the kernel maintains three main global variables pertaining to environments:
```
struct Env *envs = NULL;        /* All environments */
struct Env *curenv = NULL;          /* the current env */
static struct Env_list env_free_list;   /* Free list */
```
Once JOS gets up and running, the envs pointer points to an array of Env structures representing all the environments in the system. Once it is allocated, the envs array will contain a single instance of the Env data structure for each of the NENV possible environments. The kernel uses the curenv variable to keep track of the currently executing environment at any given time. During boot up, before the first environment is run, curenv is initially set to NULL.

The Env structure is defined in inc/env.h as follows (Only important fields are mentioned):
```
struct Env {
        struct Trapframe env_tf;    // Saved registers
        struct Env *env_link;       // Next free Env
        envid_t env_id;             // Unique environment identifier
        enum EnvType env_type;      // Indicates special system environments
        unsigned env_status;        // Status of the environment
        uint32_t env_runs;          // Number of times environment has run
        pml4e_t *env_pml4e;         // Kernel virtual address of page map level-4
};
```
Here's what the Env fields are for:

* `env_tf`: This structure, defined in inc/trap.h, holds the saved register values for the environment while that environment is not running: i.e., when the kernel or a different environment is running. The kernel saves these when switching from user to kernel mode, so that the environment can later be resumed where it left off.
* `env_link`: This is a link to the next Env on the env_free_list. env_free_list points to the first free environment on the list.
* `env_id`: The kernel stores here a value that uniquely identifiers the environment currently using this Env structure (i.e., using this particular slot in the envs array).
* `env_type`: This is used to distinguish special environments. For most environments, it will be ENV_TYPE_USER. The idle environment is ENV_TYPE_IDLE and we'll introduce a few more special types for special system service environments in later labs.
* `env_status`: This variable holds one of the following values:
     1. ENV_FREE: Indicates that the Env structure is inactive, and therefore on the env_free_list.
     2. ENV_RUNNABLE: Indicates that the Env structure represents a currently active environment, and the environment is waiting to run on the processor.
     3. ENV_RUNNING: Indicates that the Env structure represents the currently running environment.
     4. ENV_NOT_RUNNABLE: Indicates that the Env structure represents a currently active environment, but it is not currently ready to run: for example, because it is waiting for an interprocess communication (IPC) from another environment.
     5. ENV_DYING: Indicates that the Env structure represents a zombie environment. A zombie environment will be freed the next time it traps to the kernel.
* `env_pml4e`: This variable holds the kernel virtual address of this environment's top-level (4th level) page directory. Like a Unix process, a JOS environment couples the concepts of "thread" and "address space". The thread is defined primarily by the saved registers (the env_tf field), and the address space is defined by the PML4,page directory pointer, page directory and page tables pointed to by env_pml4e and env_cr3. To run an environment, the kernel must set up the CPU with both the saved registers and the appropriate address space.

Note that in Unix-like systems, individual environments have their own kernel stacks. In JOS, however, only one environment can be active in the kernel at once, so JOS needs only a single kernel stack.
