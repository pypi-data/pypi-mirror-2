"""
    tdl is a ctypes port of The Doryen Library.
"""

from pkg_resources import resource_filename
import ctypes
import weakref
import os

from tcod import _lib, _Color

import noise
import event
from local import *

_fontinitialized = False
_rootinitialized = False
_rootconsole = None

# remove dots from common functions
_setchar = _lib.TCOD_console_set_char
_setfore = _lib.TCOD_console_set_fore
_setback = _lib.TCOD_console_set_back

def _assert_colors(fgcolor, bgcolor):
    assert _iscolor(fgcolor), \
           'foreground color must be a 3 item tuple or None, recived %s' % repr()
    assert _iscolor(bgcolor), \
           'background color must be a 3 item tuple or None, recived %s' % repr()

class TDLError(Exception):
    pass

class TDLDrawError(TDLError):
    pass

class TDLBlitError(TDLError):
    pass

class TDLIndexError(TDLError):
    pass

class Console(object):
    """The Console is the main object of the tdl library.

    The console created by the init function is the root console and is the
    consle that is rendered to the screen with flush.

    Any console made from Console is an off screen console that must be blited
    to the root console to be visisble.
    """

    __slots__ = ('_as_parameter_', 'width', 'height', '__weakref__')

    def __init__(self, w, h):
        if (w, h) == (0, 0):
            # because _drawable will always fail this should be safe
            self._as_parameter_ = None
        else:
            self._as_parameter_ = _lib.TCOD_console_new(w, h)
        self.width = w
        self.height = h

    def __del__(self):
        # If this is the root console the window will close when collected
        try:
            if isinstance(self._as_parameter_, ctypes.c_void_p):
                global _rootinitialized, _rootconsole
                _rootinitialized = False
                _rootconsole = None
            _lib.TCOD_console_delete(self)
        except StandardError:
            pass

    def _replace(self, console):
        """Used internally"""
        # Used to replace this Console object with the root console
        # If another Console object is used then they are swapped
        
        if isinstance(console, Console):
            self._as_parameter_, console._as_parameter_ = \
              console._as_parameter_, self._as_parameter_ # swap tcod consoles
        else:
            self._as_parameter_ = console
        self.width = _lib.TCOD_console_get_width(self)
        self.height = _lib.TCOD_console_get_height(self)
        return self

    def blit(self, source, x=0, y=0, width=None, height=None, srcx=0, srcy=0, alpha=255):
        """Blit another console or Window onto the current console.

        By default it blits the entire source to the topleft corner.
        """
        assert isinstance(source, (Console, Window)), "source muse be a Window or Console instance"
        if not (0 <= x < self.width and 0 <= y < self.height):
            raise TDLIndexError('Cannot blit to (%i, %i)' % (x, y))
        if not (0 <= srcx < source.width and 0 <= srcy < source.height):
            raise TDLIndexError('(%i, %i) not valid on source' % (x, y))


        assert width is None or isinstance(width, (int, long)), "width must be a number or None"
        assert height is None or isinstance(height, (int, long)), "height must be a number or None"

        if width is None:
            width = min(source.width, self.width) - x
        elif x + width > self.width:
            raise TDLBlitError('width is too long')
        if height is None:
            height = min(source.height, self.height) - y
        elif y + height > self.height:
            raise TDLBlitError('height is too long')

        assert isinstance(srcx, (int, long)), "srcx must be a number"
        assert isinstance(srcy, (int, long)), "srcy must be a number"

        if isinstance(source, Window):
            srcx += source.x
            srcy += source.y
            source = source.console
        _lib.TCOD_console_blit(source, srcx, srcy, width, height, self, x, y, alpha)

#    def blit_image(self, x, y, image, scalex=1, scaley=1, angle=0, blend=BND_SET):
#        """Draws an image onto the console.
#        """
#        assert isinstance(image, image.Image)
#        _lib.TCOD_image_blit(image, self, x, y, blend, scalex, scaley, angle)

