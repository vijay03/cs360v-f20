## Project 1 - Background

This README series contains some background related to project 1. Reading this document will help in understanding what exactly you are implementing on a high level as you work on Project-1.

This README series is broken down into 4 parts:
1. [Bootloader and Kernel](http://https://github.com/vijay03/cs378-f19/bootloader.md) which will help you in the understanding first part of the project, namely what happens when you boot up your PC (in our case, create or boot the guest).
2. [Virtual Memory](http://https://github.com/vijay03/cs378-f19/virtual_memory.md) which will help you in understanding the second part - where we transfer the multiboot structure from the host to the guest, for the guest to understand how much memory it is allocated and how much it can use. This part also contains details about segmentation and paging, which are a good background for the project in general.
3. [environments](http://https://github.com/vijay03/cs378-f19/environments.md) which will help you in understanding what exactly is an environment, and some details about the environment structure which is used in sys_ept_map() and the trapframe structure.
4. [File system](http://https://github.com/vijay03/cs378-f19/file_system.md) which will help you in understanding the second part of the lab, where we handle vmcalls related to reading and writing of data to a disk.

