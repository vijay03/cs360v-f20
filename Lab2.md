## Guest Bootloader and Kernel; Understanding vmlaunch and vmresume

In this lab assignment you will be completing the Guest bootloader and kernel code.
You will be implementing the memory manipulation code to copy the guest kernel and bootloader into the VM.
You will also familiarize yourself with the assembly code that helps launch/resume the JOS VM.

Before beginning this lab assignment, read [bootloader.md](https://github.com/vijay03/cs360v-f20/blob/master/bootloader.md).

### Mapping in the guest bootloader and kernel

In user/vmm.c we have provided the structure of the code to set up the guest and bootloader.
In this lab assignment, you will be implementing the functions `copy_guest_kern_gpa` that copies the guest kernel code into the guest physical address (gpa).
You will also implement the function `map_in_guest` that copies the bootloader into the guest.

Like any other user application in JOS, the vmm has the ability to open files, read pages, and map pages into other environments via IPC.
For supporting this, we have added a new system call `sys_ept_map`, which you must implement in kern/syscall.c.
The high-level difference between `sys_ept_map` and `sys_page_map` is whether the page is added using extended page tables or regular page tables.

Skim Chapter 28.2 of the [Intel manual](http://www.cs.utexas.edu/~vijay/cs378-f17/projects/64-ia-32-architectures-software-developer-vol-3c-part-3-manual.pdf)
to familiarize yourself with low-level EPT programming. Several helpful definitions have been provided in vmm/ept.h.

### Part-1 Coding Assignment

Implement `sys_ept_map()` in kern/syscall.c, as well as `ept_lookup_gpa()` and `ept_map_hva2gpa()` in vmm/ept.c.
Once this is complete, you should have complete support for nested paging.
The hints for implementing these functions are present as comments in the code.

At this point, you have enough host-level support function to map the guest bootloader and kernel into the guest VM.
For mapping the guest bootloader and kernel, you will need to read the kernel's ELF headers and copy the segments into the guest.

### Part-2 Coding Assignment

Implement `copy_guest_kern_gpa()` and `map_in_guest()` in user/vmm.c.
For the bootloader, we use map_in_guest directly, since the bootloader is only 512 bytes,
whereas the kernel's ELF header must be read by copy_guest_kern_gpa, which should then call map_in_guest for each segment.

The workflow (and hints) for this part is as follows:
1. `copy_guest_kern_gpa()` reads the ELF header from the kernel executable (using system calls present in lib/fd.c) into the struct Elf.
The kernel ELF contains multiple segments which must be copied from the host to the guest. So this function loops over all the segment headers
(i.e. program headers) and calls `map_in_guest()` for each of these segments. Each segment also contains the `gpa` that should be passed to `map_in_guest()`

2. `map_in_guest()` breaks down each segment in number of pages, loads each page into `UTEMP`, and
calls `sys_ept_map()` for each page by passing the `UTEMP` as the srcva.

3. `sys_ept_map()` first walks the page table levels at the host (given the srcva), and then gets
the physical page corresponding to the virtual address srcva (i.e. it returns the struct PageInfo).
The corresponding virtual address of this page is then computed using `page2kva()`, which basically
acts as the hva in the call to `ept_map_hva2gpa()`.

4. `ept_map_hva2gpa()` does a walk on the page table levels at the guest (given the gpa) using `ept_lookup_gpa()`
and then gets a page table entry at level 0 corresponding to the gpa. This function then inserts the physical address
corresponding to the hva, in the page table entry returned by `ept_lookup_gpa()`.

5. `ept_lookup_gpa()` does the walk on the page table hierarchy at the guest and returns the page table entry
corresponding to a gpa. It does this by making use of the `ADDR_TO_IDX` macro in vmm/ept.h starting from the
top-most EPT level, till it reaches the page table entry at level 0 which points to the actual page.

On a high level, in this section, each page of the kernel as well as the bootloader is mapped from the host
to the guest at particular physical addresses, and thus the kernel and the bootloader becomes available to the guest for when the guest is launched.

Once this is complete, the kernel will attempt to run the guest, and will panic because asm_vmrun is incomplete. This error looks like:
```
kernel panic on CPU 0 at ../vmm/vmx.c:637: asm_vmrun is incomplete
```

### Part-3 vmlaunch and vmresume

In this exercise, you will need to understand some assembly that launches the VM.
Although much of the VMCS setup is completed for you, this exercise will require you to use the vmwrite instruction to set the host stack pointer,
as well as the vmlaunch and vmresume instructions to start the VM.

In order to facilitate interaction between the guest and the JOS host kernel, we copy the guest register state into the environment's Trapframe structure.
Thus, you will also write assembly to copy the relevant guest registers to and from this trapframe struct.

Skim Chapter 26 of the [Intel manual](http://www.cs.utexas.edu/~vijay/cs378-f17/projects/64-ia-32-architectures-software-developer-vol-3c-part-3-manual.pdf)
to familiarize yourself with the vmlaunch and vmresume instructions. Complete the assembly code in `asm_vmrun()` in vmm/vmx.c.
Also remove the panic in the call to `asm_vmrun()`.

Once this is complete, you should be able to run the VM until the guest attempts a vmcall instruction, which traps to the host kernel.
Because the host isn't handling traps from the guest yet, the VM will be terminated. You should see an error like:
```
Unhandled VMEXIT, aborting guest.
```
