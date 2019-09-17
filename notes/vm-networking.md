* Review previous class: Shadow Page Tables
* Discuss Memory Virtualization with hardware support: Nested Paging  

* Problem: processing network in a virtualized setting
    * When packet arrives, VM that is currently running gets interrupted
    * Hypervisor determines which VM the packet should go to
    * Target VM may be involved in copying packet over, and immediately processing it if required
    * When this is done, the interrupted VM can run again
    * This drastically reduces performance if a lot of network IO is done
    * Key bottleneck: Hypervisor is involved in deciding where each packet should go
* Lets look at Hardware Support for IO
* Virtual Machine Device Queues (VMDQ)
    * Hardware determines which VM each packet is meant for
    * Places packet on queue for each VM
    * Hypervisor *still involved* in copying over data from each queue into each VM
    * VMDQ removes sorting overhead from hypervisor
* Single Root IO Virtualization (SR-IOV)
    * Introduces "Network Functions" Drivers
    * The hardware resources of the network adaptor (such as memory, registers, and queues) are split up among "network functions"
        * Each network function has *dedicated* access to a set of hardware resources
            * Each network function can then be bound to a specific VM
        * When a packet arrives for a specific VM, the network function of that VM is responsible for processing that packet
            * It can do so without interference from other VMs
    * What happens when there are more virtual machines than virtual network adaptors?
      * Several VMs have to share the same Virtual Function
    * Difference with VMDQ:
        * Hypervisor no longer involved in copying data over to the VM
        * Hypervisor completely removed from the loop, only involved in setup phase
        * VMDQ has different queue for each VM, SR-IOV has different Virtual Function for each VM
* Intel IO Acceleration Technology (IOAT)
    * Suite of hardware features
    * QuickData - Hardware DMA to VMs
    * Direct Cache Access - Access caches directly (unclear whether this is different from DDIO)
    * Extended Message Signaled Interrupts (MSI-X): distribute interrupts among CPUs
    * Tune interrupt arrival times based on content of packets (Fast Packet Introspection)
* Intel DDIO
    * IO directly in and out of the processor last-level cache! 
    * Very exciting for performance
    * Last-level cache on Xeon processor is 20 MB, so a lot of space
* The packet processing game:
    * 10 Gbps delivers 14.8M packets per second (assuming 64 byte packets and 20 byte pre-amble)
    * That gives us 67 ns to process a single packet
    * 67 ns is about 200 cycles on a 3 Ghz processor -- not a lot
    * For comparison: 
        * A cache miss is 32 ns
        * L2 cache access 4 ns
        * L3 cache access 8 ns
        * Atomic lock operation : 8 ns
        * Syscall: 40 ns
        * TLB miss: several cache misses
    * Need to batch and process packets
    * What to avoid:
        * A context switch: > 1000 ns
        * A page fault: > 1000 ns 
* **Data Plane Development Kit (DPDK)**
* Open-source project with contributions from Intel and others
    * C code (GCC 4.5.X or later)
    * Linux kernel 2.6.34 or later
    * With kernel boot option isolcpus
* Set of user-space libraries for fast packet processing
    * Can handle 11x the traffic of the Linux kernel! 
* Lightweight, low level, performance driven framework
* All traffic bypasses the kernel
* Started with Intel x86, now supports other architectures like IBM Power 8
* Poll Mode Driver (PMD) per Hardware NIC
    * Support for RX/TX (Receive and Transmit)
    * Mapping PCI memory
    * Mapping user memory onto NIC
    * Managing hardware support
    * Implemented as a user space pthread
    * PMD drivers are non pre-emptive, not thread-safe
    * Threads communicate using librte_ring: lockless queue
* User space libraries
    * Initialize and use PMD
    * Provide threads (based on pthread)
    * Memory management
        * Used with Huge Pages (2 MB, 1 GB)
    * Hashing, scheduler, pipelining etc
* All resources initialized at the start 
* Implementation Tricks:
    * Don’t use linked lists
    * Use arrays instead
* What does a basic forwarding example do?
    * DPDK Init
    * Get all available nics
    * Initialize packet buffers (create mem pool)
    * Initialize ports
* PMD loop for forwarding:
    * Get burst of packets from first port in port-pair
    * Send packets to second port in port-pair
    * Free unsent packets
    * Do this in a loop
* RTE Ring
    * Fixed sized, "lockless", queue ring
    * Non Preemptive.
    * Supports multiple/single producer/consumer, and bulk actions.
    * Uses:
        * Single array of pointers.
        * Head/tail pointers for both producer and consumer (total 4 pointers).
    * To enqueue (Just like dequeue):
        * Until successful:
            * Save in local variable the current head_ptr.
            * head_next = head_ptr + num_objects
            * CAS the head_ptr to head_next
        * Insert objects.
        * Until successful:
            * Update tail_ptr = head_next + 1 when tail_ptr == head_ptr
    * Analysis:
        * Light weight.
        * In theory, both loops are costly.
        * In practice, as all threads are cpu bound, the amortized cost is low for the first loop, and very unlikely at the second loop.
* RTE Mempool
    * Spread objects across different channels of the DRAM controller (different channels can be concurrently accessed)
    * Maintain a per-core cache, send requests in bulk to mempool ring
* Performance Evaluation:
    * DPDK can forward 22 M pps (L3 forwarding, NIC port to NIC port)
    * DPDK can forward 11 M pps (PHY-OVS-PHY)
    * DPDK can forward 2 M pps (NIC to VM to OVS to VM to NIC)
    * 4X40Gb ports
    * E5-2695 V4 2.1Ghz Processor
    * 16X1GB Huge Pages, 2048X2MB Huge Pages
* **Open vSwitch (OvS)**
    * Software switch used to form network of virtualized machines
    * Ethernet switching done in the hypervisor
    * Critical part of software-defined networking (implements OpenFlow)
    * User-space controller, fast path in kernel
    * DPDK is used to accelerate OvS
    * The first packet of a new flow goes to user-space
        * User space decides on a rule to handle this flow
        * The rule is cached in the kernel
        * Further packets of flow just go through the kernel
    * Database used to persistently store rules (ovsdb-server)
        * Communicates with user space component via RPC
* Reading:
    * [Overview of IO-SRV](https://docs.microsoft.com/en-us/windows-hardware/drivers/network/overview-of-single-root-i-o-virtualization--sr-iov-)
    * 10 min [Video explaining IO-SRV](https://www.intel.com/content/dam/www/program/support/us/en/videos/Intel-SR-IOV-Explanation.mp4)
    * [Introduction to NFV](https://portal.etsi.org/nfv/nfv_white_paper.pdf)
    * [Intel DDIO](https://www-ssl.intel.com/content/www/us/en/io/data-direct-i-o-technology.html)
    * [22 min talk on DDIO](https://linuxplumbers.ubicast.tv/videos/data-direct-io-ddio-advancing-system-io-performance/) 
    * Introduction to DPDK: [https://www.slideshare.net/kerneltlv/introduction-to-dpdk](https://www.slideshare.net/kerneltlv/introduction-to-dpdk) 
    * [http://dpdk.org/doc/guides-16.04/prog_guide/mempool_lib.html](http://dpdk.org/doc/guides-16.04/prog_guide/mempool_lib.html)
    * Understanding the Performance of DPDK as a Computer Architect: [https://www.youtube.com/watch?v=VdskkbCzglE](https://www.youtube.com/watch?v=VdskkbCzglE) 
