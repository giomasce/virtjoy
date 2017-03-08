#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This file is part of virtjoy.
# Copyright 2017 Giovanni Mascellani <gio@debian.org>
#
# Virtjoy is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# Virtjoy is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Nome-Programma.  If not, see
# <http://www.gnu.org/licenses/>.

import uinput
import time

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

BTN_MAP = {
    #Gdk.KEY_Right: uinput.BTN_DPAD_RIGHT,
    #Gdk.KEY_Up: uinput.BTN_DPAD_UP,
    #Gdk.KEY_Left: uinput.BTN_DPAD_LEFT,
    #Gdk.KEY_Down: uinput.BTN_DPAD_DOWN,

    Gdk.KEY_d: uinput.BTN_C,
    Gdk.KEY_w: uinput.BTN_Y,
    Gdk.KEY_a: uinput.BTN_A,
    Gdk.KEY_s: uinput.BTN_B,

    Gdk.KEY_3: uinput.BTN_SELECT,
    Gdk.KEY_1: uinput.BTN_START,
    Gdk.KEY_q: uinput.BTN_X,
    Gdk.KEY_e: uinput.BTN_Z,

    Gdk.KEY_c: uinput.BTN_DPAD_UP,
    Gdk.KEY_v: uinput.BTN_DPAD_DOWN,
}

AXIS_MAP = {
    Gdk.KEY_Right: (uinput.ABS_X, 1),
    Gdk.KEY_Up: (uinput.ABS_Y, -1),
    Gdk.KEY_Left: (uinput.ABS_X, -1),
    Gdk.KEY_Down: (uinput.ABS_Y, 1),
}

def key_acted(widget, event, data):
    device, status = data
    pressed = event.type == Gdk.EventType.KEY_PRESS
    control = event.keyval
    #print("Key {} was {}".format(event.keyval, "pressed" if pressed else "released"))
    if control in BTN_MAP:
        device.emit(BTN_MAP[control], 1 if pressed else 0)
    if control in AXIS_MAP:
        axis, direction = AXIS_MAP[control]
        status[control] = 1 if pressed else 0
        axes = {}
        for control2, (axis2, dir2) in AXIS_MAP.items():
            if axis2 not in axes:
                axes[axis2] = 0
            axes[axis2] += dir2 if status[control2] else 0
        for axis2, value in axes.items():
            device.emit(axis2, value)
    return True

# Based on http://unix.stackexchange.com/a/290606/31311
# See also http://thiemonge.org/getting-started-with-uinput
# Events in /usr/include/linux/input-event-codes.h
# There does not appear to be much more docs available, although
# docstrings may help a little bit...
def main():
    events = []
    status = {}
    for btn in BTN_MAP.values():
        events.append(btn)
    for control, (axis, direction) in AXIS_MAP.items():
        events.append(axis + (-1, 1, 0, 0))
        status[control] = 0
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
    win.connect("key-press-event", key_acted, (device, status))
    win.connect("key-release-event", key_acted, (device, status))
    win.show_all()

    Gtk.main()

if __name__ == '__main__':
    main()
