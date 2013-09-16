import kivy
from kivy_util import ScrollableLabel
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.settings import Settings, SettingItem, SettingsPanel, SettingTitle
from kivy.uix.image import AsyncImage
from kivy.uix.screenmanager import FadeTransition
from kivy.uix.screenmanager import WipeTransition
from kivy.uix.screenmanager import SwapTransition
from kivy.uix.screenmanager import SlideTransition


from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.textinput import TextInput
from kivy.uix.dropdown import DropDown

from kivy.properties import BooleanProperty, ListProperty, ObjectProperty, NumericProperty, StringProperty

from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.config import Config
from kivy.config import ConfigParser
from kivy.uix.scatter import Scatter
from kivy.utils import get_color_from_hex
#from kivy.core.clipboard import Clipboard


from ChessBoard import ChessBoard
from sets import Set
from uci import UCIEngine
from uci import UCIOption
from threading import Thread
import itertools as it
from time import sleep
from chess import polyglot_opening_book
from chess.position import Position
from chess.notation import SanNotation


GAME_HEADER = 'New Game'

ENGINE_PLAY = "engine_play"

ENGINE_ANALYSIS = "engine_analysis"

ENGINE_HEADER = '[b][color=000000][ref='+ENGINE_ANALYSIS\
                +']Analysis[/ref][ref='+ENGINE_PLAY+']\n\n\n' \
                'Play vs Comp [/ref][/color][/b]'

BOOK_ON = "Book"
BOOK_OFF = "Hide"

BOOK_HEADER = '[b][color=000000][ref=Book]'+BOOK_ON+'[/ref][/color][/b]'


SQUARES = ["a8", "b8", "c8", "d8", "e8", "f8", "g8", "h8", "a7", "b7", "c7", "d7", "e7", "f7", "g7", "h7", "a6",
              "b6", "c6", "d6", "e6", "f6", "g6", "h6", "a5", "b5", "c5", "d5", "e5", "f5", "g5", "h5", "a4", "b4",
              "c4", "d4", "e4", "f4", "g4", "h4", "a3", "b3", "c3", "d3", "e3", "f3", "g3", "h3", "a2", "b2", "c2",
              "d2", "e2", "f2", "g2", "h2", "a1", "b1", "c1", "d1", "e1", "f1", "g1", "h1"]

light_squares = Set([0,2,4,6,9,11,13,15,16,18,20,22,25,27,29,31,32,34,36,38,41,43,45,47,48,50,52,54,57,59,61,63])

IMAGE_PIECE_MAP = {
    "B": "wb",
    "R": "wr",
    "N": "wn",
    "Q": "wq",
    "K": "wk",
    "P": "wp",
    "b": "bb",
    "r": "br",
    "n": "bn",
    "q": "bq",
    "k": "bk",
    "p": "bp"
}

img_piece_abv={"B":"WBishop", "R":"WRook", "N":"WKnight", "Q":"WQueen", "K":"WKing", "P": "WPawn",
"b":"BBishop", "r":"BRook", "n":"BKnight", "q":"BQueen", "k":"BKing", "p":"BPawn"}

COLOR_MAPS = {
    'black': (1, 1, 1, 1),
    'white': (0, 0, 0, 1),
    #'cream': get_color_from_hex('#f9fcc6'),
    #'brown': get_color_from_hex('#969063'),
    'cream': get_color_from_hex('#f1ece7'),
    'brown': get_color_from_hex('#f2a257'),
    }

DARK_SQUARE = COLOR_MAPS['brown']
LIGHT_SQUARE = COLOR_MAPS['cream']

#engine_config = ConfigParser()
#engine_config.read('resources/engine.ini')

class SettingsScreen(Screen):
    pass

class ChessPiece(Scatter):

    image = ObjectProperty(None)
    moving = BooleanProperty(False)
    allowed_to_move = BooleanProperty(False)

    hide = BooleanProperty(False)


    def __init__(self, image_source, **kwargs):
        super(ChessPiece, self).__init__(**kwargs)

        self.image = Image(source=image_source)
        self.image.allow_stretch = True
        self.add_widget(self.image)
        self.auto_bring_to_front = True

    def on_hide(self, *args):
        self.remove_widget(self.image)

        if not self.hide:
            self.add_widget(self.image)

    def set_size(self, size):
        # Set both sizes otherwise the image
        # won't sit properly, and the scatter becomes larger than
        # the image.
        self.size = size[0], size[1]
        self.image.size = size[0], size[1]

    def set_pos(self, pos):
        self.pos = pos[0], pos[1]

    def on_touch_move(self, touch):
        if not self.allowed_to_move:
            return
        if super(ChessPiece, self).on_touch_move(touch):
            self.moving = True

    def on_touch_up(self, touch):
        if super(ChessPiece, self).on_touch_up(touch):
