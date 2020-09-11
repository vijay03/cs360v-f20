## Project-1

In this project, you will implement a few exciting pieces of a paravirtual hypervisor. You will use the JOS operating system running on QEMU for this project. Check the [tools page](http://www.cs.utexas.edu/~vijay/cs378-f17/projects/tools.htm) for an overview on JOS and useful commands of QEMU. The project covers bootstrapping a guest OS, programming extended page tables, emulating privileged instructions, and using hypercalls to implement hard drive emulation over a disk image file. You will work on them over the next 3 or 4 lab assignments.

## Lab-1

For Lab-1, you will first set up your working environment and then implement code for making the guest environment.

## Getting Started

You may use your laptops / computers for this project. Please enable qemu-kvm on your machines. Alternatively you can also use any of the following (gilligan) CS machines. As you need access to KVM module for this project, you cannot use other CS machines.
- ginger
- lovey
- mary-ann
- skipper
- the-professor
- thurston-howell-iii

For lab-1, you will use a virtual machine with Ubuntu 16.04 operating system. Follow the instructions below for:
1. Setting up a Virtual Machine
2. Installing Dependencies and
3. Using GDB

#### 1. Setting up a Virtual Machine

1. Download the [VM image](http://www.cs.utexas.edu/~soujanya/project1-vm.qcow2) on the CS gilligan machines or your personal laptops (with QEMU and KVM enabled).
```
$ wget http://www.cs.utexas.edu/~soujanya/project1-vm.qcow2
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
$ scp -P <port-id> $HOME/.ssh/id_rsa.pub $USER@localhost:~/.ssh/id_rsa.pub
$ scp -P <port-id> $HOME/.ssh/id_rsa $USER@localhost:~/.ssh/id_rsa
```

6. You will now be able to use gitolite and clone the <project-repo> and access it from the VM.

#### 2. Installing Dependencies

Before compiling and running the jos-vmm code, you will need to install Python3.4, gcc-4.8, and the patched gdb_7.7. Please install gcc-4.8 and follow the instructions below to install Python3.4 and gdb7.7

Download and install python3.4 as given below:

```
$ wget https://www.python.org/ftp/python/3.4.5/Python-3.4.5rc1.tar.xz
$ tar xf Python-3.4.5rc1.tar.xz
$ cd Python-3.4.5rc1
$ ./configure --prefix=$HOME/python3.4 --enable-shared --with-threads
$ make
$ make install
```

The standard version of gdb does not correctly handle the transition to long mode during JOS boot, yielding a "Packet too long" error. For debugging 64-bit code on a 32-bit platform, you need both gdb and gdb-multiarch. Below we post patched Ubuntu package [gdb_7.7.1](http://www.cs.utexas.edu/~vijay/cs378-f17/projects/gdb_7.7.1-0ubuntu5~14.04.2_amd64.deb)

If you are using personal machines or running inside the VM, install gdb using following command:
```
$ sudo dpkg -i gdb_7.7.1-0ubuntu5~14.04.2_amd64.deb
```

If you are using the gilligan lab machines, install gdb using following command:
```
$ dpkg -x gdb_7.7.1-0ubuntu5~14.04.2_amd64.deb $HOME/gdb_7.7
GDB executable can be found at $HOME/gdb_7.7/usr/bin
```

After installing python3.4 and gdb7.7, open $HOME/.bashrc and add the following lines.
```
export LD_LIBRARY_PATH=/stage/public/ubuntu64/lib:$HOME/python3.4/lib
export PATH=$HOME/gdb7.7/usr/bin:$PATH
```

Finally, open (create if doesn't exist) $HOME/.gdbinit and add the following line:
```
set auto-load safe-path /
```

#### 3. Using GDB
Open a terminal window, type source ~/.bashrc to set the environment variables LD_LIBRARY_PATH and PATH. Then open (create if doesn't exist) $HOME/.bash_profile and add the line `source ~/.bashrc`.
```
$ cd <project-repo>/project-1
$ make clean
$ make
$ make run-vmm-nox-gdb
```

Open another terminal window and run the following commands to use GDB and to set breakpoints for example.
```
$ cd <project-repo>/project-1
$ gdb
```

## VMM Bootstrapping and Making a Guest Environment

The JOS VMM is launched by a fairly simple program in user/vmm.c. This application calls a new system call to create an environment (similar to a process) that runs in guest mode (sys_env_mkguest). Once the guest is created, the VMM then copies the bootloader and kernel into the guest's physical address space, marks the environment as runnable, and waits until the guest exits.

You will need to implement key pieces of the supporting system calls for the VMM, as well as some of the copying functionality.

Compile the code using the command:
```
$ make clean
$ make
```
Please note that the compilation works with gcc version <= 5.0.0. The Makefile specifically uses GCC 4.8.0, which is present in the gilligan lab machines. Please install gcc-4.8 if you haven't already to avoid the bootloader too large error.

You can try running the vmm from the shell in your guest by typing:
```
$ make run-vmm-nox
```
This will currently panic the kernel because the code to detect vmx and extended page table support is not implemented, but as you complete the project, you will see this launch a JOS-in-JOS environment. You will see the following error:
```
kernel panic on CPU 0 at ../vmm/vmx.c:65: vmx_check_support not implemented
```

### Coding Assignment

The JOS bookkeeping for sys_env_mkguest is already provided for you in kern/syscall.c. You may want to skim this code, as well as the code in kern/env.c to understand how environments are managed. A major difference between a guest and a regular environment is that a guest has its type set to ENV_TYPE_GUEST and has a VmxGuestInfo structure and a vmcs structure associated with it.

The vmm directory includes the kernel-level support needed for the VMM--primarily extended page table support.

Your first task will be to implement detection that the CPU supports vmx and extended paging. Do this by checking the output of the cpuid instruction and reading the values in certain model specific registers (MSRs).

Read Chapters 23.6, 24.6.2, and Appendices A.3.2-3 from the [Intel Manual](http://www.cs.utexas.edu/~vijay/cs378-f17/projects/64-ia-32-architectures-software-developer-vol-3c-part-3-manual.pdf) to learn how to discover if the CPU supports vmx and extended paging.

Once you have read these sections, implement the vmx_check_support() and vmx_check_ept() functions in vmm/vmx.c. You will also need to add support to sched_yield() in kern/sched.c to call vmxon() for launching a guest environment.

If these functions are properly implemented, an attempt to start the VMM will not panic the kernel, but will fail because the vmm can't map guest bootloader and kernel into the VM. The error will look something like this:
```
Error copying page into the guest - 4294967289
```

## Submission Details

Submissions will be handled through gitolite. We will send out an announcement once gitolite is set up.

Please use gitolite to modify the source code, commit, and push your code changes. Commits made until midnight on the day of the submission deadline will be used for grading.

## Contact Details

Reach out to the TAs in case of any difficulties.