#    def blit_image_rect(self, x, y, image, w=-1, h=-1, blend=BND_SET):
#        """Draws an image onto the console.
#        """
#        assert isinstance(image, image.Image)
#        _lib.TCOD_image_blit_rect(image, self, x, y, w, h, blend)

    def get_size(self):
        """Return the size of the console as (width, height)
        """
        return self.width, self.height

    def _drawable(self, x, y):
        """Used internally
        Checks if a cell is part of the console.
        Raises an exception if it can not be used.
        """
        assert isinstance(x, int), 'x must be an integer, %s' % repr(x)
        assert isinstance(y, int), 'y must be an integer, %s' % repr(y)
        if 0 <= x < self.width and 0 <= y < self.height:
            return
        raise TDLIndexError('(%i, %i) is an invalid postition.' % (x, y))

    def clear(self, fillcolor):
        """Clears the entire console.
        """
        assert _iscolor(fillcolor), 'fillcolor must be a 3 item list'
        assert fillcolor is not None, 'fillcolor can not be None'
        _lib.TCOD_console_set_foreground_color(self, _Color(*C_WHITE))
        _lib.TCOD_console_set_background_color(self, _Color(*fillcolor))
        _lib.TCOD_console_clear(self)

    def draw_char(self, fgcolor, bgcolor, char, x, y, bgblend=BND_SET):
        """Draws a single character.

        char should be an integer but can be a None if you only want to change
        colors of the tile or it can be a single charecter string or unicode.

        For fgcolor and bgcolor you use a 3 item object or a Color object. None
        will keep the color unchanged.

        bgblend is used to tell how the bgcolor blends into the background. The
        default is BND_SET.

        Having the x or y values outside of the console will raise a
        tdl.BadIndex error.
        """
        assert _iscolor(fgcolor), 'fgcolor must be a 3 item list or None'
        assert _iscolor(bgcolor), 'bgcolor must be a 3 item list or None'
        if isinstance(char, (str, unicode)):
            assert len(char) == 1, 'strings must only have one character'
            char = ord(char)
        assert isinstance(char, int) or char is None, \
               'char must be an integer, single character string, or None'

        self._drawable(x, y)

        if char is not None:
            _setchar(self, x, y, char)
        if fgcolor is not None:
            _setfore(self, x, y, _Color(*fgcolor))
        if bgcolor is not None:
            _setback(self, x, y, _Color(*bgcolor), bgblend)


    def draw_str(self, fgcolor, bgcolor, string, x, y, bgblend=BND_SET):
        """Draws a string starting at x and y.

        A string that goes past the end will wrap around.  No warning will be
        made if it reaches the end of the console.

        \\r and \\n are drawn on the console as normal character tiles.

        For fgcolor and bgcolor, None will keep the color unchanged.

        If a large enough tileset is loaded you can use a unicode string.
        """
        assert _iscolor(fgcolor), 'fgcolor must be a 3 item list or None'
        assert _iscolor(bgcolor), 'bgcolor must be a 3 item list or None'

        self._drawable(x, y)

        assert isinstance(string, (str, unicode))
        if string == '':
            return

        width, height = self.width, self.height

        if bgcolor is None or fgcolor is None:
            if fgcolor is not None:
                fgcolor = _Color(*fgcolor)
            if bgcolor is not None:
                bgcolor = _Color(*bgcolor)

            # remove dots
            setc = _lib.TCOD_console_set_char
            setfg = _lib.TCOD_console_set_fore
            setbg = _lib.TCOD_console_set_back

            for char in string:
                setc(self, x, y, ord(char))
                if fgcolor is not None:
                    setfg(self, x, y, fgcolor)
                if bgcolor is not None:
                    setbg(self, x, y, bgcolor)
                x += 1
                if x == width:
                    x = 0
                    y += 1
                    if y == height:
                        return
        else:
            _lib.TCOD_console_set_foreground_color(self, _Color(*fgcolor))
            _lib.TCOD_console_set_background_color(self, _Color(*bgcolor))
            draw = _lib.TCOD_console_put_char
            for char in string:
                draw(self, x, y, ord(char), bgblend)
                x += 1
                if x == width:
                    x = 0
                    y += 1
                    if y == height:
                        return

    def draw_rect(self, fgcolor, bgcolor, char, x=0, y=0, width=None, height=None,
                  filled=True, bgblend=BND_SET):
        """Draws a rectangle starting from x and y and extending to width and
        height.  If width or height are None then it will extend to the edge
        of the console.  The rest are the same as draw_char.
        """
        assert _iscolor(fgcolor), 'fgcolor must be a 3 item list or None, not %s' % repr(fgcolor)
        assert _iscolor(bgcolor), 'bgcolor must be a 3 item list or None, not %s' % repr(fgcolor)
        if isinstance(char, (str, unicode)) and len(char) == 1:
            char = ord(char)
        assert isinstance(char, int) or char is None, \
               'char must be an integer, single character string, or None'

        self._drawable(x, y)

        if width is None:
            width = self.width - x
        if height is None:
            height = self.height - y

        if width == 1 and height == 1:
            self.draw_char(fgcolor, bgcolor, char, x, y, bgblend)
            return
        elif width == 1:
            self.draw_vline(fgcolor, bgcolor, char, x, y, height, bgblend)
            return
        elif height == 1:
            self.draw_hline(fgcolor, bgcolor, char, x, y, width, bgblend)
            return

        width = min(width, self.width - x)
        height = min(height, self.height - y)

        right = x + width - 1
        bottom = x + width - 1

        if bgcolor is None or fgcolor is None:
            if fgcolor is not None:
                fgcolor = _Color(*fgcolor)
            if bgcolor is not None:
                bgcolor = _Color(*bgcolor)
            setc = _lib.TCOD_console_set_char
            setfg = _lib.TCOD_console_set_fore
            setbg = _lib.TCOD_console_set_back
            if filled: # fill
                for drawy in xrange(y, y + height):
                    for drawx in xrange(x, x + width):
                        if char is not None:
                            setc(self, drawx, drawy, char)
                        if fgcolor is not None:
                            setfg(self, drawx, drawy, fgcolor)
                        if bgcolor is not None:
                            setbg(self, drawx, drawy, bgcolor, bgblend)
            else: # frame
                for drawy in xrange(y, y + height):
                    if char is not None:
                        setc(self, x, drawy, char)
                        setc(self, right, drawy, char)
                    if fgcolor is not None:
                        setfg(self, x, drawy, fgcolor)
                        setfg(self, right, drawy, fgcolor)
                    if bgcolor is not None:
                        setbg(self, x, drawy, bgcolor, bgblend)
                        setbg(self, right, drawy, bgcolor, bgblend)
                for drawx in xrange(x + 1, right):
                    if char is not None:
                        setc(self, drawx, y, char)
                        setc(self, drawx, bottom, char)
                    if fgcolor is not None:
                        setfg(self, drawx, y, fgcolor)
                        setfg(self, drawx, bottom, fgcolor)
                    if bgcolor is not None:
                        setbg(self, drawx, y, bgcolor, bgblend)
                        setbg(self, drawx, bottom, bgcolor, bgblend)
        else:
            _lib.TCOD_console_set_foreground_color(self, _Color(*fgcolor))
            _lib.TCOD_console_set_background_color(self, _Color(*bgcolor))
            draw = _lib.TCOD_console_put_char
            if filled: # faster fill
                # note: this could be even faster
                for drawy in xrange(y, y + height):
                    for drawx in xrange(x, x + width):
                        draw(self, drawx, drawy, char, bgblend)
            else: # faster frame
                # note: this could be even faster also
                for drawy in xrange(y, y + height):
                    draw(self, x, drawy, char, bgblend)
                    draw(self, right, drawy, char, bgblend)
                for drawx in xrange(x + 1, right):
                    draw(self, drawx, y, char, bgblend)
                    draw(self, drawx, bottom, char, bgblend)

    def draw_hline(self, fgcolor, bgcolor, char, x, y, width=None, bgblend=BND_SET):
        assert _iscolor(fgcolor), 'fgcolor must be a 3 item list or None'
        assert _iscolor(bgcolor), 'bgcolor must be a 3 item list or None'

        if isinstance(char, (str, unicode)) and len(char) == 1:
            char = ord(char)
        assert isinstance(char, int) or char is None, \
               'char must be an integer, single character string, or None'

        assert isinstance(width, (int, long)) or width is None, \
               'width must be an integer or None'

        if width is None:
            width = self.width - x

        if fgcolor and bgcolor and char:
            _lib.TCOD_console_set_foreground_color(self, _Color(*fgcolor))
            _lib.TCOD_console_set_background_color(self, _Color(*bgcolor))
            _lib.TCOD_console_hline(self, x, y, width, bgblend)
        else:
            setc = _lib.TCOD_console_set_char
            setfg = _lib.TCOD_console_set_fore
            setbg = _lib.TCOD_console_set_back

            for x in xrange(x, x + width):
                if char is not None:
                    setc(self, x, y, char)
                if fgcolor is not None:
                    setfg(self, x, y, fgcolor)
                if bgcolor is not None:
                    setbg(self, x, y, bgcolor, bgblend)

    def draw_vline(self, fgcolor, bgcolor, char, x, y, height=None, bgblend=BND_SET):
        assert _iscolor(fgcolor), 'fgcolor must be a 3 item list or None'
        assert _iscolor(bgcolor), 'bgcolor must be a 3 item list or None'

        if isinstance(char, (str, unicode)) and len(char) == 1:
            char = ord(char)
        assert isinstance(char, int) or char is None, \
               'char must be an integer, single character string, or None'

        assert isinstance(height, (int, long)) or height is None, \
               'height must be an integer or None'

        if height is None:
            height = self.height - y

        if fgcolor and bgcolor and char:
            _lib.TCOD_console_set_foreground_color(self, _Color(*fgcolor))
            _lib.TCOD_console_set_background_color(self, _Color(*bgcolor))
            _lib.TCOD_console_hline(self, x, y, height, bgblend)
        else:
            setc = _lib.TCOD_console_set_char
            setfg = _lib.TCOD_console_set_fore
            setbg = _lib.TCOD_console_set_back

            for y in xrange(y, y + height):
                if char is not None:
                    setc(self, x, y, char)
                if fgcolor is not None:
                    setfg(self, x, y, fgcolor)
                if bgcolor is not None:
                    setbg(self, x, y, bgcolor, bgblend)


    def get_char(self, x, y):
        """Return the character and colors of a cell as (ch, fg, bg)

        The charecter is returned as a number.
        """
        self._drawable(x, y)
        char = _lib.TCOD_console_get_char(self, x, y)
        fgcolor = tuple(_lib.TCOD_console_get_fore(self, x, y))
        bgcolor = tuple(_lib.TCOD_console_get_back(self, x, y))
        return char, fgcolor, bgcolor

    # todo: some kind of way to handle line breaks

    def __repr__(self):
        return "<Console (Width=%i Height=%i)>" % (self.width, self.height)


