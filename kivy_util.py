from kivy.resources import resource_find
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Rectangle
from kivy.graphics import Color
from data_grid import DataGrid

class ScrollableLabel(ScrollView):
    def __init__(self, text, ref_callback=None, font_size=13, font_name='DroidSans', *args, **kwargs):
        super(ScrollableLabel, self).__init__(*args, **kwargs)
        with self.canvas.before:
            Color(0.7, .02, 0.91, mode="hsv")
            # Color(.69, .93, .93)
            self.background = Rectangle(size_hint=(1,1))

        self.label = Label(text=text, font_size=font_size, font_name=font_name, size_hint_y=None, pos_hint={'x':0.1, 'y':0.1})
        self.label.bind(texture_size=self._set_summary_height, on_ref_press=ref_callback)
        # self.label.text=text
        self.label.markup=True

        self.add_widget(self.label)
        self.bind(pos=self.change_position)
        self.bind(size=self.change_size)

    def _set_summary_height(self, instance, size):
        instance.height = size[1]

    def change_position(self, instance, position):
        self.background.pos = position

    def change_size(self, instance, size):
        self.background.size = size
        self.label.text_size = (size[0]-50, None)

class ScrollableGrid(ScrollView):
    def __init__(self, table_header, footer, editable, top_level_header=None, callback=None, *args, **kwargs):
        super(ScrollableGrid, self).__init__()

        with self.canvas.before:
            Color(0.7, .02, 0.91, mode="hsv")
            self.background = Rectangle(size_hint=(1,1))

        self.table_header = table_header
        self.top_level_header = top_level_header
        self.callback = callback
        self.grid = DataGrid(table_header, [], '', '', top_level_header=top_level_header, callback=callback)

        self.do_scroll_y = True
        self.do_scroll_x = False
        self.add_widget(self.grid)
        self.bind(pos=self.change_position)
        self.bind(size=self.change_size)

    def _set_summary_height(self, instance, size):
        instance.height = size[1]

    def change_position(self, instance, position):
        self.background.pos = position

    def change_size(self, instance, size):
        self.background.size = size
        self.grid.text_size = (size[0]-50, None)

    def reset_grid(self):
        self.remove_widget(self.grid)
#        self.grid.clear_widgets(children=None)
#        self.grid.process_header(self.callback, self.table_header, self.top_level_header)
        self.grid = DataGrid(self.table_header, [], '', '', top_level_header=self.top_level_header, callback = self.callback)
        self.add_widget(self.grid)