#            if self.parent and self.moving:
#                app.check_piece_in_square(self)

            self.moving = False

    def on_touch_down(self, touch):
        if super(ChessPiece, self).on_touch_down(touch):
            pass

class ChessSquare(Button):
    coord = NumericProperty(0)
    piece = ObjectProperty(None, allownone=True)
    show_piece = BooleanProperty(True)
    show_coord = BooleanProperty(False)

    def __init__(self, **kwargs):
        super(ChessSquare, self).__init__(**kwargs)
        self.background_normal = ''
        self.background_down = ''

    def add_piece(self, piece):
        self.remove_widget(self.piece)
        self.piece = piece
        if self.piece:
            self.piece.hide = not self.show_piece
            self.add_widget(piece)
            piece.set_size(self.size)
            piece.set_pos(self.pos)

#    def on_release(self):
#        self.state = 'down'
#        app.process_move(self)

    def remove_piece(self):
        if self.piece:
            self.remove_widget(self.piece)


    def on_size(self, instance, size):
        # print '%s Size: %s' % (get_square_abbr(self.coord), size)
        if self.piece:
            self.piece.set_size(size)


    def on_pos(self, instance, pos):
        # print '%s Positions: %s' % (get_square_abbr(self.coord), pos)
        if self.piece:
            self.piece.set_pos(pos)

            # def on_touch_down(self, touch):
            #     if super(ChessSquare, self).on_touch_down(touch):
            #         app.process_move(self)


class Chess_app(App):
    def generate_settings(self):

        settings_panel = Settings() #create instance of Settings

#        def add_one_panel(from_instance):
#            panel = SettingsPanel(title="I like trains", settings=self)
#            panel.add_widget(AsyncImage(source="http://i3.kym-cdn.com/entries/icons/original/000/004/795/I-LIKE-TRAINS.jpg"))
#            settings_panel.add_widget(panel)
#            print "Hello World from ", from_instance

        engine_panel = SettingsPanel(title="Engine") #create instance of left side panel
        board_panel = SettingsPanel(title="Board") #create instance of left side panel

        setup_pos_item = SettingItem(panel=board_panel, title="Input FEN") #create instance of one item in left side panel
        fen_input = TextInput(text="", focus=True, multiline=False, use_bubble = True)
#        print Clipboard['application/data']

        def on_fen_input(instance):
            if self.chessboard.setFEN(instance.text):
                self.refresh_board()
                self.start_pos_changed = True
                self.custom_fen = instance.text

        ##            print 'The widget', instance.text
        #
        fen_input.bind(on_text_validate=on_fen_input)


        setup_pos_item.add_widget(fen_input)
        level_item = SettingItem(panel=engine_panel, title="Level") #create instance of one item in left side panel

        board_panel.add_widget(setup_pos_item) # add item1 to left side panel

        engine_panel.add_widget(level_item) # add item2 to left side panel

        settings_panel.add_widget(board_panel)
        settings_panel.add_widget(engine_panel) #add left side panel itself to the settings menu

        def go_back():
            self.root.current = 'main'

        settings_panel.on_close=go_back

        return settings_panel # show the settings interface
#
#        parent = BoxLayout(size_hint=(1, 1))
#        bt = Button(text='Settings')
#        parent.add_widget(bt)
#
#        def go_back(instance):
#            self.root.current = 'main'
#
#        back_bt = Button(text='Back to Main')
#        back_bt.bind(on_press=go_back)
#        parent.add_widget(back_bt)
#
#        return parent

    def build(self):
        self.custom_fen = None
        self.start_pos_changed = False
        self.engine_mode = None
        self.engine_computer_move = True
        self.from_move = None
        self.to_move = None
        self.chessboard = ChessBoard()
        self.analysis_board = ChessBoard()
        self.squares = []
        self.use_engine = False
        self.book_display = False
        self.last_touch_down_move = None
        self.last_touch_up_move = None
        self.book = polyglot_opening_book.PolyglotOpeningBook('book.bin')


        parent = BoxLayout(size_hint=(1,1))
        grid = GridLayout(cols = 8, rows = 8, spacing = 0, size_hint=(1, 1))

        for i, name in enumerate(SQUARES):
            bt = ChessSquare(allow_stretch=True)
            bt.sq = i
            bt.name = name
