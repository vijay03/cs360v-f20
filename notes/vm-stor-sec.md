## Virtualizing Storage



## Security in Virtual Machines
*Security depends upon a number of manual actions such as patching a machine
    * Hard to do in VMs because of how many VMs there might be in an
      organization, and how easy it is to spin up new VMs
    * Hard to understand state of the network
    * VMs appearing and disappearing all the time
    * You might think you have fixed all machines, but a vulnerable VM
      could simply be suspended
* What happens if you checkpoint VM and roll
back to an earlier state?  
    * The older state may not have security patches applied 
    * Random number generation in VMs may not be “fresh” 
    * Arbitrary time between generation and use 
    * Random numbers should be obtained from VMM instead of VM 
* Diversity: a number of VMs may have OSes at different update
points 
    * This is hard for admin, who usually try to keep all machines
    updated and patched to the same point
* Identity: typically a real machine is identified by its MAC address 
  * What to do for VMs?
* In a non-virtualized setting, OS trusts the hardware 
* In virtualized settings, VMs trust the VMM. However, is the VMM as
  trust-worthy as the hardware?
* Solution: Trusted Platform Module 
  * Can attest to integrity of software components 
  * Outside the CPU
  * VMs introduce “introspection” capabilities, the ability to monitor
    at a fine-grained level what is going on inside the VM
* Time-based limited trials can be broken 
* Encryption keys in software can be read 
* Attack: VMM Rootkits. 
   *  Transparently inserting a VMM under and OS
   *  Example from [survey paper](http://dforeman.homedns.org/~dj/550pages/Readings/garfinkle05when.pdf)
   *   “Consider this example: Company A has a virtual
server in an outsourced datacenter that undertakes financial
transactions. Depending upon the contract with the data- center, it is
likely that the datacenter does not have permission to view or alter
any transactions undertaken (based on least need-to-know
principles). However, because Company A does not control the
underlying VMM, it has no way to ensure that the VMM has not altered
transaction details or recorded credentials, a potential problem in
many ways, as any local audit trails can be similarly compromised."
* Ristenpart’s great paper: [Hey, You, Get Off my Cloud](https://css.csail.mit.edu/6.858/2011/readings/get-off-my-cloud.pdf)
* “Using the Amazon EC2 service as a case study, we show that it is
possible to map the internal cloud infrastructure, identify where a
particular target VM is likely to reside, and then instantiate new VMs
until one is placed co-resident with the target. We explore how such
placement can then be used to mount cross-VM side-channel attacks to
extract information from a target VM on the same machine.”  Can one
determine where in the cloud infrastructure an instance is located?
(Section 5)
* Can one easily determine if two instances are co-resident on the same
 physical machine? (Section 6) 
* Can an adversary launch instances that will be co-resident with other
 user’s instances? (Section 7) 
* Can an adversary exploit cross-VM information leakage once
 co-resident? (Section 8) 
* Answer to all the above questions is yes!

## Reading
