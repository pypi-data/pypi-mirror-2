#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Helm
# helm_launcher.py

# Copyright (C) 2011 Anaël Verrier <elghinn@free.fr>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 only.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import sys

import glib


def main():
    config_dirs = (glib.get_user_config_dir(),) + glib.get_system_config_dirs()
    for config_dir in config_dirs:
        config_file = os.path.join(config_dir, 'helm', 'config.py')
        if os.path.exists(config_file):
            break
    else:
        config_file = 'config.py'
        if not os.path.exists(config_file):
            sys.exit('There is a problem with your helm installation.\n'
                     'I can not even find the default config file.')
    os.execl('/usr/bin/env', 'env', 'python', config_file)


if __name__ == '__main__':
    main()
