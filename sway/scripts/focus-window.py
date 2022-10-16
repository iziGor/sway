#!/usr/bin/env python3
#
# vim: autoindent smartindent expandtab smarttab tabstop=4 softtabstop=4 shiftwidth=4 foldmethod=marker:

from argparse import ArgumentParser
from subprocess import check_output, Popen, CalledProcessError
from os.path import basename
from sys import exit
import i3ipc

i3 = i3ipc.Connection()

def all_windows():
    tree = i3.get_tree()

    leaves = tree.leaves()
    aLeaves = []
    for container in leaves:

        if container:
            coname = container.name
            wsname = container.workspace().name
            con_id = container.id
            aLeaves.append({"name": "{}: {}".format(wsname, coname), "con_id": con_id})

        # print(':', coname)
        # print(wsname +':', 'con_id:', con_id, coname)

    return aLeaves


if __name__ == '__main__':
    parser = ArgumentParser(description = 'Print the names of the focused window of each workspace.')
    parser.add_argument('--menu', default='rofi', help='The menu command to run (ex: --menu=dmenu)')
    # parser.parse_args()
    (args, menu_args) = parser.parse_known_args()

    if len(menu_args) and menu_args[0] == '--':
        menu_args = menu_args[1:]

    win = ''
    aLeaves = all_windows()

    # set default menu args for supported menus
    if basename(args.menu) == 'dmenu':
        menu_args += ['-i', '-f']
    elif basename(args.menu) == 'rofi':
        menu_args += ['-show', '-dmenu', '-p', 'Win: ', '-theme-str', 'listview {{ lines: {}; }}'.format( min( len(aLeaves), 10 ) )]

    try:
        win = check_output([args.menu] + menu_args, input=bytes('\n'.join([e.get("name") for e in aLeaves]),
                'UTF-8')).decode('UTF-8').strip()
    except CalledProcessError as e:
        exit(e.returncode)

    if not win:
        # nothing to do
        exit(0)

    for e in aLeaves:
        # print("win:", '"'+win+'"', "\nname:", '"'+e.get("name")+'"')
        if  win == e.get("name").strip():
            i3.command("[con_id=%s] focus" % e.get("con_id"))
            # print("name:", e.get("name"))
            # print("con_id:", e.get("con_id"))
            break
