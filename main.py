import traceback
import kivy
import os
import shutil
import random
from kivy.config import ConfigParser
# from kivy.config import Config
# Config.set('graphics', 'fullscreen', 0)
# Config.write()

from kivy_util import ScrollableLabel
from kivy_util import ScrollableGrid

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.settings import Settings, SettingItem, SettingsPanel
from kivy.uix.screenmanager import SlideTransition
from kivy.graphics import Color

from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.textinput import TextInput

from kivy.properties import BooleanProperty, ObjectProperty, NumericProperty

from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.scatter import Scatter
from kivy.utils import get_color_from_hex
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.popup import Popup
from kivy.uix.switch import Switch
from kivy.uix.slider import Slider
from kivy.graphics import Rectangle
from kivy.core.text.markup import MarkupLabel
from kivy.adapters.listadapter import ListAdapter

from kivy.uix.listview import ListItemButton, CompositeListItem, ListView
from kivy.uix.dropdown import DropDown
from kivy.uix.filechooser import FileChooserListView

#from kivy.core.clipboard import Clipboard

#from ChessBoard import ChessBoard
from sets import Set
from uci import UCIEngine
from threading import Thread
import itertools as it
from operator import attrgetter
from time import sleep
from chess import polyglot_opening_book

THINKING_TIME = "[color=000000]Thinking..\n[size=24]{0}    [b]{1}[/size][/b][/color]"
THINKING = "[color=000000][b][size=16]Thinking..[/size][/b][/color]"

try:
    import libchess
except ImportError:
    from chess import libchess

from libchess import Position
# from chess.libchess import SanNotation
# from chess.libchess import MoveError
from libchess import Move
from chess.game import Game
from chess.game_node import PIECE_FONT_MAP
from chess import PgnFile
#from chess import PgnIndex
from chess.game_node import GameNode
from libchess import Piece
from libchess import Square
from chess.game_header_bag import GameHeaderBag
import stockfish as sf

# DGT
from dgt.dgtnix import *
import os
import datetime
import leveldb

INDEX_TOTAL_GAME_COUNT = "total_game_count"

INDEX_FILE_POS = "last_pos"

DELETE_FROM_USER_BOOK = "delete_from_user_book"

ADD_TO_USER_BOOK = "add_to_user_book"

REF_ = '[ref='

BOOK_POSITION_UPDATE = "BOOK_POSITION_UPDATE"

Clock.max_iteration = 20

GAME_HEADER = 'New Game'

ENGINE_PLAY = "engine_play"

ENGINE_PLAY_STOP = "play_stop"

ENGINE_PLAY_HINT = "play_hint"

YOURTURN_MENU = "[color=000000][size=24][i]{2}[/i]    [b]{3}[/b][/size]\nYour turn\n[ref="+ENGINE_PLAY_STOP+"]Stop[/ref]\n\n[ref="+ENGINE_PLAY_HINT+"]Hint: {0}\nScore: {1} [/ref][/color]"

TRAIN_MENU = "[color=000000][b]{0}    [/b]{1}[b]\n\n\n[ref="+ENGINE_PLAY_STOP+"]Stop[/ref][/b][/color]"

ENGINE_ANALYSIS = "engine_analysis"

ENGINE_TRAINING = "engine_training"

ENGINE_HEADER = '[b][color=000000][ref='+ENGINE_ANALYSIS\
                +']Analysis[/ref][ref='+ENGINE_PLAY+']\n\n' \
                'Play vs Comp [/ref][ref='+ENGINE_TRAINING+']\n\nTrain[/ref][/color][/b]'

MOVE_OUT_FORMAT = '[color=000000][b]{0}[/b][/color]'

BOOK_ON = "Book"
USER_BOOK_ON = "User Book"
SHOW_GAMES = "Show Games"
SHOW_REF_GAMES = "Show Reference Games"
BOOK_OFF = "Hide"

BOOK_HEADER = '[b][color=000000][ref=Book]{0}[/ref][/color][/b]'

DATABASE_HEADER = '[b][color=000000][ref=Database]{0}[/ref][/color][/b]'

DB_SORT_ASC = unichr(8710)
DB_SORT_DESC = 'V'


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

SPOKEN_PIECE_SOUNDS = {
    "B": " Bishop ",
    "N": " Knight ",
    "R": " Rook ",
    "Q": " Queen ",
    "K": " King ",
    "O-O": " Castles ",
    "++": " Double Check ",
}

img_piece_abv={"B":"WBishop", "R":"WRook", "N":"WKnight", "Q":"WQueen", "K":"WKing", "P": "WPawn",
"b":"BBishop", "r":"BRook", "n":"BKnight", "q":"BQueen", "k":"BKing", "p":"BPawn"}

COLOR_MAPS = {
    'black': get_color_from_hex('#000000'),
    'white': (0, 0, 0, 1),
    'wood': get_color_from_hex('#a68064'),
    #'cream': get_color_from_hex('#f9fcc6'),
    #'brown': get_color_from_hex('#969063'),
    'cream': get_color_from_hex('#f1ece7'),
    'brown': get_color_from_hex('#f2a257'),
    }

DARK_SQUARE = "img/board/dark/"
LIGHT_SQUARE = "img/board/light/"

MERIDA = "img/pieces/Merida-shadow/"

INITIAL_BOARD_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
DB_HEADER_MAP = {"White": 0, "WhiteElo": 1, "Black": 2,
                 "BlackElo": 3, "Result": 4, "Date": 5, "Event": 6, "Site": 7,
                 "ECO": 8, INDEX_FILE_POS:9, "FEN":10}
config = ConfigParser()


class DBGame(object):
    def __init__(self, id, **kwargs):
        self.id = id

#    def __init__(self, id, white, whiteelo, black, blackelo, result, date, eco, event, **kwargs):
#        self.id = id
#        self.white = white
#        try:
#            self.whiteelo = int(whiteelo)
#        except ValueError:
#            self.whiteelo = whiteelo
#        self.black = black
#        try:
#            self.blackelo = int(blackelo)
#        except ValueError:
#            self.blackelo = blackelo
#        self.result = result
#        self.date = date
#        self.eco = eco
#        self.event = event

class DBSortCriteria(object):
    def __init__(self, key, rank, asc, **kwargs):
        self.key = key
        self.rank = rank
        self.asc = asc

class DBHeaderButton(Button):
    def __init__(self, field, **kwargs):
        # self.bind(height = self._resize)
        super(DBHeaderButton, self).__init__(**kwargs)
        self.field = field

class CustomListItemButton(ListItemButton):
    def __init__(self, **kwargs):
        # self.bind(height = self._resize)
        super(CustomListItemButton, self).__init__(**kwargs)
        # self.height = 10
        # with self.canvas.before:
        #     # grid.canvas.clear()
        #     Color(1, 1, 1)
        #     self.background = Rectangle()
            # Rectangle(size=Window.size)
        self.markup = True
        # self.selected_color = (0,0,0,0)
        self.border = (0,0,0,0)
        self.deselected_color = (1,1,1, 1)
        self.background_color = (1,1,1, 1)
        self.background_normal = 'img/background_normal.png'
        # self.background_down = 'img/background_pressed.png'
        # self.background_down = 'img/background_pressed.png'

    # def _resize(self,instance, height):
    #     # start with simple case of calculating scalefactor from height
    #     # print height
    #     # print self.size[1]
    #     # scalefactor = self.size[1]*1.0/height
    #     # print scalefactor
    #     self.font_size = '{0}dp'.format(self.height *0.4)
    #     # self.font_size = height * 0.35

class PositionEval(object):
    def __init__(self, informant_eval, integer_eval):
        self.informant_eval = informant_eval
        self.integer_eval = integer_eval
    def __str__( self):
        return "{0}, {1}".format(self.informant_eval, self.integer_eval)

pos_evals = [PositionEval("-+", -2), PositionEval("=+", -1), PositionEval("=", 0), PositionEval("+=", 1), PositionEval("+-", 2), PositionEval("none", 5)]

class SettingsScreen(Screen):
    pass

class ChessPiece(Scatter):
    image = ObjectProperty()
    moving = BooleanProperty(True)
    allowed_to_move = BooleanProperty(False)

    hide = BooleanProperty(False)

    def __init__(self, image_source, **kwargs):
        super(ChessPiece, self).__init__(**kwargs)

        self.image = Image(source=image_source)
        self.image.allow_stretch = True
        self.image.keep_ratio = True

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
        # self.scale = 0.9

    def set_pos(self, pos):
        self.pos = pos[0], pos[1]

    def on_touch_move(self, touch):
        if not self.allowed_to_move:
            return
        if super(ChessPiece, self).on_touch_move(touch):
            self.moving = True
        #     self.image.size = self.size[0]*1.2, self.size[1]*1.2

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

    def add_piece(self, piece):
        self.remove_widget(self.piece)
        self.piece = piece
        # print self.size
        if self.piece:
            self.piece.hide = not self.show_piece
            self.add_widget(piece)
            # print self.size
            piece.set_size(self.size)
            piece.set_pos(self.pos)

    def remove_piece(self):
        if self.piece:
            self.remove_widget(self.piece)


    def on_size(self, instance, size):
        # print 'Size: %s' % ( size)
        if self.piece:
            self.piece.set_size(size)


    def on_pos(self, instance, pos):
        # print '%s Positions: %s' % (get_square_abbr(self.coord), pos)
        if self.piece:
            self.piece.set_pos(pos)

            # def on_touch_down(self, touch):
            #     if super(ChessSquare, self).on_touch_down(touch):
            #         app.process_move(self)

class DataItem(object):
    def __init__(self, text='', is_selected=False):
        self.text = text
        self.is_selected = is_selected


