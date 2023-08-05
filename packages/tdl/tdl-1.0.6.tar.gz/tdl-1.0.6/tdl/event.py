"""
    This module handles user input.

    QUIT
    KEYDOWN  key char alt ctrl shift lalt lctrl ralt rctrl
    MOUSEDOWN  button pos cell
    MOUSEUP  button pos cell
    MOUSEMOTION  pos cell relpos relcell

    You can use the pygame like tdl.event.get function or use the keywait and
    window_closed functions.
"""

import ctypes

from tcod import _lib, _Mouse
import local

# make sure that the program does not lock up from missing event flushes
_eventsflushed = False # not that it works to well to fix that problem

_autoflush = True

_mousel = 0
_mousem = 0
_mouser = 0

class Event(object):
    __slots__ = ()
    type = None

    def __repr__(self):
        attrdict = {}
        for varname in dir(self):
            if '_' in varname:
                continue
            attrdict[varname] = self.__getattribute__(varname)
        return '%s Event %s' % (self.__class__.__name__, repr(attrdict))

class Quit(Event):
    __slots__ = ()
    type = local.QUIT

class KeyEvent(Event):
    __slots__ = ('key', 'char', 'lalt', 'lctrl', 'ralt', 'rctrl', 'shift',
                 'alt', 'ctrl')

    def __init__(self, key, char, lalt, lctrl, ralt, rctrl, shift):
        self.key = key
        self.char = char.replace('\x00', '') # change null to empty string
        self.lalt = bool(lalt)
        self.ralt = bool(ralt)
        self.lctrl = bool(lctrl)
        self.rctrl = bool(rctrl)
        self.shift = bool(shift)
        self.alt = bool(lalt or ralt)
        self.ctrl = bool(lctrl or rctrl)

class KeyDown(KeyEvent):
    __slots__ = ()
    type = local.KEYDOWN

class KeyUp(KeyEvent):
    __slots__ = ()
    type = local.KEYUP

class MouseButtonEvent(Event):
    __slots__ = ('button', 'pos', 'cell')
    type = local.MOUSEDOWN

    def __init__(self, button, pos, cell):
        self.button = button
        self.pos = pos
        self.cell = cell

class MouseDown(MouseButtonEvent):
    __slots__ = ()
    type = local.MOUSEDOWN

class MouseUp(MouseButtonEvent):
    __slots__ = ()
    type = local.MOUSEUP

class MouseMotion(Event):
    __slots__ = ('pos', 'cell', 'relpos', 'relcell')
    type = local.MOUSEMOTION

    def __init__(self, pos, cell, relpos, relcell):
        self.pos = pos
        self.cell = cell
        self.relpos = relpos
        self.relcell = relcell

def get():
    """Returns a list of events.
    Anyone who has used pygame before should know how this function works.
    You can check the type of event by using event.type or isinstance.
    """
    global _mousel, _mousem, _mouser, _eventsflushed
    _eventsflushed = True
    events = []
    while 1:
        libkey = _lib.TCOD_console_check_for_keypress(3)
        if libkey.vk == local.K_NONE:
            break
        if libkey.pressed:
            keyevent = KeyDown
        else:
            keyevent = KeyUp
        events.append(keyevent(libkey.vk, libkey.c, libkey.lalt, libkey.lctrl,
                               libkey.ralt, libkey.rctrl, libkey.shift))

    mouse = _Mouse()
    _lib.TCOD_mouse_get_status(mouse)
    if mouse.dx or mouse.dy:
        events.append(MouseMotion((mouse.x, mouse.y),
                                  (mouse.cx, mouse.cy),
                                  (mouse.dx, mouse.dy),
                                  (mouse.dcx, mouse.dcy)))

    mousepos = ((mouse.x, mouse.y), (mouse.cx, mouse.cy))

    for oldstate, newstate, released, button in zip((_mousel, _mousem, _mouser),
                                (mouse.lbutton, mouse.mbutton, mouse.rbutton),
                                (mouse.lbutton_pressed,
                                 mouse.mbutton_pressed,
                                 mouse.rbutton_pressed), (1, 2, 3)):
        if released:
            if not oldstate:
                events.append(MouseDown(button, *mousepos))
            events.append(MouseUp(button, *mousepos))
            if newstate:
                events.append(MouseDown(button, *mousepos))
        elif newstate and not oldstate:
            events.append(MouseDown(button, *mousepos))

    _mousel = mouse.lbutton
    _mousem = mouse.mbutton
    _mouser = mouse.rbutton

    if _lib.TCOD_console_is_window_closed():
        events.append(Quit())

    return events

def keywait():
    """Waits until the user presses a key.  Returns KeyDown events.
    """
    global _eventsflushed
    _eventsflushed = True
    flush = False
    libkey = _lib.TCOD_console_wait_for_keypress(flush)
    return KeyDown(libkey.vk, chr(libkey.c), libkey.lalt, libkey.lctrl,
                   libkey.ralt, libkey.rctrl, libkey.shift)

def keypressed(key):
    """Returns True when key is currently pressed.

    key can be a number or single length string
    """
    assert isinstace(key, (str, unicode, int)), "key must be a string or int"
    if not isinstance(key, int):
        assert len(key) == 1, "key can not be a multi character string"
        key = ord(key)
    return _lib.TCOD_console_check_for_keypress(key)

def window_closed():
    """Returns True if the exit button on the window has been clicked and
    stays True afterwards.
    """
    return _lib.TCOD_console_is_window_closed()

__all__ = [var for var in locals().keys() if not '_' in var[0]]
