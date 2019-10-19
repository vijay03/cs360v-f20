from gradelib import *

def addlines():
    inputfile = open('GNUmakefile', 'r').readlines()
    write_file = open('GNUmakefile','w')
    found = 0
    for line in inputfile:
        write_file.write(line)
        if 'USER_CFLAGS' in line:
	    if (found == 0):
        	write_file.write("\nifndef GUEST_KERN\nKERN_CFLAGS += -DTEST_EPT_MAP\nUSER_CFLAGS += -DTEST_EPT_MAP\nendif\n") 
		found = 1
    write_file.close()


def dellines():
    inputfile = open('GNUmakefile', 'r').readlines()
    write_file = open('GNUmakefile','w')
    found = 0
    count = 5
    for line in inputfile:
        if(found == 0):
            write_file.write(line)
            if 'USER_CFLAGS' in line:
	        found = 1

	if(found == 1):
	    if(count > 0):
                count = count - 1
            else:
	        found = 0

    write_file.close()


r = Runner(save("jos.out"),
           stop_breakpoint("readline"))

@test(30, "sys_ept_tests")
def sys_ept_map_test():
    addlines()
    r.run_qemu()
    r.match("Cheers! sys_ept_map seems to work correctly")
    dellines()

def matchtest(parent, name, points, *args, **kw):
    def do_test():
        r.match(*args, **kw)
    test(points, name, parent=parent)(do_test)

@test(0, "VMM Tests")
def test_vm():
    r.user_test("vmm")
matchtest(test_vm,"start vmxon:", 10, "VMXON")

matchtest(test_vm, "VMX extension test:", 20, "VMX extension hidden from guest")

matchtest(test_vm, "Print message in VM:", 30, "What is the tortoise")

matchtest(test_vm, "VM correctly started:", 10, "vm\$")

run_tests()
