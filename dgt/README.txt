To compile the DGT libraries with clock support, execute the below:
g++ dgtnix.c  -w -shared -Wl,-install_name,libdgtnix.so -o libdgtnix.so

After this is done, the library call be called from dgtnix.py and dgtnixTest.py.
The enclosed libdgtnix.so is the Mac OS X shared object binary.

One can then execute python dgtnixTest.py and test output from the board and clock.
