## Handling VM exits - part 2

Recall that JOS uses three hypercall (vmcall) instructions, the first one of which we handled in lab-3. In this lab, we will handle the other two hypercalls, which are related to host-level IPC. JOS has a user-level file system server daemon, similar to a microkernel. We place the guest's disk image as a file on the host file system server. When the guest file system daemon requests disk reads, rather than issuing ide-level commands, we will instead use vmcalls to ask the host file system daemon for regions of the disk image file. This is depicted in the image below.
![alt text](http://www.cs.utexas.edu/~vijay/cs378-f17/projects/disk-architecture.jpg)

You need to modify the `bc_pgfault()` amd `flush_block()` in fs/bc.c to issue I/O requests using the `host_read()` and `host_write()` hypercalls. Use the macro VMM_GUEST to select different behavior for the guest and host OS. You will also have to implement the IPC send and receive hypercalls in `handle_vmcall()`, as well as the client code to issue `ipc_host_send()` and `ipc_host_recv()` vmcalls in lib/ipc.c.

Finally, you will need to extend the `sys_ipc_try_send()` to detect whether the environment is of type `ENV_TYPE_GUEST` or not, and you also need to implement the `ept_page_insert()` function.

The workflow (and hints) for the ipc_* functions is as follows:
1. `ipc_host_send()` checks whether pg is NULL. If it is, it sets the pg to UTOP. Then this function gets the gpa corresponding to pg and does a vmcall to VMX_VMCALL_IPCSEND by setting the corresponding registers in the guest.
2. `ipc_host_recv()` also checks whether pg is NULL. If it is, it sets the pg to UTOP. Then it allocates a page at pg and does a vmcall to VMX_VMCALL_IPCRECV with corresponding registers set at the guest.
3. `handle_vmcall(): VMX_VMCALL_IPCSEND` loads the values from the trapframe registers. Then it ensures that the destination environment is HOST FS. If the destination environment is not HOST FS, then this function returns E_INVAL. Now, this function traverses all the environments, and sets the `to_env` to the environment ID corresponding to ENV_TYPE_FS at the host. After this is done, it converts the gpa to hva and then calls `sys_ipc_try_send()`
4. `handle_vmcall(): VMX_VMCALL_IPCRECV` just calls `sys_ipc_recv()`, after incrementing the program counter.
5. `sys_ipc_try_send()` checks whether the guest is sending a message to the host or whether the host is sending a message to the guest. If the curenv type is GUEST and the destination va is below UTOP, it means that the guest is sending a message to the host and it should insert a page in the host's page table. If the dest environment is GUEST and the source va is below UTOP, it means that the host is sending a message to the guest and it should insert a page in the EPT. Finally, at the end of this function, if the dest environment is GUEST, then the rsi register of the trapframe should be set with 'value'.
6. `ept_page_insert()` uses `ept_lookup_gpa` to traverse the EPT and insert a page if not present.

Once these steps are complete, you should have a fully running JOS-on-JOS.
This marks the end of project-1.



### Submission and Deadline

Please submit your code via gitolite. To mark your submission, please have a commit labelled "Lab 4 submission. 0/1/.. slip days used.". You can modify and add a dummy file for this commit if you want. We will consider the last such commit for evaluation. The deadline for lab-4 of project-1 is:

```diff
+ November 9th, 11:59 PM CST
```
