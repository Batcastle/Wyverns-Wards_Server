#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  w&w_server.py
#
#  Copyright 2024 Thomas Castleman <batcastle@draugeros.org>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#
"""Explain what this program does here!!!"""
from __future__ import print_function
import sys
import random
from flask import Flask


def __eprint__(*args, **kwargs):
    """Make it easier for us to print to stderr"""
    print(*args, file=sys.stderr, **kwargs)


if sys.version_info[0] == 2:
    __eprint__("Please run with Python 3 as Python 2 is End-of-Life.")
    exit(2)

APP = Flask(__name__)


def generate_session_key():
        """Generate a random string that follows these rules:
        - 8-64 characters long
        - Characters should be a randomly generated string of letters and numbers
        """
        remaining_len = random.randint(8, 64)
        allowed_letters = ["A", "B", "C", "D", "E", "F", "G", "H", "J", "K",
                           "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U",
                           "V", "W", "X", "Y", "Z", "a", "b", "c", "d", "e",
                           "f", "g", "h", "i", "j", "k", "l", "m", "n", "o",
                           "p", "q", "r", "s", "t", "u", "v", "w", "x", "y",
                           "z"]
        allowed_numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        allowed_special = ["@", ":", ";", "&", "$", "%", "*", "+", "=", "-",
                           "_", "~", ",", "."]
        string = []
        while remaining_len > 0:
            choice = random.randint(0, 100) % 3
            if choice == 0:
                # letter
                string.append(random.sample(allowed_letters, 1)[0])
            elif choice == 1:
                # special
                string.append(random.sample(allowed_special, 1)[0])
            else:
                # number
                string.append(random.sample(allowed_numbers, 1)[0])
            remaining_len -= 1
        string = "".join(string)
        return string

keys = []

@APP.route("/get_key")
def get_key():
    """Create new key
    This will follow a given session through to the end.
    A given client needs a key to interact with the server in any way.
    """
    key = generate_session_key()
    keys.append(key)
    return {"Session Key": key, "Access": f"http://192.168.1.59:5000/{ key }"}


@APP.route("/<key>")
def KeyAccept(key):
    """Quick and dirty key test. If a client gets 500, request a new key."""
    if key in keys:
        return {"Status": 200}
    return {"Status": 500}
    

if __name__ == "__main__":
    # get length of argv
    ARGC = len(sys.argv)
    if ("--debug" in sys.argv) or ("-debug" in sys.argv) or ("-d" in sys.argv):
        mode=True
    else:
        mode=False
    APP.run(host="0.0.0.0", debug=mode)

