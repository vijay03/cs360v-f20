* A review of the basics
    * Traps
    * Rings
    * Instruction execution
* What is a virtual machine?
    * A virtual machine provides the illusion of an operating system
      running on top of a different physical machine inside the host
      machine
    * This is termed full-machine virtualization
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
* The basic way to do virtualization: trap and emulate
    * Whenever guest OS executes any instruction, it results in a trap
    * When we handle the trap in the host OS, we emulate whatever the guest was trying to do
    * For example, if it was trying to write into the trap handler table, we do the write on its behalf
* Why is the basic approach bad?
    * Super slow

    
    