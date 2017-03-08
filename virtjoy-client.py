#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import time
import struct
import uinput
import socket

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib

VERSION = 0
SEND_TIMEOUT = 100

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
    status, conf = data
    pressed = event.type == Gdk.EventType.KEY_PRESS
    control = event.keyval
    #print("Key {} was {}".format(event.keyval, "pressed" if pressed else "released"))
    if control in BTN_MAP:
        status[control] = 1 if pressed else 0
    if control in AXIS_MAP:
        status[control] = 1 if pressed else 0
    send_packet(data)
    return True

def build_emitted_status(status):
    emitted = {}
    for control, btn in BTN_MAP.items():
        emitted[btn] = status[control]
    axes = {}
    for control, (axis, dir_) in AXIS_MAP.items():
        if axis not in axes:
            axes[axis] = 0
        axes[axis] += dir_ if status[control] else 0
    for axis, value in axes.items():
        emitted[axis] = value
    return emitted

def build_packet(name, emitted):
    packet = bytes()
    packet += struct.pack('B', VERSION)
    packet += struct.pack('B', len(name))
    packet += name.encode('utf-8')
    packet += struct.pack('B', len(emitted))
    for (evtype, elem), value in emitted.items():
        packet += struct.pack('!BHh', evtype, elem, value)
    return packet

def send_packet(data):
    status, conf = data
    packet = build_packet(conf['name'], build_emitted_status(status))
    #print(repr(packet))
    conf['sock'].sendto(packet, (conf['ip'], conf['port']))
    return True

# Based on http://unix.stackexchange.com/a/290606/31311
# See also http://thiemonge.org/getting-started-with-uinput
# Events in /usr/include/linux/input-event-codes.h
# There does not appear to be much more docs available, although
# docstrings may help a little bit...
def main():
    conf = {}
    conf['ip'] = sys.argv[1]
    conf['port'] = int(sys.argv[2])
    conf['name'] = sys.argv[3]
    conf['sock'] = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    events = []
    status = {}
    for control, btn in BTN_MAP.items():
        events.append(btn)
        status[control] = 0
    for control, (axis, direction) in AXIS_MAP.items():
        events.append(axis + (-1, 1, 0, 0))
        status[control] = 0

    GLib.timeout_add(SEND_TIMEOUT, send_packet, (status, conf))

    win = Gtk.Window()
    win.connect("delete-event", Gtk.main_quit)
    win.connect("key-press-event", key_acted, (status, conf))
    win.connect("key-release-event", key_acted, (status, conf))
    win.show_all()

    Gtk.main()

if __name__ == '__main__':
    main()
