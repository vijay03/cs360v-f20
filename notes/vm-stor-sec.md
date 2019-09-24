## Virtualizing Storage
* Simplest approach: let VM take a single device or a partition
  * Wastes resources if VMs don’t fully utilize their partitions
* Storage is virtualized by emulating multiple logical devices from a
single physical device
    * For example, a VMDK (Virtual Machine Disk) file represents a virtual
disk as seen by the VM
* Operations on the VMDK are translated into operations on the
underlying storage device
* The stack:
  * File system inside VM (ext4 on virtual disk)
  * Virtual Disk inside VM
  * File system on host (the VMDK file sits on this file system)
  * Physical storage device on host
* Benefits
    * You can overprovision your virtual disks. You can provide 5 1 TB
virtual disks on top of a single 1 TB storage device. This works as
long as the VMs don’t fully utilize their space. 
    * The VMDK starts out
completely un-allocated. 
    * As the VM writes to a disk block, it becomes
allocated on host storage device.
    * You can snapshot a virtual disk simply by copying the VMDK file
    * You can do de-duplication among multiple VMDKs since they are just
files on the host
* All these layers introduce a number of performance problems
  * Example: double journaling. Journaling inside the VM, and on the VMDK
file on the host
    * If you are updating an inode in the guest file system, it is journaled
(2X IO)
    * If the host file system also uses journaling, the metadata of VMDK is
also journaled (3X IO)
* File systems make assumptions about the storage device
  * If not true, optimizations actually reduce performance
* The combination of the file system on the guest and the file system on
the host is really important
    * The wrong combination can reduce throughput to 67% of max (reiserfs on
ext2)
    * When ext2 runs on top of ext3, throughput reduced by 10%
    * When ext3 runs on top of ext3, throughput reduced by 40%
    * For read only workloads, stacking file systems actually helps
      * Why? Read-ahead issued by the host file system 
* Ideally, host should not have smarts: use act as a simple on-demand
allocator for guest file system

## Security in Virtual Machines
* Security depends upon a number of manual actions such as patching a machine
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
* Great paper on cloud security: [Hey, You, Get Off my Cloud](https://css.csail.mit.edu/6.858/2011/readings/get-off-my-cloud.pdf)
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
* [Performance of Virtualized Storage](http://static.usenix.org/events/fast/tech/full_papers/Le.pdf)
* [Hey, You, Get Off my Cloud](https://css.csail.mit.edu/6.858/2011/readings/get-off-my-cloud.pdf)
