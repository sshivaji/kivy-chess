import os
import signal
import sys
import subprocess
from threading import Thread
import select

try:
    from Queue import Queue, Empty
except ImportError:
    from queue import Queue, Empty  # python 3.x

ON_POSIX = 'posix' in sys.builtin_module_names

LOG_DIR = "logs"

class UCIOption:
    def __init__(self, name, value):
        self.name = name
        self.value = value


class UCIEngine:
    def __init__(self):
        """Constructor for an AI player.

        'name' is the name of the player (string).
        'profile' is the profile to use for the AI (Profile).
        'level' is the difficulty level to use (string).
        """

        self.__positionCommand = 'position startpos'
        self.__haveMoves = False


        self.readyToConfigure = False
        self.__options          = None

        self.ready            = False
        self.__inCallback       = False
        self.eng_process = None


        self.STATE_IDLE = 'IDLE'
        self.STATE_CONNECTING = 'CONNECTING'

        self.options = {}
        self.__queuedCommands = []
        self.eng_process = None
        try:
            self.eng_process = subprocess.Popen("engines/stockfish4-mac-64", stdout=subprocess.PIPE, stdin=subprocess.PIPE, bufsize=0)
            self.buffer = Queue()
            t = Thread(target=self.enqueue_output, args=(self.eng_process, self.buffer))
            t.daemon = True # thread dies with the program
            t.start()

        except OSError:
            print "OS error in starting engine"

    def enqueue_output(self, p, queue):
        out = p.stdout
        while True:
            queue.put(out.readline())

    def logText(self, text, style):
        """
        """
        pass

    def onOutgoingData(self, data):
        """
        """
        self.eng_process.stdin.write(data)

#        pass

    def onMove(self, move):
        """Called when the AI makes a move.

        'move' is the move the AI has decided to make (string).
        """
        print 'UCI move: ' + move

    def registerIncomingData(self):
        """
        """
        self.__inCallback = True
        buffer = ''
        try:
            line = self.buffer.get(timeout=0.3) # or q.get(timeout=.1)
        except Empty:
            pass
        else: # got line
            buffer = line
        while True:
            index = buffer.find('\n')
            if index < 0:
                break
            line = buffer[:index]
            buffer = buffer[index + 1:]
            self.parseLine(line)
        self.__inCallback = False

        if self.__options is not None and self.readyToConfigure:
            options = self.__options
            self.__options = None
            self.configure(options)

        # Send queued commands once have OK
        if len(self.__queuedCommands) > 0 and self.ready:
            commands = self.__queuedCommands
            self.__queuedCommands = []
            for c in commands:
                self.__sendCommand(c)

    def __sendCommand(self, command):
        """
        """
        if self.ready and not self.__inCallback:
            self.onOutgoingData(command + '\n')
        else:
            self.__queuedCommands.append(command)
            # print "Sending: %s"%command

    def start(self):
        """
        """
        self.onOutgoingData('uci\n')

    def stop(self):
        self.onOutgoingData('stop\n')

    def startGame(self):
        """
        """
        self.__sendCommand('ucinewgame')
        self.__sendCommand(self.__positionCommand)

    def configure(self, options):
        """ Options should be a dictionary
        """
        if not self.readyToConfigure:
            self.__options = options
            return

        for k,v in options.iteritems():
            # if not hasattr(option, 'name'):
            #     print 'Ignoring unnamed UCI option'
            #     continue
            # if option.value == '':
            #     continue
            self.onOutgoingData('setoption name ' + k + ' value ' + v + '\n')
        self.onOutgoingData('isready\n')

    def requestAnalysis(self, whiteTime=30000, blackTime=30000):
        """
        """
        # Some AI's don't work unless assigned some time
        # TODO: which ones? I think Glaurung had issues

#        self.__sendCommand('go wtime %d btime %d' % (whiteTime, blackTime))
        self.__sendCommand('go infinite')

    def requestMove(self, movetime=None, wtime=30000, btime=30000, winc=None, binc=None):
        """
        """
        if movetime:
            self.__sendCommand('go movetime %s'%movetime)
        else:
            self.__sendCommand('go wtime {0} btime {1} winc {2} binc {3}'.format(wtime*1000, btime*1000, winc*1000, binc*1000))

    def sendFen(self, fen):
        self.__positionCommand = "position fen "+fen
        self.__haveMoves = False
        # print "position command:"+self.__positionCommand
        self.__sendCommand(self.__positionCommand)

    def reportMoves(self, moves):
        if not self.__haveMoves:
            self.__positionCommand += ' moves'
        self.__haveMoves = True

        if moves:
#            print type(moves)
            if type(moves) is list:
                moves = " ".join(moves)
#            str_move_list = " ".join(moves)
#             print "debug command: %s %s"%(self.__positionCommand, moves)
            self.__sendCommand("%s %s"%(self.__positionCommand, moves))

    def reportMove(self, move):
        """
        """
        if not self.__haveMoves:
            self.__positionCommand += ' moves'
        self.__haveMoves = True
        if move:
            self.__positionCommand += ' ' + move
#            print "position_command: "
#            print self.__positionCommand
            self.__sendCommand(self.__positionCommand)

    def parseLine(self, line):
        """
        """
        words = line.split()

        while True:
            if len(words) == 0:
                self.logText(line + '\n', 'input')
                return

            style = self.parseCommand(words[0], words[1:])
            if style is not None:
                self.logText(line + '\n', style)
                return

            print 'WARNING: Unknown command: ' + repr(words[0])
            words = words[1:]

    def parseCommand(self, command, args):
        """
        """
        if command == 'id':
            return 'info'

        elif command == 'uciok':
            if len(args) != 0:
                print 'WARNING: Arguments on uciok: ' + str(args)
            self.readyToConfigure = True
            return 'info'

        elif command == 'readyok':
            if len(args) != 0:
                print 'WARNING: Arguments on readyok: ' + str(args)
            self.ready = True
            return 'info'

        elif command == 'bestmove':
            if len(args) == 0:
                print 'WARNING: No move with bestmove'
                return 'error'
            else:
                move = args[0]
                self.onMove(move)
                # TODO: Check for additional ponder information
                return 'move'

        elif command == 'info':
            return 'info'

        elif command == 'option':
            return 'info'

        return None

    def getOutput(self):
        try:
            line = self.buffer.get()
            return line
        except Empty:
            pass

if __name__=="__main__":
    uci_engine = UCIEngine()
    uci_engine.start()
    uci_engine.configure()

    # Wait until the uci connection is setup
    while not uci_engine.ready:
        uci_engine.registerIncomingData()

    uci_engine.startGame()
    uci_engine.requestMove()

    while True:
        line = uci_engine.getOutput()
        if line:
            print line

##    uci_engine.reportMove('e2e4')
#    print uci_engine.registerIncomingData()
#    print uci_engine.registerIncomingData()
#    print uci_engine.registerIncomingData()

#    print uci_engine.requestMove()


