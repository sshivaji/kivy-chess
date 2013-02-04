import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.config import Config
from ChessBoard import ChessBoard
from sets import Set

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
        self.squares = []
        Config.set('graphics', 'width', '1280')
        Config.set('graphics', 'height', '960')
        parent = Widget(width = Config.getint('graphics', 'width'),
            height = Config.getint('graphics', 'height'))
        grid = GridLayout(cols = 8, rows = 9, size = parent.size, spacing = 1)

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

        ## Spacers
        grid.add_widget(Widget())
        grid.add_widget(Widget())
        grid.add_widget(Widget())

        # Move control buttons
        back_bt = Button(markup=True)
       # back_bt.background_normal="img/empty-l.png"
        back_bt.text="[color=ff3333]Back[/color]"
        back_bt.bind(on_press=self.back)
        grid.add_widget(back_bt)

        fwd_bt = Button(markup=True)
        #fwd_bt.background_normal="img/empty-d.png"
        fwd_bt.text="[color=3333ff]Fwd[/color]"

        fwd_bt.bind(on_press=self.fwd)
        grid.add_widget(fwd_bt)


        parent.add_widget(grid)
        self.refresh_board()
        return parent

    def back(self, obj):
        self.chessboard.undo()
        self.refresh_board()

    def fwd(self, obj):
        self.chessboard.redo()
        self.refresh_board()

    def callback(self, obj):
#        print 'Button state:%s' %obj.state
        print 'Square %s was clicked' %(obj.name)
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


    def refresh_board(self):
        # flatten lists into one list of 64 squares
        squares = [item for sublist in self.chessboard.getBoard() for item in sublist]

        for i, p in enumerate(squares):
            sq = self.squares[i]
            if p==".":
                sq.background_normal=sq.background_down

            if p!=".":
                p_color = 'w' if p.isupper() else 'b'
                sq.background_normal="img/Pieces/Merida/"+sq.sq_color+p_color+p.lower()+".png"

Chess_app().run()