class Chess_app(App):
    def validate_device(self, text):
        if not os.path.exists(text):
            popup = Popup(title='Sorry, DGT Device NOT found!',
                content=Label(text="DGT device {0} was NOT found".format(text)),
                size_hint=(None, None), size=(400, 400))
            popup.open()
            return False
        return True

    def open_create_index(self, f):
        folder_tokens = f[0].split('/')
        leveldb_path = None
        if '.db' in folder_tokens[-2]:
            leveldb_path = folder_tokens[:-1]
            if leveldb_path:
                leveldb_path = '/'.join(leveldb_path)

        elif '.pgn' in folder_tokens[-1]:
            pgn_path = f[0]
            leveldb_path = self.gen_leveldb_path(pgn_path)
            if not os.path.exists(leveldb_path):
                command = "polyglot make-book -pgn '{0}' -leveldb '{1}' -min-game 1".format(pgn_path, leveldb_path)
                # print command
                os.system(command)
        return leveldb_path

    def gen_leveldb_path(self, fname):
        return fname + '.db'

    def process_database(self, obj, f, mevent):
        leveldb_path = self.open_create_index(f)
        if leveldb_path:
            self.db_popup.dismiss()
            self.db_index_book = leveldb.LevelDB(leveldb_path)

    def process_ref_database(self, obj, f, mevent):
        leveldb_path = self.open_create_index(f)

        if leveldb_path:
            self.db_popup.dismiss()
            self.ref_db_index_book = leveldb.LevelDB(leveldb_path)


    def open_database(self, x):
        self.fileChooser = fileChooser = FileChooserListView(path='~')
        fileChooser.bind(on_submit=self.process_database)

        self.open_db_popup()


    def open_db_popup(self):
        self.db_popup = Popup(title='Select PGN file (.pgn) or PGN Index folder (.db)',
                              content=self.fileChooser, size_hint=(0.75, 1))
        self.db_popup.open()

    def open_ref_database(self, x):
        self.fileChooser = fileChooser = FileChooserListView(path='~')
        fileChooser.bind(on_submit=self.process_ref_database)

        self.open_db_popup()

    def generate_settings(self):

        def go_to_setup_board(value):
            self.root.current = 'setup_board'


        def on_dgt_dev_input(instance):
#            print instance.text
            text = self.dgt_dev_input.text
            self.validate_device(text)

        def on_dgt_sound(instance, value):
            self.dgt_clock_sound = value

        def on_dgt_connect(instance, value):
        #            print "bind"
        #            print instance
        #            print value
        #            print self.dgt_dev_input.text
        # Load the library
            if not value:
                if self.dgtnix:
                    self.dgtnix.Close()
                self.dgt_connected = False

            else:
                try:
                    self.dgtnix = dgtnix("dgt/libdgtnix.so")
                    self.dgtnix.SetOption(dgtnix.DGTNIX_DEBUG, dgtnix.DGTNIX_DEBUG_ON)
                    # Initialize the driver with port argv[1]
                    result=self.dgtnix.Init(self.dgt_dev_input.text)
                    if result < 0:
                        print "Unable to connect to the device on {0}".format(self.dgt_dev_input.text)
                    else:
                        print "The board was found"
                        self.dgtnix.update()
                        self.dgt_connected = True
                except DgtnixError, e:
                    print "unable to load the library : %s " % e

        settings_panel = Settings() #create instance of Settings

        engine_panel = SettingsPanel(title="Engine") #create instance of left side panel
        board_panel = SettingsPanel(title="Board") #create instance of left side panel
        setup_pos_item = SettingItem(panel=board_panel, title="Input FEN") #create instance of one item in left side panel
        setup_board_item = SettingItem(panel=board_panel, title="Setup Board") #create instance of one item in left side panel
        setup_board_item.bind(on_release=go_to_setup_board)

        database_panel = SettingsPanel(title="Database") #create instance of left side panel
        self.db_open_item = SettingItem(panel=board_panel, title="Open Database") #create instance of one item in left side panel
        self.db_open_item.bind(on_release=self.open_database)

        self.ref_db_open_item = SettingItem(panel=board_panel, title="Open Reference Database") #create instance of one item in left side panel
        self.ref_db_open_item.bind(on_release=self.open_database)

        database_panel.add_widget(self.db_open_item)
        database_panel.add_widget(self.ref_db_open_item)

        dgt_panel = SettingsPanel(title="DGT")
        setup_dgt_item = SettingItem(panel=dgt_panel, title="Input DGT Device (/dev/..)") #create instance of one item in left side panel
#        setup_dgt_item.bind(on_release=on_dgt_dev_input)
        self.dgt_dev_input = TextInput(text="/dev/cu.usbserial-00004006", focus=True, multiline=False, use_bubble = True)
        self.dgt_dev_input.bind(on_text_validate=on_dgt_dev_input)

        setup_dgt_item.add_widget(self.dgt_dev_input)
#        setup_dgt_item.add_widget(connect_dgt_bt)
        dgt_switch = Switch()
        dgt_switch.bind(active=on_dgt_connect)

        connect_dgt_item = SettingItem(panel=dgt_panel, title="Status") #create instance of one item in left side panel
        connect_dgt_item.add_widget(dgt_switch)

        sound_switch = Switch()
        sound_switch.bind(active=on_dgt_sound)

        clock_dgt_item = SettingItem(panel=dgt_panel, title="DGT Clock Sound") #create instance of one item in left side panel
        clock_dgt_item.add_widget(sound_switch)


        dgt_panel.add_widget(setup_dgt_item)
        dgt_panel.add_widget(connect_dgt_item)
        dgt_panel.add_widget(clock_dgt_item)


        fen_input = TextInput(text="", focus=True, multiline=False, use_bubble = True)
#        print Clipboard['application/data']

        def on_level_value(slider, value):
            # self.level_label.text=value
            # print slider.value
            # print type(value)
            self.level_label.text = "%d" % value

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
        level_slider = Slider(min=0, max=20, value=20, step=1)
        level_slider.bind(value=on_level_value)
        self.level_label = Label(text=self.engine_level)
        level_item.add_widget(level_slider)
        level_current = SettingItem(panel=engine_panel, title="Selected Level") #create instance of one item in left side panel
        level_current.add_widget(self.level_label)

        board_panel.add_widget(setup_pos_item) # add item1 to left side panel
        board_panel.add_widget(setup_board_item)

        engine_panel.add_widget(level_item) # add item2 to left side panel
        engine_panel.add_widget(level_current) # add item2 to left side panel

        settings_panel.add_widget(board_panel)
        settings_panel.add_widget(database_panel)
        settings_panel.add_widget(dgt_panel)
        settings_panel.add_widget(engine_panel) #add left side panel itself to the settings menu

        def go_back():
            self.root.current = 'main'
            if self.engine_level != self.level_label.text:
                self.engine_level = self.level_label.text
                sf.set_option('skill level', self.engine_level)

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

    def create_chess_board(self, squares, type="main"):
        if type == "main":
            grid = GridLayout(cols=8, rows=8, spacing=1, padding=(10,10))
        else:
            grid = GridLayout(cols=8, rows=12, spacing=1, size_hint=(1, 1))



        for i, name in enumerate(SQUARES):
            bt = ChessSquare(keep_ratio=True, size_hint_x=1, size_hint_y=1)
            bt.sq = i
            bt.name = name
            if i in light_squares:
                bt.sq_color = "l"
                bt.background_normal = LIGHT_SQUARE+"fir-lite.jpg"
                # marble
                # bt.background_normal = LIGHT_SQUARE+"marble_166.jpg"
            else:
