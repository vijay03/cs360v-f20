* Hosted Virtualization (or full virtualization) - what we covered in previous classes - has a significant performance overhead due to all the trap-and-emulate crossings that happen
* Before hardware support for virtualization was introduced, binary translation was the only practical solution, and even that had performance overhead
* Enter: Para Virtualization
  * We  give up the illusion of each virtual machine running on bare-metal in exchange for higher performance
* Main appeal: performance **within a few percent** of un-virtualized case
* Paravirtualization filled a gap between when binary translation was used and until good hardware support for virtualization was introduced
* With the introduction of virtualization hardware support, paravirtualization has been relegated to the few cases where the trap-and-emulate overhead is too high for IO or storage 
* Xen: most famous para-virtualization hypervisor
  * From the University of Cambridge
  * Released in 2003
  * Maintained as open source project
  * Based on the Exokernel architecture (see reading)
* Three main requirements Xen tries to satisfy:
  * VMs should be isolated
  * A variety of OS should be supported
  * High Performance (this is where Xen excels)
* Divides up the machine into “domains”
  * Each virtual machine runs on one domain
  *  The hypervisor is managed from domain 0 (or dom0)
  * Dom0 runs para-virtualized operating system
  * Other domains can run para-virtualized operating systems (at nearly full performance)
  * **Each OS has to be ported to Xen (main disadvantage)**
* While the OS has to be changed, the applications inside the OS do not have to be changed
* Para-virtualized (PV) OS knows its not on running on bare-metal
  *  Instead of privileged instructions, will make hypercalls
* Hypercalls are just calls to the hypervisor
* Para-virtualization is particularly useful for IO and networking
* PV virtual machines can directly use specialized device drivers through dom0
  * HVM virtual machines have to emulate the hardware (pay performance cost)
  * More on this when we cover storage and networking virtualization in later classes
* Xen does support unmodified OS if hardware support is available
  * These VMs are called Hardware Virtual Machines (HVM)
* Intel and AMD contributed to Xen to support their virtualization extensions
  * Without hardware support, unmodified OS cannot run. This is not true of full hosted virtualization we saw previously
* In 2005, VMware proposed a transparent paravirtualization interface, the Virtual Machine Interface (VMI)
  * A standardized interface would help different hypervisors and guests communicate
  * Developed by consortium of companies
  * The OS is written to the VMI interface
  * The VMI calls can be implemented using native code when the OS runs on bare metal
  * The VMI calls can be implemented using VMware or Xen-specific code for virtualization
* Main modification required of an OS: has to execute in x86 ring 1 instead of ring 0 (highest privilege)
  * Typically OS executes in ring 0, and user space applications execute in ring 3
  * System calls, page faults and other exceptions always trap to Xen
  * Xen then redirects to dom 0 (if required), does the work, and returns back to faulting VM
  * Clearing interrupts etc can be done directly by Xen
  * Redirection usually done when IO is involved -- dom0 will have much better device drivers than Xen itself
* System calls have a “fast track” path
* VM can register a function to be called on system call
  * This function is validated by Xen
  * The system call then no longer needs to trap to Xen every time
* The Xen hypervisor is mapped into the top 64MB of each virtual machine
  * When doing hypercalls, no need to context switch
  * If this was not done, the TLB would need to be flushed on a hypercall
* Device IO is perfomed by Xen
  * Transferred to each domain using shared memory
* VM Page Tables are directly read by the VM
  * But updates have to go through Xen (through hypercalls)
  * Each page table needs to be registered with Xen
  * Interrupts are replaced by Xen events
* Each VM has a bitmap indicating whether an event has occurred
  * Xen updates these bitmaps
  * Xen can also call a handler that is registered by the VM
* Communication between Domains and Xen
  * Domain to Xen: synchronous HyperCalls
  * Xen to Domain: async events
* Memory is statically partitioned among domains
* Reading:
  * The original Xen paper
  * The exokernel paper from SOSP 1995 
  * HVM vs PV as seen by Amazon in 2014
  * Old tech report from VMware written after paravirtualization just came out in 2008
