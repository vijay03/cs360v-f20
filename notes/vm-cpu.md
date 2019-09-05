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
        * Splits each target CPU instruction into micro-operations
        * Fewer micro-ops than full set of instructions and operands
        * `dyngen` takes a file containing micro-ops as input and
          outputs a dynamic code generator
        * Dynamic code generator is invoked at run time 
        * `dyngen` uses constant parameters to locate relocated code
        * Translator produces Translated Blocks (TBs) which are cached
          in a 16 MB Translator Cache
        * QEMU does simple register allocation on the host: usually
          memory, rarely host registers
        * QEMU makes one Translation Block jump to another block: this
          is called Direct Block Chaining
        * Memory management unit emulated using `mmap`
        * Handling self-modifying code: in un-virtualized case, a
          special instruction is used to invalidate cached code in the
          Instruction Cache. QEMU uses this instruction to invalidate
          Translation Blocks
        * On getting an exception (such as divide by zero), QEMU
          recreates the exact CPU state when the exception
          occurred. If required, TBs are re-executed. 
* **Hardware Support for Virtualization**
    * TBD

* Acknowledgements and Suggested Reading
    * [AnandTech blog](https://www.anandtech.com/show/2480/4)
    * [VMware: Software and Hardware Techniques for virtualizing x86](https://www.vmware.com/content/dam/digitalmarketing/vmware/en/pdf/techpaper/software_hardware_tech_x86_virt.pdf)
    * [QEMU ATC 2005 paper](http://archives.cse.iitd.ernet.in/~sbansal/csl862-virt/2010/readings/bellard.pdf)