#                bt.background_color = DARK_SQUARE
                bt.background_normal = DARK_SQUARE+"wood-chestnut-oak2.jpg"
                # marble
                # bt.background_normal = DARK_SQUARE+"marble_252.jpg"
                bt.sq_color = "d"
            bt.background_down = bt.background_normal


            if type == "main":
                bt.bind(on_touch_down=self.touch_down_move)
                bt.bind(on_touch_up=self.touch_up_move)
            else:
                bt.bind(on_touch_down=self.touch_down_setup)
                bt.bind(on_touch_up=self.touch_up_setup)


            grid.add_widget(bt)
            squares.append(bt)


        if type!="main":
            for index, i in enumerate([".", ".", ".", ".", ".", ".", ".", ".", ".", "R", "N", "B", "Q", "K", "P",  ".", ".", "r", "n", "b", "q", "k", "p", "."]):
                bt = ChessSquare()
                bt.sq = i
                bt.name = i
                # bt.sq_color = "l"

                if i!=".":
                    piece = ChessPiece(MERIDA+'%s.png' % IMAGE_PIECE_MAP[i])
                    bt.add_piece(piece)

                bt.bind(on_touch_down=self.touch_down_setup)
                bt.bind(on_touch_up=self.touch_up_setup)

                grid.add_widget(bt)

        return grid

    def try_dgt_legal_moves(self, from_fen, to_fen):
        dgt_first_tok = to_fen.split()[0]
        for m in Position(from_fen).get_legal_moves():
            pos = Position(from_fen)
            mi = pos.make_move(m)
            cur_first_tok = str(pos).split()[0]
            if cur_first_tok == dgt_first_tok:
                self.dgt_fen = to_fen
                self.process_move(move=str(m))

                return True


    def update_clocks(self, *args):
        if self.engine_mode == ENGINE_PLAY:
            if self.engine_computer_move:
                self.update_time(color=self.engine_comp_color)
                self.engine_score.children[0].text = THINKING_TIME.format(self.format_time_str(self.time_white), self.format_time_str(self.time_black))
            else:
                self.update_player_time()
                if self.show_hint:
                    if not self.ponder_move_san and self.ponder_move and self.ponder_move!='(none)':
                        # print self.ponder_move
                        try:
                            self.ponder_move_san = self.get_san([self.ponder_move])[0]
                            # print "ponder_move_san: "+self.ponder_move_san
                            # if not self.spoke_hint:
                            #     self.spoke_hint = True
                            #     self.speak_move(self.ponder_move)
                        except IndexError:
                            self.ponder_move_san = "None"
                    if self.ponder_move_san:
                        self.engine_score.children[0].text = YOURTURN_MENU.format(self.ponder_move_san, self.eng_eval, self.format_time_str(self.time_white), self.format_time_str(self.time_black))
                        if not self.spoke_hint:
                            self.spoke_hint = True
                            self.speak_move(self.ponder_move, immediate=True)
                    else:
                        self.engine_score.children[0].text = YOURTURN_MENU.format("Not available", self.eng_eval, self.format_time_str(self.time_white), self.format_time_str(self.time_black))
                else:
                    self.engine_score.children[0].text = YOURTURN_MENU.format("hidden", "hidden", self.format_time_str(self.time_white), self.format_time_str(self.time_black))


    def dgt_probe(self, *args):
        if self.dgt_connected and self.dgtnix:
            try:
                new_dgt_fen = self.dgtnix.GetFen()
    #            print "length of new dgt fen: {0}".format(len(new_dgt_fen))
    #            print "new_dgt_fen just obtained: {0}".format(new_dgt_fen)
                if self.dgt_fen and new_dgt_fen:
                    if new_dgt_fen!=self.dgt_fen:
                        if not self.try_dgt_legal_moves(self.chessboard.position.fen, new_dgt_fen):
                            if self.chessboard.previous_node:
    #                            print new_dgt_fen
    #                            print self.chessboard.previous_node.position.fen
                                dgt_fen_start = new_dgt_fen.split()[0]
                                prev_fen_start = self.chessboard.previous_node.position.fen.split()[0]
                                if dgt_fen_start == prev_fen_start:
                                    self.back('dgt')
                        if self.engine_mode != ENGINE_PLAY and self.engine_mode != ENGINE_ANALYSIS:
                            if len(self.chessboard.variations)>0:
                                self.dgtnix.SendToClock(self.format_move_for_dgt(str(self.chessboard.variations[0].move)), self.dgt_clock_sound, False)

                elif new_dgt_fen:
                    self.dgt_fen = new_dgt_fen
                if self.engine_mode == ENGINE_PLAY and self.engine_computer_move:
                    # Print engine move on DGT XL clock
                    self.dgtnix.SendToClock(self.format_str_for_dgt(self.format_time_str(self.time_white,separator='')+self.format_time_str(self.time_black, separator='')), False, True)

            except Exception:
                    self.dgt_connected = False
                    self.dgtnix=None
                    print traceback.format_exc()

    def update_grid_border(self, instance, width, height):
        with self.grid.canvas.before:
            # grid.canvas.clear()
            Color(0.5, 0.5, 0.5)
            Rectangle(size=Window.size)

    def update_database_display(self, game, ref_game=None):
        game = self.get_grid_click_input(game, ref_game)
        if game == SHOW_GAMES or game == SHOW_REF_GAMES:
            if self.database_display:
                self.database_panel.reset_grid()
            self.database_display = True
            if not self.database_display:
                self.db_stat_label.text = "No Games"
                self.db_adapter.data = {}
            if game == SHOW_REF_GAMES:
                self.use_ref_db = True
                self.update_database_panel()
            else:
                self.use_ref_db = False
                self.update_database_panel()
            # self.update_book_panel()
            # self.database_display = False

    def update_book_display(self, mv, ref_move=None):
        mv = self.get_grid_click_input(mv, ref_move)
        if mv == BOOK_ON:
            if self.book_display:
                self.book_panel.reset_grid()
            self.book_display = not self.book_display
            self.update_book_panel()


    def db_selection_changed(self, *args):
        # print '    args when selection changes gets you the adapter', args
        if len(args[0].selection) == 1:
            game_index = args[0].selection[0].id
            current_pos_hash = self.chessboard.position.__hash__()
            # reset sort criteria if a game is being loaded
            # db_sort_criteria = self.db_sort_criteria
            # self.reset_db_sort_criteria()
            # db_index = self.db_index_book
            # if self.use_ref_db:
            #     db_index = self.ref_db_index_book

            self.load_game_from_index(int(game_index))
            self.go_to_move(None, current_pos_hash)
            # self.db_sort_criteria = db_sort_criteria
            # print args[0].selection[0].text
        # self.selected_item = args[0].selection[0].text

    def reset_db_sort_criteria(self):
        self.db_sort_criteria = []
        self.db_filter_field.text = ""

        for bt in self.db_header_buttons:
            if bt.text.endswith(DB_SORT_DESC) or bt.text.endswith(DB_SORT_ASC):
                bt.text = bt.text[:-2]

    def update_db_sort_criteria(self, label):
        # print label.field
        if label.text.endswith(DB_SORT_DESC):
            label.text = label.text[:-2]+ ' ' +DB_SORT_ASC
            self.db_sort_criteria[0].asc = True
        elif label.text.endswith(DB_SORT_ASC):
            self.db_sort_criteria = []
            label.text = label.text[:-2]
        else:
            self.db_sort_criteria = [DBSortCriteria(label.field, 1, True)]
            label.text += ' ' +DB_SORT_DESC
            self.db_sort_criteria[0].asc = False

        self.update_database_panel()

    def get_token(self, tokens, index):
        try:
            return tokens[index]
        except IndexError:
            return '*'

    def generate_rows(self, rec, record):

        tokens = record.split("|")

        white = self.get_token(tokens, 0)
        whiteelo = self.get_token(tokens, 1)
        black = self.get_token(tokens, 2)
        blackelo = self.get_token(tokens, 3)
        result = self.get_token(tokens, 4)
        date = self.get_token(tokens, 5)
        event = self.get_token(tokens, 6)
        eco = self.get_token(tokens, 8)
        return {'text': rec,
                'size_hint_y': None,
                'size_hint_x': 0.5,
                'height': 30,
                'cls_dicts': [{'cls': CustomListItemButton,
                               'kwargs': {'id': rec.id, 'text': '[color=000000]' + white + '[/color]'}},
                              {'cls': CustomListItemButton,
                               'kwargs': {'id': rec.id, 'text': '[color=000000]' + whiteelo + '[/color]'}},
                              {'cls': CustomListItemButton,
                               'kwargs': {'id': rec.id, 'text': '[color=000000]' + black + '[/color]'}},
                              {'cls': CustomListItemButton,
                               'kwargs': {'id': rec.id, 'text': '[color=000000]' + blackelo + '[/color]'}},
                              {'cls': CustomListItemButton,
                               'kwargs': {'id': rec.id, 'text': '[color=000000]' + result + '[/color]'}},
                              {'cls': CustomListItemButton,
                               'kwargs': {'id': rec.id, 'text': '[color=000000]' + date + '[/color]'}},
                              {'cls': CustomListItemButton,
                               'kwargs': {'id': rec.id, 'text': '[color=000000]' + event + '[/color]'}},
                              {'cls': CustomListItemButton,
                               'kwargs': {'id': rec.id, 'text': '[color=000000]' + eco + '[/color]'}},
                ]
        }

    def generate_empty_rows(self, rec):
        return {'text': rec,
                'size_hint_y': None,
                'size_hint_x': 0.5,
                'height': 30,
                'cls_dicts': []
        }

    def args_conv(self, row_index, rec):
        if not self.database_display:
            return self.generate_empty_rows(rec)

        record = self.get_game_header(rec.id, "ALL")
        return self.generate_rows(rec, record)

    def build(self):
        self.custom_fen = None
        self.pyfish_fen = 'startpos'
        self.variation_dropdown = None
        self.start_pos_changed = False
        self.engine_mode = None
        self.engine_computer_move = True
        self.engine_comp_color = 'b'
        self.engine_level = '20'
        self.time_last = None
        self.dgt_time = None
        self.time_white = 0
        self.time_inc_white = 0
        self.time_black = 0
        self.time_inc_black = 0

        self.from_move = None
        self.to_move = None
        self.db_sort_criteria = []
        self.show_hint = False
        self.speak_move_queue = []
#        PGN Index test
#        index = PgnIndex("kasparov-deep-blue-1997.pgn")
##
#        #print len(index)
#        first = index.get_pos(5)
##        second = index.get_pos(6)
#        #print second
#        f = open("kasparov-deep-blue-1997.pgn")
#        f.seek(first)
#        line = 1
#        lines = []
#        while line:
#            line = f.readline()
##            pos = f.tell()
#            #print pos
##            if pos<=second:
#            lines.append(line)
##            else:
##                break
#
        # games = PgnFile.open("test/french_watson.pgn")
##        first_game = games[5]
#
        self.chessboard = Game()
        self.chessboard_root = self.chessboard
        self.ponder_move = None
        self.ponder_move_san = None
        self.eng_eval = None

        self.train_eng_score = {}

        self.setup_chessboard = Position()
        self.setup_chessboard.clear_board()

        self.squares = []
        self.setup_board_squares = []
        self.use_engine = False
        self.use_ref_db = False
        self.stop_called = False
        # self.engine_running = False
        self.spoke_hint = False
        sf.add_observer(self.update_engine_output)
        # print sf.getOptions()
        sf.set_option('OwnBook','true')
        # Make this an option later
        self.use_tb = False
       # sf.set_option('SyzygyPath', '/Users/shiv/chess/tb/syzygy')

        self.book_display = True
        self.database_display = False
        self.user_book_display = True
        self.last_touch_down_move = None
        self.last_touch_up_move = None
        self.last_touch_down_setup = None
        self.last_touch_up_setup = None
        self.book = polyglot_opening_book.PolyglotOpeningBook('book.bin')
        # self.book = PolyglotOpeningBook("book.bin")

        self.dgt_connected = False
        self.dgtnix = None
        self.dgt_fen = None
        self.dgt_clock_sound = False

        # user book
        try:
            from chess.leveldict import LevelJsonDict
            # import leveldb
            # from chess.leveldict import LevelDict
            self.user_book = LevelJsonDict('book/custom/watson.db')
            self.ref_db_index_book = leveldb.LevelDB('book/polyglot_index.db')
            self.db_index_book = None
#            self.pgn_index = LevelJsonDict('book/test_pgn_index.db')


#            print "Created userbook"
        except ImportError:
            self.user_book = None
            self.db_index_book = None
