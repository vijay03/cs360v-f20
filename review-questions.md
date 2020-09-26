To help you review the material we have covered so far, here are some questions you should
be able to answer. If you are unsure about any of the questions, come
talk to me during office hours. 

## Questions

* What is the difference between para-virtualization and full-hosted
  virtualization?
* What hardware support does Intel provide for CPU virtualization?
* What hardware support does Intel provide for memory virtualization?
* Does EPT use less memory for page tables than shadow page tables?
  Why or why not?
* If you have ten virtual machines each running 20 processes on a
  single physical machine (assume the host is not running any other
  application), how many page tables total are allocated in memory?
* What is the main weakness of paravirtualization? Why is it not
  employed widely today?
* When you have nested virtualization, when the L2 VM generates a
  trap, who handles it: L1 or L0? Why?
* Lets assume L1 is employing shadow page tables to virtualize L2
  memory, and L0 is employing EPT to virtualize L1 memory. What does
  CR3 point to? What are the two page tables pointed to by the
  hardware EPT?
* When using shadow page tables, if the virtual machine is executing
  10 applications, and the host OS is executing 20 applications, how
  many page tables in total are allocated in memory at this point?
* Why was the x86 instruction set considered not virtualizable?
  Explain with an example.
* What is be a scenario where para-virtualization is preferrable to hardware-assisted virtualization?
* Why are para-virtualized device drivers split into front-end and back-end? What does this achieve?
* How is memory virtualized in Xen? Is this faster than memory virtualization with EPT? 
* Given that binary translation is done on the fly, why is this approach effective for full-machine virtualization? Why isn't the overhead prohibitive?
