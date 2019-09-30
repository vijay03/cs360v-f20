## Project 1 - Paravirtual VMM

### Updates to README:
1. Added compilation instructions for JOS in `Part 1 - VMM Bootstrap`, and added setup as well as submission instructions in `Getting Started` on 09/17
2. Added the outputs that are expected after each step of the project

### Introduction
This project will guide you through writing a basic paravirtual hypervisor. We will use the JOS operating system running on a qemu emulator. Check the [tools page](http://www.cs.utexas.edu/~vijay/cs378-f17/projects/tools.htm) for getting an overview of JOS and useful commands of QEMU. The main topics covered in this project are: bootstrapping a guest OS, programming extended page tables, emulating privileged instructions, and using hypercalls to implement hard drive emulation over a disk image file.

### Getting Started

To fetch the source for this project, use gitolite:
```
git clone cs378-vijay@git.cs.utexas.edu:<groupname>-project1
```

To push the code to the repository you need to use:
```
git push origin master
```

Additionally, The source for this project is present in this repository: [project-1.tar.gz](https://github.com/vijay03/cs378-f19/blob/master/project-1.tar.gz)
Untar it with the following command: `tar -xvf project-1.tar.gz`

The submission of the code will be done through gitolite. Please use gitolite in order to modify the source code, commit and push your code. Commits made until midnight on the day of the submission deadline will be used for grading.

You need access to kvm module for this project. So please use one of the following (gilligan) lab machines for this project:
1. ginger
2. lovey
3. mary-ann
4. skipper
5. the-professor
6. thurston-howell-iii

You can also enable qemu-kvm on your personal laptops / computers and work on the project.

### Part 1 - VMM Bootstrap
The JOS VMM is launched by a fairly simple program in user/vmm.c. This application calls a new system call to create an environment (similar to a process) that runs in guest mode (sys_env_mkguest). Once the guest is created, the VMM then copies the bootloader and kernel into the guest's physical address space, marks the environment as runnable, and waits until the guest exits.

You will need to implement key pieces of the supporting system calls for the VMM, as well as some of the copying functionality.

Compile the code using the command:
```
$ make clean
$ make
```
Please note that the compilation works with gcc version less than or equal to 5.0.0. If you decide to use one of the gilligan lab machines mentioned above for the project, please modify line 77 of GNUmakefile to the following:
```
CC      := $(GCCPREFIX)gcc-4.8 -pipe
```
This will make sure that you use gcc-4.8 for compilation of JOS. The compile using the commands above.

You can try running the vmm from the shell in your guest by typing:
```
$ make run-vmm-nox
```
This will currently panic the kernel because the code to detect vmx and extended page table support is not implemented, but as you complete the project, you will see this launch a JOS-in-JOS environment. You will see an error like `kernel panic on CPU 0 at ../vmm/vmx.c:65: vmx_check_support not implemented`

#### Making a guest environment
The JOS bookkeeping for sys_env_mkguest is already provided for you in kern/syscall.c. You may want to skim this code, as well as the code in kern/env.c to understand how environments are managed. A major difference between a guest and a regular environment is that a guest has its type set to ENV_TYPE_GUEST and has a VmxGuestInfo structure and a vmcs structure associated with it.

The vmm directory includes the kernel-level support needed for the VMM--primarily extended page table support.

Your first task will be to implement detection that the CPU supports vmx and extended paging. Do this by checking the output of the cpuid instruction and reading the values in certain model specific registers (MSRs).

Read Chapters 23.6, 24.6.2, and Appendices A.3.2-3 from the [Intel manual](http://www.cs.utexas.edu/~vijay/cs378-f17/projects/64-ia-32-architectures-software-developer-vol-3c-part-3-manual.pdf) to learn how to discover if the CPU supports vmx and extended paging.

Once you have read these sections, implement the `vmx_check_support()` and `vmx_check_ept()` functions in vmm/vmx.c. You will also need to add support to `sched_yield()` to call vmxon() when launching a guest environment.

If these functions are properly implemented, an attempt to start the VMM will not panic the kernel, but will fail because the vmm can't map guest bootloader and kernel into the VM. The error should look something like `Error copying page into the guest - 4294967289`

#### Mapping in the guest bootloader and kernel
In user/vmm.c we have provided the structure of the code to set up the guest and bootloader. However, you must implement the memory manipulation code to copy the guest kernel and bootloader into the VM.

Like any other user application in JOS, the vmm has the ability to open files, read pages, and map pages into other environments via IPC. One difference is that we've added a new system call sys_ept_map, which you must implement. The high-level difference between sys_ept_map and sys_page_map is whether the page is added using extended page tables or regular page tables.

Skim Chapter 28.2 of the [Intel manual](http://www.cs.utexas.edu/~vijay/cs378-f17/projects/64-ia-32-architectures-software-developer-vol-3c-part-3-manual.pdf) to familiarize yourself with low-level EPT programming. Several helpful definitions have been provided in vmm/ept.h.

Implement `sys_ept_map()` in kern/syscall.c, as well as `ept_lookup_gpa()` and `ept_map_hva2gpa()` in vmm/ept.c. Once this is complete, you should have complete support for nested paging.

At this point, you have enough host-level support function to map the guest bootloader and kernel into the guest VM. You will need to read the kernel's ELF headers and copy the segments into the guest.

Implement `copy_guest_kern_gpa()` and `map_in_guest()` in user/vmm.c. For the bootloader, we use map_in_guest directly, since the bootloader is only 512 bytes, whereas the kernel's ELF header must be read by copy_guest_kern_gpa, which should then call map_in_guest for each segment.

Once this is complete, the kernel will attempt to run the guest, and will panic because asm_vmrun is incomplete. The error should look like: `kernel panic on CPU 0 at ../vmm/vmx.c:637: asm_vmrun is incomplete`

#### Implementing vmlaunch and vmresume
In this exercise, you will need to write some assembly to launch the VM. Although much of the VMCS setup is completed for you, this exercise will require you to use the vmwrite instruction to set the host stack pointer, as well as the vmlaunch and vmresume instructions to start the VM.

In order to facilitate interaction between the guest and the JOS host kernel, we copy the guest register state into the environment's Trapframe structure. Thus, you will also write assembly to copy the relevant guest registers to and from this trapframe struct.

Skim Chapter 26 of the [Intel manual](http://www.cs.utexas.edu/~vijay/cs378-f17/projects/64-ia-32-architectures-software-developer-vol-3c-part-3-manual.pdf) to familiarize yourself with the vmlaunch and vmresume instructions. Complete the assembly code in `asm_vmrun()` in vmm/vmx.c. Also remove the panic in the call to `asm_vmrun()`.

Once this is complete, you should be able to run the VM until the guest attempts a vmcall instruction, which traps to the host kernel. Because the host isn't handling traps from the guest yet, the VM will be terminated. You should see an error like `Unhandled VMEXIT, aborting guest.`

### Part 2 - Handling VM exits
The equivalent event to a trap from an application to the operating system is called a VM exit. We have provided some skeleton code to dispatch the major types of exits we expect our guest to provide in the vmm/vmx.c function `vmexit()`. You will need to identify the reason for the exit from the VMCS, as well as implement handler functions for certain events in vmm/vmexits.c.

Similar to issuing a system call (e.g., using the int or syscall instruction), a guest can programmatically trap to the host using the vmcall instruction (sometimes called hypercalls). The current JOS guest uses three hypercalls: one to read the e820 map, which specifies the physical memory layout to the OS; and two to use host-level IPC, discussed below.

#### Multi-boot map (aka e820)
JOS is "told" the amount of physical memory it has by the bootloader. JOS's bootloader passes the kernel a multiboot info structure which possibly contains the physical memory map of the system. The memory map may exclude regions of memory that are in use for reasons including IO mappings for devices (e.g., the "memory hole"), space reserved for the BIOS, or physically damaged memory. For more details on how this structure looks and what it contains, refer to the [specification](https://www.gnu.org/software/grub/manual/multiboot/multiboot.html). A typical physical memory map for a PC with 10 GB of memory looks like below.
```
        e820 MEMORY MAP
        address: 0x0000000000000000, length: 0x000000000009f400, type: USABLE
        address: 0x000000000009f400, length: 0x0000000000000c00, type: RESERVED
        address: 0x00000000000f0000, length: 0x0000000000010000, type: RESERVED
        address: 0x0000000000100000, length: 0x00000000dfefd000, type: USABLE
        address: 0x00000000dfffd000, length: 0x0000000000003000, type: RESERVED
        address: 0x00000000fffc0000, length: 0x0000000000040000, type: RESERVED
        address: 0x0000000100000000, length: 0x00000001a0000000, type: USABLE
```

For the JOS guest, rather than emulate a BIOS, we will simply use a vmcall to request a "fake" memory map. Complete the implementation of `vmexit()` by identifying the reason for the exit from the VMCS. You may need to search Chapter 27 of the [Intel manual](http://www.cs.utexas.edu/~vijay/cs378-f17/projects/64-ia-32-architectures-software-developer-vol-3c-part-3-manual.pdf) to solve this part of the exercise.
Implement the `VMX_VMCALL_MBMAP` case of the function `handle_vmcall()` in vmm/vmexits.c. Also, be sure to advance the instruction pointer so that the guest doesn't get in an infinite loop. Once the guest gets a little further in boot, it will attempt to discover whether the CPU supports long mode, using the cpuid instruction. Our VMCS is configured to trap on this instruction, so that we can emulate it---hiding the presence of vmx, since we have not implemented emulation of vmx in software. Now you will see an error of the form `kernel panic on CPU 0 at ../vmm/vmexits.c:262: cpuid not implemented`.

Implement `handle_cpuid()` in vmm/vmexits.c. When the host can emulate the cpuid instruction, your guest should run until it attempts to perform disk I/O, giving an error of the form `Unhandled VMEXIT, aborting guest.`

JOS has a user-level file system server daemon, similar to a microkernel. We place the guest's disk image as a file on the host file system server. When the guest file system daemon requests disk reads, rather than issuing ide-level commands, we will instead use vmcalls to ask the host file system daemon for regions of the disk image file. This is depicted in the image below.
![alt text](http://www.cs.utexas.edu/~vijay/cs378-f17/projects/disk-architecture.jpg)

Once this is completed, you need to modify the `bc_pgfault()` amd `flush_block()` in fs/bc.c to issue I/O requests using the `host_read()` and `host_write()` hypercalls. Use the macro VMM_GUEST to select different behavior for the guest and host OS. You will also have to implement the IPC send and receive hypercalls in `handle_vmcall()`, as well as the client code to issue `ipc_host_send()` and `ipc_host_recv()` vmcalls in lib/ipc.c.

Finally, you will need to extend the `sys_ipc_try_send()` to detect whether the environment is of type `ENV_TYPE_GUEST` or not, and you also need to implement the `ept_page_insert()` function.

Once these steps are complete, you should have a fully running JOS-on-JOS.

### Hints
All the functions to be implemented contain hints on how to implement the respective functions as comments in the function names. So please pay attention to the commented code as well.
