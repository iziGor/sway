#!/usr/bin/env python3
#
# vim: autoindent smartindent expandtab smarttab tabstop=4 softtabstop=4 shiftwidth=4 foldmethod=marker:

from argparse import ArgumentParser
from subprocess import run, CalledProcessError
from os.path import basename
from sys import exit
from i3ipc import Connection

i3 = Connection()

def all_windows():
    tree = i3.get_tree()
    aNodes = []
    for ws in tree.workspaces():
        for e in ws.leaves() + ws.floating_nodes:
            # coname = e.name
            # wsname = e.workspace().name
            # con_id = e.id
            aNodes.append({ "name": "{}: {}".format( e.workspace().name, e.name )
                          , "con_id": e.id })
    return aNodes


if  __name__ == '__main__':
    parser = ArgumentParser(description = 'Print the names of the focused window of each workspace.')
    parser.add_argument('--menu', default='rofi', help='The menu command to run (ex: --menu=dmenu)')
    # parser.parse_args()
    (args, menu_args) = parser.parse_known_args()

    if  len(menu_args) and menu_args[0] == '--':
        menu_args = menu_args[1:]

    win = ''
    aNodes = all_windows()

    # set default menu args for supported menus
    if  basename(args.menu) == 'dmenu':
        menu_args += [ '-i', '-f' ]
    elif basename(args.menu) == 'rofi':
        menu_args += [ '-show', '-dmenu', '-p', 'Win: '
                     , '-theme-str', 'listview {{ lines: {}; }}'.format( min( len(aNodes), 10 )) ]
    try:
        win = run( [args.menu] + menu_args
                 , input='\n'.join([ e.get("name") for e in aNodes ])
                 , check=True
                 , capture_output=True
                 , encoding='UTF-8'
                 ).stdout.strip()
    except CalledProcessError as e:
        exit(e.returncode)

    if  win:
        for e in aNodes:
            if  win == e.get("name").strip():
                i3.command("[con_id=%s] focus" % e.get("con_id"))
                break
    # nothing to do
    exit(0)

