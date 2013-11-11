import sys, os
import kivy

kivy.require('1.7.2')

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.listview import ListView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton

Builder.load_string('''
<MainScreen>:
	BoxLayout:
		orientation: 'vertical'

<TableCell>:
	background_normal: 'img/background_normal.png'
	background_down: 'img/background_pressed.png'
	markup: True
	size_hint_x: 0.5

<TableHeader>:
	background_normal: 'img/background_header.png'
	background_down: 'img/background_header.png'
	size_hint_x: 0.5

<TopTableHeader>:
	background_normal: 'img/background_normal.png'
	background_down: 'img/background_normal.png'
	size_hint_x: 0.5

''')

class TopTableHeader(ToggleButton):
    cell_pos = [None, None]

class TableHeader(ToggleButton):
    cell_pos = [None, None]

class TableFooter(ToggleButton):
    cell_pos = [None, None]

class TableCell(ToggleButton):
    cell_pos = []

    def on_press(self):
        def invert_state(cell):
            if cell.state == 'normal':
                cell.state = 'down'
            else:
                cell.state = 'normal'

        row_to_select = self.cell_pos[0]
        t_cells = self.parent.children
        for t_cell in t_cells:
            if t_cell.cell_pos[0] == row_to_select:
                invert_state(t_cell)
        invert_state(self)


class DataGrid(GridLayout):
    def process_header_cell(self, cell, top_header = False, top_header_id = "Top_Header", callback = None):
        if top_header:
            cell_str = '[color=000000][b][ref='+cell[0] +']'+ cell[0] + '[/ref][/b][/color]'
            tmp = TopTableHeader(text=cell_str, markup=True, id=top_header_id, size_hint_x=None, size_hint_y=None, height=20)

        else:
            cell_str = "[b]" + str(cell[0]) + "[/b]"
            tmp = TableHeader(text=cell_str, markup=True, id="Header", size_hint_x=None, size_hint_y=None, height=30)

        tmp.halign = cell[1]
        tmp.valign = 'middle'
        if top_header:
            tmp.bind(size=(tmp.setter('text_size')), on_press=callback, on_ref_press=callback)
        else:
            tmp.bind(size=(tmp.setter('text_size')))

        self.add_widget(tmp)

    def process_header(self, callback, header, top_level_header):
        if top_level_header:
            self.rows += 1
            self.process_header_cell(top_level_header, top_header=True, callback=callback)

            for i in range(0, self.cols - 1):
                self.process_header_cell(['', 'center'], top_header=True, top_header_id="Blank_" + str(i))
        for cell in header:
            self.process_header_cell(cell)

    def __init__(self, header, body, footer, editable, top_level_header=None, callback=None, **kwargs):
        super(DataGrid, self).__init__(**kwargs)
        self.size_hint_y=None
        self.bind(minimum_height=self.setter('height'))

        self.cols = len(header)
        self.rows = max(len(body) + 1,10)

        self.spacing = [1, 1]
        self.size_hint_x = 1

        self.process_header(callback, header, top_level_header)

        if body:
            count_01 = 0
            for row in body:
                count_02 = 0
                for cell in row:
                    cell_text = '[color=000000]' + cell + '[/color]'
                    tmp = TableCell(text=cell_text, id="Body", size_hint_x=None, size_hint_y=None, height=30, width=10)
                    tmp.bind(size=(tmp.setter('text_size')), bold=True)
                    tmp.halign = "center"
                    tmp.valign = "middle"
                    tmp.cell_pos = [count_01, count_02]
                    self.add_widget(tmp)
                    count_02 += 1
                count_01 += 1
        if footer != None:
            for cell in footer:
                pass

    def add_row(self, row_data, callback = None, **kwargs):
        n = 0
        # print "add_row"
        # print row_data
        for cell_data in row_data:
            cell_height = 30
#            cell_width = 10
            if type(cell_data) is tuple:
                cell_data, cell_height = cell_data

