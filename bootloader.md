
This document contains some background related to project 1. Reading this document will help in understanding what exactly you are implementing on a high level as you work on Project-1.

### PC Bootstrap
A PC's physical address space is hard-wired to have the following general layout:
![alt_text](https://github.com/vijay03/cs378-f19/blob/master/figures/pc-bootstrap.png)

The first PCs, which were based on the 16-bit Intel 8088 processor, were only capable of addressing 1MB of physical memory. The physical address space of an early PC would therefore start at 0x00000000 but end at 0x000FFFFF instead of 0xFFFFFFFF. The 640KB area marked "Low Memory" was the only random-access memory (RAM) that an early PC could use; in fact the very earliest PCs only could be configured with 16KB, 32KB, or 64KB of RAM!

The 384KB area from 0x000A0000 through 0x000FFFFF was reserved by the hardware for special uses such as video display buffers and firmware held in non-volatile memory. The most important part of this reserved area is the Basic Input/Output System (BIOS), which occupies the 64KB region from 0x000F0000 through 0x000FFFFF. In early PCs the BIOS was held in true read-only memory (ROM), but current PCs store the BIOS in updateable flash memory. The BIOS is responsible for performing basic system initialization such as activating the video card and checking the amount of memory installed. After performing this initialization, the BIOS loads the operating system from some appropriate location such as floppy disk, hard disk, CD-ROM, or the network, and passes control of the machine to the operating system.

When Intel finally "broke the one megabyte barrier" with the 80286 and 80386 processors, which supported 16MB and 4GB physical address spaces respectively, the PC architects nevertheless preserved the original layout for the low 1MB of physical address space in order to ensure backward compatibility with existing software. Modern PCs therefore have a "hole" in physical memory from 0x000A0000 to 0x00100000, dividing RAM into "low" or "conventional memory" (the first 640KB) and "extended memory" (everything else). In addition, some space at the very top of the PC's 32-bit physical address space, above all physical RAM, is now commonly reserved by the BIOS for use by 32-bit PCI devices.

Recent x86 processors can support more than 4GB of physical RAM, so RAM can extend further above 0xFFFFFFFF. In this case the BIOS must arrange to leave a second hole in the system's RAM at the top of the 32-bit addressable region, to leave room for these 32-bit devices to be mapped. Because of design limitations JOS will use only the first 256MB of a PC's physical memory anyway, so for now we will pretend that all PCs have "only" a 32-bit physical address space.

When the BIOS runs, it sets up an interrupt descriptor table and initializes various devices such as the VGA display.

After initializing the PCI bus and all the important devices the BIOS knows about, it searches for a bootable device such as a floppy, hard drive, or CD-ROM. Eventually, when it finds a bootable disk, the BIOS reads the boot loader from the disk and transfers control to it.

### The Bootloader
Floppy and hard disks for PCs are divided into 512 byte regions called sectors. A sector is the disk's minimum transfer granularity: each read or write operation must be one or more sectors in size and aligned on a sector boundary. If the disk is bootable, the first sector is called the boot sector, since this is where the boot loader code resides. When the BIOS finds a bootable floppy or hard disk, it loads the 512-byte boot sector into memory at physical addresses 0x7c00 through 0x7dff, and then uses a jmp instruction to set the CS:IP to 0000:7c00, passing control to the boot loader. Like the BIOS load address, these addresses are fairly arbitrary - but they are fixed and standardized for PCs. The boot loader must perform the following main functions:
1. First, the boot loader obtains a map of the physical memory present in the system from the BIOS. This is done using a system call to the BIOS (int 0x15), which returns a structure called an e820 map. This call is possible only while the processor is still in real mode. JOS's bootloader constructs a multiboot structure, which it passes to the kernel. Multiboot is a standard for passing boot information from the bootloader to a kernel.
2. The boot loader then switches the processor from real mode to 32-bit protected mode, because it is only in this mode that software can access all the memory above 1MB in the processor's physical address space. One of the arcane x86 features the bootloader handles is properly configuring address bit 20. To better understand this, skim this article.
3. The bootloader sets up the stack and starts executing the kernel's C code in boot/main.c.
4. Finally, the boot loader reads the kernel from the hard disk by directly accessing the IDE disk device registers via the x86's special I/O instructions.

### The Kernel
Like the boot loader, the kernel begins with some assembly language code that sets things up so that C language code can execute properly.

The initial assembly code of the kernel does the following:

1. When the kernel starts executing, the processor is in the 32-bit protected mode. The first thing the kernel does is it tests whether the CPU supports long (64-bit) mode.
2. The kernel initializes a simple set of page tables for the first 4GB of memory. These pages map virtual addresses in the lowest 3GB to the same physical addresses, and then map the upper 256 MB back to the lowest 256 MB of memory. At this point, the kernel places the CPU in long mode. The kernel could determine dynamically whether to run in 64 or 32-bit mode based on whether the CPU supports long mode. Of course, this would substantially complicate the kernel.
3. Finally, the kernel sets up the stack and a few other things to start executing C code.
Look through the kernel source files kern/entry.S and kern/bootstrap.S and be able to answer the following question

At what point does the processor start executing 64-bit code? What exactly causes the switch from 32- to 64-bit mode?

#### Using segmentation to work around position dependence
Operating system kernels often like to be linked and run at very high virtual address, such as 0x8004100000, in order to leave the lower part of the processor's virtual address space for user programs to use.

Many machines don't have any physical memory at address 0x8004100000 so we can't count on being able to store the kernel there. Instead, we will use the processor's memory management hardware to map virtual address0x8004100000 - the link address at which the kernel code expects to run - to physical address 0x100000--- where the boot loader loaded the kernel. This way, although the kernel's virtual address is high enough to leave plenty of address space for user processes, it will be loaded in physical memory at the 1MB point in the PC's RAM, just above the BIOS ROM. This approach requires that the PC have at least a few megabytes of physical memory (so that address 0x00100000 works), but this is likely to be true of any PC built after about 1990.

### Physical Page Management
The operating system must keep track of which parts of physical RAM are free and which are currently in use. JOS manages the PC's physical memory with page granularity so that it can use the MMU to map and protect each piece of allocated memory.