#            bt.border = [0.5,0.5,0.5,0.5]
            if i in light_squares:
                bt.sq_color = "l"

#                bt.background_down = "img/empty-l.png"
                bt.background_color = LIGHT_SQUARE
            #                bt.background_color=[1,1,1,1]
            else:
                bt.background_color = DARK_SQUARE
                bt.sq_color = "d"
#                bt.background_down = "img/empty-d.png"

            #                bt.background_color=[0,0,0,0]
            #                print i
            # bt.bind(on_press=self.callback)
            bt.bind(on_touch_down=self.touch_down_move)
            bt.bind(on_touch_up=self.touch_up_move)
            # bt.bind(on_touch_up=self.touch_move)


            grid.add_widget(bt)
            self.squares.append(bt)


        b = BoxLayout(size_hint=(0.15,0.15))
        ## Spacers
#        b.add_widget(Button(spacing=1))
#        b.add_widget(Button(spacing=1))
#        b.add_widget(Button(spacing=1))

        # Move control buttons
#        back_bt = Button(markup=True)
#       # back_bt.background_normal="img/empty-l.png"
#        back_bt.text="[color=ff3333]Back[/color]"
#        back_bt.bind(on_press=self.back)
#        b.add_widget(back_bt)
#
        save_bt = Button(markup=True)
        #fwd_bt.background_normal="img/empty-d.png"
        save_bt.text="Save"
        # save_bt.text="Save"

        save_bt.bind(on_press=self.save)
        b.add_widget(save_bt)

#        b.add_widget(Button(spacing=10))
#        b.add_widget(Button(spacing=10))
#        b.add_widget(Button(spacing=10))

#        grid.add_widget(b)

#        board_box.add_widget(grid)
#        board_box.add_widget(b)

#        fen_input = TextInput(text="FEN", focus=True, multiline=False)
#        def on_fen_input(instance):
#            self.chessboard.setFEN(instance.text)
#            self.refresh_board()
###            print 'The widget', instance.text
##
#        fen_input.bind(on_text_validate=on_fen_input)
##        self._keyboard.bind(on_key_down=self._on_keyboard_down)
#
#
#        b.add_widget(fen_input)

        settings_bt = Button(markup=True, text='Setup')
        settings_bt.bind(on_press=self.go_to_settings)
        b.add_widget(settings_bt)


#        self.root.current='settings'


        parent.add_widget(grid)

        info_grid = GridLayout(cols = 1, rows = 4, spacing = 1, size_hint=(0.3, 1), orientation='vertical')
        info_grid.add_widget(b)


        self.game_score = ScrollableLabel('[color=000000][b]%s[/b][/color]' % GAME_HEADER, ref_callback=self.go_to_move)

        info_grid.add_widget(self.game_score)

        self.engine_score = ScrollableLabel(ENGINE_HEADER, ref_callback=self.add_eng_moves)
        info_grid.add_widget(self.engine_score)


        self.book_panel = ScrollableLabel(BOOK_HEADER, ref_callback=self.add_book_moves)
        info_grid.add_widget(self.book_panel)

        parent.add_widget(info_grid)
        self.refresh_board()

        platform = kivy.utils.platform()
        self.uci_engine = None
        if self.is_desktop():
            self._keyboard = Window.request_keyboard(
                self._keyboard_closed, self)
            self._keyboard.bind(on_key_down=self._on_keyboard_down)
            # Clock.schedule_interval(self.update_engine_output, 0.01)

            self.start_engine_thread()
        sm = ScreenManager(transition=SlideTransition())
        board_screen = Screen(name='main')
        board_screen.add_widget(parent)
        sm.add_widget(board_screen)

        settings_screen = SettingsScreen(name='settings')
        settings_screen.add_widget(self.generate_settings())

        sm.add_widget(settings_screen)

        return sm

    def go_to_settings(self, instance):
        self.root.current='settings'

    def go_to_move(self, instance, value):
#        print 'Going back to move.. ', value

        move_num, color = value.split(":")

        half_move_num = int(move_num)*2 - 1
#        print "half_move_num:%d"%half_move_num

        if color == 'b':
            half_move_num+=1

        self.chessboard.gotoMove(half_move_num)
        self.refresh_board()

    def add_book_moves(self, instance, mv):
