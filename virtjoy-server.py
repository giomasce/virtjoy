#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import uinput
import time
import select
import socket

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib

BUFSIZE = 2500

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

# uinput code is ased on http://unix.stackexchange.com/a/290606/31311
# See also http://thiemonge.org/getting-started-with-uinput
# Events in /usr/include/linux/input-event-codes.h
# There does not appear to be much more docs available, although
# docstrings may help a little bit...
def main():
    conf = {}
    ip = sys.argv[1]
    port = int(sys.argv[2])

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((ip, port))

    events = []
    for btn in BTN_MAP.values():
        events.append(btn)
    for axis, direction in AXIS_MAP.values():
        events.append(axis + (-1, 1, 0, 0))
    device = uinput.Device(events, 'virtjoy')

    #for event in events:
    #    device.emit(event, 0, syn=False)
    #while True:
    #    device.emit(uinput.BTN_NORTH, 1)
    #    time.sleep(1.0)
    #    device.emit(uinput.BTN_NORTH, 0)
    #    time.sleep(1.0)

    while True:
        data, addr = sock.recvfrom(BUFSIZE)
        print("received from {}: {}".format(data, addr))

if __name__ == '__main__':
    main()