#            print cell_height

            cell_text = '[color=000000]' + cell_data + '[/color]'
            if cell_height:
                tmp = TableCell(text=cell_text, id="Body", size_hint_y = None, size_hint_x = None, height=cell_height, padding=(5,5), spacing = 1)
            else:
                tmp = TableCell(text=cell_text, id="Body", size_hint_y = None, size_hint_x = None, padding=(5,5), spacing = 1)

            tmp.bind(size=(tmp.setter('text_size')), on_press=callback, on_ref_press=callback)

            tmp.cell_pos = [self.rows - 1, n]
            tmp.halign = "center"
            tmp.valign = 'middle'
            n += 1
            self.add_widget(tmp)
        self.rows += 1
        # print "rows:{0}".format(self.rows)

    def remove_all_data_rows(self, **kwargs):
        # print "Removing all data rows"
        self.clear_widgets(children=None)


    def remove_selected_row(self, **kwargs):
        selected = 0
        cells = reversed(self.children)
        for cell in cells:
            if cell.state == 'down':
                self.remove_widget(cell)
                selected += 1
        cells = self.children
        if selected == 0:
            row_to_delete = self.rows
            deleted = 0
            for x in range(self.cols):
                for cell in cells:
                    if cell.id == 'Body':
                        self.remove_widget(cell)
                        deleted += 1
                        break
                    else:
                        deleted = 0
            if deleted != 0:
                self.rows -= 1
        else:
            self.rows -= (selected / self.cols)

    def select_all(self, **kwargs):
        cells = self.children
        for cell in cells:
            if cell.id == 'Body':
                cell.state = 'down'

    def deselect_all(self, **kwargs):
        cells = self.children
        for cell in cells:
            if cell.id == 'Body':
                cell.state = 'normal'


class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)

        table_header = [['ID', 'center', 'center', 'string', 0.1, 'hidden'],
                        ['Field 01', 'center', 'left', 'option', 0.4, 'visible'],
                        ['Field 02', 'center', 'right', 'number', 0.3, 'visible'],
                        ['Field 03', 'center', 'right', 'coin', 0.2, 'visible']]
        table_body = [
            ['01', 'Item 01', '12', '1.8'],
            ['02', 'Item 02', '43', '1.8'],
            ['03', 'Item 03', '3', '1.8'],
            ['04', 'Item 04', '23', '1.8'],
            ['05', 'Item 05', '12', '1.8'],
            ['06', 'Item 06', '23', '1.8']]
        table_footer = ['footer 01', 'footer 02', 'footer 03']

        grid = DataGrid(table_header, table_body, '', '')
        # _size=(400, 500000)
        scroll = ScrollView(size_hint=(1, 1), scroll_y=0,
                            pos_hint={'center_x': .5, 'center_y': .5}, effect_y=None, scroll_distance=0)
        scroll.add_widget(grid)
        scroll.do_scroll_y = True
        scroll.do_scroll_x = False

        self.children[0].add_widget(scroll)
        new_data = ['XX', 'Novo Produto', '1023', '2.12']


        def add_new_row(self):
            grid.add_row(new_data)

        def remove_sel_row(self):
            grid.remove_selected_row()

        def select_all_cells(self):
            grid.select_all()

        def deselect_all_cells(self):
            grid.deselect_all()

        self.children[0].add_widget(Button(text="add row", on_release=add_new_row, size_hint_y=.2))
        self.children[0].add_widget(Button(text="remove row", on_release=remove_sel_row, size_hint_y=.2))
        self.children[0].add_widget(Button(text="select all", on_release=select_all_cells, size_hint_y=.2))
        self.children[0].add_widget(Button(text="deselect all", on_release=deselect_all_cells, size_hint_y=.2))


sm = ScreenManager()
sm.add_widget(MainScreen(name="main_screen"))


class MainApp(App):
    def build(self):
        return sm


if __name__ == '__main__':
    MainApp().run()
