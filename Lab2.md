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

In this exercise, you will use the assembly code below to complete the `asm_vmrun()` that launches the VM.
The code below will help you use the vmwrite instruction to set the host stack pointer,
as well as the vmlaunch and vmresume instructions to start the VM.

In order to facilitate interaction between the guest and the JOS host kernel, we copy the guest register state into the environment's Trapframe structure.
Thus, you will also write assembly to copy the relevant guest registers to and from this trapframe struct.

Skim Chapter 26 of the [Intel manual](http://www.cs.utexas.edu/~vijay/cs378-f17/projects/64-ia-32-architectures-software-developer-vol-3c-part-3-manual.pdf)
to familiarize yourself with the vmlaunch and vmresume instructions. Complete the assembly code in `asm_vmrun()` in vmm/vmx.c.
Also remove the panic in the call to `asm_vmrun()`. You can try implementing `asm_vmrun` yourself or you can use the code below to complete the function.
For this part of the lab assignment you will submit a readme `assembly_code.md` that has your understanding of the assembly code below.

```
void asm_vmrun(struct Trapframe *tf) {

        // NOTE: Since we re-use Trapframe structure, tf.tf_err contains the value
        // of cr2 of the guest.
        tf->tf_ds = curenv->env_runs;
        tf->tf_es = 0;
        vmcs_dump_cpu();
        unlock_kernel();
        asm(
                "push %%rdx; push %%rbp;"
                "push %%rcx \n\t" /* placeholder for guest rcx */
                "push %%rcx \n\t"
                /* Set the VMCS rsp to the current top of the frame. */
                /* Your code here */
                "vmwrite %%rsp, %%rdx\n\t"
                "1: \n\t"
                /* Reload cr2 if changed */
                "mov %c[cr2](%0), %%rax \n\t"
                "mov %%cr2, %%rdx \n\t"
                "cmp %%rax, %%rdx \n\t"
                "je 2f \n\t"
                "mov %%rax, %%cr2 \n\t"
                "2: \n\t"
                /* Check if vmlaunch of vmresume is needed, set the condition code
                 * appropriately for use below.
                 *
                 * Hint: We store the number of times the VM has run in tf->tf_ds
                 *
                 * Hint: In this function,
                 *       you can use register offset addressing mode, such as '%c[rax](%0)'
                 *       to simplify the pointer arithmetic.
                 */
                /* Your code here */
                "cmpl $1, %c[launched](%0) \n\t"
                /* Load guest general purpose registers from the trap frame.  Don't clobber flags.
                 *
                 */
                /* Your code here */
                "mov %c[rax](%0), %%rax \n\t"
                "mov %c[rbx](%0), %%rbx \n\t"
                "mov %c[rdx](%0), %%rdx \n\t"
                "mov %c[rsi](%0), %%rsi \n\t"
                "mov %c[rdi](%0), %%rdi \n\t"
                "mov %c[rbp](%0), %%rbp \n\t"
                "mov %c[r8](%0),  %%r8  \n\t"
                "mov %c[r9](%0),  %%r9  \n\t"
                "mov %c[r10](%0), %%r10 \n\t"
                "mov %c[r11](%0), %%r11 \n\t"
                "mov %c[r12](%0), %%r12 \n\t"
                "mov %c[r13](%0), %%r13 \n\t"
                "mov %c[r14](%0), %%r14 \n\t"
                "mov %c[r15](%0), %%r15 \n\t"
                "mov %c[rcx](%0), %%rcx \n\t" /* kills %0 (ecx) */
                /* Enter guest mode */
                /* Your code here:
                 *
                 * Test the condition code from rflags
                 * to see if you need to execute a vmlaunch
                 * instruction, or just a vmresume.
                 *
                 * Note: be careful in loading the guest registers
                 * that you don't do any compareison that would clobber the condition code, set
                 * above.
                 */
                "jne .Llaunched \n\t"
                " vmlaunch \n\t"
                "jmp .Lvmx_return \n\t"
                ".Llaunched: vmresume \n\t"
                ".Lvmx_return: "

                /* POST VM EXIT... */
                "mov %0, %c[wordsize](%%rsp) \n\t"
                "pop %0 \n\t"
                /* Save general purpose guest registers and cr2 back to the trapframe.
                 *
                 * Be careful that the number of pushes (above) and pops are symmetrical.
                 */
                /* Your code here */
                "mov %%rax, %c[rax](%0) \n\t"
                "mov %%rbx, %c[rbx](%0) \n\t"
                "popq %c[rcx](%0) \n\t"
                "mov %%rdx, %c[rdx](%0) \n\t"
                "mov %%rsi, %c[rsi](%0) \n\t"
                "mov %%rdi, %c[rdi](%0) \n\t"
                "mov %%rbp, %c[rbp](%0) \n\t"
                "mov %%r8,  %c[r8](%0) \n\t"
                "mov %%r9,  %c[r9](%0) \n\t"
                "mov %%r10, %c[r10](%0) \n\t"
                "mov %%r11, %c[r11](%0) \n\t"
                "mov %%r12, %c[r12](%0) \n\t"
                "mov %%r13, %c[r13](%0) \n\t"
                                "mov %%r14, %c[r14](%0) \n\t"
                "mov %%r15, %c[r15](%0) \n\t"
                "mov %%rax, %%r10 \n\t"
                "mov %%rdx, %%r11 \n\t"

                "mov %%cr2, %%rax   \n\t"
                "mov %%rax, %c[cr2](%0) \n\t"
                "pop  %%rbp; pop  %%rdx \n\t"

                "setbe %c[fail](%0) \n\t"
                : : "c"(tf), "d"((unsigned long)VMCS_HOST_RSP),
                  [launched]"i"(offsetof(struct Trapframe, tf_ds)),
                  [fail]"i"(offsetof(struct Trapframe, tf_es)),
                  [rax]"i"(offsetof(struct Trapframe, tf_regs.reg_rax)),
                  [rbx]"i"(offsetof(struct Trapframe, tf_regs.reg_rbx)),
                  [rcx]"i"(offsetof(struct Trapframe, tf_regs.reg_rcx)),
                  [rdx]"i"(offsetof(struct Trapframe, tf_regs.reg_rdx)),
                  [rsi]"i"(offsetof(struct Trapframe, tf_regs.reg_rsi)),
                  [rdi]"i"(offsetof(struct Trapframe, tf_regs.reg_rdi)),
                  [rbp]"i"(offsetof(struct Trapframe, tf_regs.reg_rbp)),
                  [r8]"i"(offsetof(struct Trapframe, tf_regs.reg_r8)),
                  [r9]"i"(offsetof(struct Trapframe, tf_regs.reg_r9)),
                  [r10]"i"(offsetof(struct Trapframe, tf_regs.reg_r10)),
                  [r11]"i"(offsetof(struct Trapframe, tf_regs.reg_r11)),
                  [r12]"i"(offsetof(struct Trapframe, tf_regs.reg_r12)),
                  [r13]"i"(offsetof(struct Trapframe, tf_regs.reg_r13)),
                  [r14]"i"(offsetof(struct Trapframe, tf_regs.reg_r14)),
                  [r15]"i"(offsetof(struct Trapframe, tf_regs.reg_r15)),
                  [cr2]"i"(offsetof(struct Trapframe, tf_err)),
                  [wordsize]"i"(sizeof(uint64_t))
                : "cc", "memory"
                  , "rax", "rbx", "rdi", "rsi"
                  , "r8", "r9", "r10", "r11", "r12", "r13", "r14", "r15"
                );
        vmcs_dump_cpu();
        panic("exiting intentionally");;
        lock_kernel();
        if(tf->tf_es) {
                cprintf("Error during VMLAUNCH/VMRESUME\n");
        } else {
                curenv->env_tf.tf_rsp = vmcs_read64(VMCS_GUEST_RSP);
                curenv->env_tf.tf_rip = vmcs_read64(VMCS_GUEST_RIP);
                vmexit();
        }
}
```

Once this is complete, you should be able to run the VM until the guest attempts a vmcall instruction, which traps to the host kernel.
Because the host isn't handling traps from the guest yet, the VM will be terminated. You should see an error like:
```
Unhandled VMEXIT, aborting guest.
```
