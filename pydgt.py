import serial
import sys
import time
from threading import Thread
from threading import RLock
from struct import unpack

BOARD = "Board"

FEN = "FEN"

DGTNIX_MSG_UPDATE = 0x05
_DGTNIX_SEND_BRD = 0x42
_DGTNIX_MESSAGE_BIT = 0x80
_DGTNIX_BOARD_DUMP =  0x06
_DGTNIX_BWTIME = 0x0d

_DGTNIX_MSG_BOARD_DUMP = _DGTNIX_MESSAGE_BIT|_DGTNIX_BOARD_DUMP

_DGTNIX_SEND_UPDATE_NICE = 0x4b

# message emitted when a piece is added onto the board
DGTNIX_MSG_MV_ADD = 0x00
#message emitted when a piece is removed from the board
DGTNIX_MSG_MV_REMOVE = 0x01

DGT_SIZE_FIELD_UPDATE = 5
_DGTNIX_FIELD_UPDATE =   0x0e
_DGTNIX_EMPTY = 0x00
_DGTNIX_WPAWN = 0x01
_DGTNIX_WROOK = 0x02
_DGTNIX_WKNIGHT = 0x03
_DGTNIX_WBISHOP = 0x04
_DGTNIX_WKING = 0x05
_DGTNIX_WQUEEN = 0x06
_DGTNIX_BPAWN =      0x07
_DGTNIX_BROOK  =     0x08
_DGTNIX_BKNIGHT =    0x09
_DGTNIX_BBISHOP =    0x0a
_DGTNIX_BKING   =    0x0b
_DGTNIX_BQUEEN  =    0x0c

_DGTNIX_CLOCK_MESSAGE = 0x2b
_DGTNIX_SEND_CLK = 0x41
_DGTNIX_SEND_UPDATE = 0x43
_DGTNIX_SEND_UPDATE_BRD = 0x44
_DGTNIX_SEND_SERIALNR = 0x45
_DGTNIX_SEND_BUSADDRESS = 0x46
_DGTNIX_SEND_TRADEMARK = 0x47
_DGTNIX_SEND_VERSION = 0x4d
_DGTNIX_SEND_EE_MOVES = 0x49
_DGTNIX_SEND_RESET = 0x40

_DGTNIX_SIZE_BOARD_DUMP = 67
_DGTNIX_NONE = 0x00
_DGTNIX_BOARD_DUMP = 0x06
_DGTNIX_EE_MOVES = 0x0f
_DGTNIX_BUSADDRESS = 0x10
_DGTNIX_SERIALNR = 0x11
_DGTNIX_TRADEMARK = 0x12
_DGTNIX_VERSION = 0x13

DGTNIX_RIGHT_DOT = 0x01
DGTNIX_RIGHT_SEMICOLON = 0x02
DGTNIX_RIGHT_1 = 0x04
DGTNIX_LEFT_DOT = 0x08
DGTNIX_LEFT_SEMICOLON = 0x10
DGTNIX_LEFT_1 = 0x20

piece_map = {
    _DGTNIX_EMPTY : ' ',
    _DGTNIX_WPAWN : 'P',
    _DGTNIX_WROOK : 'R',
    _DGTNIX_WKNIGHT : 'N',
    _DGTNIX_WBISHOP : 'B',
    _DGTNIX_WKING : 'K',
    _DGTNIX_WQUEEN : 'Q',
    _DGTNIX_BPAWN : 'p',
    _DGTNIX_BROOK : 'r',
    _DGTNIX_BKNIGHT : 'n',
    _DGTNIX_BBISHOP : 'b',
    _DGTNIX_BKING : 'k',
    _DGTNIX_BQUEEN : 'q'
}

dgt_send_message_list = [_DGTNIX_CLOCK_MESSAGE, _DGTNIX_SEND_CLK, _DGTNIX_SEND_BRD, _DGTNIX_SEND_UPDATE,
                         _DGTNIX_SEND_UPDATE_BRD, _DGTNIX_SEND_SERIALNR, _DGTNIX_SEND_BUSADDRESS, _DGTNIX_SEND_TRADEMARK,
                         _DGTNIX_SEND_VERSION, _DGTNIX_SEND_UPDATE_NICE, _DGTNIX_SEND_EE_MOVES, _DGTNIX_SEND_RESET]

class Event(object):
    pass



