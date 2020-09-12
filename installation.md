## Installing Dependencies

If you are working on your personal machine with Ubuntu 16.04.6 LTS (instead of inside a VM):

Before compiling and running the jos-vmm code, you will need to install Python3.4, gcc-4.8, and the patched gdb_7.7. Please install gcc-4.8 and follow the instructions below to install Python3.4 and gdb7.7

Download and install python3.4 as given below:

```
$ wget https://www.python.org/ftp/python/3.4.5/Python-3.4.5rc1.tar.xz
$ tar xf Python-3.4.5rc1.tar.xz
$ cd Python-3.4.5rc1
$ ./configure --prefix=$HOME/python3.4 --enable-shared --with-threads
$ make
$ make install
```

The standard version of gdb does not correctly handle the transition to long mode during JOS boot, yielding a "Packet too long" error. For debugging 64-bit code on a 32-bit platform, you need both gdb and gdb-multiarch. Below we post patched Ubuntu package [gdb_7.7.1](http://www.cs.utexas.edu/~vijay/cs378-f17/projects/gdb_7.7.1-0ubuntu5~14.04.2_amd64.deb)

If you are using personal machines or running inside the VM, install gdb using following command:
```
$ sudo dpkg -i gdb_7.7.1-0ubuntu5_14.04.2_amd64.deb
```

If you are using the gilligan lab machines, install gdb using following command:
```
$ dpkg -x gdb_7.7.1-0ubuntu5_14.04.2_amd64.deb $HOME/gdb_7.7
GDB executable can be found at $HOME/gdb_7.7/usr/bin
```

After installing python3.4 and gdb7.7, open $HOME/.bashrc and add the following lines.
```
export LD_LIBRARY_PATH=/stage/public/ubuntu64/lib:$HOME/python3.4/lib
export PATH=$HOME/gdb7.7/usr/bin:$PATH
```

Finally, open (create if doesn't exist) $HOME/.gdbinit and add the following line:
```
set auto-load safe-path /
```
