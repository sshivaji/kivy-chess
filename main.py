import kivy
from kivy_util import ScrollableLabel
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window

from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.config import Config
from ChessBoard import ChessBoard
from sets import Set
from uci import UCIEngine
from threading import Thread

import itertools as it

SQUARES = ["a8", "b8", "c8", "d8", "e8", "f8", "g8", "h8", "a7", "b7", "c7", "d7", "e7", "f7", "g7", "h7", "a6",
              "b6", "c6", "d6", "e6", "f6", "g6", "h6", "a5", "b5", "c5", "d5", "e5", "f5", "g5", "h5", "a4", "b4",
              "c4", "d4", "e4", "f4", "g4", "h4", "a3", "b3", "c3", "d3", "e3", "f3", "g3", "h3", "a2", "b2", "c2",
              "d2", "e2", "f2", "g2", "h2", "a1", "b1", "c1", "d1", "e1", "f1", "g1", "h1"]

light_squares = Set([0,2,4,6,9,11,13,15,16,18,20,22,25,27,29,31,32,34,36,38,41,43,45,47,48,50,52,54,57,59,61,63])

img_piece_abv={"B":"WBishop", "R":"WRook", "N":"WKnight", "Q":"WQueen", "K":"WKing", "P": "WPawn",
"b":"BBishop", "r":"BRook", "n":"BKnight", "q":"BQueen", "k":"BKing", "p":"BPawn"}

class Chess_app(App):
    def build(self):
        self.from_move = None
        self.to_move = None
        self.chessboard = ChessBoard()
        self.analysis_board = ChessBoard()
        self.squares = []
        self.use_engine = False
#        Config.set('graphics', 'width', '900')
#        Config.set('graphics', 'height', '900')
#        Config.set('graphics','fullscreen', 1)
        parent = BoxLayout(size_hint=(1,1))
        grid = GridLayout(cols = 8, rows = 8, spacing = 1, size_hint=(1, 1))
#        board_box = BoxLayout(orientation='vertical')

        for i, name in enumerate(SQUARES):
            bt = Button()
            bt.sq = i
            bt.name = name
            bt.border = [0,0,0,0]
            if i in light_squares:
                bt.sq_color = "l"
                bt.background_down = "img/empty-l.png"

            #                bt.background_color=[1,1,1,1]
            else:
                bt.sq_color = "d"
                bt.background_down = "img/empty-d.png"

            #                bt.background_color=[0,0,0,0]
            #                print i
            bt.bind(on_press=self.callback)
#            bt.bind(on_touch_down=self.touch_down_move)
#            bt.bind(on_touch_up=self.touch_up_move)

            grid.add_widget(bt)
            self.squares.append(bt)


        b = BoxLayout(size_hint=(0.15,0.15))
        ## Spacers
#        b.add_widget(Button(spacing=1))
#        b.add_widget(Button(spacing=1))
#        b.add_widget(Button(spacing=1))

        # Move control buttons
        back_bt = Button(markup=True)
       # back_bt.background_normal="img/empty-l.png"
        back_bt.text="[color=ff3333]Back[/color]"
        back_bt.bind(on_press=self.back)
        b.add_widget(back_bt)

        fwd_bt = Button(markup=True)
        #fwd_bt.background_normal="img/empty-d.png"
        fwd_bt.text="[color=3333ff]Fwd[/color]"

        fwd_bt.bind(on_press=self.fwd)
        b.add_widget(fwd_bt)

#        b.add_widget(Button(spacing=10))
#        b.add_widget(Button(spacing=10))
#        b.add_widget(Button(spacing=10))

#        grid.add_widget(b)

