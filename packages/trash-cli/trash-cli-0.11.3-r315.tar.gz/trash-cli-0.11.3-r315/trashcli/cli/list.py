#!/usr/bin/python
# trash-list: list trashed files
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

def get_option_parser():
    from trashcli import version
    from optparse import OptionParser
    from optparse import IndentedHelpFormatter
    from trashcli.cli.util import NoWrapFormatter

    parser = OptionParser(usage="%prog",
                          description="List trashed files",
                          version="%%prog %s" % version,
                          formatter=NoWrapFormatter(),
                          epilog=
    """Report bugs to http://code.google.com/p/trash-cli/issues""")

    return parser

from trashcli.trash import *

def main(argv=None) :
    trashsystem = GlobalTrashCan()

    parser = get_option_parser()
    (options, args) = parser.parse_args(argv)

    for trashed_file in trashsystem.trashed_files() :
        print "%s %s" % (trashed_file.deletion_date, trashed_file.path)