#            self.pgn_index = None
            print "cannot import leveldb userbook"

        Clock.schedule_interval(self.dgt_probe, 1)
        Clock.schedule_interval(self.update_clocks, 1)

        grandparent = GridLayout(size_hint=(1,1), cols=1, orientation = 'vertical')
        parent = BoxLayout()
        self.grid = self.create_chess_board(self.squares)

        # Dummy params for listener
        self.update_grid_border(0,0,0)
        Window.bind(on_resize=self.update_grid_border)

        self.b = BoxLayout(size_hint=(0.15,0.15))

        back_bt = Button(markeup=True)
        back_bt.text = "<"

        back_bt.bind(on_press=self.back)
        self.b.add_widget(back_bt)

        self.prev_move = Label(markup=True,font_name='img/CAChess.ttf',font_size=16)
        self.b.add_widget(self.prev_move)

        fwd_bt = Button(markeup=True)
        fwd_bt.text = ">"

        fwd_bt.bind(on_press=self.fwd)
        self.b.add_widget(fwd_bt)

        comment_bt = Button(markup=True)
        comment_bt.text = "!?"

        comment_bt.bind(on_press=self.comment)
        self.b.add_widget(comment_bt)

        new_bt = Button(markeup=True)
        new_bt.text = "New"

        new_bt.bind(on_press=self.new)
        self.b.add_widget(new_bt)


        save_bt = Button(markup=True)
        save_bt.text = "Save"

        save_bt.bind(on_press=self.save)
        self.b.add_widget(save_bt)

        settings_bt = Button(markup=True, text='Setup')
        settings_bt.bind(on_press=self.go_to_settings)
        self.b.add_widget(settings_bt)

        parent.add_widget(self.grid)

        self.info_grid = GridLayout(cols=1, rows=4, spacing=5, padding=(8, 8), orientation='vertical')
        self.info_grid.add_widget(self.b)

        self.game_score = ScrollableLabel('[color=000000][b]%s[/b][/color]' % GAME_HEADER, font_name='img/CAChess.ttf',
                                          font_size=17, ref_callback=self.go_to_move)

        self.info_grid.add_widget(self.game_score)

        self.engine_score = ScrollableLabel(ENGINE_HEADER, font_name='img/CAChess.ttf', font_size=17, ref_callback=self.add_eng_moves)
        self.info_grid.add_widget(self.engine_score)

        # book_grid = GridLayout(cols = 2, rows = 1, spacing = 1, size_hint=(0.3, 1))

        self.book_panel = ScrollableGrid([['Move', 'center', 'center', 'string', 0.3, 'visible'],
                                         ['Weight', 'center', 'left', 'option', 0.3, 'visible']],
                                         '',
                                         '',
                                         top_level_header=['Book', 'center', 'center', 'string', 0.4, 'visible'], callback=self.update_book_display)

        self.info_grid.add_widget(self.book_panel)
        integers_dict = \
        {str(i): {'text': str(i), 'is_selected': False} for i in range(100)}
        # print integers_dict

        self.db_adapter = ListAdapter(
                           data=integers_dict,
                           args_converter=self.args_conv,
                           selection_mode='single',
                           # propagate_selection_to_data=True,
                           allow_empty_selection=True,
                           cls=CompositeListItem)


        self.database_list_view = ListView(adapter=self.db_adapter)
        self.database_list_view.adapter.bind(on_selection_change=self.db_selection_changed)

        # self.add_widget(list_view)

        self.database_panel = ScrollableGrid([['White', 'center', 'center', 'string', 0.1, 'hidden'],
                                         ['Elo', 'center', 'center', 'string', 0.1, 'visible'],

                                         ['Black', 'center', 'left', 'option', 0.1, 'visible'],
                                         ['Elo', 'center', 'center', 'string', 0.1, 'visible'],

                                         ['Result', 'center', 'left', 'option', 0.1, 'visible'],
                                         ['Event', 'center', 'left', 'option', 0.1, 'visible'],
                                         # ['Site', 'center', 'left', 'option', 0.1, 'visible'],

                                         ['Date', 'center', 'left', 'option', 0.1, 'visible'],
                                         ['Eco', 'center', 'left', 'option', 0.1, 'visible'],
                                         # ['Round', 'center', 'left', 'option', 0.1, 'visible'],
                                         ['Ply', 'center', 'left', 'option', 0.1, 'visible']
                                             ],
                                         '',
                                         '',
                                         top_level_header=['Database', 'center', 'center', 'string', 0.1, 'hidden'], callback=self.update_database_display)
# ['Event', 'Site', 'Date', 'White', 'Black', 'Result', 'PlyCount', 'ECO', 'Round', 'EventDate', 'WhiteElo', 'BlackElo', 'PlyCount'
            # ScrollableLabel(DATABASE_HEADER.format(DATABASE_ON), ref_callback=self.database_action)
#        info_grid.add_widget(self.database_panel)
#        info_grid.add_widget(self.user_book_panel)

        # info_grid.add_widget(book_grid)

        # parent.add_widget(Label(size_hint=(0.5,1)))
        parent.add_widget(self.info_grid)
        grandparent.add_widget(parent)
        database_grid = BoxLayout(size_hint=(1, 0.4), orientation='vertical')

        database_controls = BoxLayout(size_hint=(1, 0.25))
        ref_db_label = Button(text=SHOW_REF_GAMES, on_press=self.update_database_display)
        db_label = Button(text=SHOW_GAMES, on_press=self.update_database_display)

        self.db_filter_field = TextInput(text="", focus=True, multiline=False, use_bubble = True)
        self.db_filter_field.bind(on_text_validate=self.update_book_panel)

        self.db_random_game_btn = Button(text="Load Random Game", on_press=self.load_random_game)

        self.db_stat_label = Label(text="No Games")

        database_controls.add_widget(ref_db_label)
        database_controls.add_widget(db_label)
        database_controls.add_widget(self.db_filter_field)
        database_controls.add_widget(self.db_random_game_btn)

        database_controls.add_widget(self.db_stat_label)

        database_header = BoxLayout(size_hint=(1, 0.15))
        self.db_header_buttons = []
        database_white_bt = DBHeaderButton("white", markup=True, text="White", on_press=self.update_db_sort_criteria)
        self.db_header_buttons.append(database_white_bt)
        database_whiteelo_bt = DBHeaderButton("whiteelo", markup=True, text="Elo", on_press=self.update_db_sort_criteria)
        self.db_header_buttons.append(database_whiteelo_bt)

        database_black_bt = DBHeaderButton("black", markup=True, text="Black", on_press=self.update_db_sort_criteria)
        self.db_header_buttons.append(database_black_bt)

        database_blackelo_bt = DBHeaderButton("blackelo", markup=True, text="Elo", on_press=self.update_db_sort_criteria)
        self.db_header_buttons.append(database_blackelo_bt)

        database_result_bt = DBHeaderButton("result", markup=True, text="Result", on_press=self.update_db_sort_criteria)
        self.db_header_buttons.append(database_result_bt)

        database_date_bt = DBHeaderButton("date", markup=True, text="Date", on_press=self.update_db_sort_criteria)
        self.db_header_buttons.append(database_date_bt)

        database_event_bt = DBHeaderButton("event", markup=True, text="Event", on_press=self.update_db_sort_criteria)
        self.db_header_buttons.append(database_event_bt)

        database_eco_bt = DBHeaderButton("eco", markup=True, text="ECO", on_press=self.update_db_sort_criteria)
        self.db_header_buttons.append(database_eco_bt)

        for i in self.db_header_buttons:
            database_header.add_widget(i)

        database_grid.add_widget(database_controls)
        database_grid.add_widget(database_header)
        database_grid.add_widget(self.database_list_view)
        grandparent.add_widget(database_grid)
        self.refresh_board()

        platform = kivy.utils.platform()
        if self.is_desktop():
            self._keyboard = Window.request_keyboard(
                self._keyboard_closed, self)
            self._keyboard.bind(on_key_down=self._on_keyboard_down)
            # Clock.schedule_interval(self.update_engine_output, 0.01)

            # self.start_engine_thread()
        sm = ScreenManager(transition=SlideTransition())
        board_screen = Screen(name='main')
        board_screen.add_widget(grandparent)
        sm.add_widget(board_screen)

        settings_screen = SettingsScreen(name='settings')
        settings_screen.add_widget(self.generate_settings())

        sm.add_widget(settings_screen)

        setup_board_screen = Screen(name='setup_board')
        setup_widget = self.create_chess_board(self.setup_board_squares, type="setup")

        def go_to_main_screen(value):
            if self.root:
                self.root.current = 'main'

        def setup_board_change_tomove(value):
            if value.state == "normal":
                # print "black to move"
                self.setup_chessboard.turn = 'b'
            else:
                # print "white to move"
                self.setup_chessboard.turn = 'w'

        def render_setup_board(bt):
            if bt.text == "Clear":
                self.setup_chessboard.clear_board()
#                clearBoard()
            elif bt.text == "DGT":
                if self.dgt_fen:
                    fen = self.dgt_fen.split()[0]
                    fen+=" {0} KQkq - 0 1".format(self.setup_chessboard.turn)
                    self.setup_chessboard = Position(fen)

            else:
                self.setup_chessboard.reset()
