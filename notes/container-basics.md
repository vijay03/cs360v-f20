### Introducing Containers

* What is the main motivation behind containers?

    * To manage "**dependency** **hell**": when your application depends on X, which depends on A, etc. Containers offer a good way to bundle up an application. In the same way that apt makes installing a package easier in Ubuntu, containers make it easier to package and deploy an application

    * To run an application in **isolation**: what that application does should not affect other applications, it should not be able to interfere or gain new resources

        * For example, running a web server in isolation: a malicious user should not gain access to the entire server

        * Note that there are several levels of isolation: a kernel crash in one container will bring down all containers. Thus, containers do not provide the same level of isolation as virtual machines. However, containers isolate the processes inside one container from processes inside another container. This is still valuable, and is the major goal of containers. 

* Core technologies behind Docker Containers:

    * Kernel namespaces

    * Cgroups

    * Copy-on-write File system

    * We will learn about these over the next few classes

* Traditional Isolation Mechanisms

    * Each process has a owner (user uid)

    * UID passed onto objects such as files of owner

    * Fine-grained Access Control Lists (ACLs) available, but increase complexity

* Alternative: chroot

    * Provides the illusion that a given directory is the root of the file system

    * The process cannot access any files outside the current "root" 

    * However, this has loopholes: a chrooted process can manually mount a device and have access to the files on the mounted file system

    * A chrooted process with sufficient privileges can "break out" using a second chroot 

    * Thus, chroot not meant to stop processes from getting access to IO

    * Chroot process and normal processes share the same process and network stack

    * Normally, a process on startup expects to find /bin, /usr/bin, etc populated

        * This is not the case with chroot

        * Makes it hard to use as a general sandboxing mechanism

        * You need to do a "bind mount", basically show /usr/lib as /chroot/usr/lib

    * How does chroot work?

        * It changes path lookup: looking up /a is translated to chroot-home/a where chroot-home is where the chroot was started

    * How to check if a process is chrooted or not?

        * See its root directory at /proc/pid/root 

        * For chrooted processes, it will pointed to the new root

    * So what’s the problem with chroot?

        * You need all the dependencies of an application copied into the chroot jail

        * For large application, the problem in the first place was that we didn’t know these dependencies

        * Chroot isolation isn’t perfect, the process can still access the underlying IO devices

        * Chroot doesn’t change working directory into the jail. If current working directory is outside the jail, then chroot is pointless

* Alternative: FreeBSD Jail

    * FreeBSD jails virtualize access to the file system, the users, and the networking subsystem

    * Introduces the** ****jail()** system call

    * A jail is characterized by four elements:

* A directory subtree: the starting point from which a jail is entered. Once inside the jail, a process is not permitted to escape outside of this subtree.

* A hostname: which will be used by the jail.

* An IP address: which is assigned to the jail. The IP address of a jail is often an alias address for an existing network interface.

* A command: the path name of an executable to run inside the jail. The path is relative to the root directory of the jail environment.

    * When a process is placed in jail, all its descendents will also be in jail

    * A jailed process can only communicate with other processes inside the same jail

    * A jailed process cannot access any privileged resources (non-root)

    * File system access is limited similar to chroot

    * A jailed process can only use a single IP address (both for sending and receiving)

    * Restrictions apply to a jailed process even if it is running with root privileges

        * Can’t load kernel modules

        * Can’t change network config

        * Can’t create devices, mount file systems, etc

    * Implementation:

        * The jail(2) system call is implemented as a non-optional system call in FreeBSD.

        * The implementation of the system call is straightforward: a data structure is allocated and populated with the arguments provided. The data structure is attached to the current process’ struct proc, its reference count set to one and a call to the chroot(2) syscall implementation completes the task. 

        * Hooks in the code implementing process creation and destruction maintains the reference count on the data structure and free it when the last reference is lost. 

        * Any new process created by a process in a jail will inherit a reference to the jail, which effectively puts the new process in the same jail. There is no way to modify the contents of the data structure describing the jail after its creation, and no way to attach a process to an existing jail if it was not created from the inside that jail.

        * Blocks escape from chroot using another chroot

        * Enforces root directory of chroot to be current working directory

        * Process visibility and access checks take jails into account

            * Procfs and sysctl modified

        * Transparently change all IPs in bind() etc to jail’s IP

        * Change points where root succeeds but jailed root will failed: 225/260 points

    * Creating a FreeBSD jail will automatically copy in all binaries and libraries from /etc, /bin, etc

    * Processes outside the jail can see processes inside the jail

    * Processes outside can directly modify files inside the jail

    * Solaris has something similar called Solaris Zones

### Reading

* [http://www.linuxjournal.com/content/docker-lightweight-linux-containers-consistent-development-and-deployment](http://www.linuxjournal.com/content/docker-lightweight-linux-containers-consistent-development-and-deployment) (2014) - written when Docker was just starting out

* [https://linuxcontainers.org](https://linuxcontainers.org)

* [https://www.freebsd.org/doc/handbook/jails.html](https://www.freebsd.org/doc/handbook/jails.html) - Intro to FreeBSD Jail

* [http://ivanlef0u.fr/repo/madchat/sysadm/bsd/kamp.pdf](http://ivanlef0u.fr/repo/madchat/sysadm/bsd/kamp.pdf) - FreeBSD Jail Tech Notes (2000)

