__author__ = 'phoehne'

import os, sys, stat

def walk_directories(current_directory):
    file_list = []
    for dir in os.listdir(current_directory):
        pathname = os.path.join(current_directory, dir)
        mode = os.stat(pathname).st_mode

        if stat.S_ISDIR(mode):
            file_list.extend(walk_directories(pathname))
        else:
            file_list.append({u'filename': dir, u'partial-directory': pathname})
    return file_list