#        print mv
        if mv == BOOK_OFF:
            self.book_display = False
            self.update_book_panel()
        elif mv == BOOK_ON:
            self.book_display = True
            self.update_book_panel()
        else:
            self.chessboard.addTextMove(mv)
            self.refresh_board()

    def add_eng_moves(self, instance, value):
        if value==ENGINE_ANALYSIS or value== ENGINE_PLAY:
#            print "Bringing up engine menu"
            if self.use_engine:
                self.use_engine = False
                if self.uci_engine:
                    self.uci_engine.stop()
            else:
                self.use_engine = True
                self.engine_mode = value
                if value == ENGINE_PLAY:
                    self.engine_computer_move = True

            self.refresh_board()
        else:
            for i, mv in enumerate(self.engine_score.raw):
                if i>=1:
                    break
                self.chessboard.addTextMove(mv)

        self.refresh_board()

    def is_desktop(self):
        platform = kivy.utils.platform()
#        print platform
        return True if platform.startswith('win') or platform.startswith('linux') or platform.startswith('mac') else False


    def back(self, obj):
        self.chessboard.undo()
        self.refresh_board()

    def _keyboard_closed(self):
#        print 'My keyboard have been closed!'
        self._keyboard.unbind(on_key_down=self.back)
        self._keyboard = None

    def start_engine_thread(self):
        t = Thread(target=self.update_engine_output, args=(None,))
        t.daemon = True # thread dies with the program
        t.start()

    def start_engine(self):
#        self.use_engine = False

        uci_engine = UCIEngine()
        uci_engine.start()
        uci_engine.configure({'Threads': '1'})
        uci_engine.configure({'OwnBook': 'true'})
        # uci_engine.configure({'Book File': 'gm1950.bin'})

        #uci_engine.configure({'Use Sleeping Threads': 'false'})

        # Wait until the uci connection is setup
        while not uci_engine.ready:
            uci_engine.registerIncomingData()

        uci_engine.startGame()
        # uci_engine.requestMove()
        self.uci_engine=uci_engine

    def parse_bestmove(self, line):
        best_move = None
        ponder_move = None
        if not line.startswith('bestmove'):
            return best_move, ponder_move
        tokens = line.split()

        try:
            bm_index = tokens.index('bestmove')
            ponder_index = tokens.index('ponder')
        except ValueError:
            bm_index = -1
            ponder_index = -1

        if bm_index!=-1:
            best_move = tokens[bm_index+1]

        if ponder_index!=-1:
            ponder_move = tokens[ponder_index+1]

        return best_move, ponder_move

    def parse_score(self, line):
        self.analysis_board.setFEN(self.chessboard.getFEN())
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
            for mv in tokens[line_index+1:]:
                self.analysis_board.addTextMove(mv)
                move_list.append(self.analysis_board.getLastTextMove())

        except ValueError:
            line_index = -1
        variation = self.generate_move_list(move_list,start_move_num=self.chessboard.getCurrentMove()+1) if line_index!=-1 else None

        #del analysis_board
        if variation and score:
            score_float = None
            try:
                score_float = float(score)
            except ValueError, e :
                print "Cannot convert score to a float"
                print e
            if self.chessboard._turn == self.chessboard.BLACK:
                if score_float:
                    score_float *= -1
                    score = score_float
            return move_list, "[color=000000][b]%s[/b]     [i][ref=%s]Stop[/ref][/i][/color]\n[color=000000]%s[/color]" %(score, ENGINE_ANALYSIS, "".join(variation))


    def update_engine_output(self, callback):
        if not self.uci_engine:
            self.start_engine()

        while True:
            output = self.engine_score
            if self.use_engine:
                line = self.uci_engine.getOutput()
                if line:
                    if self.engine_mode == ENGINE_ANALYSIS:
                        #out_score = None
                        out_score = self.parse_score(line)
                        if out_score:
                            raw_line, cleaned_line = out_score
                            if cleaned_line:
                                output.children[0].text = cleaned_line
                            if raw_line:
                                output.raw = raw_line
                    elif self.engine_mode == ENGINE_PLAY:
                        if self.engine_computer_move:
                            best_move, ponder_move = self.parse_bestmove(line)
                            if best_move:
                                self.chessboard.addTextMove(best_move)
                                self.engine_computer_move = False
                                output.children[0].text = "Your turn"
                                self.refresh_board()
                            else:
                                output.children[0].text = "Thinking.."
                                # sleep(1)
                        else:
                            output.children[0].text = "Your turn"
                            # sleep(1)
            else:
                # if output.children[0].text != ENGINE_HEADER:
                output.children[0].text = ENGINE_HEADER
                sleep(1)



    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if self.root.current!="main":
            return False
