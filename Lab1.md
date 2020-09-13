## Project-1

In this project, you will implement a few exciting pieces of a paravirtual hypervisor. You will use the JOS operating system running on QEMU for this project. Check the [tools page](https://github.com/vijay03/cs360v-f20/blob/master/tools.md) for an overview on JOS and useful commands of QEMU. The project covers bootstrapping a guest OS, programming extended page tables, emulating privileged instructions, and using hypercalls to implement hard drive emulation over a disk image file. You will work on them over the next 3 or 4 lab assignments and at the end, you will launch a JOS-in-JOS environment. 

### Background

This README series contains some background related to project-1. Reading this document will help you understand the pieces you will be implementing on a high level as you work on project-1.

The README series is broken down into 4 parts:
1. [Bootloader and Kernel](https://github.com/vijay03/cs360v-f20/blob/master/bootloader.md) which will help you in the understanding first part of the project, namely what happens when you boot up your PC (in our case, create or boot the guest).
2. [Virtual Memory](https://github.com/vijay03/cs360v-f20/blob/master/virtual_memory.md) which will help you in understanding the second part - where we transfer the multiboot structure from the host to the guest, for the guest to understand how much memory it is allocated and how much it can use. This part also contains details about segmentation and paging, which are a good background for the project in general.
3. [Environments](https://github.com/vijay03/cs360v-f20/blob/master/environments.md) which will help you in understanding what exactly is an environment, and some details about the environment structure which is used in sys_ept_map() and the trapframe structure.
4. [File System](https://github.com/vijay03/cs360v-f20/blob/master/file_system.md) which will help you in understanding the second part of the lab, where we handle vmcalls related to reading and writing of data to a disk.

## Lab-1

For Lab-1, you will first set up your working environment and then implement code for making the guest environment.
```diff
+ Deadline: 27th Sept 2020
```

## 1. Getting Started

You may use your laptops / computers for this project. Please enable qemu-kvm on your machines. Alternatively you can also use any of the following (gilligan) CS machines. As you need access to KVM module for this project, you cannot use other CS machines.
- ginger
- lovey
- mary-ann
- skipper
- the-professor
- thurston-howell-iii

For lab-1, you will use a virtual machine with Ubuntu 16.04 operating system. Follow the instructions below for
1. Setting up a VM and other essentials
2. Running JOS code for project-1

#### Setting up a Virtual Machine and Other Essentials

1. Download the compressed [VM image](https://www.cs.utexas.edu/~vijay/teaching/project1.tar.gz) (3.4 GB) on CS gilligan machines or your personal laptops (with QEMU and KVM enabled). The uncompressed VM image is available for download [here](http://www.cs.utexas.edu/~soujanya/project1-vm.qcow2).
```
$ wget https://www.cs.utexas.edu/~vijay/teaching/project1.tar.gz
```


2. Now start up a VM that listens on a specific port using the following command. To avoid contention over ports, use `<port-id> = 5900 + <team-number>`. For example, if your group-id is 15, your port-id will be 5915.
```
$ qemu-system-x86_64 -cpu host -drive file=<path-to-qcow2-image>,format=qcow2 -m 512 -net user,hostfwd=tcp::<port-id>-:22 -net nic -nographic -enable-kvm
```

3. On another terminal, connect to the VM using the following command. On connecting, enter the password as `abc123`.
```
$ ssh -p <port-id> cs378@localhost
```

5. Copy your public *and* private ssh keys from the CS lab machine or from your local machine into the VM.
Alternatively, you can generate a new key-pair on the VM using `ssh-keygen -t rsa`. You should send the public key in the VM to the TAs.
```
$ scp -P <port-id> $HOME/.ssh/id_rsa.pub cs378@localhost:~/.ssh/id_rsa.pub
$ scp -P <port-id> $HOME/.ssh/id_rsa cs378@localhost:~/.ssh/id_rsa
```

6. You will now be able to clone the project code `project-1.tar.gz` and access it from the VM. We will provide additional instructions later on how to use gitolite for project-1.
```
$ wget http://www.cs.utexas.edu/~soujanya/project-1.tar.gz
$ tar -zxf project-1.tar.gz
$ cd project-1
```

7. Verify that you have gdb 7.7 and gcc 4.8. Also cross check that you have python-3.4 installed or in your $HOME directory. In case you need to install any of them, follow the instructions on the [installations](https://github.com/vijay03/cs360v-f20/blob/master/installation.md) page. Note that to exit from QEMU VM press `Ctrl a` then `x`.


#### Running JOS VMM

Compile the code using the command:
```
$ make clean
$ make
```
Please note that the compilation works with gcc version <= 5.0.0. The Makefile uses gcc 4.8.0, which is present in the gilligan lab machines. Please install gcc-4.8 if you don't have it installed already.

You can run the vmm from the shell by typing:
```
$ make run-vmm-nox
```

## 2. Coding Assignment (Making a Guest Environment)

Currently, `make run-vmm-nox` will panic the kernel as the code that detects support for vmx and extended page table support is not yet implemented. You will see the following error and you will fix this in Lab-1:
```
kernel panic on CPU 0 at ../vmm/vmx.c:65: vmx_check_support not implemented
```

The JOS VMM is launched by a fairly simple program in user/vmm.c. This program,
- Calls a new system call to create an environment (similar to a process) that runs in guest mode (sys_env_mkguest).
- Once the guest is created, the VMM then copies the bootloader and kernel into the guest's physical address space.
- Then, it marks the environment as runnable, and waits for the guest to exit.

You will be implementing key pieces of the supporting system calls for the JOS VMM, as well as some of the copying functionality.

Before diving into the implementation details, You may want to skim the 
- JOS bookkeeping code for sys_env_mkguest that is already provided for you in kern/syscall.c
- Code in kern/env.h to understand how guest/regular environments are managed

Note that a major difference between a guest and a regular environment is that a guest has its type set to ENV_TYPE_GUEST. Additionally guest has a VmxGuestInfo structure and a vmcs structure associated with it.

The vmm directory includes the kernel-level support needed for the VMM--primarily extended page table support. In lab-1, you have two tasks at hand:
1. Checking support for vmx and extended paging
2. Running a guest environment

#### Checking Support for VMX and Extended Paging

Your first task will be to implement detection that the CPU supports vmx and extended paging. You will have to check the output of the cpuid instruction and check the values in certain model specific registers (MSRs). To understand how to implement the checks for the vmx and extended paging support, read Chapters 23.6, 24.6.2, and Appendices A.3.2-3 from the [Intel Manual](http://www.cs.utexas.edu/~vijay/cs378-f17/projects/64-ia-32-architectures-software-developer-vol-3c-part-3-manual.pdf).

Once you have read these sections, you will understand how to check support for vmx and extended paging. Now, implement the vmx_check_support() and vmx_check_ept() functions in vmm/vmx.c. Please read the hints above these functions to spot code that is already provided, for example, to read MSRs.

#### Running a Guest Environment

Your second task will be to add support to sched_yield() in kern/sched.c to call vmxon() when launching a guest environment.

If these functions are properly implemented, an attempt to start the VMM will not panic the kernel, but will fail because the vmm can't map guest bootloader and kernel into the VM. The error will look something like this:
```
Error copying page into the guest - 4294967289
```

## Hints

In all lab assignments in project-1, the functions you will be implementing might have hints on how to implement them as comments above. So please pay attention to the comments in the code.

## Submission Details

Submissions will be handled through gitolite. We will send out an announcement once gitolite is set up.

Please use gitolite to modify the source code, commit, and push your code changes. Commits made until midnight on the day of the submission deadline will be used for grading.

## Contact Details

Reach out to the TAs in case of any difficulties.
