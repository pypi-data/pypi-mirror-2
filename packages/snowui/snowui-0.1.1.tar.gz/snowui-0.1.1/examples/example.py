from pyglet import clock
from pyglet.window import mouse, key
import rabbyt

import sys, os
sys.path.append("..")

import snowui



class Game(object):
    def __init__(self):
        clock.set_fps_limit(35)
        self.time = 0

        self.window = snowui.Window()
        self.view = snowui.View(self.window)
        #self.view.keep_within([-100, self.board.height,
                #self.board.width, 0])

        self.gui = MyGUI(self)
        self.window.push_handlers(self.gui)

    def loop(self):
        self.window.dispatch_events()
        self.time += clock.tick()
        rabbyt.set_time(self.time)
        rabbyt.clear()

        self.view.set_viewport()

        self.gui.render()

        self.window.flip()
        return True




class MyGUI(snowui.GUI):
    def __init__(self, game):
        snowui.GUI.__init__(self, shape=(0,0,100,600), bounds="rect")
        self.game = game

        self.view = snowui.View(game.window)
        self.view.x = self.view.width/2
        self.view.y = self.view.height/2

        self.mouse_xy = 0,0

        MyButton = snowui.widget_setting(CoolButton,
                texture="button.png",
                fade_time=.5,
                default_color=(.4,.7,.4,1),
                hover_color=(0,.5,0,1),
                shape=(0,32,32,0),
                bounds="rect")

        self.add(MyButton(rx=10, ry=30, icon="icon.png"))
        self.add(MyButton(rx=10, ry=70, callback=self.mycallback, cb_data="hi"))

        PanButton = snowui.widget_setting(CoolButton,
                texture="button_wide.png",
                default_color=(.7,.7,1,.6),
                hover_color=(0.3,0.3,1,.6),
                shape=(0,32,180,0),
                bounds="rect")

        sb = snowui.ScrollBox(shape=(0,400,200,0), x=200, y=130, bounds="always")
        sb.add(PanButton(callback=self.mycallback, cb_data="ho"))
        for i in range(20):
            sb.add(PanButton())
        self.add(sb)


        exit_button = CoolButton(rx=50, ry=30,
                texture="button2.png",
                fade_time=.2,
                default_color=(.6,.6,.6,1),
                hover_color=(.6,0,0,1),
                shape=(0,32,32,0),
                icon="icon2.png",
                callback=sys.exit)
        self.add(exit_button)

    def mycallback(self, data):
        print data


    def handle_mouse_motion(self, x, y, dx, dy):
        self.mouse_xy = x,y
        xy = self.game.view.to_world_pixels((x,y))


    def render(self):
        self.view.set_viewport()
        snowui.GUI.render(self)


class CoolButton(snowui.Button):
    def handle_mouse_press(self, x, y, button, modifiers):
        if button == mouse.LEFT:
            self.is_hovering = False
            self.rgba = (1,1,1,0)
            self.handle_mouse_motion(x, y)
            snowui.Button.handle_mouse_press(self, x, y, button, modifiers)

snowui.Widget.style = {
        "ScrollBar.block": "scrollblock.png",
        "ScrollBar": "scrollbar.png",
        "ScrollBox.Pan": "scrollbox.png",
    }

def main():
    game = Game()

    while True:
        game.loop()


if __name__ == "__main__":
    main()
