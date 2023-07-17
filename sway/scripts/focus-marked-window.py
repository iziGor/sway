#!/usr/bin/env python3
#
# vim: autoindent smartindent expandtab smarttab tabstop=4 softtabstop=4 shiftwidth=4 foldmethod=marker:

from argparse import ArgumentParser
from subprocess import run, CalledProcessError
from os.path import basename
from sys import exit
import i3ipc

i3 = i3ipc.Connection()

def all_windows():
    ''' obteno dil tota listo markizita fenestri, inkluzante kladala '''
    tree = i3.get_tree()
    aNodes = []
    for e in tree.find_marked():
        # aNodes.append({ "name": "{}: {}".format( e.workspace().name, e.name )
        aNodes.append({ "name": make_choice_string( e )
                      , "con_id": e.id })
        # aNodes.append( e )

    return aNodes

def make_choice_string( e ):
    ''' kompozo do lineo kun informajo pri fenestro markizita '''
    return '{}: \"{}\" marks={}'.format(
        '(hidden)' if e.workspace().name == '__i3_scratch' else e.workspace().name,
        e.name,
        repr( e.marks ))

# def make_choice_strings( a ):
    # aRet = []
    # for e in a:
        # aRet.append( '{}: \"{}\" marks={}'.format(
            # e.workspace().name
            # , e.name
            # , repr( e.marks )
            # ) )
    # return aRet

if __name__ == '__main__':
    parser = ArgumentParser(description = 'Print the names of the focused window of each workspace.')
    parser.add_argument('--menu', default='rofi', help='The menu command to run (ex: --menu=dmenu)')
    parser.add_argument('--focus', action='store_true', help='Switch to selected marked window')
    parser.add_argument('--mark', action='store_true', help='Set mark on window')
    # parser.parse_args()
    (args, menu_args) = parser.parse_known_args()

    if len(menu_args) and menu_args[0] == '--':
        menu_args = menu_args[1:]

    win = ''

    # set default menu args for supported menus
    if basename(args.menu) == 'dmenu':
        menu_args += ['-i', '-f']
    elif basename(args.menu) == 'rofi':
        # menu_args += ['-show', '-dmenu', '-p', 'Win: ', '-theme-str', 'listview {{ lines: {}; }}'.format( min( len(aNodes), 10 ) )]
        menu_args += [ '-dmenu'
                     , '-p', 'Enter mark:'
                     , '-theme-str', 'inputbar { border-radius: 15px 15px 15px 15px; }']
                     # , '-theme-str', 'inputbar { border-radius: 15px 15px 15px 15px; } listview { enabled: false; }']

    if  args.focus:
        aNodes = all_windows()
        if  len(aNodes) == 0:
            menu_args = [ '-e', 'Marked windows not found'
                         , '-theme-str', 'window { width: 25%; } textbox { horizontal-align: 0.5; }']
            run( [args.menu] + menu_args )
            exit(0)

        menu_args = [ '-dmenu'
                    , '-p', 'Select from marks:'
                    , '-theme-str', 'listview {{ lines: {}; }}'.format( min( len(aNodes), 10 ) )]
        try:
            win = run( [args.menu] + menu_args
                     , input='\n'.join([ e.get("name") for e in aNodes ])
                     , check=True
                     , capture_output=True
                     , encoding='UTF-8'
                     ).stdout.strip()
            # win = run( [args.menu] + menu_args
                     # , input=bytes('\n'.join([e.get("name") for e in aNodes]), 'UTF-8')
                     # , check=True
                     # , stdout=PIPE
                     # ).stdout.decode('UTF-8').strip()
        except CalledProcessError as e:
            exit(e.returncode)

        if not win:
            # nothing to do
            exit(0)

        for e in aNodes:
            if  win == e.get("name").strip():
                i3.command("[con_id=%s] focus" % e.get("con_id"))
                break

    if  args.mark:
        tree = i3.get_tree()
        curr_win = tree.find_focused().id
        menu_args = [ '-dmenu'
                    , '-p', 'Enter a character for mark:'
                    , '-theme-str', 'configuration { inputchange { action: "kb-accept-entry"; } }'
                    , '-theme-str', 'window { width: 25%; }'
                    , '-theme-str', 'inputbar { border-radius: 10px; }'
                    , '-theme-str', 'listview { enabled: false; }' ]
        mrk = run( [args.menu] + menu_args
                 , input=''
                 , check=True
                 , capture_output=True
                 , encoding='UTF-8'
                 ).stdout.strip()
        if  mrk:
            i3.command( f"[con_id={curr_win}] mark {mrk}" )
