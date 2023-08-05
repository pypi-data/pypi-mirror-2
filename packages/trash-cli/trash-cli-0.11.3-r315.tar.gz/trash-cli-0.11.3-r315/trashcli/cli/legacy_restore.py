#!/usr/bin/python
# restore-trash: restore trashed file from the trashcan
#
# Copyright (C) 2007-2009 Andrea Francia Trivolzio(PV) Italy
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.

from trashcli.trash import *
import os

def main(argv=None):
    trashcan = GlobalTrashCan()

    def is_trashed_from_curdir(trashedfile):
        dir = os.path.realpath(os.curdir)
        if trashedfile.path.path.startswith(dir + os.path.sep) :
            return True

    trashed_files = []
    i = 0
    for trashedfile in filter(is_trashed_from_curdir, trashcan.trashed_files()) :
        trashed_files.append(trashedfile)
        print "%4d %s %s" % (i, trashedfile.deletion_date, trashedfile.path)
        i += 1

    if len(trashed_files) == 0 :
        print "No files trashed from current dir ('%s')" % os.path.realpath(os.curdir)
    else :
        index=raw_input("What file to restore [0..%d]: " % (len(trashed_files)-1))
        if index == "" :
            print "Exiting"
        else :
            index = int(index)
            try:
            	trashed_files[index].restore()
            except IOError, e:
	 	import sys
                print >> sys.stderr, str(e)
	 	sys.exit(1)	
