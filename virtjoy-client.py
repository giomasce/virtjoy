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

import sys
import time
import struct
import events
import socket

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib

VERSION = 0
SEND_TIMEOUT = 100

# For some reason keys are interpreted in funny ways by programs
# consuming them; I am not really sure where the issue is, but in my
# experient START and SELECT are L1 and R1, while DPAP_UP and
# DPAD_DOWN and START and SELECT; the others appear to be correct
BTN_MAP = {
    Gdk.KEY_d: events.BTN_C,
    Gdk.KEY_w: events.BTN_Y,
    Gdk.KEY_a: events.BTN_A,
    Gdk.KEY_s: events.BTN_B,

    Gdk.KEY_3: events.BTN_SELECT,
    Gdk.KEY_1: events.BTN_START,
    Gdk.KEY_q: events.BTN_X,
    Gdk.KEY_e: events.BTN_Z,

    Gdk.KEY_c: events.BTN_DPAD_UP,
    Gdk.KEY_v: events.BTN_DPAD_DOWN,
}

AXIS_MAP = {
    Gdk.KEY_Right: (events.ABS_X, 1),
    Gdk.KEY_Up: (events.ABS_Y, -1),
    Gdk.KEY_Left: (events.ABS_X, -1),
    Gdk.KEY_Down: (events.ABS_Y, 1),
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
