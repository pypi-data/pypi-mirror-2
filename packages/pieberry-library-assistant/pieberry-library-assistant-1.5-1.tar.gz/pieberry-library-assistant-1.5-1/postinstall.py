#!python

import distutils
import sys, os

std = get_special_folder_path('CSIDL_DESKTOPDIRECTORY')

if argv[1] == '-install':
    os.mkdir(os.path.join(std, 'Pieberry'))
    create_shortcut('pieberrydl', 'Pieberry', os.path.join(std, 'Pieberry', 'pbrun'))

            