class Window(object):
    """A Window contains a small isolated part of a Console.

    Drawing on the Window draws on the Console.  This works both ways.

    If you make a Window without setting its size (or set the width and height
    as None) it will extend to the edge of the console.

    You can't blit Window instances but drawing works as expected.
    """

    __slots__ = ('console', 'x', 'y', 'width', 'height')

    def __init__(self, console, x=0, y=0, width=None, height=None):
        assert isinstance(x, int)
        assert isinstance(y, int)
        assert isinstance(width, int) or width is None
        assert isinstance(height, int) or height is None
        if isinstance(console, Console):
            self.console = console
            self.x = x
            self.y = y
            if width is None:
                self.width = console.width - x
            else:
                self.width = width
            if height is None:
                self.height = console.height - y
            else:
                self.height = height
        elif isinstance(console, Window):
            self.console = console.console
            self.x = console.x + x
            self.y = console.y + y
            if width is None:
                self.width = console.width - self.x
            else:
                self.width = width
            if height is None:
                self.height = console.height - self.y
            else:
                self.height = height
        else:
            raise TypeError('console must be a Console or Window instance')
        assert x + width <= console.width
        assert y + height <= console.height

    def _drawable(self, x, y):
        """Used internally"""
        # Check if a cell is part of the console.
        # Raises an exception if it can not be used.
        #
        # This check is used BEFORE translation! (before x and y are changed)
        assert isinstance(x, int)
        assert isinstance(y, int)
        if 0 <= x < self.width and 0 <= y < self.height:
            return
        raise TDLIndexError('(%i, %i) is outside of the Window' % (x, y))


    def blit(self, source, x=0, y=0, width=None, height=None, srcx=0, srcy=0, alpha=255):
        if width is None:
            width = min(source.width, self.width) - x
        if height is None:
            height = min(source.height, self.height) - y

        if isinstance(source, Window):
            srcx += source.x
            srcy += source.y
            source = source.console

        self.console.blit(source, x + self.x, y + self.y, width, height,
                          srcx, srcy, alpha)

    def clear(self, fillcolor):
        """Clears the entire Window.
        """
        assert _iscolor(fillcolor), 'fillcolor must be a 3 item list'
        assert fillcolor is not None, 'fillcolor can not be None'
        self.draw_rect(C_WHITE, fillcolor, -1)

    def draw_char(self, fgcolor, bgcolor, char, x, y, bgblend=BND_SET):
        self._drawable(x, y)
        self.console.draw_char(fgcolor, bgcolor, char, x + self.x, y + self.y, bgblend)

    def draw_str(self, fgcolor, bgcolor, string, x, y, bgblend=BND_SET):
        # same as Console.draw.str with only a few changes
        assert _iscolor(fgcolor), 'fgcolor must be a 3 item list or None'
        assert _iscolor(bgcolor), 'bgcolor must be a 3 item list or None'
        self._drawable(x, y)
        x += self.x
        y += self.y

        assert isinstance(string, (str, unicode))
        if string == '':
            return

        width, height = self.width, self.height
        wrapx = self.x
        console = self.console

        if bgcolor is None or fgcolor is None:
            if fgcolor is not None:
                fgcolor = _Color(*fgcolor)
            if bgcolor is not None:
                bgcolor = _Color(*bgcolor)
            setc = _lib.TCOD_console_set_char
            setfg = _lib.TCOD_console_set_fore
            setbg = _lib.TCOD_console_set_back
            for char in string:
                setc(console, x, y, ord(char))
                if fgcolor is not None:
                    setfg(console, x, y, fgcolor)
                if bgcolor is not None:
                    setbg(console, x, y, bgcolor)
                x += 1
                if x == wrapx + width:
                    x = wrapx
                    y += 1
                    if y == self.y + height:
                        return
        else:
            _lib.TCOD_console_set_foreground_color(console, _Color(*fgcolor))
            _lib.TCOD_console_set_background_color(console, _Color(*bgcolor))
            draw = _lib.TCOD_console_put_char
            for char in string:
                draw(console, x, y, ord(char), bgblend)
                x += 1
                if x == x + width:
                    x = wrapx
                    y += 1
                    if y == y + height:
                        return

    def draw_rect(self, fgcolor, bgcolor, char, x=0, y=0, width=None, height=None,
                  filled=True, bgblend=BND_SET):
        self._drawable(x, y)
        rootx = self.x + x
        rooty = self.y + y

        if width is None:
            width = self.width - x
        if height is None:
            height = self.height - y

        if x + width > self.width or y + height > self.height:
            raise TDLDrawError('Rectangle extends outside of the Window')

        self.console.draw_rect(fgcolor, bgcolor, char, rootx, rooty, width, height,
                               filled, bgblend)

    def draw_hline(fgcolor, bgcolor, char, x, y, width=None, bgblend=BND_SET):
        self._drawable(x, y)

        assert isinstance(width, (int, long)) or width is None, \
               'width must be an integer or None'

        if width is None:
            width = self.width - x

        self.console.draw_hline(fgcolor, bgcolor, char, x + self.x, y + self.y, width, bgblend)

    def draw_vline(fgcolor, bgcolor, char, x, y, height=None, bgblend=BND_SET):
        self._drawable(x, y)

        assert isinstance(height, (int, long)) or height is None, \
               'width must be an integer or None'

        if height is None:
            height = self.height - y

        self.console.draw_hline(fgcolor, bgcolor, char, x + self.x, y + self.y, height, bgblend)

    def get_char(self, x, y):
        """Return the character and colors of a cell as (ch, fg, bg)
        """
        self._drawable(x, y)
        return self.console.get_char(x + self.x, y + self.y)

    def get_size(self):
        """Return the size of the Window as (width, height)
        """
        return self.width, self.height

    def __repr__(self):
        return "<Window(X=%i Y=%i Width=%i Height=%i)>" % (self.x, self.y,
                                                          self.width,
                                                          self.height)