#            squares = [item for sublist in self.setup_chessboard.getBoard() for item in sublist]
#            for i, p in enumerate(squares):
#                self.fill_chess_board(self.setup_board_squares[i], p)

            for i, p in enumerate(SQUARES):
                self.fill_chess_board(self.setup_board_squares[i], self.setup_chessboard[p])

        def validate_setup_board(value):

            fen = str(self.setup_chessboard.fen)
            can_castle = False
            castling_fen = ''

            if self.setup_chessboard[Square("e1")]==Piece("K") and self.setup_chessboard[Square("h1")]==Piece("R"):
                can_castle = True
                castling_fen+='K'

            if self.setup_chessboard[Square("e1")]==Piece("K") and self.setup_chessboard[Square("a1")]==Piece("R"):
                can_castle = True
                castling_fen+='Q'

            if self.setup_chessboard[Square("e8")]==Piece("k") and self.setup_chessboard[Square("h8")]==Piece("r"):
                can_castle = True
                castling_fen+='k'

            if self.setup_chessboard[Square("e8")]==Piece("k") and self.setup_chessboard[Square("a8")]==Piece("r"):
                can_castle = True
                castling_fen+='q'

            if not can_castle:
                castling_fen = '-'

            # TODO: Support fen positions where castling is not possible even if king and rook are on right squares
            fen = fen.replace("KQkq", castling_fen)
            if fen == INITIAL_BOARD_FEN:
                # print "new game.."
                self.chessboard = Game()
#                self.chessboard.resetBoard()
                self.refresh_board()
                self.root.current = 'main'
            else:
                g = Game()
                bag = GameHeaderBag(game=g, fen=fen)
                g.set_headers(bag)
                self.chessboard = g
                self.chessboard_root = self.chessboard

                self.start_pos_changed = True
                self.custom_fen = fen

                self.refresh_board()
                self.root.current = 'main'

        wtm = ToggleButton(text="White to move", state="down", on_press=setup_board_change_tomove)
        setup_widget.add_widget(wtm)

        clear = Button(text="Clear", on_press=render_setup_board)
        setup_widget.add_widget(clear)

        initial = Button(text="Initial", on_press=render_setup_board)
        setup_widget.add_widget(initial)

        dgt = Button(text="DGT", on_press=render_setup_board)
        setup_widget.add_widget(dgt)

        validate = Button(text="OK", on_press=validate_setup_board)
        setup_widget.add_widget(validate)

        cancel = Button(text="Cancel", on_press=go_to_main_screen)
        setup_widget.add_widget(cancel)

        setup_board_screen.add_widget(setup_widget)
        sm.add_widget(setup_board_screen)

        return sm

    def go_to_settings(self, instance):
        self.root.current='settings'

    def go_to_move(self, label, pos_hash):
        if GameNode.positions.has_key(pos_hash):
            self.chessboard = GameNode.positions[pos_hash]
            self.refresh_board()

    def is_position_inf_eval(self, mv):
        for p in pos_evals:
            if p.informant_eval == mv:
                return True
        return False

    def convert_inf_eval_to_int(self, inf):
         for i, p in enumerate(pos_evals):
            if p.informant_eval == inf:
               return p.integer_eval

    def convert_int_eval_to_inf(self, int_eval):
         for i, p in enumerate(pos_evals):
            if p.integer_eval == int_eval:
               return p.informant_eval

    def toggle_position_eval(self, inf_eval=None, int_eval=None):
        if inf_eval and int_eval:
            raise ValueError("Only one of inf_eval or int_eval is expected as a keyword arg")
        for i, p in enumerate(pos_evals):
            if p.informant_eval == inf_eval:
                if i == len(pos_evals)-1:
                    return pos_evals[0].informant_eval
                else:
                    return pos_evals[i+1].informant_eval
            if p.integer_eval == int_eval:
                if i == len(pos_evals)-1:
                    return pos_evals[0].integer_eval
                else:
                    return pos_evals[i+1].integer_eval

    def update_user_book_positions(self, color="white", delete = False):
        game = self.chessboard
        while game.previous_node:
            prev = game.previous_node
            move = game.move
            move = str(move)
            # curent_pos_hash = str(game.position.__hash__())
            # print "move:{0}".format(move)
            prev_pos_hash = str(prev.position.__hash__())
            if prev_pos_hash not in self.user_book:
                v = {"moves":[move], "annotation":"", "color" : [color],
                 "eval": 5, "games":[], "misc":""}
                # print "not in book"
                self.user_book[prev_pos_hash] = v
            else:

                j = self.user_book[prev_pos_hash]
                # print "prev_pos_hash:"
                # print prev_pos_hash
                # print "book_moves:"
                # print j
                if move not in j["moves"]:
                    # print "move not in book"
                    moves = j["moves"]
                    moves.append(move)
                    j["moves"] = moves
                    if color not in j["color"]:
                        j["color"].append(color)
                    self.user_book[prev_pos_hash] = j
                else:
                    if delete:
                        moves = j["moves"]
                        moves.remove(move)
                        j["moves"] = moves
                        self.user_book[prev_pos_hash] = j

                        # c = self.user_book[curent_pos_hash]
                        # c["color"]=[]
                        # self.user_book[curent_pos_hash] = c
                # else:
                    # print "move already in book"
            if not delete:
                game = game.previous_node
            else:
                return


    def get_ref_tags(self, t):
        m = MarkupLabel(text=t.text)
        ref_tags = []
        for s in m.markup:
            if s.startswith(REF_) and s.endswith(']'):
                ref_tags.append(s.split(REF_)[1].strip(']'))

        return ref_tags


    def get_grid_click_input(self, mv, ref_move):
        if ref_move:
            mv = ref_move
        else:
            tags = self.get_ref_tags(mv)
            if tags:
                mv = tags[0]
            else:
                mv = mv.text
        return mv

    def load_random_game(self, x):
        db_index = self.db_index_book
        if self.use_ref_db:
            db_index = self.ref_db_index_book

        total_games = int(db_index.Get(INDEX_TOTAL_GAME_COUNT))

        rand_game_num = random.randint(0, total_games)
        self.load_game_from_index(rand_game_num)


    def load_game_from_index(self, game_num):
        db_index = self.db_index_book
        if self.use_ref_db:
            db_index = self.ref_db_index_book

        first = db_index.Get("game_{0}_data".format(game_num)).split("|")[DB_HEADER_MAP[INDEX_FILE_POS]]

#        if game_num+1 < self.pgn_index[INDEX_TOTAL_GAME_COUNT]:
#            second = self.db_index_book.Get("game_{0}_{1}".format(game_num+1,INDEX_FILE_POS))

#        second = self.pgn_index["game_index_{0}".format(game_num+1)][INDEX_FILE_POS]
        try:
            second = db_index.Get("game_{0}_data".format(game_num+1)).split("|")[DB_HEADER_MAP[INDEX_FILE_POS]]
            second = int(second)
        except KeyError:
            second = None

        with open(db_index.Get("pgn_filename")) as f:
            first = int(first)

            f.seek(first)
            line = 1
            lines = []
            while line:
                line = f.readline()
                pos = f.tell()
                if second and pos >= second:
                    break
                # print pos
                lines.append(line)
        # f.close()
        # print lines
        games = PgnFile.open_text(lines)
        # print games[0].'White'
        self.chessboard = games[0]
        # print self.chessboard.headers.headers
        self.chessboard_root = self.chessboard
        self.refresh_board()

        # self.game_score = games[0]

    def add_book_moves_white(self, mv, ref_move = None):
        self.add_book_moves(mv, ref_move=ref_move, color="white")

    def add_book_moves_black(self, mv, ref_move = None):
        self.add_book_moves(mv, ref_move=ref_move, color="black")

    def add_book_moves(self, mv, ref_move=None, color="white"):
        mv = self.get_grid_click_input(mv, ref_move)
        # print "mv:"+str(mv)
        # if mv ==
        if str(mv) == DELETE_FROM_USER_BOOK:
            self.update_user_book_positions(delete=True, color=color)
            self.update_book_panel()
        elif str(mv) == ADD_TO_USER_BOOK:
            self.update_user_book_positions(color=color)
            self.update_book_panel()
        elif self.is_position_inf_eval(mv):
            # print "is_pos_eval"
            # print "is_pos_eval"
            ev = self.toggle_position_eval(inf_eval=mv)
            # print ev
            # print int_eval_symbol[ev]
            self.update_book_panel(ev=ev)
        else:
            self.add_try_variation(str(mv).encode("utf-8"))
            # self.chessboard.addTextMove(mv)
            self.refresh_board()

    def stop_engine(self):
        sf.stop()
        # print "stopping engine"
        # sleep(1)

        self.use_engine = False
        self.engine_score.children[0].text = ENGINE_HEADER
        # self.refresh_board()
        # print "Stopping engine"

    def reset_clock_update(self):
        self.time_last = datetime.datetime.now()

    def time_add_increment(self, color='w'):
        if color == 'w':
            self.time_white+=self.time_inc_white
        else:
            self.time_black+=self.time_inc_black

    def update_time(self, color='w'):
        current = datetime.datetime.now()
        seconds_elapsed = (current - self.time_last).total_seconds()
#        print "seconds_elapsed:{0}".format(seconds_elapsed)
        self.time_last = current
        if color == 'w':
            self.time_white-=seconds_elapsed
        else:
            self.time_black-=seconds_elapsed

    def reset_clocks(self):
#        self.white_time_now = time.clock()
#        self.black_time_now = time.clock()
        self.time_last = datetime.datetime.now()

        self.time_white = 60
        self.time_inc_white = 3
        self.time_black = 420
        self.time_inc_black = 8
        if self.engine_comp_color == 'b':
            # Swap time allotments if comp is black (comp gets less time)
            self.time_white, self.time_black = self.time_black, self.time_white
            self.time_inc_white, self.time_inc_black = self.time_inc_black, self.time_inc_white

    def add_eng_moves(self, instance, value):
#        print "value:"
#        print value
#        print "instance:"
#        print instance
        if value == ENGINE_ANALYSIS or value == ENGINE_PLAY or value == ENGINE_TRAINING:
#            print "Bringing up engine menu"
            if self.use_engine:
                self.stop_engine()
            else:
                self.use_engine = True
                self.engine_mode = value
                if value == ENGINE_PLAY:
                    self.engine_computer_move = True
                    self.engine_comp_color = self.chessboard.position.turn
                    self.reset_clocks()

            # self.refresh_board()
        elif value == ENGINE_PLAY_STOP:
