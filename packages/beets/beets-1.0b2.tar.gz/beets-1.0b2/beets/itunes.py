# This file is part of beets.
# Copyright 2010, Adrian Sampson.
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
# 
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.

import os
import urllib

PREAMBLE = '''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple Computer//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
'''
POSTAMBLE = "</dict>\n</plist>\n"

TRACKS_INTRO = "<key>Tracks</key>\n<dict>\n"
TRACKS_OUTRO = "</dict>\n"
TRACK_INTRO = "<key>%i</key>\n<dict>\n"
TRACK_OUTRO = "</dict>\n"

KV_INT = "<key>%s</key><integer>%i</integer>\n"
KV_STR = "<key>%s</key><string>%s</string>\n"
KV_TRUE = "<key>%s</key><true/>\n"
KV_FALSE = "<key>%s</key><false/>\n"

def fileurl(path):
    return 'file://' + urllib.pathname2url(path)

def write_kv(fh, key, val):
    if isinstance(val, int):
        fh.write(KV_INT % (key, val))
    elif isinstance(val, basestring):
        # fixme XML escaping?
        fh.write(KV_STR % (key, val))
    elif isinstance(val, bool):
        if val:
            fh.write(KV_TRUE % key)
        else:
            fh.write(KV_FALSE % key)

def write_itunes_xml(lib, fh):
    # Preamble.
    fh.write(PREAMBLE)
    
    # Library settings.
    write_kv(fh, 'Major Version', 1)
    write_kv(fh, 'Minor Version', 1)
    write_kv(fh, 'Application Version', '8.2')
    write_kv(fh, 'Features', 1)
    write_kv(fh, 'Show Content Ratings', True) #fixme mimic current library
    write_kv(fh, 'Music Folder', fileurl(lib.options['directory']))
    
    # Tracks.
    fh.write(TRACKS_INTRO)
    for item in lib.items():
        fh.write(TRACK_INTRO % item.id)
        write_kv(fh, 'Track ID', item.id)
        write_kv(fh, 'Name', item.title)
        # write_kv(fh, 'Album Artist', item.albumartist)
        write_kv(fh, 'Genre', item.genre)
        # 'Kind', 'beets audio file', #FIXME
        # write_kv(fh, 'Size', XXX, #FIXME
        write_kv(fh, 'Total Time', int(item.length))
        # 'Date Modified'
        # 'Date Added'
        write_kv(fh, 'Bit Rate', item.bitrate)
        # write_kv(fh, 'Sample Rate', item.samplerate)
        write_kv(fh, 'Comments', item.comments)
        write_kv(fh, 'Persistent ID', str(item.id)) #FIXME ????
        write_kv(fh, 'Location', fileurl(item.path))
        write_kv(fh, 'File Folder Count', -1)
        write_kv(fh, 'Library Folder Count', -1)
        fh.write(TRACK_OUTRO)
    fh.write(TRACKS_OUTRO)
    
    fh.write(POSTAMBLE)

def export_itunes_xml(lib, path='~/Music/iTunes/iTunes Music Library.xml'):
    # CLOBBER BINARY DB
    path = os.path.expanduser(path)
    if os.path.lexists(path):
        os.rename(path, path + '.old')
    fh = open(path, 'w')
    write_itunes_xml(lib, fh)
    fh.close
