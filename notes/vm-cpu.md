* Review previous class material
* **Binary Translation**
    * VMware used this in 1999 to solve the "sensitive" instructions problem in x86
    * VMware uses a Binary Translator (BT)
    * Guest user code is un-changed
    * Guest OS code goes into BT -> translated code runs in Ring 1 (not Ring 0)
    * Translated code is kept in a Translator Cache (TC)
    * Guest OS code that manipulates hardware -> user-mode code that manipulates virtual hardware
    * Guest OS code that does privileged instructions -> user-mode code + system calls into host OS
    * Tricky parts:
        * Remember what is getting translated is x86 instructions, not high-level code
        * Original code has "jump to address 100 bytes forward" -> the jump has to be translated and changed
        * Translator Cache also keeps track of the control flow
        * Register Allocation
    * [Quick Emulator (QEMU) uses binary translation](http://archives.cse.iitd.ernet.in/~sbansal/csl862-virt/2010/readings/bellard.pdf)
        * Dynamic translation at runtime
        * Uses a translator cache like VMware
        * Basic idea: guest code -> intermediate C code
          (micro-operations) -> host code
        * write C code on host, compile the code, use parts of
          generated code to translate guest into host code
        * `dyngen` takes a file containing micro-ops as input and
          outputs a dynamic code generator
        * Dynamic code generator is invoked at run time 
        * `dyngen` uses constant parameters to locate relocated code
        * `dyngen` replaced today with `Tiny Code Generator (tcg)`
        * Translator produces Translated Blocks (TBs) which are cached
          in a 16 MB Translator Cache
        * An entire TB must be in either user mode or kernel mode:
          QEMU doesn't mix this
        * After each translated basic block is executed, QEMU uses the
          simulated Program Counter (PC) and other cpu state
          information (such as the CS segment base value) to find the
          next basic block.
        * QEMU does simple register allocation on the host: usually
          memory, rarely host registers
        * QEMU makes one Translation Block jump to another block: this
          is called Direct Block Chaining
          * Normally, there is special code surrounding each TB for
            initializing processor state and restoring processor state
          * Block chaining increases performance significantly by
            avoiding special code
        * Memory management unit emulated using `mmap`
        * Handling self-modifying code: in un-virtualized case, a
          special instruction is used to invalidate cached code in the
          Instruction Cache in most instruction sets. QEMU uses this
          instruction to invalidate Translation Blocks. 
              * Unfortunately, this is not the case in x86.
              * QEMU handles this in x86 by preventing code regions
                from being modified; a write to a code region raises a
                SEGV signal which is then handled by invalidating all
                TBs related to that code page, allowing the write, and
                redoing translation. 
        * On getting an exception (such as divide by zero), QEMU
          recreates the exact CPU state when the exception
          occurred. If required, TBs are re-executed.
        * QEMU checks for pending interrupts periodically (not at
          every TB) 
        * QEMU is about 30x faster than Bochs (which uses trap and emulate)
* **Hardware Support for CPU Virtualization**
    * Intel VT-X (available from Pentium 4) and AMD-V (available from
      Opteron Rev F)
    * Both allow direct execution of virtual machine on the processor
      (termed `vmentry`) until a privileged instruction is executed
    * `vmexit` happens when privilege is required
    * Hardware support also allows the hypervisor to control when
      `vmexit` happens (in other words, which instructions can trigger
      a trap)

* Acknowledgements and Suggested Reading
    * [AnandTech blog](https://www.anandtech.com/show/2480/4)
    * [VMware: Software and Hardware Techniques for virtualizing x86](https://www.vmware.com/content/dam/digitalmarketing/vmware/en/pdf/techpaper/software_hardware_tech_x86_virt.pdf)
    * [QEMU ATC 2005
      paper](http://archives.cse.iitd.ernet.in/~sbansal/csl862-virt/2010/readings/bellard.pdf)
    * [QEMU Translator Internals](https://people.redhat.com/pbonzini/qemu-test-doc/_build/html/topics/Translator-Internals.html)
    * [QEMU Internals
      Slides](https://www.csd.uoc.gr/~hy428/reading/qemu-internals-slides-may6-2014.pdf)
      by Manolis Marazakis at FORTH-ICS