#            self.stop_engine()
            if self.engine_mode == ENGINE_PLAY:
                self.engine_mode = ENGINE_ANALYSIS
            elif self.engine_mode == ENGINE_TRAINING:
                # Reset Skill level
                sf.set_option('skill level', '20')
                self.engine_mode = None
                # print "Stopping train"
                self.use_engine = False
                self.engine_score.children[0].text = ENGINE_HEADER
            # self.refresh_board()
        elif value == ENGINE_PLAY_HINT:
            self.show_hint = True
        else:
            for i, mv in enumerate(self.engine_score.can_line):
                # if i >= 1:
                #     break
                self.add_try_variation(mv)

        self.refresh_board()

    def is_desktop(self):
        platform = kivy.utils.platform()
#        print platform
        return True if platform.startswith('win') or platform.startswith('linux') or platform.startswith('mac') else False

    def is_mac(self):
        platform = kivy.utils.platform()
        return True if platform.startswith('mac') else False

    def new(self, obj):
        self.chessboard = Game()
        self.chessboard_root = self.chessboard
        self.refresh_board(update=True)

    def comment(self, obj):
        print "Comment button clicked"

    def back(self, obj):
        if self.chessboard.previous_node:
            self.chessboard = self.chessboard.previous_node
            self.refresh_board(update=False)

    def _keyboard_closed(self):
#        print 'My keyboard have been closed!'
        self._keyboard.unbind(on_key_down=self.back)
        self._keyboard = None

    def parse_bestmove(self, line):
#        print "line:{0}".format(line)
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

    def get_score(self, line):
        tokens = line.split()
        try:
            score_index = tokens.index('score')
        except ValueError, e:
            score_index = -1
        score = None
        depth = None
        score_type = ""
        # print line
        if score_index != -1:
            try:
                depth_index = tokens.index('depth') + 1
                depth = int(tokens[depth_index])
            except ValueError as e:
                # print "No depth"
                depth = None
            score_type = tokens[score_index + 1]
            if tokens[score_index + 1] == "cp":
                score = float(tokens[score_index + 2]) / 100 * 1.0
                try:
                    score = float(score)
                except ValueError, e:
                    print "Cannot convert score to a float"
                    print e
            elif tokens[score_index + 1] == "mate":
                score = int(tokens[score_index + 2])
                try:
                    score = int(score)
                except ValueError, e:
                    print "Cannot convert Mate number of moves to a int"
                    print e

            # print self.chessboard.position.turn
            if self.chessboard.position.turn == 'b':
                if score:
                    score *= -1
            if score_type == "mate":
                score = score_type + " " + str(score)
        return depth, score

    def get_san(self, moves, figurine=False):
        prev_fen = sf.get_fen(self.pyfish_fen,  self.chessboard.get_prev_moves())

        move_list = sf.to_san(prev_fen, moves)
        if figurine:
            for i, m in enumerate(move_list):
                m = self.convert_san_to_figurine(m)
                move_list[i] = m
        return move_list

    def parse_score(self, line, figurine=False):
        # print line
        depth, score = self.get_score(line)
        move_list = []
        can_move_list = []
        tokens = line.split()
        # print tokens
        first_mv = None
        try:
            line_index = tokens.index('pv')
            first_mv = tokens[line_index+1]
            # prev_fen = sf.get_fen(self.pyfish_fen,  self.chessboard.get_prev_moves())
            # # print prev_fen
            # move_list = sf.to_san(prev_fen, tokens[line_index+1:])
            move_list = self.get_san(tokens[line_index+1:], figurine=True)
            can_move_list = tokens[line_index+1:]
            # print move_list
        except ValueError, e:
            line_index = -1
            # raise
        variation = self.generate_move_list(move_list,start_move_num=self.chessboard.half_move_num) if line_index!=-1 else None

        #del analysis_board
        if variation and score is not None:
            if self.use_tb and score == 151:
                score = "Tablebase [b]1-0[/b]"
            elif self.use_tb and score == -151:
                score = "Tablebase [b]0-1[/b]"
            else:
                score = "[b]{0}[/b]".format(score)

            return first_mv, can_move_list, move_list, "[color=000000]%s     [i][ref=%s]Stop[/ref][/i][/color]\n[color=000000]%s[/color]" %(score, ENGINE_ANALYSIS, "".join(variation))
        # else:
        #     print "no score/var"
        #     print variation
        #     print score


    def format_time_str(self,time_a, separator='.'):
        return "%d%s%02d" % (int(time_a/60), separator, int(time_a%60))


    def speak_move(self, best_move, immediate=False):
        if self.is_mac():
            # print "best_move:{0}".format(best_move)
            # print sf.position()
            try:
                san = self.get_san([best_move])[0]
            except IndexError:
                return
            # print san
            spoken_san = san
            spoken_san = spoken_san.replace('O-O-O', ' castles long ')
            spoken_san = spoken_san.replace('+', ' check ')

            for k, v in SPOKEN_PIECE_SOUNDS.iteritems():
                spoken_san = spoken_san.replace(k, v)
            spoken_san = spoken_san.replace('x', ' captures ')
            spoken_san = spoken_san.replace('=', ' promotes to ')
            # print spoken_san
            if immediate:
                os.system("say " + spoken_san)
            else:
                if spoken_san not in self.speak_move_queue:
                    self.speak_move_queue.append(spoken_san)
            # os.system("say " + spoken_san)

    def update_engine_output(self, line):
        # if not self.uci_engine:
            # self.start_engine()
        # # while True:
        # print line
        if self.use_engine:
            output = self.engine_score
            if self.engine_mode == ENGINE_ANALYSIS:
                out_score = self.parse_score(line, figurine=True)
                #out_score = None
                if out_score:
                    first_mv, can_line, raw_line, cleaned_line = out_score

                    if self.dgt_connected and self.dgtnix:
                        # Display score on the DGT clock
                        depth, score = str(self.get_score(line))
                        if score.startswith("mate"):
                            score = score[4:]
                            score = "m "+score
                        score = score.replace("-", "n")
                        self.dgtnix.SendToClock(self.format_str_for_dgt(score), False, True)
                        if first_mv:
                            sleep(1)
                            self.dgtnix.SendToClock(self.format_move_for_dgt(first_mv), False, False)

                    if cleaned_line:
                        output.children[0].text = cleaned_line
                    if raw_line:
                        output.raw = raw_line
                    if can_line:
                        output.can_line = can_line
            elif self.engine_mode == ENGINE_PLAY:
                if self.engine_computer_move:
                    best_move, self.ponder_move = self.parse_bestmove(line)
    #                            print "ponder_move:{0}".format(self.ponder_move)

                    depth, score = self.get_score(line)
                    if score:
                        self.eng_eval = score
                    # self.update_time(color=self.engine_comp_color)
                    if best_move:
                        # print "comp best_move:{0}".format(best_move)
                        # self.speak_move(best_move)

                        # self.chessboard = self.chessboard.add_variation(Move.from_uci(best_move))

                        self.process_move(best_move)
                        # self.engine_computer_move = False
                        # self.engine_running = False

                        # self.refresh_board(spoken=True)
                        self.time_add_increment(color=self.engine_comp_color)
                        if self.dgt_connected and self.dgtnix:
                            # Print engine move on DGT XL clock
                            self.dgtnix.SendToClock(self.format_move_for_dgt(best_move), self.dgt_clock_sound, False)
                        self.show_hint = False
                        self.spoke_hint = False
                        self.ponder_move_san = None
                        # se(best_move)
            elif self.engine_mode == ENGINE_TRAINING:

                output.children[0].text = THINKING
                best_move, self.ponder_move = self.parse_bestmove(line)
    #                            print "best_move:{0}".format(best_move)
    #                            print "ponder_move:{0}".format(self.ponder_move)

                depth, score = self.get_score(line)
                # print score

                if depth:
                    self.train_eng_score[depth] = score
                    # print "depth : {0}".format(depth)
                if best_move:
                    # print "best_move"
                    # print "training_score : {0}".format(score)
                    random_depth = random.randint(3, 10)
                    # print "random_depth : {0}".format(random_depth)
                    san = self.get_san([best_move])[0]
                    # print "san :{0}".format(san)
                    score = ""
                    if self.train_eng_score.has_key(random_depth):
                        score = self.train_eng_score[random_depth]
                    output.children[0].text = TRAIN_MENU.format(san, score)
                    self.train_eng_score = {}


        # else:
        #     print line
        #     best_move, self.ponder_move = self.parse_bestmove(line)
        #     if best_move:
        #         self.engine_running = False

    def format_str_for_dgt(self, s):
        while len(s)>6:
            s = s[:-1]
        while len(s) < 6:
            s = " " + s
        return s

    def format_move_for_dgt(self, s):
        mod_s = s[:2]+' '+s[2:]
        if len(mod_s)<6:
            mod_s+=" "
        return mod_s

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if self.root.current != "main":
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
        # return False

    def select_variation(self, i):
        try:
            i = int(i)
            self.chessboard = self.chessboard.variations[i]
            self.refresh_board(update=False)
        except IndexError:
            pass


    def fwd(self, obj):
        try:
            self.chessboard = self.chessboard.variations[0]
            self.refresh_board(update=False)
        except IndexError:
            pass
            # TODO: log error if in debug mode

    def save(self, obj):
        use_db = False
        pgn_file = None
        if self.db_index_book is not None:
            use_db = True
            # Write to the open database
            pgn_file = self.db_index_book.Get("pgn_filename")
            f = open(pgn_file, 'ab')
        else:
            f = open('game.pgn', 'wb')
#        f.write('Game Header - Analysis \n\n')
        f.write(self.chessboard_root.game_score(format="file"))