#        board_box.add_widget(grid)
#        board_box.add_widget(b)
        parent.add_widget(grid)


        info_grid = GridLayout(cols = 1, rows = 4, spacing = 1, size_hint=(0.3, 1), orientation='vertical')
        self.game_score = ScrollableLabel('New Game')

        info_grid.add_widget(self.game_score)

        self.engine_score = ScrollableLabel('Analysis')
        info_grid.add_widget(self.engine_score)


        info_grid.add_widget(Button(text="Text"))
        info_grid.add_widget(b)

        parent.add_widget(info_grid)
        self.refresh_board()

        self._keyboard = Window.request_keyboard(
            self._keyboard_closed, self)

        self._keyboard.bind(on_key_down=self._on_keyboard_down)

        self.start_engine_thread()

        return parent


    def back(self, obj):
        self.chessboard.undo()
        self.refresh_board()

    def _keyboard_closed(self):
        print 'My keyboard have been closed!'
        self._keyboard.unbind(on_key_down=self.back)
        self._keyboard = None


    def start_engine_thread(self):
        t = Thread(target=self.update_engine_output, args=(self.engine_score,))
        t.daemon = True # thread dies with the program
        t.start()

    def start_engine(self):
        uci_engine = UCIEngine()
        uci_engine.start()
        uci_engine.configure()

        # Wait until the uci connection is setup
        while not uci_engine.ready:
            uci_engine.registerIncomingData()

        uci_engine.startGame()
        uci_engine.requestMove()
        self.use_engine = True
        self.uci_engine=uci_engine

    def update_engine_output(self, output):
        if not self.use_engine:
            self.start_engine()

        def parse_score(line):
            analysis_board = ChessBoard()
            analysis_board.setFEN(self.chessboard.getFEN())
            tokens = line.split()
            try:
                score_index = tokens.index('score')
            except ValueError:
                score_index = -1
            score = None
            move_list = []
            if score_index!=-1 and tokens[score_index+1]=="cp":
                score = float(tokens[score_index+2])/100*1.0
            try:
                line_index = tokens.index('pv')
#                print "curr_move: %d"%curr_move
                for mv in tokens[line_index+1:]:
                    analysis_board.addTextMove(mv)
                    move_list.append(analysis_board.getLastTextMove())
#                analysis_board.gotoMove(curr_move)

            except ValueError:
                line_index = -1
            variation = self.generate_move_list(move_list,start_move_num=self.chessboard.getMoveCount()+1) if line_index!=-1 else None

            del analysis_board
            if variation and score:
                return "[b]%s[/b]\n[color=77b5fe]%s[/color]" %(score,"".join(variation))

        while True:
            line = self.uci_engine.getOutput()
            if line:
#                print line
                cleaned_line = parse_score(line)
                if cleaned_line:
                    output.children[0].text = cleaned_line




    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
#        print 'The key', keycode, 'have been pressed'
#        print ' - text is %r' % text
#        print ' - modifiers are %r' % modifiers

        # Keycode is composed of an integer + a string
        # If we hit escape, release the keyboard
        if keycode[1] == 'escape':
            keyboard.release()

        if keycode[1] == 'left':
            self.back(None)
        elif keycode[1] == 'right':
            self.fwd(None)


        # Return True to accept the key. Otherwise, it will be used by
        # the system.
        return True

    def fwd(self, obj):
        self.chessboard.redo()
        self.refresh_board()

    def callback(self, obj):
#        print 'Button state:%s' %obj.state
#        print 'Square %s was clicked' %(obj.name)
        squares = [item for sublist in self.chessboard.getBoard() for item in sublist]


        if not self.from_move:
            if squares[SQUARES.index(obj.name)]!='.':
                self.from_move = obj.name
        else:
            self.to_move = obj.name
            if self.chessboard.addTextMove(self.from_move+self.to_move):
                self.refresh_board()
            self.to_move = None
            self.from_move = None
#        print "from_move:%s, to_move:%s"%(self.from_move, self.to_move)


    def generate_move_list(self, all_moves, start_move_num = 1):
        score = ""
        for i, mv in it.izip(it.count(start_move_num), all_moves):
            if i % 2 == 1:
                score += "%d. " % ((i + 1) / 2)
            if mv:
                score += mv + " "
#            if i % 5 == 0:
#                score += "\n"
        return score

    def refresh_board(self):
        # flatten lists into one list of 64 squares
        squares = [item for sublist in self.chessboard.getBoard() for item in sublist]

        for i, p in enumerate(squares):
            sq = self.squares[i]
            if p==".":
                sq.background_normal=sq.background_down

            if p!=".":
                p_color = 'w' if p.isupper() else 'b'
                sq.background_normal="img/pieces/Merida/"+sq.sq_color+p_color+p.lower()+".png"

        # Update game notation
        all_moves = self.chessboard.getAllTextMoves()
        if all_moves:
            score = self.generate_move_list(all_moves)

            self.game_score.children[0].text="[color=37c855]%s[/color]"%score

        if self.use_engine:
#            print self.chessboard.getLastTextMove()
            self.analysis_board.setFEN(self.chessboard.getFEN())
            self.uci_engine.stop()
            self.uci_engine.reportMove(self.chessboard.getLastTextMove(format=0))
            self.uci_engine.requestMove()


Chess_app().run()