def _iscolor(color):
    """Used internally
    A debug function to see if an object can be used as a TCOD color struct.
    None counts as a parameter to not change colors.
    """
    try:
        if color is None or len(color) == 3:
            return True
    except TypeError: # object has no __len__ function
        pass
    return False


def init(w, h, title='TDL', fullscreen=False):
    """Start the main console with a width of w and height of h and return the
    root console.

    Remember to use flush() after drawing on all consoles.

    After the root console is garbage collected the window will close.
    """
    global _rootinitialized, _rootconsole
    if not _fontinitialized: # set the default font to the one that comes with tdl
        set_font(resource_filename(__name__, 'terminal8x8_aa_as.png'),
                 16, 16, FONT_LAYOUT_ASCII_INCOL)

    # If a console already exists then make a clone to replace it
    if _rootconsole is not None:
        oldroot = _rootconsole()
        rootreplacement = Console(oldroot.width, oldroot.height)
        rootreplacement.blit(oldroot)
        oldroot._replace(rootreplacement)
        del rootreplacement

    _lib.TCOD_console_init_root(w, h, title, fullscreen)

    event.get() # flush the libtcod event queue to fix some issues
    # issues may be fixed already

    event._eventsflushed = False
    _rootinitialized = True
    rootconsole = Console(0, 0)._replace(ctypes.c_void_p())
    _rootconsole = weakref.ref(rootconsole)

    return rootconsole

