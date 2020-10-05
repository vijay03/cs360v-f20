## Project-1

In this project, you will implement a few exciting pieces of a paravirtual hypervisor.
You will use the JOS operating system running on QEMU for this project.
Check the [tools page](https://github.com/vijay03/cs360v-f20/blob/master/tools.md) for an overview on JOS and useful commands of QEMU.
The project covers bootstrapping a guest OS, programming extended page tables, emulating privileged instructions, and using hypercalls
to implement hard drive emulation over a disk image file. You will work on them over the next 3 or 4 lab assignments and at the end,
you will launch a JOS-in-JOS environment. 

Please find the different lab assignment for project-1 here:

1. [Lab-1](https://github.com/vijay03/cs360v-f20/blob/master/Lab1.md)
2. [Lab-2](https://github.com/vijay03/cs360v-f20/blob/master/Lab2.md)


### Background

This README series contains some background related to project-1. Reading this document will help you understand the pieces you will be implementing on a high level as you work on project-1.

The README series is broken down into 4 parts:
1. [Bootloader and Kernel](https://github.com/vijay03/cs360v-f20/blob/master/bootloader.md) which will help you in the understanding first part of the project, namely what happens when you boot up your PC (in our case, create or boot the guest).
2. [Virtual Memory](https://github.com/vijay03/cs360v-f20/blob/master/virtual_memory.md) which will help you in understanding the second part - where we transfer the multiboot structure from the host to the guest, for the guest to understand how much memory it is allocated and how much it can use. This part also contains details about segmentation and paging, which are a good background for the project in general.
3. [Environments](https://github.com/vijay03/cs360v-f20/blob/master/environments.md) which will help you in understanding what exactly is an environment, and some details about the environment structure which is used in sys_ept_map() and the trapframe structure.
4. [File System](https://github.com/vijay03/cs360v-f20/blob/master/file_system.md) which will help you in understanding the second part of the lab, where we handle vmcalls related to reading and writing of data to a disk.
