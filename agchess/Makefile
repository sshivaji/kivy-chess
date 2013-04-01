# Makefile and source taken from libagchess.
# This only works on Mac OS X.
# On linux, need to change -install_name to -soname. TODO: Support this Makefile on multiple platforms
# 
# Instructins:
# 1. Execute "make"
# 2. Execute "python test_agchess.py" to test the python to C to C++ bridge!
agchess : 
			g++ -c -fPIC wrapper.cpp -o wrapper.o
			g++ libagchess/*.cpp -w -shared -Wl,-install_name,agchess.so -o agchess.so wrapper.o
			
clean :
	rm -f *.o
	rm -rf *.so