def flush():
    """Make all changes visible and update the screen.
    """
    if not _rootinitialized:
        raise TDLError('Cannot flush without first initializing')
    if event._autoflush and not event._eventsflushed:
        event.get()
    else: # do not flush events after the user starts using them
        event._autoflush = False
    event._eventsflushed = False
    _lib.TCOD_console_flush()

def set_font(path, h, v, flags):
    """Changes the font to be used for this session
    This should be called before tdl.init

    path must be a string for where a bitmap file is found.

    w and h should be the width and height of an individual tite.

    flags are used to define the characters layout in the bitmap and the font type :
    FONT_LAYOUT_ASCII_INCOL : characters in ASCII order, code 0-15 in the first column
    FONT_LAYOUT_ASCII_INROW : characters in ASCII order, code 0-15 in the first row
    FONT_LAYOUT_TCOD : simplified layout, see libtcod documents
    FONT_TYPE_GREYSCALE : create an anti-aliased font from a greyscale bitmap
    """
    global _fontinitialized
    _fontinitialized = True
    _lib.TCOD_console_set_custom_font(path, flags, h, v)

def get_fullscreen():
    """Returns if the window is fullscreen

    The user can't make the window fullscreen so you must use the
    set_fullscreen function
    """
    if not _rootinitialized:
        raise TDLError('Initialize first')
    return _lib.TCOD_console_is_fullscreen()

