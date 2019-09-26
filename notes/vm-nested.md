## Nested Virtualization
* Why?
  * Allows virtualizing hypervisors, instead of just operating systems
  * Allows moving hypervisors + its virtual machines from one physical
    machine to another as a single unit
  * Allows research and development on hypervisors without needing
    bare metal hardware
  * Allows security approaches that require a vulnerable hypervisor
* The Turtles Project
  * Multiples multiple levels of virtualization on the single level of
  arch support available
  * Traps sent to the lowest hypervisor, which then forwards it to the
  right level
  * Multi-dimensional paging collapses different levels into the page
  tables provided by hardware
  * Multi-level device assignment directly assigns I/O devices to
    different virtual machines
* Each hypervisor layer **emulates** architectural support for
  virtualization, such as VMX, to upper layers
* All nested hypervisors and virtual machines effectively run as
  virtual machines of the lowest-level hypervisor (L0)
* CPU: Nested VMX Virtualization
  * VMCS contains: guest state, host state, control data
  * L0 hypervisor uses VMCS1-0 for running guest VMs on top of L0
  * L1 hypervisor uses VMCS2-1 for running guests VMs on top of L1
    * VMCS2-1 not used directly on hardware
      * Because VMCS2-1 points to page table created by L1 for L2
      * Because host state part of VMCS is for L1
    * VMCS2-0 created by L0 and used on the hardware
      * Includes pointer to page table created by L0 for L2
      * Host state is for L0
    * VMCS2-1 guest state can be directly copied to VMCS2-0
  * Every VMX instruction executed by L1 or L2 will trap to L0
    hypervisor
    * VMEntry by L1 will cause VMExit L1->L0 and then VMEntry L0->L2
  * When an interrupt arrives when running L2, whether it is handled
    purely at L0 or requires forwarding to L1 depends on kind of event
    * If it was part of VMCS2-1, it must be forwarded to L1
    * Else, it is viewed as a "hardware" event, can be handled at L0
* MMU Nested Virtualization
  * Shadow page tables on top of shadow page tables
  * Shadow page tables on top of EPT
    * L0 configures the MMU to use SPT1-2 as the first translation
      table and EPT0-1 as the second translation table.
    * L2 page table modifications must be handled in L1
    * L2 tries to modify page table: L2->L0->L1
    * Shadow on EPT is slower than Shadow because traps for modifying
      page tables are more expensive
  * EPT on top of EPT
    * L2P->L2V done in guest, this is top of EPT
    * Bottom of EPT is new L2V->L0P, this table is constructed on the
      fly
    * L2V->L0P constructed by inspecting L2P->L1P and L1P->L0P
