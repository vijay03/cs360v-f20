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
    * **ls -al /proc/<pid>/ns**
    * **lrwxrwxrwx 1 root root 0 Apr 24 17:29 ipc -> ipc:[4026531839]**
    * **lrwxrwxrwx 1 root root 0 Apr 24 17:29 mnt -> mnt:[4026531840]**
    * **lrwxrwxrwx 1 root root 0 Apr 24 17:29 net -> net:[4026531956]**
    * **lrwxrwxrwx 1 root root 0 Apr 24 17:29 pid -> pid:[4026531836]**
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

## Root Capabilities
* More fine-grained access control than just root or non-root. 
* A process could be non-root, but given root-like privileges for a
specific task (example: using a network port)
* Alternatively, a process could be root, and be denied access because
of missing capabilities
* For example, root could be denied permission to mount new devices
* This is used to make the “container root” user significantly less
powerful than the host root

## UnionFS
* Copy-on-write file system that is the union of existing file systems
* UnionFS allows several containers to share common data (if we are
running 5 containers based on the same image, we don’t have to keep
five copies)
* On write to the UnionFS, the overwritten data is saved to a new path,
specific to that container
* Thus, writes of one container do not affect reads of another container

## Docker
* Built on top of kernel namespaces, cgroups, unionFS, and capabilities
* Each container gets its own set of namespaces and cgroups
* Namespaces isolate containers from each other: one container can’t
even see the list of processes in another container
* Cgroups allow the admin to isolate the resources used by each
container and its children
* Running the docker daemon requires root privileges
* As of Docker 1.3.2, images are now extracted in a chrooted subprocess
on Linux/Unix platforms, being the first-step in a wider effort toward
privilege separation
* Docker provides a whitelist of capabilities to root users inside a
container



### Reading
* [http://www.haifux.org/lectures/299/netLec7.pdf](http://www.haifux.org/lectures/299/netLec7.pdf)
* [https://lwn.net/Articles/531114/](https://lwn.net/Articles/531114/)