def set_fullscreen(fullscreen):
    """Sets the fullscreen state to the boolen value
    """
    if not _rootinitialized:
        raise TDLError('Initialize first')
    _lib.TCOD_console_set_fullscreen(fullscreen)

def set_title(title):
    """Change the window title.
    """
    if not _rootinitialized:
        raise TDLError('Initialize first')
    _lib.TCOD_console_set_window_title(title)

def set_fade(color, fade):
    """Have the screen fade out into a color.

    color is a 3 item tuple or list.
    fade is a number between 0 and 255 with 0 making the screen one solid color
    and 255 turning the fade effect off.
    """
    if not _rootinitialized:
        raise TDLError('Initialize first')
    _lib.TCOD_console_set_fade(fade, _Color(*color))

def get_fade():
    """Return the current fade of the screen as (color, fade)
    """
    if not _rootinitialized:
        raise TDLError('Initialize first')
    fade = _lib.TCOD_console_get_fade()
    fadecolor = tuple(_lib.TCOD_console_get_fading_color())
    return fadecolor, fade

def screenshot(fileobj=None):
    """Capture the screen and place it in fileobj.

    fileobj can be a filelike object or a filepath to save the screenshot
    if fileobj is none the file will be placed in the current folder with named
    screenshotNNNN.png
    """
    if not _rootinitialized:
        raise TDLError('Initialize first')
    if isinstance(fileobj, str):
        _lib.TCOD_sys_save_screenshot(path)
    elif isinstance(fileobj, file):
        filename = os.tempnam()
        _lib.TCOD_sys_save_screenshot(filename)
        fileobj.write(file(filename, 'r').read())
        os.remove(filename)
    elif fileobj is None:
        filelist = os.listdir('.')
        n = 0
        filename = 'screenshot%.4i.png' % n
        while filename in filelist:
            n += 1
            filename = 'screenshot%.4i.png' % n
        _lib.TCOD_sys_save_screenshot(filename)
    else:
        raise TypeError('fileobj is an invalid type: %s' % type(fileobj))

def set_fps(fps):
    """Set the frames per second.

    You can set no limit by using None or 0.
    """
    if fps is None:
        fps = 0
    assert isinstance(fps, int), 'fps must be an integer or None'
    _lib.TCOD_sys_set_fps(fps)

def get_fps():
    """Return the frames per second.
    """
    return _lib.TCOD_sys_get_fps()

def force_resolution(w, h):
    """Change the fullscreen resoulution
    """
    _lib.TCOD_sys_force_fullscreen_resolution(w, h)

def bresenham(startx, starty, endx, endy):
    """Returns a list of points between and including the start and end points.
    The points create a bresenham line.
    """
    _lib.TCOD_line_init(startx, starty, endx, endy)
    finished = False
    pointlist = []
    x = ctypes.c_int()
    y = ctypes.c_int()
    while not finished:
        finished = _lib.TCOD_line_step(x, y)
        pointlist.append((x.value, y.value))
    return pointlist

__all__ = [var for var in locals().keys() if not '_' in var[0]]

