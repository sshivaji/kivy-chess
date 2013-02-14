import kivy

from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label


class ScrollableLabel(ScrollView):

    def build(self,textinput):

        self.summary_label = Label(text="",
                              size_hint_y=None,size_hint_x=None)

        self.summary_label.bind(texture_size=self._set_summary_height)
        # remove the above bind
        self.summary_label.text = str(textinput)

        #and try setting height in the following line
        self.sv = ScrollView(size_hint_y=None)
        # it does not scroll the scroll view.

        self.sv.add_widget(self.summary_label)
        self.summary_label.markup= True

        return self.sv

    def _set_summary_height(self, instance, size):
#        print "_set_summary_height", size
        instance.height = size[1]
        instance.width = size[0]