#        print self.root.current
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

    def save(self, obj):
        f = open('game.pgn','w')
        f.write('Game Header - Analysis \n\n')
        f.write(self.generate_move_list(self.chessboard.getAllTextMoves(),raw=True))
        f.close()

    def touch_down_move(self, img, touch):
        if not img.collide_point(touch.x, touch.y):
            return
        # print "touch_move"
        # print touch
        mv = img.name
        squares = [item for sublist in self.chessboard.getBoard() for item in sublist]

        if squares[SQUARES.index(mv)]!='.':
            # self.from_move = move
            self.last_touch_down_move = mv

            # self.process_move(mv)

    def touch_up_move(self, img, touch):
        if not img.collide_point(touch.x, touch.y):
            return
        # print "touch_move"
        # print touch
#        mv = img.name
        self.last_touch_up_move = img.name
        if self.last_touch_up_move and self.last_touch_down_move and self.last_touch_up_move != self.last_touch_down_move:
            self.process_move()

    def process_move(self):
        if self.chessboard.addTextMove(self.last_touch_down_move+self.last_touch_up_move):
            if not self.engine_computer_move and self.engine_mode == ENGINE_PLAY:
                self.engine_computer_move = True
            self.refresh_board()

    def generate_move_list(self, all_moves, start_move_num = 1, raw = False):
        score = ""
        # if raw:
        #     return " ".join(all_moves)
        for i, mv in it.izip(it.count(start_move_num), all_moves):
            move = "b"
            if i % 2 == 1:
                score += "%d. " % ((i + 1) / 2)
                move = "w"

            if mv:
                if raw:
                    score += " % s" % mv
                    if i % 5 == 0:
                        score += "\n"

                else:
                    score += " [ref=%d:%s] %s [/ref]"%((i + 1) / 2, move, mv)
        return score

    def update_book_panel(self):
        if self.book_display:
            p = Position(fen=self.chessboard.getFEN())
            self.book_panel.children[0].text = "[color=000000][i][ref=" + BOOK_OFF + "]" + BOOK_OFF + "[/ref][/i]\n"
            book_entries = 0
            for e in self.book.get_entries_for_position(p):
                san = SanNotation(p, e["move"])
                self.book_panel.children[0].text += "[ref=%s]%s[/ref]    %d\n\n" % (san, san, e["weight"])
                book_entries += 1
                if book_entries >= 5:
                    break
            self.book_panel.children[0].text+='[/color]'
        else:
            self.book_panel.children[0].text = BOOK_HEADER

    def refresh_board(self):
        # flatten lists into one list of 64 squares
        squares = [item for sublist in self.chessboard.getBoard() for item in sublist]

        for i, p in enumerate(squares):
            sq = self.squares[i]
            if p==".":
                sq.remove_piece()
#                sq.background_normal=sq.background_down

            if p!=".":
                p_color = 'w' if p.isupper() else 'b'
#                sq.source="img/pieces/Merida/"+sq.sq_color+p_color+p.lower()+".png"
#                sq.background_normal="img/pieces/Merida/"+sq.sq_color+p_color+p.lower()+".png"
#                sq.background_normal="img/pieces/Merida/pieces/"+p_color+p.lower()+".png"
                piece = ChessPiece('img/pieces/Merida/%s.png' % IMAGE_PIECE_MAP[p])
                sq.add_piece(piece)
    # Update game notation
        all_moves = self.chessboard.getAllTextMoves()
        if all_moves:
            score = self.generate_move_list(all_moves)
            self.game_score.children[0].text="[color=000000]%s[/color]"%score

        if self.use_engine and self.uci_engine:
            #self.analysis_board.setFEN(self.chessboard.getFEN())
            self.uci_engine.stop()
            self.uci_engine.reportMoves(self.chessboard.getAllTextMoves(format=0, till_current_move=True))
            if self.start_pos_changed:
                self.uci_engine.sendFen(self.custom_fen)
                self.start_pos_changed = False
            if self.engine_mode == ENGINE_ANALYSIS:
                self.uci_engine.requestAnalysis()
            else:
                if self.engine_mode == ENGINE_PLAY and self.engine_computer_move:
                    self.uci_engine.requestMove()

        self.update_book_panel()

if __name__ == '__main__':
    Chess_app().run()
