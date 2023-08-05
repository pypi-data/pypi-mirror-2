import rabbyt
from pyglet.window import mouse, key


def widget_setting(widget, **kwargs):
    """
    ``widget_setting(widget, **kwargs)``

    This factory is used for creating widgets with default settings::

        MyButton = snowui.widget_setting(snowui.Button, texture="button.png")

    MyButton would then be a function to create a button that has a default
    texture of "button.png"::

        exit_button = MyButton(callback=sys.exit)
    """
    def factory(**fargs):
        k = kwargs.copy()
        k.update(fargs)
        cls = widget(**k)
        return cls

    return factory



class Widget(rabbyt.Sprite):
    """
    ``Widget(**kwargs)``

    This is the base widget class that all things gui subclass from.

    The way the passed keyword arguments are handled is a bit differnt. For each
    argument it sees if there is a method that matches the key prepended with
    an underscore.

    for example the argument ry::

        Widget(ry=0)

    will call ``Widget._ry`` passing it 0.

    ``Widget`` is subclassed from ``rabbyt.Sprite`` so ``x`` and ``y`` change
    absolute positioning. But if you set ``rx`` or ``ry`` (relative x and y)
    they will be used instead for positioning and the sprite x and y will be
    overwritten respectively.
    """
    _v_rx = rabbyt.anim_slot(0)
    _v_ry = rabbyt.anim_slot(0)

    style = {}

    def __init__(self, **kwargs):
        self.children = []
        self.__parent = None
        self.bounds = None
        self.use_rx = False
        self.use_ry = False

        self.is_focused = False
        self.is_active = True

        rabbyt.Animable.__init__(self)

        settings = []

        for (key,value) in kwargs.items():
            if hasattr(self, "_"+key):
                if not callable(getattr(self, "_"+key)):
                    raise ValueError("No reciving function for "+key)
                f = lambda k,v: getattr(self, "_"+k)(v)
                settings.append((f,key,value))
                del kwargs[key]

        rabbyt.Sprite.__init__(self, **kwargs)

        # A hack so we can have the original shape (when it is centered).
        self.orig_shape = self.shape.bottom, self.shape.left

        if not kwargs.has_key("shape") and not kwargs.has_key("texture"):
            self.shape = (0,0)
        if not kwargs.has_key("shape"):
            self.shape.bottom = 0
            self.shape.left = 0

        [s(k,v) for (s,k,v) in settings]

    def center_to_view(self, view):
        """
        Centers this sprite on `view`
        Expects both self and view to be bottom-left centered.
        """
        self.x = view.x - self.shape.width/2
        self.y = view.y - self.shape.height/2


    def get_style(self, key):
        texture = None
        if self.style.has_key(key):
            texture = self.style[key]
        return texture

    def set_style(self, key, kwargs):
        if not kwargs.has_key("texture") or kwargs["texture"] == None:
            kwargs["texture"] = self.get_style(key)


    def _parent(self, p):
        self.__parent = p

        # If we are using relative positioning we need to update our positions.
        if self.use_rx:
            self._rx(self._v_rx)
        if self.use_ry:
            self._ry(self._v_ry)
    parent = property(lambda self:self.__parent, _parent)


    def _rx(self, x):
        self.use_rx = True
        self._v_rx = x
        if self.parent:
            self.x = self.attrgetter("_v_rx") + self.parent.attrgetter("x")
        else:
            self.x = self.attrgetter("_v_rx")
    rx = property(lambda self:self._v_rx, _rx)


    def _ry(self, y):
        self.use_ry = True
        self._v_ry = y
        if self.parent:
            self.y = self.attrgetter("_v_ry") + self.parent.attrgetter("y")
        else:
            self.y = self.attrgetter("_v_ry")
    ry = property(lambda self:self._v_ry, _ry)

    def _rxy(self, xy):
        self.rx,self.ry = xy
    rxy = property(lambda self:(self.rx, self.ry), _rxy)


    def _bounds(self, b):
        self.bounds = b

    def render(self):
        rabbyt.Sprite.render(self)
        for c in self.children:
            c.render()

    def add(self, widget):
        if widget.parent:
            raise ValueError(str(widget)+" already has a parent.")
        if widget not in self.children:
            self.children.append(widget)
            widget.parent = self
        else:
            print "WARNING:", widget, "is already a child of",self

    def remove(self, w):
        if w in self.children:
            self.children.remove(w)
            w.parent = None

    def collide(self, xy):
        if not self.is_active:
            return False
        if self.bounds:
            b = self.bounds
            if b == "always":
                return True
            elif b == "rect":
                x,y = xy
                # gotta wait until Matthew makes just a tuple work with this.
                return rabbyt.collisions.aabb_collide_single(
                        rabbyt.Quad((x,y,x,y)), [self])
        else:
            # FIXME: This is really bad and buggy
            w = (self.shape.width/2)
            b = self.x+w, self.y+w, w
        return rabbyt.collisions.collide_single(b, [xy])


    def handle_mouse_motion(self, x, y, dx, dy):
        pass

    def on_mouse_motion(self, x, y, dx, dy):
        if not self.is_active:
            return
        self.handle_mouse_motion(x, y, dx, dy)
        for c in reversed(self.children):
            if not c.is_active:
                continue
            c.on_mouse_motion(x, y, dx, dy)


    def handle_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        pass

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if not self.is_active:
            return False
        self.handle_mouse_drag(x, y, dx, dy, buttons, modifiers)
        for c in reversed(self.children):
            if not c.is_active:
                continue
            c.on_mouse_drag(x, y, dx, dy, buttons, modifiers)


    def handle_mouse_press(self, x, y, button, modifiers):
        pass

    def on_mouse_press(self, x, y, button, modifiers):
        if not self.is_active:
            return
        if self.collide((x,y)):
            self.do_focus()
            self.handle_mouse_press(x, y, button, modifiers)
            for c in reversed(self.children):
                if not c.is_active:
                    continue
                if c.on_mouse_press(x, y, button, modifiers):
                    break
            return True
        else:
            self.do_blur()


    def handle_mouse_release(self, x, y, button, modifiers):
        pass

    def on_mouse_release(self, x, y, button, modifiers):
        if not self.is_active:
            return
        # TODO: Make this only called when needed?
        self.handle_mouse_release(x, y, button, modifiers)
        for c in reversed(self.children):
            if not c.is_active:
                continue
            c.on_mouse_release(x, y, button, modifiers)
        return True


    def handle_key_press(self, symbol, modifiers):
        pass

    def on_key_press(self, symbol, modifiers):
        if not self.is_active:
            return
        if self.is_focused:
            self.handle_key_press(symbol, modifiers)
            for c in reversed(self.children):
                if not c.is_active:
                    continue
                if c.on_key_press(symbol, modifiers):
                    break
            return True

    def handle_text(self, text):
        pass

    def on_text(self, text):
        if not self.is_active:
            return
        if self.is_focused:
            self.handle_text(text)
            for c in reversed(self.children):
                if not c.is_active:
                    continue
                if c.on_text(text):
                    break
            return True

    def do_focus(self):
        self.is_focused = True

    def do_blur(self):
        """
        ``do_blur()``

        It's up to the widget with what is done with this. For example a button
        widget would fade out.
        """
        self.is_focused = False
