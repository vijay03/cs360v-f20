* A review of the basics: see [OSTEP](http://pages.cs.wisc.edu/~remzi/OSTEP/cpu-mechanisms.pdf) for refresher
    * Traps
    * Rings
    * Instruction execution
* What is a virtual machine?
    * Definition from [Popek and Goldberg](https://cs.nyu.edu/courses/fall14/CSCI-GA.3033-010/popek-goldberg.pdf): "A virtual machine is taken to be an efficient, isolated duplicate of the real machine" 
    * A virtual machine provides the illusion of a different physical
      machine inside the host machine, running its own operating system
    * This is termed *full-machine virtualization*
    * Terminology
        * The OS running in the virtual machine is called the **the guest OS**
        * The OS running in the host physical machine is called the **host OS** or **hypervisor**
        * The hypervisor may or may not have all the functions of a
          traditional OS; it could be light-weight, just doing
          virtualization
* What is involved in full-machine virtualization?
    * What happens when you execute an instruction?
    * What happens when you access memory?
        * Remember the virtualized operating system has a kernel and user-space of its own
    * What happens when you send a packet over the network?
    * What happens when you read or write a file?
* The two types of virtualization:
    * **Host Virtualization**: where the guest OS is unaware of being virtualized
        * Does not require the guest OS to be modified in any way whatsoever
        * Thus, will work with *all* OS written to the same instruction set
        * Guest OS thinks it is running on bare-metal machine: maintaining this illusion is expensive
    * **Para-virtualization**: where the guest OS knows it is being virtualized, and participates in the process
* What properties would we like virtual machines to have?
    * Isolation: a problem in the virtual machine should not affect the host or other virtual machines
    * Encapsulation: it should be possible to move a virtual machine from one physical machine to another
    * Performance: running an application on a virtual machine should have performance similar to running it on the host machine. 
* Three goals for a virtual machine architecture:
    1. Equivalence: The VM should be indistinguishable from the underlying hardware.
    2. Resource control: The VM should be in complete control of any virtualized resources.
    3. Efficiency: Most VM instructions should be executed directly on the underlying CPU without involving the hypervisor.

* Virtualization Basic Approach #1: [Hosted Interpretation](http://www.eecs.harvard.edu/~cs161/notes/virtualization.pdf)
    * Hypervisor or host OS maintains a software-level representation of physical hardware
        * For example, the value of various registers as seen by the guest OS
    * When guest OS executes an instruction, host OS updates software representation
    * Used by Bochs to emulate x86, used in video game emulators
    * No guest instruction is directly executed on hardware
    * Flexible approach
    * Doing this becomes harder as thing being emulated becomes complex (such as modern processors)
    * Very slow (100x slower than direct execution on hardware)
* Virtualization Basic Approach #2: trap and emulate
    * Host OS runs in Ring 1, Guest OS runs in Ring 0, Host and guest applications run in Ring 3
    * Whenever guest OS executes any privileged instruction, it results in a trap
    * When we handle the trap in the host OS, we emulate whatever the guest was trying to do
    * For example, if it was trying to write into the trap handler table, we do the write on its behalf
* Why is this approach bad?
    * Slow (faster than #1, but still slow)
    * Executing one instruction vs trap, emulate (many instructions),
      handle control back to host OS (many instructions)
    * Similar to #1, host OS has to maintain software-level representation of guest state
    * Doesn't always work:
            * For an instruction set to be virtualizable, all **sensitive** instructions (which deal with privileged state) must also be **privileged** instructions taht cause a trap when executed with lower privilege. 
        * What if an instruction *silently fails* if it is run in user mode
        * We can't emulate such instructions without trapping on every instruction (horribly slow)
        * Unfortunately, x86 has such instructions. Example: `popf` and `push`
        * `push %cs` pushes `%cs` to top of stack
            * `%cs` contains 2 bits indicating current privilege level
            * `push %cs` in ring 1 does not cause a trp
            * Guest OS could use this to find out its not running at Ring 0!
        * `pushf/popf` read/write the `%eflags` register
            * Bit 9 of `%eflags` enables interrupts
            * In Ring 0, popfcan set bit 9, but in Ring 1, CPU silently ignores popf!
    * Trap and emulate is a **reactive** approach: we execute instructions, and react to problems or insufficient privilege
* Approach #3: **Binary Translation**
    * Pro-active approach to virtualization
    * Privileged or senstive instructions are *translated* into the appropriate actions on software-level representation of guest state
    * Don't have to worry about whether something will cause traps: we rewrite anyway!
    * Translated instruction blocks execute directly on the physical hardware
    * No need to rewrite applications or guest OS
    * This was the breakthrough that led to VMware being successful and launching VMware ESX Server
    * Similar to approach #1, the complexity of binary translation increases with the complexity of the guest OS 
* Approach #4 used today: **Hardware-Assisted Virtualization**
    * Intel and AMD added virtualization support to the hardware
    * Sensitive instructions cause a trap (the original problem with approch #2)
    * New hardware structures (`VMCS`) to control which sensitive instructions cause a trap
    * Most virtual machines run today take advantage of hardware support 
* Approach #5: **Para-virtualization**
    * Rewriting the guest OS to remove sensitive-but-unprivileged instructions
    * Guest applications are unmodified
    * Uses a subset of x86 that is virtualizable
    * Xen hypervisor built using this approach, we'll look at it in detail later
    
* Acknowledgements:
    * [James Mickens](https://mickens.seas.harvard.edu/) [fantastic slides on Virtualization](http://www.eecs.harvard.edu/~cs161/notes/virtualization.pdf)
    