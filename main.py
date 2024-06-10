from random import random

from kivy.app import App
from kivy.core.window import Window
from kivy.graphics import Color
from kivy.graphics import Rectangle
from kivy.uix.button import Button
from kivy.uix.widget import Widget

BLOCKSIZE = 50


class MyPaintWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        with self.canvas.before:
            Rectangle(
                source='assets/board.jpg',
                pos=self.pos, size=Window.size,
            )

    def on_touch_down(self, touch):
        color = (random(), 1, 1)
        print(touch.x, touch.y)
        if touch.x > 150 and touch.y < 450 and touch.y > 20:
            with self.canvas:
                Color(*color, mode='hsv')
                Rectangle(
                    pos=(
                        touch.x - BLOCKSIZE / 2, touch.y -
                        BLOCKSIZE / 2,
                    ), size=(BLOCKSIZE, BLOCKSIZE),
                )


class MyPaintApp(App):

    def build(self):
        parent = Widget()
        self.painter = MyPaintWidget()
        clearbtn = Button(text='Clear', background_color=[1.0, 1.0, 1.0, 0.0])
        clearbtn.bind(on_release=self.clear_canvas)
        parent.add_widget(self.painter)
        parent.add_widget(clearbtn)
        return parent

    def clear_canvas(self, obj):
        print('clicked')
        self.painter.canvas.clear()


if __name__ == '__main__':
    MyPaintApp().run()
