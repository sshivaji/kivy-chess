from ctypes import cdll,c_long
lib = cdll.LoadLibrary('./agchess.so')
#lib.test_c_position()
#lib.get_start_pos.restype=c_long
#p = lib.get_start_pos()
lib.get_board()
lib.reset_current_pos()
lib.get_board()