class DGTBoard(object):
    def __init__(self, device, virtual = False, send_board = True):
        self.board_reversed = False
        self.clock_ack_recv = False
        self.dgt_clock_lock = RLock()

        if not virtual:
            self.ser = serial.Serial(device,stopbits=serial.STOPBITS_ONE)
            self.write(chr(_DGTNIX_SEND_UPDATE_NICE))
            if send_board:
                self.write(chr(_DGTNIX_SEND_BRD))

        self.callbacks = []

    def subscribe(self, callback):
        self.callbacks.append(callback)

    def fire(self, **attrs):
        e = Event()
        e.source = self
        for k, v in attrs.iteritems():
            setattr(e, k, v)
        for fn in self.callbacks:
            fn(e)

    def convertInternalPieceToExternal(self, c):
        if piece_map.has_key(c):
            return piece_map[c]

    def sendMessageToBoard(self, i):
        if i in dgt_send_message_list:
            self.write(i)
        else:
            raise "Critical, cannot send - Unknown command: {0}".format(unichr(i))

    def dump_board(self, board):
        pattern = '>'+'B'*len(board)
        buf = unpack(pattern, board)

        if self.board_reversed:
            buf = buf[::-1]

        output = "__"*8+"\n"
        for square in xrange(0,len(board)):
            if square and square%8 == 0:
                output+= "|\n"
                output += "__"*8+"\n"

            output+= "|"
            output+= self.convertInternalPieceToExternal(buf[square])
        output+= "|\n"
        output+= "__"*8
        return output

    # Two reverse calls will bring back board to original orientation
    def reverse_board(self):
        print "Reversing board!"
        self.board_reversed = not self.board_reversed

    def extract_base_fen(self, board):
        FEN = []
        empty = 0
        for sq in range(0, 64):
            if board[sq] != 0:
                if empty > 0:
                    FEN.append(str(empty))
                    empty = 0
                FEN.append(self.convertInternalPieceToExternal(board[sq]))
            else:
                empty += 1
            if (sq + 1) % 8 == 0:
                if empty > 0:
                    FEN.append(str(empty))
                    empty = 0
                if sq < 63:
                    FEN.append("/")
                empty = 0

        return FEN

    def get_fen(self, board, tomove='w'):
        pattern = '>'+'B'*len(board)
        board = unpack(pattern, board)

        if self.board_reversed:
            board = board[::-1]

        FEN = self.extract_base_fen(board)# Check if board needs to be reversed
        if ''.join(FEN) == "RNBKQBNR/PPPPPPPP/8/8/8/8/pppppppp/rnbkqbnr":
            self.reverse_board()
            board = board[::-1]
            # Redo FEN generation - should be a fast operation
            FEN = self.extract_base_fen(board)# Check if board needs to be reversed

        FEN.append(' ')

        FEN.append(tomove)

        FEN.append(' ')
