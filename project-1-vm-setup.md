### Setting up a Virtual Machine for Project-1

A Virtual Machine has been setup for this project. The image file can be downloaded [here](https://drive.google.com/open?id=1TOwha-yAAYJLpqV_-RKEwDd1CV2uGthR).

#### Steps to setup the VM:
1. Download the image file on the CS gilligan machines or your personal laptops (which have QEMU and KVM enabled).
2. On one terminal, run the following command:
```
$ qemu-system-x86_64 -drive file=<path-to-qcow2-image>,format=qcow2 -m 512 -net user,hostfwd=tcp::<port-id>-:22 -net nic -nographic -enable-kvm
```
where `<port-id> = 5900 + <group-id>`. For example, if your group-id is 15, your port-id will be 5915.
This command will start up the VM, which will listen on the port that you have entered.
3. On another terminal, connect to the VM using the following command:
```
$ ssh -p <port-id> cs378@localhost
```
This command will let you connect to the VM.
4. On connecting, enter the password as `abc123`.
5. Copy your public *and* private ssh keys from the CS lab machine or from your local machine (`$HOME/.ssh/id_rsa` and `$HOME/.ssh/id_rsa.pub`) into the VM in the location `$HOME/.ssh/id_rsa` and `$HOME/.ssh/id_rsa.pub` respectively. (Use scp command with port-id as the -P option for copying the keys to the VM).
Alternatively, you can generate a new key-pair on the VM (using `ssh-keygen -t rsa`) and send me the public key along with your group name, and I will add the key to your group repository.
6. Now you can clone the repository (`git clone cs378-vijay@git.cs.utexas.edu:<group-name>-project1`) and run the project like you do on the lab machines or your personal machines. (`sudo make run-vmm-nox`)

Send an e-mail to `rak@cs.utexas.edu` in case of any difficulties.
