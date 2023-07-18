#!/usr/bin/env python3
#
# vim: autoindent smartindent expandtab smarttab tabstop=4 softtabstop=4 shiftwidth=4 foldmethod=marker:

from argparse import ArgumentParser
from subprocess import run, CalledProcessError
from os.path import basename
from sys import exit
import i3ipc

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

def clear_all_marks_of_current_window( id ):
    # kompleta efaco di omna marki che fenestro aktualigita,
    # qua atingesas per remplasigar omna marki dil fenestro
    # per marko "clear" e posa efaco ca marko
    i3.command( f"[con_id={id}] mark --replace --toggle clear" )
    i3.command( f"[con_id={id}] mark --replace --toggle clear" )


if  __name__ == '__main__':
    parser = ArgumentParser(description = 'Operacas marki dil fenestri')
    parser.add_argument('--menu', default='rofi', help='The menu command to run (ex: --menu=dmenu)')
    parser.add_argument('--focus', action='store_true', help='Switch to selected marked window')
    parser.add_argument('--mark', action='store_true', help='Set mark on window')
    parser.add_argument('--add', action='store_true', help='Add-mode on setting of current windows mark')
    parser.add_argument('--replace', action='store_true', help='Replace-mode on setting of current windows mark')
    parser.add_argument('--clear', action='store_true', help='Clear-mode on setting of current windows mark')
    parser.add_argument('--clear-all', action='store_true', help='Clear all marks on current window')
    # parser.parse_args()
    (args, menu_args) = parser.parse_known_args()

    if  len(menu_args) and menu_args[0] == '--':
        menu_args = menu_args[1:]

    # set default menu args for supported menus
    if  basename(args.menu) == 'dmenu':
        menu_args += ['-i', '-f']
    elif basename(args.menu) == 'rofi':
        # menu_args += ['-show', '-dmenu', '-p', 'Win: ', '-theme-str', 'listview {{ lines: {}; }}'.format( min( len(aNodes), 10 ) )]
        menu_args += [ '-dmenu'
                     , '-p', 'Enter mark:'
                     , '-theme-str', 'inputbar { border-radius: 15px 15px 15px 15px; }']
                     # , '-theme-str', 'inputbar { border-radius: 15px 15px 15px 15px; } listview { enabled: false; }']

    win = ''
    i3 = i3ipc.Connection()

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

        if  win:
            for e in aNodes:
                if  win == e.get("name").strip():
                    i3.command("[con_id=%s] focus" % e.get("con_id"))
                    break

        # nothing to do more
        exit(0)

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

        # nothing to do more
        exit(0)

    if  args.clear_all:
        clear_all_marks_of_current_window( i3.get_tree().find_focused().id )

        # nothing to do more
        exit(0)