#         possible castlings
        FEN.append('K')
        FEN.append('Q')
        FEN.append('k')
        FEN.append('q')
        FEN.append(' ')
        FEN.append('-')
        FEN.append(' ')
        FEN.append('0')
        FEN.append(' ')
        FEN.append('1')
        FEN.append('0')

        return ''.join(FEN)

    def read(self, message_length):
        return self.ser.read(message_length)

    def write(self, message):
        self.ser.write(message)

    # Converts a lowercase ASCII character or digit to DGT Clock representation
    @staticmethod
    def char_to_lcd_code(c):
        if c == '0':
            return 0x01 | 0x02 | 0x20 | 0x08 | 0x04 | 0x10
        if c == '1':
            return 0x02 | 0x04
        if c == '2':
            return 0x01 | 0x40 | 0x08 | 0x02 | 0x10
        if c == '3':
            return 0x01 | 0x40 | 0x08 | 0x02 | 0x04
        if c == '4':
            return 0x20 | 0x04 | 0x40 | 0x02
        if c == '5':
            return 0x01 | 0x40 | 0x08 | 0x20 | 0x04
        if c == '6':
            return 0x01 | 0x40 | 0x08 | 0x20 | 0x04 | 0x10
        if c == '7':
            return 0x02 | 0x04 | 0x01
        if c == '8':
            return 0x01 | 0x02 | 0x20 | 0x40 | 0x04 | 0x10 | 0x08
        if c == '9':
            return 0x01 | 0x40 | 0x08 | 0x02 | 0x04 | 0x20
        if c == 'a':
            return 0x01 | 0x02 | 0x20 | 0x40 | 0x04 | 0x10
        if c == 'b':
            return 0x20 | 0x04 | 0x40 | 0x08 | 0x10
        if c == 'c':
            return 0x01 | 0x20 | 0x10 | 0x08
        if c == 'd':
            return 0x10 | 0x40 | 0x08 | 0x02 | 0x04
        if c == 'e':
            return 0x01 | 0x40 | 0x08 | 0x20 | 0x10
        if c == 'f':
            return 0x01 | 0x40 | 0x20 | 0x10
        if c == 'g':
            return 0x01 | 0x20 | 0x10 | 0x08 | 0x04
        if c == 'h':
            return 0x20 | 0x10 | 0x04 | 0x40
        if c == 'i':
            return 0x02 | 0x04
        if c == 'j':
            return 0x02 | 0x04 | 0x08 | 0x10
        if c == 'k':
            return 0x01 | 0x20 | 0x40 | 0x04 | 0x10
        if c == 'l':
            return 0x20 | 0x10 | 0x08
        if c == 'm':
            return 0x01 | 0x40 | 0x04 | 0x10
        if c == 'n':
            return 0x40 | 0x04 | 0x10
        if c == 'o':
            return 0x40 | 0x04 | 0x10 | 0x08
        if c == 'p':
            return 0x01 | 0x40 | 0x20 | 0x10 | 0x02
        if c == 'q':
            return 0x01 | 0x40 | 0x20 | 0x04 | 0x02
        if c == 'r':
            return 0x40 | 0x10
        if c == 's':
            return 0x01 | 0x40 | 0x08 | 0x20 | 0x04
        if c == 't':
            return 0x20 | 0x10 | 0x08 | 0x40
        if c == 'u':
            return 0x08 | 0x02 | 0x20 | 0x04 | 0x10
        if c == 'v':
            return 0x08 | 0x02 | 0x20
        if c == 'w':
            return 0x40 | 0x08 | 0x20 | 0x02
        if c == 'x':
            return 0x20 | 0x10 | 0x04 | 0x40 | 0x02
        if c == 'y':
            return 0x20 | 0x08 | 0x04 | 0x40 | 0x02
        if c == 'z':
            return 0x01 | 0x40 | 0x08 | 0x02 | 0x10
        return 0

    def send_message_to_clock(self, message, beep, dots):
        # Todo locking?
        with self.dgt_clock_lock:
            self._sendMessageToClock(self.char_to_lcd_code(message[0]), self.char_to_lcd_code(message[1]),
                                self.char_to_lcd_code(message[2]), self.char_to_lcd_code(message[3]),
                                self.char_to_lcd_code(message[4]), self.char_to_lcd_code(message[5]),
                                beep, dots)



    def _sendMessageToClock(self, a, b, c, d, e, f, beep, dots):
        # pthread_mutex_lock (&clock_ack_mutex);

        # if(!(g_debugMode == DGTNIX_DEBUG_OFF))
        #   {
        #     _debug("Sending message to clock\n");
        #     if(g_descriptorDriverBoard < 0)
        #       {
        #         perror("dgtnix critical:sendMessageToBoard: invalid file descriptor\n");
        #         exit(-1);
        #       }
        #   }
        print "Sending Message to Clock.."
        num_tries = 0
        # while not self.clock_ack_recv:
        num_tries +=1
        self.ser.write(chr(_DGTNIX_CLOCK_MESSAGE))
        self.ser.write(chr(0x0b))
        self.ser.write(chr(0x03))
        self.ser.write(chr(0x01))
        self.ser.write(chr(c))
        self.ser.write(chr(b))
        self.ser.write(chr(a))
        self.ser.write(chr(f))
        self.ser.write(chr(e))
        self.ser.write(chr(d))

        if dots:
            self.ser.write(chr(dots))
        else:
            self.ser.write(chr(0))
        if beep:
          self.ser.write(chr(0x03))
        else:
          self.ser.write(chr(0x01))
        self.ser.write(chr(0x00))
        # time.sleep(1)
        self.read_message_from_board()
            # if num_tries>1:
            #     print "try : {0}".format(num_tries)
            # if num_tries>=5:
            #     break
        # self.clock_ack_recv = False
        # Retry logic?
        # time.sleep(1)
        # Check clock ack?


    def read_message_from_board(self, head=None):
        # print "got message"
        header_len = 3
        if head:
            header = head + self.read(header_len-1)
        else:
            header = self.read(header_len)
        if not header:
            # raise
            raise Exception("Invalid First char in message")
        pattern = '>'+'B'*header_len
        buf = unpack(pattern, header)
#        print buf
#        print buf[0] & 128
#        if not buf[0] & 128:
#            raise Exception("Invalid message -2- readMessageFromBoard")
        command_id = buf[0] & 127
        print "command_id: {0}".format(command_id)
