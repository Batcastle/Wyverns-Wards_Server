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
from flask_restful import Api, Resource
from flask import Flask


def __eprint__(*args, **kwargs):
    """Make it easier for us to print to stderr"""
    print(*args, file=sys.stderr, **kwargs)


if sys.version_info[0] == 2:
    __eprint__("Please run with Python 3 as Python 2 is End-of-Life.")
    exit(2)

APP = Flask(__name__)
API = Api(APP)


def connect_api(obj, api=API, path="/"):
    """Decorator to make adding API paths easier"""
    api.add_resource(obj, path)
    return obj


@connect_api
class HelloResource(Resource):
    def get(self):
        return {'Hello': 'World!'}



if __name__ == "__main__":
    # get length of argv
    ARGC = len(sys.argv)
    if ("--debug" in sys.argv) or ("-debug" in sys.argv) or ("-d" in sys.argv):
        mode=True
    else:
        mode=False
    APP.run(host="0.0.0.0", debug=mode)

