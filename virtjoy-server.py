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
import uinput
import time
import select
import socket
import struct

BUFSIZE = 2500

VERSION = 0

def split_packet(packet, i):
    if len(packet) < i:
        raise Exception()
    return packet[:i], packet[i:]

def decode_packet(packet):
    try:
        piece, packet = split_packet(packet, 1)
        version, = struct.unpack('B', piece)
        if version != VERSION:
            return None

        piece, packet = split_packet(packet, 1)
        length, = struct.unpack('B', piece)
        if length == 0:
            return None
        piece, packet = split_packet(packet, length)
        name = piece.decode('utf-8')

        piece, packet = split_packet(packet, 1)
        length, = struct.unpack('B', piece)
        status = {}
        for i in range(length):
            piece, packet = split_packet(packet, 5)
            evtype, elem, value = struct.unpack("!BHh", piece)
            status[(evtype, elem)] = value

        return name, status

    # Packet is not valid
    except:
        return None

def process_packet(packet, devices):
    name, status = decode_packet(packet)
    if name not in devices:
        events = []
        for elem in status:
            # Append limits to axes
            if elem[0] == 3:
                events.append(elem + (-1, 1, 0, 0))
            else:
                events.append(elem)
        devices[name] = uinput.Device(events, 'virtjoy-{}'.format(name))

    device = devices[name]
    for elem, value in status.items():
        device.emit(elem, value)

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

    devices = {}
    while True:
        packet, addr = sock.recvfrom(BUFSIZE)
        process_packet(packet, devices)

if __name__ == '__main__':
    main()