#        f.write("\n")
        f.close()
        if use_db:
            # Rebuild index
            # db_folder_path = os.path.abspath(os.path.join(pgn_file, os.pardir))
            db_folder_path = self.gen_leveldb_path(pgn_file)
            del self.db_index_book
            self.db_index_book = None
            # shutil.rmtree(db_folder_path)
            command = "polyglot make-book -pgn '{0}' -leveldb '{1}' -min-game 1".format(pgn_file, db_folder_path)
            # print command
            os.system(command)
            self.db_index_book = leveldb.LevelDB(db_folder_path)

    def touch_down_move(self, img, touch):
        if not img.collide_point(touch.x, touch.y):
            return

        # print "touch_move"
        # print touch
        mv = img.name
        squares = self.chessboard.position

        if squares[mv]:
            self.last_touch_down_move = mv

    def touch_down_setup(self, img, touch):
        if not img.collide_point(touch.x, touch.y):
            return
            # print "touch_move"
        # print touch
        mv = img.name
        self.last_touch_down_setup = mv

    def touch_up_setup(self, img, touch):
        if not img.collide_point(touch.x, touch.y):
            return
        self.last_touch_up_setup = img.name
        if self.last_touch_up_setup and self.last_touch_down_setup and self.last_touch_up_setup != self.last_touch_down_setup:
#            print "touch_down_setup:"
#            print self.last_touch_down_setup
#            # print len(self.last_touch_down_setup)
#            print "touch_up_setup:"
#            print self.last_touch_up_setup
            # print len(self.last_touch_up_setup)
            if len(self.last_touch_down_setup)==1 and len(self.last_touch_up_setup)==2:
                sq = Square(self.last_touch_up_setup)
                self.setup_chessboard[sq] = Piece(self.last_touch_down_setup)
                self.fill_chess_board(self.setup_board_squares[SQUARES.index(self.last_touch_up_setup)], self.setup_chessboard[self.last_touch_up_setup])

            elif len(self.last_touch_down_setup)==2 and len(self.last_touch_up_setup)==1:
                del self.setup_chessboard[self.last_touch_down_setup]
                self.fill_chess_board(self.setup_board_squares[SQUARES.index(self.last_touch_down_setup)], self.setup_chessboard[self.last_touch_down_setup])

            elif len(self.last_touch_down_setup)==2 and len(self.last_touch_up_setup)==2:
                sq = Square(self.last_touch_up_setup)
                self.setup_chessboard[sq] = self.setup_chessboard[Square(self.last_touch_down_setup)]
                self.fill_chess_board(self.setup_board_squares[SQUARES.index(self.last_touch_up_setup)], self.setup_chessboard[self.last_touch_up_setup])
                del self.setup_chessboard[self.last_touch_down_setup]
                self.fill_chess_board(self.setup_board_squares[SQUARES.index(self.last_touch_down_setup)], self.setup_chessboard[self.last_touch_down_setup])

    def touch_up_move(self, img, touch):
        if not img.collide_point(touch.x, touch.y):
            return
        # print "touch_move"
        # print touch
#        mv = img.name
        self.last_touch_up_move = img.name
        if self.last_touch_up_move and self.last_touch_down_move and self.last_touch_up_move != self.last_touch_down_move:
            self.process_move()

    def add_try_variation(self, move):
        try:
            if type(move) is str:
                self.chessboard = self.chessboard.add_variation(Move.from_uci(move))
            else:
                self.chessboard = self.chessboard.add_variation(move)
        except ValueError:
            for v in self.chessboard.variations:
                if str(v.move) == move:
                    self.chessboard = v

    def update_player_time(self):
        color = 'w'
        if self.engine_comp_color == 'w':
            color = 'b'
        self.update_time(color=color)

    def update_player_inc(self):
        color = 'w'
        if self.engine_comp_color == 'w':
            color = 'b'
        self.time_add_increment(color=color)

    def is_promotion(self, move):
        from_rank = move[1]
        to_rank = move[3]
        from_sq = move[:2]

        if from_rank == '7' and to_rank == '8' and self.chessboard.position[Square(from_sq)] == Piece("P"):
            return True

        if from_rank == '2' and to_rank == '1' and self.chessboard.position[Square(from_sq)] == Piece("p"):
            return True
        return False

    def add_promotion_info(self, move):
        # Promotion info already present?
        if len(move) > 4:
            return move
        else:
            # Auto queen for now
            return move + "q"

    def process_move(self, move=None):
        # print "process_move"
        # print "move:{0}".format(move)

#        if self.chessboard.addTextMove(self.last_touch_down_move+self.last_touch_up_move):
        try:
            if not move:
                move = self.last_touch_down_move+self.last_touch_up_move
            # print "move:{0}".format(move)
            if self.is_promotion(move):
                move = self.add_promotion_info(move)

            if self.engine_mode == ENGINE_PLAY:
                if not self.engine_computer_move:
                    # self.update_player_time()
                    self.update_player_inc()
                    # self.speak_move_queue.append(move)
                    self.engine_computer_move = True
                else:
                    self.engine_computer_move = False
            if self.engine_mode == ENGINE_PLAY:
                self.speak_move(move)
                self.add_try_variation(move)
                self.refresh_board(spoken=True)
            else:
                self.add_try_variation(move)
                self.refresh_board()
        except Exception, e:
            print e
            raise
            # TODO: log error

    def generate_move_list(self, all_moves, start_move_num = 1, raw = False):
        score = ""
        if raw:
             return " ".join(all_moves)
        for i, mv in it.izip(it.count(start_move_num), all_moves):
            move = "b"
            if i % 2 == 1:
                score += " %d. " % ((i + 1) / 2)
                move = "w"

            if mv:
                if raw:
                    score += " % s" % mv
                    if i % 5 == 0:
                        score += "\n"
                else:
                    score += " [ref=%d:%s] %s [/ref]"%((i + 1) / 2, move, mv)
        return score


    def database_action(self):
        print "action"
        pass

    def get_game_header(self, g, header, first_line=False):

        try:
            ref_db = self.use_ref_db
            if ref_db:
                record = self.ref_db_index_book.Get("game_{0}_data".format(g))
            else:
                record = self.db_index_book.Get("game_{0}_data".format(g))
            if header == "ALL":
                return record
            text = ""
            text = record.split("|")[DB_HEADER_MAP[header]]
            # try:
            #     j = json.loads(record, "latin-1")
            #     text = j[header]
            # except UnicodeDecodeError:
            #     print record
            # except ValueError:
            #     print record
            #     j = json.loads(repair_json(record), "latin-1")
            #     text = j[header]

            # text = self.db_index_book.Get("game_{0}_{1}".format(g,header))
            if first_line:
#                text = self.pgn_index["game_index_{0}".format(g)][header]
                if "," in text:
                    return text.split(",")[0]
            return text
#            return self.pgn_index["game_index_{0}".format(g)][header]
        except KeyError:
            return "Unknown"

    def update_database_panel(self):
        pos_hash = str(self.chessboard.position.__hash__())
        # pos_hash = str(sf.key())
        if self.use_ref_db:
            db_index = self.ref_db_index_book
        else:
            db_index = self.db_index_book
        if db_index is not None and self.database_display:
            try:
                game_ids = db_index.Get(pos_hash).split(',')[:-1]

            except KeyError, e:
                print "key not found!"
                game_ids = []

            db_game_list = []
            filter_text = []
            db_operator = ["-", " "]
            db_text = self.db_filter_field.text
            if db_text:
                operator_match = False
                for op in db_operator:
                    if op in db_text:
                        filter_tokens = db_text.split(op)
                        for i, f in enumerate(filter_tokens):
                            filter_tokens[i] = f.strip()
                        filter_text = filter_tokens
                        operator_match = True
                        break
                if not operator_match:
                    filter_text = [db_text]

            for i in game_ids:
                db_game = DBGame(i)
                if self.db_sort_criteria or len(filter_text) > 0:
                    record = self.get_game_header(i, "ALL")
                    tokens = record.split("|")
                    db_game.white = tokens[0]
                    db_game.whiteelo = tokens[1]
                    db_game.black = tokens[2]
                    db_game.blackelo = tokens[3]
                    db_game.result = tokens[4]
                    db_game.date = tokens[5]
                    db_game.event = tokens[6]
                    db_game.site = tokens[7]
                    db_game.eco = tokens[8]
                if len(filter_text) > 0:
                    match = True
                    # print filter_text
                    for f in filter_text:
                        if f in db_game.white or f in db_game.black or f in db_game.event or f in db_game.site:
                            pass
                        else:
                            match = False
                    if match:
                        db_game_list.append(db_game)
                            # db_game_list.append(db_game)
                else:
                    db_game_list.append(db_game)


            if self.db_sort_criteria:
                db_game_list = sorted(db_game_list, reverse = not self.db_sort_criteria[0].asc, key=attrgetter(self.db_sort_criteria[0].key))

            self.db_stat_label.text = "{0} games".format(len(game_ids))
#            self.db_adapter.data = {str(i): {'text': str(g.id), 'is_selected': False} for i, g in enumerate(db_game_list)}
#             if ref_db:
#                 self.database_list_view.adapter.bind(on_selection_change=self.ref_db_selection_changed)
#             else:
#             self.database_list_view.adapter.bind(on_selection_change=self.db_selection_changed)

            self.db_adapter.data = db_game_list
            self.database_list_view.scroll_to(0)


    def update_book_panel(self, ev=None):
        # print "ev:"+str(ev)
        fen = self.chessboard.position.fen

        if self.book_display:
            user_book_moves_set = set()
            pos_hash = str(self.chessboard.position.__hash__())

            # print pos_hash
            user_book_moves = None
            if self.user_book is not None:
                # self.user_book_panel.children[0].text = "[color=000000][i][ref=" + BOOK_OFF + "]" + BOOK_OFF + "[/ref][/i]\n"
                #            print "found user_book\n"
                move_text = ""

                if pos_hash in self.user_book:
