### Kernel Namespaces
* Lightweight way to virtualize process
* Kernel namespaces split kernel resources into one instance per namespace
* This partitions processes, users, network stacks and other components into separate analogous pieces in order to provide processes a unique view
* Originated in 1992 in the Plan 9 operating system
* For example, one bash shell have a different hostname than a different bash shell if they are running in different namespaces
* There are currently 6 namespaces: 
    * mnt (mount points, filesystems) 
    * pid (processes) 
    * net (network stack) 
    * ipc (System V IPC) 
    * uts (hostname) 
    * user (UIDs)
* Namespace system calls:
    * clone() - creates a new process and a new namespace; 
        * the process is attached to the new namespace.
        *  Process creation and process termination methods, fork() and exit() methods, were patched to handle the new namespace CLONE_NEW* flags. 
    *  unshare() - does not create a new process; creates a new namespace and attaches the current process to it.
    * setns() - a new system call was added, for joining an existing namespace.
* Namespaces do not have names
*  /proc/pid/ns lists the namespace number for each namespace for each process
    * **ls -al /proc//ns **
    * **lrwxrwxrwx 1 root root 0 Apr 24 17:29 ipc -> ipc:[4026531839]**
    * **lrwxrwxrwx 1 root root 0 Apr 24 17:29 mnt -> mnt:[4026531840] **
    * **lrwxrwxrwx 1 root root 0 Apr 24 17:29 net -> net:[4026531956] **
    * **lrwxrwxrwx 1 root root 0 Apr 24 17:29 pid -> pid:[4026531836] **
    * **lrwxrwxrwx 1 root root 0 Apr 24 17:29 user -> user:[4026531837]**
    * **lrwxrwxrwx 1 root root 0 Apr 24 17:29 uts -> uts:[4026531838]**
* How are namespaces implemented?
    * By extensive modifications in the kernel to recognize namespaces at appropriate places 
    * Took over 5 years
* Example: gethostname() used to read system->nodename, now reads u->nodename where u is the namespace
* **UTS Namespace:**
* Provides namespace-specific hostname and domainname (for Network Information Service)
* **Network Namespace**:
* A network namespace is logically another copy of the network stack, with its own routes, firewall rules, and network devices.
* The network namespace is struct net. (defined in include/net/net_namespace.h) 
* Struct net includes all network stack ingredients, like: loopback device, all network tables:routing, neighboring, etc, all sockets, /procfs and /sysfs entries
* Each network namespace has its own IP addresses
* A network device belongs to exactly one network namespace
* A socket belongs to exactly one network namespace
* When you delete a namespace, all its migratable network devices are moved to the the default namespace
* Communicating between two network namespaces:
    * Veth (virtual ethernet) is used like a pipe between two namespaces
    * Sockets also work
* **Mount Namespace**:
* On creation, we copy the file system tree to new space 
* All previous mounts will be visible
* Future mounts/unmounts invisible to the rest of the system
* Weird bug: mount command updates /etc/mtab, which is visible across all namespaces
    * So mount in one namespace will be visible to another
    * However, if you cat /proc/mounts, namespace-specific mounts wont be visible externally
* Another weird bug:
    * By default, Fedora systemd will share all mount information across namespaces
    * Have to explicitly mark as private
* More sophisticated than chroot jails:
    * Mount namespaces can be connected so changes in one show up in another (called mount propogation)
* **PID Namespace:**
* Processes in different PID namespaces can have the same process ID
* When creating the first process in a new namespace, its PID is 1
* **User Namespace:**
* A process will have distinct set of UIDs, GIDs and capabilities
* **IPC Namespace:**
* Each namespace gets its own IPC objects and POSIX message queues
### CGroups
* Control Groups (cgroups) are a mechanism for applying hardware resource limits and access controls to a process or collection of processes
* The cgroup mechanism and the related subsystems provide a tree-based hierarchical, inheritable and optionally nested mechanism of resource control
* This work was started by engineers at Google (primarily Paul Menage and Rohit Seth) in 2006 under the name "process containers; in 2007, renamed to "Control Groups".
* The implementation of cgroups requires a few, simple hooks into the rest of the kernel, none in performance-critical paths:
    *  In boot phase (init/main.c) to preform various initializations.
    *  In process creation and destroy methods, fork() and exit().
    *  A new file system of type "cgroup" (VFS) – Process descriptor additions (struct task_struct) – Add procfs entries: 
    * For each process: /proc/pid/cgroup.
    * System-wide: /proc/cgroups 
* Note that the cgroups is not dependent upon namespaces; you can build cgroups without namespaces kernel support.
* There are 11 cgroup subsystems: cpuset, freezer, mem, blkio, net_cls, net_prio, devices, perf, hugetlb, cpu_cgroup, cpuacct
* In order to mount a subsystem, you should first create a folder for it under /cgroup. In order to mount a cgroup, you first mount some tmpfs root folder: 
    * mount -t tmpfs tmpfs /cgroup 
    * Mounting of the memory subsystem, for example, is done thus: 
    * mkdir /cgroup/memtest 
    * mount -t cgroup -o memory test /cgroup/memtest/
* The cpuset control group identifies a set of processors on which each process in a group may run, and it also identifies a set of memory nodes from which processes in a group can allocate memory
* Net_cl and Net_prio uniquely identify each group inside sockets and other networking events
### Reading
* [http://www.haifux.org/lectures/299/netLec7.pdf](http://www.haifux.org/lectures/299/netLec7.pdf)
* [https://lwn.net/Articles/531114/](https://lwn.net/Articles/531114/)
