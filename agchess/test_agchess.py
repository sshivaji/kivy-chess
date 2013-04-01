from ctypes import cdll
lib = cdll.LoadLibrary('./agchess.so')
lib.test_c_position()
