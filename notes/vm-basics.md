* A review of the basics
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
* The basic way to do virtualization: trap and emulate
    * Whenever guest OS executes any instruction, it results in a trap
    * When we handle the trap in the host OS, we emulate whatever the guest was trying to do
    * For example, if it was trying to write into the trap handler table, we do the write on its behalf
* Why is the basic approach bad?
    * Super slow
    * Executing one instruction vs trap, emulate (many instructions),
      handle control back to host OS (many instructions)
    * How can we do better?
        * Allow most instructions to execute directly on CPU, with reduced privilege
        * Trap on all instructions that require higher privelege
        * Better than basic approach, but still slow
    * Doesn't always work:
        * Need instructions that run either in user mode or kernel mode
        * What if we had an instruction that could run in either?
        * Even worse, what if the instruction *silently fails* if it is run in user mode
        * We can't emulate such instructions without trapping on every instruction (horribly slow)
* Three goals for a virtual machine architecture:
    1. Equivalence: The VM should be indistinguishable from the underlying hardware.
    2. Resource control: The VM should be in complete control of any virtualized resources.
    3. Efficiency: Most VM instructions should be executed directly on the underlying CPU without involving the hypervisor.
           
    
    