#                    print "found position"
    #                print self.user_book[self.chessboard.position.fen]
                    user_book_moves = self.user_book[pos_hash]
                    # print user_book_moves
                    try:
                        col = user_book_moves["color"]
                    except KeyError:
                        print user_book_moves
                        col = ["white"]
                    color = "bold"
                    if "white" in col and "black" not in col:
                        color = "3333ff"
                    elif "white" in col and "black" in col:
                        color = "ff0000"
                    # elif "white" not in col and "black" in col:
                    #     color = "bold"

                    user_book_moves = user_book_moves["moves"]
                    # print user_book_moves
                    if user_book_moves:
                        for m in user_book_moves:
                            # print m
                            pos = Position(fen)
                            move_info = pos.make_move(Move.from_uci(m.encode("utf-8")))
                            san = move_info.san
                            move_text += "[ref={0}]{1}[/ref]\n".format(m, san)
                            user_book_moves_set.add(m)

                    if ev is not None:
                        j = self.user_book[pos_hash]
                        j["eval"] = self.convert_inf_eval_to_int(ev)
                        self.user_book[pos_hash] = j
                else:
                    # Not found
                    #     print "pos not found"
                        self.user_book[pos_hash] = {"moves":[], "annotation":"", "color": [],
                                                                      "eval":5, "games":[], "misc":""}

            p = Position(fen)
            # print p
            # self.book_panel.children[0].text = "[color=000000][i][ref=" + BOOK_OFF + "]" + BOOK_OFF + "[/ref][/i]\n"
            book_entries = 0
#            self.book_panel.grid.remove_all_data_rows()
            self.book_panel.reset_grid()
            polyglot_entries = list(self.book.get_entries_for_position(p))
#            if user_book_moves:
#                for m in user_book_moves:
#                    print m
            for p in polyglot_entries:
                # print p.raw_move
                p.in_user_book = False
#                print str(p.move)
#                print user_book_moves
                if user_book_moves and str(p.move) in user_book_moves:
                    p.in_user_book = True
                    user_book_moves_set.remove(str(p.move))

            polyglot_entries = sorted(polyglot_entries, key=lambda p: p.in_user_book, reverse = True)

            # print user_book_moves_set
            for m in user_book_moves_set:
                try:
                    pos = Position(fen)
                    move_info = pos.make_move(Move.from_uci(m.encode("utf-8")))
                    san = move_info.san

                    # print "color:{0}".format(color)

                    if color == "bold":
                        self.book_panel.grid.add_row(["[ref={0}][b]{1}[/b][/ref]".format(m, san), ''], callback=self.add_book_moves)
                    else:
                        self.book_panel.grid.add_row(["[ref={0}][b][color={2}]{1}[/color][/b][/ref]".format(m, san, color), ''], callback=self.add_book_moves)

                except Exception, ex:
                    pass

             # 'key', 'learn', 'move', 'raw_move', 'weight'
            for e in polyglot_entries:
                # print e.move
                try:
                    pos = Position(fen)
                    move_info = pos.make_move(Move.from_uci(e.move.uci))
                    san = move_info.san

                    if e.in_user_book:
                        weight = str(e.weight)
                        if color == "bold":
                            self.book_panel.grid.add_row(["[ref={0}][b]{1}[/b][/ref]".format(e.move.uci, san), weight], callback=self.add_book_moves)
                        else:
                            self.book_panel.grid.add_row(["[ref={0}][b][color={2}]{1}[/color][/b][/ref]".format(e.move.uci, san, color), weight], callback=self.add_book_moves)
                        # self.book_panel.grid.add_row(["[ref={0}][b]{1}[/b][/ref]".format(e.move.uci, san), weight], callback=self.add_book_moves)
                    else:
                        self.book_panel.grid.add_row(["[ref={0}]{1}[/ref]".format(e.move.uci, san), str(e.weight)], callback=self.add_book_moves)
                    book_entries += 1
                    if book_entries >= 5:
                        break
                except Exception, ex:
                    pass

            current_eval = self.user_book[pos_hash]["eval"]
            # print "current_eval:"+str(current_eval)
            weight = self.convert_int_eval_to_inf(current_eval)
            # print weight

            self.book_panel.grid.add_row(["[color=3333ff][ref=add_to_user_book]Add to White Rep[/ref][/color]",
                                          ("[color=3333ff][ref=%s]Delete[/ref][/color]" % DELETE_FROM_USER_BOOK)], callback=self.add_book_moves_white)
            self.book_panel.grid.add_row(["[ref=add_to_user_book]Add to Black Rep[/ref]",
                                          ("[ref=%s]Delete[/ref]" % DELETE_FROM_USER_BOOK)], callback=self.add_book_moves_black)
            self.book_panel.grid.add_row(["Eval", "[ref={0}]{0}[/ref]".format(weight)], callback=self.add_book_moves)

                # current_eval = NONE
                # self.book_panel.grid.add_row(["__", "[ref={0}]{0}[/ref]".format(eval_symbol[NONE])], callback=self.add_book_moves)
                # Level db write issue?
            #         # Leveldb opening book schema:
#         # {'fen':
#         #   {
#         #   "moves":["e4", "d4"],
#         #   "annotation":text,
#         #   "eval": number, (higher means better for white) (+-, +=, =, =+, -+)
#         #   "games": game_ids of games played from this position,
#         #   "misc": Extra stuff?
#         #    ""
#         #   }
#         # }


    def fill_chess_board(self, sq, p):
#        print "p:%s"%p
#        print "sq:%s"%sq
#        if p == ".":
#            sq.remove_piece()
        if p:
            # print p.symbol
            piece = ChessPiece(MERIDA+'%s.png' % IMAGE_PIECE_MAP[p.symbol])
            sq.add_piece(piece)
        else:
            sq.remove_piece()
            # Update game notation

    def convert_san_to_figurine(self, san):
        for k, v in PIECE_FONT_MAP.iteritems():
            san = san.replace(k, v)
        return san

    def refresh_board(self, update = True, spoken = False):
        # print "refresh_board"
        # flatten lists into one list of 64 squares
#        squares = [item for sublist in self.chessboard.getBoard() for item in sublist]
        squares = self.chessboard.position
        # print self.chessboard.position.fen
        # print self.chessboard.position.get_ep_square()

        for i, p in enumerate(SQUARES):
            self.fill_chess_board(self.squares[i], squares[p])

        if self.chessboard.san:
            filler = ''
            # current turn is toggle from previous
            # add in a dot if is now white to move
            if self.chessboard.position.turn == 'w':
                filler = '.'
            san = self.chessboard.san
            san = self.convert_san_to_figurine(san)
            self.prev_move.text = u"{0}.{1} {2}".format(self.chessboard.half_move_num/2, filler, san)


#        all_moves = self.chessboard.getAllTextMoves()
#        print self.chessboard_root.game_score()

        if update:
            all_moves = self.chessboard_root.game_score(figurine=True)
            if all_moves:
                self.game_score.children[0].text=u"[color=000000]{0}[/color]".format(all_moves)
        if self.variation_dropdown:
            self.variation_dropdown.dismiss()
        if len(self.chessboard.variations) > 1:
            self.variation_dropdown = DropDown()
            for i,v in enumerate(self.chessboard.variations):
            # for index in range(len(self.chessboard.variations)):
                btn = Button(id=str(i), text='{0}'.format(v.san), size_hint_y=None, height=20)
                # btn = Button(text='Value %d' % index)


                # for each button, attach a callback that will call the select() method
                # on the dropdown. We'll pass the text of the button as the data of the
                # selection.
                btn.bind(on_release=lambda btn: self.select_variation(btn.id))
                # print i

                # then add the button inside the dropdown
                self.variation_dropdown.add_widget(btn)
            self.variation_dropdown.open(self.b)

        # print self.chessboard.get_prev_moves()

        # print "Before stopping"
        # if self.engine_running:
        if self.engine_mode != ENGINE_PLAY:
            sf.stop()
            sleep(0.05)
            # print self.chessboard_root.game_score()

        if self.chessboard_root.headers.headers.has_key('FEN') and len(self.chessboard_root.headers.headers['FEN']) > 1:
            self.custom_fen = self.chessboard_root.headers.headers['FEN']

        if self.custom_fen:
            self.pyfish_fen = self.custom_fen
            # sf.position(self.custom_fen, self.chessboard.get_prev_moves())
        else:
            self.pyfish_fen = 'startpos'
            # sf.position('startpos', self.chessboard.get_prev_moves())

        if self.use_engine:
            if self.start_pos_changed:
                # self.uci_engine.sendFen(self.custom_fen)
                self.start_pos_changed = False

            # if self.engine_running:
            #     # sf.stop()
            #         # sleep(1)
            #     self.stop_engine()
            #     while self.engine_running:
            #         pass
            #     self.use_engine = True

            # print "self.engine_mode: "
            # print self.engine_mode
            if self.engine_mode == ENGINE_ANALYSIS:
                # if self.engine_running:
                sf.go(fen=self.pyfish_fen, moves=self.chessboard.get_prev_moves(), infinite=True)
                # print "Started engine"
                # self.engine_running = True
            elif self.engine_mode == ENGINE_TRAINING:
                sf.set_option('skill level', '17')
                sf.go(fen=self.pyfish_fen, moves=self.chessboard.get_prev_moves(), depth=15)
            else:
                # print "computer_move: "
                # print self.engine_computer_move
                if self.engine_mode == ENGINE_PLAY and self.engine_computer_move:
                    # print "before go play"
                    # sf.go(movetime=10)
                    sf.go(fen=self.pyfish_fen, moves=self.chessboard.get_prev_moves(), wtime=int(self.time_white*1000), btime=int(self.time_black*1000), winc=int(self.time_inc_white*1000), binc=int(self.time_inc_black*1000))
                    # print "Started engine"
                    # self.engine_running = True

                    # self.uci_engine.requestMove(wtime=self.time_white, btime=self.time_black,
                    #     winc=self.time_inc_white, binc=self.time_inc_black)

        self.update_book_panel()
        # print self.speak_move_queue
        if spoken:
            if len(self.speak_move_queue)>0:
                for e in self.speak_move_queue:
                    self.speak_move_queue = []
                    os.system("say "+e)
        # self.update_database_panel()
#        self.update_user_book_panel()

if __name__ == '__main__':
    Chess_app().run()
