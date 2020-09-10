* Review last class
* At this point should understand: five types of virtualization, pros
  and cons of each, how each works at a high level
* Today: virtualizing memory
* Reviewing how memory virtualization works normally
  * Basics: address translation
  * Physical address to virtual address
  * Translation stored in page tables
  * Translation cached in TLBs
  * TLBs filled by a hardware page table walker
  * Root of page table stored in `CR3` register
  * TLBs flushed based on `invlpg` instruction and context switch
* On virtual machines, we need to do two translations:
  * Guest Virtual Address -> Guest Physical Address
  * Guest Physical Address -> Host Physical Address
  * We can store only one translation in the TLB
  * Guest Virtual Address -> Host Physical Address
* Virtualizing memory without hardware support: Shadow Page Tables
  * We store the translations (since only a few will fit in the TLB) in a
“shadow” page table:
  * Index is the same as on the virtual machine: guest virtual address
  * Output: host physical address
* Control Flow of translating Guest Virtual to Host Physical:
  1. Miss in TLB, go to shadow page table, find entry missing (this means the guest page table is missing an entry for this guest virtual address)
  2. Trap to hypervisor
  3. Trap to guest OS (simulate a page fault to guest OS)
  4. Guest OS tries to install new entry in its page table (which is read-only)
  5. Trap to hypervisor, install corresponding entry in shadow page table
  6. Install corresponding entry in guest page table
  7. Return to guest OS
  8. Return to hypervisor
  9. Return to guest application
* Every time the guest tries to update its own page table, we must trap
into the hypervisor
    * The shadow page table must be updated
    * Accomplished by marking guest page table as read-only, a write will
generate a fault
* When is page table modified?
  * To add page table entries (e.g., upon page fault)
  * To remove page table entries (e.g., upon munmap())
  * To change protection bits for page (e.g., make mmap page shared etc) 
* Page table access/dirty bits increase overhead
  * Setting these bits in guest page table requires trapping to hypervisor
* Every process in guest has its own address table
  * Every process also needs a shadow page table!
  * 2X memory requirements for page tables 
* Virtualizing memory with Hardware Support:
  * Intel: Extended Page Tables (EPT)
  * Operation: see 6.2 in [here](http://pages.cs.wisc.edu/~remzi/Classes/838/Spring2013/Papers/p3-agesen.pdf)
  * AMD: Nested Page Tables (NPT)
  * EPT doesn’t support dirty bits
  * TLB has VPID - address translations for different VMs are tagged with
  different VPID
  * No need to flush TLB when you switch VMs! 
  * No need for hypervisor involvement
  * HW will walk guest page table, then host page table, install entry in
TLB
  * Hypervisor involved only on page faults (why? Because it needs to
allocate pages)
* Shadow Page Tables vs EPT:
  * Both techniques maintain extra page tables
  * Key difference with Shadow Page Tables:
    * Hypervisor maintains guest physical address to host physical
translation
    * Shadow page tables have guest virtual to host physical translation
    * `CR3` register will point to a guest physical address that is the root
of guest page table
    * When using Shadow Page Tables, hypervisor has to be involved in:
      * Modifications to page tables
      * Page Faults
      * Context Switches
      * Invalidating page Table Entries
  * When using EPT:
      * All those overheads gone
      * But page table walks are more expensive (need to walk two page
        tables)
      * TLB misses are much more expensive
        * TLB miss normally: O(D) accesses where the page table has D
          levels.
        * TLB miss with EPT: O(D*D) accesses: O(D) in the guest page
          table, and each block of the guest page table needs to be
          found using O(D) in the host page table.
  * Overall, EPT faster than Shadow Page Tables ([2--6x faster](https://www.vmware.com/pdf/Perf_ESX_Intel-EPT-eval.pdf))

* Suggested Reading
  * [The Evolution of an x86 Virtual Machine
    Monitor](http://pages.cs.wisc.edu/~remzi/Classes/838/Spring2013/Papers/p3-agesen.pdf)
  * [Virtual Machines: Virtualizing Virtual Memory](
 https://corensic.wordpress.com/2011/12/05/virtual-machines-virtualizing-virtual-memory/) 
  * [Hardware Virtualization: Nuts and Bolts](https://www.anandtech.com/show/2480/10)
  * [Best Practices for Paravirtualization Enhancements from Intel
 Virtualization Technology: EPT and
 VT-d](https://software.intel.com/en-us/articles/best-practices-for-paravirtualization-enhancements-from-intel-virtualization-technology-ept-and-vt-d) 
  * [Performance Evaluation of Intel EPT Hardware Assist](https://www.vmware.com/pdf/Perf_ESX_Intel-EPT-eval.pdf)
 
 
