#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import uinput
import time

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

BTN_MAP = {
    Gdk.KEY_Right: uinput.BTN_DPAD_RIGHT,
    Gdk.KEY_Up: uinput.BTN_DPAD_UP,
    Gdk.KEY_Left: uinput.BTN_DPAD_LEFT,
    Gdk.KEY_Down: uinput.BTN_DPAD_DOWN,

    Gdk.KEY_d: uinput.BTN_EAST,
    Gdk.KEY_w: uinput.BTN_NORTH,
    Gdk.KEY_a: uinput.BTN_WEST,
    Gdk.KEY_s: uinput.BTN_SOUTH,

    Gdk.KEY_x: uinput.BTN_START,
    Gdk.KEY_z: uinput.BTN_SELECT,
    Gdk.KEY_q: uinput.BTN_TL,
    Gdk.KEY_e: uinput.BTN_TR,
    Gdk.KEY_1: uinput.BTN_TL2,
    Gdk.KEY_3: uinput.BTN_TR2,
}

def key_acted(widget, event, device):
    pressed = event.type == Gdk.EventType.KEY_PRESS
    #print("Key {} was {}".format(event.keyval, "pressed" if pressed else "released"))
    if event.keyval in BTN_MAP:
        device.emit(BTN_MAP[event.keyval], 1 if pressed else 0)
    return True

# Based on http://unix.stackexchange.com/a/290606/31311
# See also http://thiemonge.org/getting-started-with-uinput
# Events in /usr/include/linux/input-event-codes.h
# There does not appear to be much more docs available, although
# docstrings may help a little bit...
def main():
    events = (
        #uinput.BTN_JOYSTICK,

        #uinput.ABS_X + (-128, 127, 0, 0),
        #uinput.ABS_Y + (-128, 127, 0, 0),
        #uinput.ABS_RX + (-128, 127, 0, 0),
        #uinput.ABS_RY + (-128, 127, 0, 0),
        #uinput.ABS_THROTTLE + (-128, 127, 0, 0),
        #uinput.ABS_RUDDER + (-128, 127, 0, 0),
        #uinput.ABS_WHEEL + (-128, 127, 0, 0),
        #uinput.ABS_GAS + (-128, 127, 0, 0),

        uinput.BTN_DPAD_RIGHT,
        uinput.BTN_DPAD_UP,
        uinput.BTN_DPAD_LEFT,
        uinput.BTN_DPAD_DOWN,

        uinput.BTN_EAST,
        uinput.BTN_NORTH,
        uinput.BTN_WEST,
        uinput.BTN_SOUTH,

        uinput.BTN_START,
        uinput.BTN_SELECT,
        uinput.BTN_TL,
        uinput.BTN_TR,
        uinput.BTN_TL2,
        uinput.BTN_TR2,
    )
    device = uinput.Device(events, 'virtjoy')
    #for event in events:
    #    device.emit(event, 0, syn=False)
    #while True:
    #    device.emit(uinput.BTN_NORTH, 1)
    #    time.sleep(1.0)
    #    device.emit(uinput.BTN_NORTH, 0)
    #    time.sleep(1.0)

    win = Gtk.Window()
    win.connect("delete-event", Gtk.main_quit)
    win.connect("key-press-event", key_acted, device)
    win.connect("key-release-event", key_acted, device)
    win.show_all()

    Gtk.main()

if __name__ == '__main__':
    main()