#
#        if buf[1] & 128:
#            raise Exception ("Invalid message -4- readMessageFromBoard")
#
#        if buf[2] & 128:
#            raise Exception ("Invalid message -6- readMessageFromBoard")

        message_length = (buf[1] << 7) + buf[2]
        message_length-=3

#        if command_id == _DGTNIX_NONE:
#            print "Received _DGTNIX_NONE from the board\n"
#            message = self.ser.read(message_length)

        if command_id == _DGTNIX_BOARD_DUMP:
            print "Received DGTNIX_DUMP message\n"
            message = self.read(message_length)
#            self.dump_board(message)
#            print self.get_fen(message)
            self.fire(type=FEN, message=self.get_fen(message))
            self.fire(type=BOARD, message=self.dump_board(message))

        elif command_id == _DGTNIX_BWTIME:
            print "Received DGTNIX_BWTIME message from the board\n"
            message = self.read(message_length)

            pattern = '>'+'B'*message_length
            buf = unpack(pattern, message)

            if buf:
                if buf[3] & 15==10 or buf[6] & 15 == 10:
                    self.clock_ack_recv = True
                    # print "clock ACK received!"

        elif command_id == _DGTNIX_EE_MOVES:
            print "Received _DGTNIX_EE_MOVES from the board\n"

        elif command_id == _DGTNIX_BUSADDRESS:
            print "Received _DGTNIX_BUSADDRESS from the board\n"

        elif command_id == _DGTNIX_SERIALNR:
            print "Received _DGTNIX_SERIALNR from the board\n"
            message = self.read(message_length)

        elif command_id == _DGTNIX_TRADEMARK:
            print "Received _DGTNIX_TRADEMARK from the board\n"
            message = self.read(message_length)

        elif command_id == _DGTNIX_VERSION:
            print "Received _DGTNIX_VERSION from the board\n"

        elif command_id == _DGTNIX_FIELD_UPDATE:
            print "Received _DGTNIX_FIELD_UPDATE from the board"
            print "message_length : {0}".format(message_length)

            if message_length == 2:
                message = self.read(message_length)
                self.write(chr(_DGTNIX_SEND_BRD))
            else:
                message = self.read(4)

#            pattern = '>'+'B'*message_length
#            buf = unpack(pattern, message)
#            print buf[0]
#            print buf[1]

        else:
            # Not a regular command id
            # Piece remove/add codes?

#            header = header + self.ser.read(1)
#            print "message_length : {0}".format(len(header))
#            print [header]
            #message[0] = code;
            #message[1] = intern_column;
            #message[2] = intern_line;
            #message[3] = piece;

#            print "diff command : {0}".format(command_id)

            if command_id == DGTNIX_MSG_MV_ADD:
                print "Add piece message"
#                board.ser.write(chr(_DGTNIX_SEND_BRD))

            elif command_id == DGTNIX_MSG_UPDATE:
                print "Update piece message"
#                board.ser.write(chr(_DGTNIX_SEND_BRD))

    # Warning, this method must be in a thread
    def poll(self):
        while True:
            c = self.read(1)
            # print "got msg"
            if c:
                self.read_message_from_board(head=c)

    def _dgt_observer(self, attrs):
        if attrs.type == FEN:
            print "FEN: {0}".format(attrs.message)
        elif attrs.type == BOARD:
            print "Board: "
            print attrs.message
            # self.send_message_to_clock(['c','h','a','n','g','e'], False, False)
            # time.sleep(1)
            # self.send_message_to_clock(['b','o','a','r','d','c'], False, False)


class VirtualDGTBoard(DGTBoard):
    def __init__(self, device, virtual = True):
        super(VirtualDGTBoard, self).__init__(device, virtual = virtual)
        self.fen = None
        self.callbacks = []

    def read(self, bits):
        if self.fen:
            return True

    def read_message_from_board(self, head = None):
        fen = self.fen
        self.fen = None
        return self.fire(type=FEN, message = fen)

    def write(self, message):
        if message == chr(_DGTNIX_SEND_UPDATE_NICE):
            print "Got Update Nice"
        elif message == chr(_DGTNIX_SEND_BRD):
            print "Got Send board"

    def set_fen(self, fen):
        self.fen = fen


def poll_dgt(dgt):
    thread = Thread(target=dgt.poll)
    thread.start()

if __name__ == "__main__":
    if len(sys.argv)> 1:
        device = sys.argv[1]
    else:
        device = "/dev/cu.usbserial-00001004"
    board = DGTBoard(device, send_board=False)
    board.subscribe(board._dgt_observer)
    # poll_dgt(board)
    # board.send_message_to_clock(['a','y',' ','d','g', 't'], False, False)
    board.poll()
    # poll_dgt(board)




