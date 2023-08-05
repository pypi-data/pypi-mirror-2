import rabbyt
from pyglet.window import mouse, key
from pyglet.text import HTMLLabel

import sys
sys.path.append("..")

from snowui.widget import Widget


class TextInput(Widget):
    def __init__(self, on_submit, **args):
        Widget.__init__(self, bounds="rect", **args)
        self.text = Text("", font_size=12, rx=3, ry=3, color=(0,0,0,255))
        self.text.active = False
        self.add(self.text)
        self.on_submit = on_submit

    def do_focus(self):
        self.rgb = rabbyt.lerp(start=(1,1,1), end=(.7,.9,1), dt=1, extend="reverse")
        self.is_focused = True

    def do_blur(self):
        self.rgb = rabbyt.lerp(end=(1,1,1), dt=.3)
        self.is_focused = False

    def handle_text(self, text):
        self.text.text += text

    def on_key_press(self, symbol, modifiers):
        if not self.is_focused:
            return
        if symbol == key.BACKSPACE:
            self.text.text = self.text.text[:-1]
        elif symbol == key.ENTER:
            self.submit()

    def submit(self):
            self.on_submit(self.text.text)

class Text(Widget):
    def __init__(self, text, anchor_x="left", color=(0,0,0,255),
            font_size=20, multiline=False, width=None, **kwargs):
        if multiline and not width:
            raise ValueError("Text widgets must specify a width when multiline is set to True")

        Widget.__init__(self, **kwargs)

        self.font_size = font_size
        self.color = color
        self.multiline = multiline
        self.width = width

        self.label = HTMLLabel(text, x=self.x, y=self.y,
                anchor_x=anchor_x, multiline=multiline, width=width)
        self._format()


    def _format(self):
        self.label.color = self.color
        self.label.font_size = self.font_size


    def render(self):
        self.label.x = self.x
        self.label.y = self.y
        self.label.draw()


    def set_text(self, t):
        self.label.text = t
        self._format()
    text = property(lambda self:self.label.text, set_text)
