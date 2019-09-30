### Virtual Memory

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

#### Virtual, Linear, and Physical Addresses
In AMD64 terminology, a virtual address consists of a segment selector and an offset within the segment. A linear address is what you get after segment translation but before page translation. A physical address is what you finally get after both segment and page translation and what ultimately goes out on the hardware bus to your RAM. Be sure you understand the difference between these three types or "levels" of addresses!
![alt_text](http://https://github.com/vijay03/cs378-f19/figures/seg-paging.png)

A C pointer is the "offset" component of the virtual address. In kern/bootstrap.S, we installed a Global Descriptor Table (GDT) that effectively disabled segment translation by setting all segment base addresses to 0 and limits to 0xffffffff. Hence the "selector" has no effect and the linear address always equals the offset of the virtual address.

From code executing on the CPU, once we're in protected/long mode, there's no way to directly use a linear or physical address. All memory references are interpreted as virtual addresses and translated by the MMU, which means all pointers in C are virtual addresses.

The JOS kernel often needs to manipulate addresses as opaque values or as integers, without dereferencing them, for example in the physical memory allocator. Sometimes these are virtual addresses, and sometimes they are physical addresses. To help document the code, the JOS source distinguishes the two cases: the type uintptr_t represents virtual addresses, and physaddr_t represents physical addresses. Both these types are really just synonyms for 64-bit integers (uint64_t), so the compiler won't stop you from assigning one type to another! Since they are integer types (not pointers), the compiler will complain if you try to dereference them.

The JOS kernel can dereference a uintptr_t by first casting it to a pointer type. In contrast, the kernel can't sensibly dereference a physical address, since the MMU translates all memory references. If you cast a physaddr_t to a pointer and dereference it, you may be able to load and store to the resulting address (the hardware will interpret it as a virtual address), but you probably won't get the memory location you intended.

The JOS kernel also sometimes needs to be able to find a physical address given the virtual address of the memory in which a kernel data structure is stored. The kernel addresses its global variables and memory that boot_alloc() allocates, with addresses in the region where the kernel was loaded, starting at 0x8004000000, the very region where we mapped all of physical memory. Thus, to turn a virtual address in this region into a physical address, the kernel can simply subtract 0x8004000000. You should use PADDR(va) to do that subtraction.

### Kernel Address Space
JOS divides the processor's linear address space into two parts. User environments (processes) will have control over the layout and contents of the lower part, while the kernel always maintains complete control over the upper part. The dividing line is defined somewhat arbitrarily by the symbol ULIM in inc/memlayout.h, reserving approximately 256MB of linear (and therefore virtual) address space for the kernel.

#### Address Space Layout Alternatives
The address space layout we use in JOS is not the only one possible. An operating system might map the kernel at low linear addresses while leaving the upper part of the linear address space for user processes. x86 kernels generally do not take this approach, however, because one of the x86's backward-compatibility modes, known as virtual 8086 mode, is "hard-wired" in the processor to use the bottom part of the linear address space, and thus cannot be used at all if the kernel is mapped there.

It is even possible, though much more difficult, to design the kernel so as not to have to reserve any fixed portion of the processor's linear or virtual address space for itself, but instead effectively to allow allow user-level processes unrestricted use of the entire 4GB of virtual address space - while still fully protecting the kernel from these processes and protecting different processes from each other!
