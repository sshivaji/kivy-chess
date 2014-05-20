import os
import signal
import sys
import subprocess
from threading import Thread
import select
import spur
import paramiko

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
    def __init__(self, exe, cloud=False, cloud_hostname=None, cloud_username=None, cloud_private_key_file=None):
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
        self.cloud = cloud

        self.STATE_IDLE = 'IDLE'
        self.STATE_CONNECTING = 'CONNECTING'

        self.options = {}
        # self.set_options = ()
        self.available_options = {}
        self.engine_info = {}
        self.__queuedCommands = []
        self.eng_process = None
        # "engines/stockfish4-mac-64"
        try:
            if not cloud:
                shell = spur.LocalShell()
                self.eng_process = shell.spawn(exe, stdout=subprocess.PIPE, store_pid=True)

            else:
                print "Trying cloud connect.."
                print "cloud_hostname : {0}".format(cloud_hostname)
                print "cloud_username : {0}".format(cloud_username)
                print "cloud_private_key_file : {0}".format(cloud_private_key_file)

                shell = spur.SshShell(
                    hostname=cloud_hostname,
                    username=cloud_username,
                    private_key_file=cloud_private_key_file,
                    missing_host_key=paramiko.AutoAddPolicy()
                )
                self.eng_process = shell.spawn([exe], stdout=subprocess.PIPE, store_pid=True, allow_error=True)

            process_stdout = self.eng_process._stdout if cloud else self.eng_process._subprocess.stdout

            self.buffer = Queue()
            t = Thread(target=self.enqueue_output, args=(process_stdout, self.buffer))
            t.daemon = True # thread dies with the program
            t.start()

        except OSError:
            print "OS error in starting engine"

    def enqueue_output(self, p, queue):
        out = p
        while True:
            # print out.readline()
            queue.put(out.readline())

    def logText(self, text, style):
        """
        """
        pass

    def onOutgoingData(self, data):
        """
        """
        self.eng_process.stdin_write(data)

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
            line = self.buffer.get() # or q.get(timeout=.1)
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

    def set_option(self, option, value):
        self.configure({option : value})
        self.available_options[option][0] = value

    def get_option(self, option):
        return self.available_options[option]

    def get_options(self):
        return self.available_options

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
            self.onOutgoingData('setoption name {0} value {1}\n'.format(k,v))
        self.onOutgoingData('isready\n')

    def requestAnalysis(self, whiteTime=30000, blackTime=30000):
        """
        """
        # Some AI's don't work unless assigned some time
        # TODO: which ones? I think Glaurung had issues

#        self.__sendCommand('go wtime %d btime %d' % (whiteTime, blackTime))
        self.__sendCommand('go infinite')

    def requestMove(self, movetime=None, wtime=5, btime=5, winc=0, binc=0):
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
            # print "line: "
            # print line
            # print "style: "
            # print style
            if style is not None:
                self.logText(line + '\n', style)
                return

            print 'WARNING: Unknown command: ' + repr(words[0])
            words = words[1:]

    def parseCommand(self, command, args):
        """
        """
        if command == 'id':
            # e.g. id name Komodo64 3
            try:
                if args[0] not in self.engine_info:
                    self.engine_info[args[0]] = " ".join(args[1:])

            except ValueError:
                print 'WARNING: Arguments on id: ' + str(args)
                pass
            return 'info'

        elif command == 'uciok':
            if len(args) != 0:
                print 'WARNING: Arguments on uciok: ' + str(args)
            self.readyToConfigure = True
            return 'info'

        elif command == 'readyok' or command.endswith('eadyok'):
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
            # print args
            try:
                name_idx = args.index("name")
                type_idx = args.index("type")
                name = " ".join(args[name_idx+1:type_idx])
                # print "name : {0}".format(name)
                type = args[type_idx+1]
                # print "type: {0}".format(args[type_idx+1])
                default_idx = args.index("default")
                default = args[default_idx+1]
                # print "default: {0}".format(args[default_idx+1])

                if type == 'spin':
                    min_idx = args.index("min")
                    min = int(args[min_idx+1])
                    max_idx = args.index("max")
                    max = int(args[max_idx+1])
                    # print "min : {0}".format(min)
                    # print "max : {0}".format(max)
                    if name not in self.available_options:
                        self.available_options[name] = [default, 'spin', default, min, max]
                else:
                    if name not in self.available_options:
                        self.available_options[name] = [default, type, default]

                 # 'Ponder': ('true', 'check', 'true')
                 # 'Space': ('100', 'spin', '100', 0, 200)
                 # 'Search Log Filename': ('SearchLog.txt', 'string', 'SearchLog.txt')

            except ValueError:
                print 'WARNING: Arguments on option: ' + str(args)
            return 'info'

        return None

    def getOutput(self):
        try:
            line = self.buffer.get()
            return line
        except Empty:
            pass

if __name__=="__main__":
    uci_engine = UCIEngine("engines/stockfish4-mac-64")
    uci_engine.start()
    uci_engine.configure({})

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


