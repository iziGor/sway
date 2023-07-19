#!/usr/bin/env python3
# vim:autoindent:smartindent:expandtab:smarttab:tabstop=4:softtabstop=4:shiftwidth=4:foldmethod=marker

from i3ipc import Connection
from subprocess import Popen, PIPE
from collections import OrderedDict


SPREFIX = "(hidden):"


def dmenu(options, dmenu):
    '''Call dmenu with a list of options.'''

    cmd = Popen( dmenu
               , shell=True
               , stdin=PIPE
               , stdout=PIPE
               , stderr=PIPE
               )
    stdout, _ = cmd.communicate('\n'.join(options).encode('utf-8'))
    return stdout.decode('utf-8').strip('\n')

def is_focused_scratchpad():
    retval = False
    main_tree = Connection().get_tree()
    scratch_tree = main_tree.scratchpad()

    for ws in main_tree.workspaces():
        for fn in ws.floating_nodes:
            if  fn.focused:
                if  fn.id in scratch_tree.focus:
                    retval = True
                break
        if  retval:
            break
    return retval

def total_scratchpad_count():
    ''' obtenar tota quanto di kladala fenestri '''
    return len(Connection().get_tree().scratchpad().focus)

def get_scratched_windows():
    ''' obtenar tota listo di kladala fenestri '''
    sw_list = []
    tree = Connection().get_tree()
    scratchpad = tree.scratchpad()
    for e in scratchpad.floating_nodes:
        sw_list.append({"wincon": e, "wsname": SPREFIX, "conname": e.name})
    return sw_list

def in_scratch_count():
    ''' quanta kladala fenestri esas celita (opoze di vidata) '''
    return len(get_scratched_windows())

def get_opened_scratched_windows():
    ''' Get all opened scratched windows. '''
    osw_list = []
    tree = Connection().get_tree()
    scratchpad = tree.scratchpad()
    scr_wids = scratchpad.focus
    wsname = ''
    workspaces = tree.workspaces()
    for ws in workspaces:
        wsname = ws.name
        if  wsname == '__i3_scratch':
            continue
        if  len(ws.floating_nodes) > 0:
            for fn in ws.floating_nodes:
                if  fn.id in scr_wids:
                    osw_list.append({"wincon": fn, "wsname": wsname, "conname": fn.name})
    return osw_list

def get_all_scratchpad_windows():
    '''
    listo di omna "scratchpad"-fenestri
    kam celita tam vidata
    '''
    pad = len(SPREFIX)
    scratchedw = add_handler( add_wrks_to_winname( 
        get_scratched_windows(), default_pad_len=pad), 
        show_scratchpad_window )
    openedscrw = add_handler( add_wrks_to_winname( 
        get_opened_scratched_windows(), default_pad_len=pad), focus )
    scratchedw.extend(openedscrw)
    return scratchedw

def add_wrks_to_winname(scrw, default_pad_len=0):
    if  len(scrw) > 0:
        aswn = [len(we.get('wsname', '').encode('utf-8')) for we in scrw]
    else:
        aswn = []
    aswn.append(default_pad_len)
    pad = max(aswn)
    norm_windows = []
    for we in scrw:
        conname = we.get('conname', '')
        wsname = we.get('wsname', '')
        we['conname'] = '{0:>{pad}}  {1}'.format( wsname, conname, pad=pad )
        norm_windows.append(we)
    return norm_windows

def add_handler(diclist, handler):
    for de in diclist:
        de['handler'] = handler
    return diclist

def create_lookup_table(windows):
    '''
    Create a lookup table from the given list of windows.
    The returned dict is in the format window title → window dict.
    '''
    rename_nonunique(windows)
    lookup = OrderedDict()
    for window in windows:
        name = window.get('conname')
        lookup[name] = window
    return OrderedDict(sorted(lookup.items(), key=lambda i: i[0]))

def rename_nonunique(windows):
    '''Rename all windows which share a name by appending an index.'''
    window_names = [ "{} : {}".format(window.get('conname', '?'), render_title(window)) for window in windows]
    for name in window_names:
        count = window_names.count(name)
        if  count > 1:
            for i in range(count):
                index = window_names.index(name)
                window_names[index] = "{}[{}]".format(name, i + 1)
    for i in range(len(windows)):
        windows[i]['conname'] = window_names[i]

def render_title(window):
    '''Render title of window'''
    ft_str = window.get('title_format', '')
    if  ft_str != '':
        wprops = window.get('window_properties', {})
        ft_str = ft_str.replace('%title', wprops.get('title', ''))
        ft_str = ft_str.replace('%class', wprops.get('class', ''))
        ft_str = ft_str.replace('%instance', wprops.get('instance', ''))
    mrk = window.get("wincon").marks
    if  len(mrk) > 0:
        if  ft_str != '':
            ft_str += ' : '
        ft_str += 'mark="' + mrk[0] + '"'
    return ft_str

def show_scratchpad_window(window):
    '''Does `scratchpad show` on the specified window.'''
    return window.command("scratchpad show")

def focus(window):
    '''Focuses the given window.'''
    return window.command("focus")

def select_from_sw(lookup):
    #
    # target = dmenu(lookup.keys(), 'rofi -dmenu -p "Select scratchpad:" -font "Iosevka Mea Medium 18"')
    target = dmenu(lookup.keys(), 'rofi -dmenu -p "Select scratchpad:"')
    tgt_dic = lookup.get(target, {})
    func_ = tgt_dic.get('handler', lambda x: x)
    success = func_(tgt_dic.get("wincon"))
    return (0 if success else 1)

def select_from_hidden_sw():
    #
    pad = len(SPREFIX)
    return select_from_sw( create_lookup_table( add_handler( add_wrks_to_winname( 
        get_scratched_windows(), default_pad_len=pad), show_scratchpad_window ) ))

def select_from_all_sw():
    #
    return select_from_sw( create_lookup_table( get_all_scratchpad_windows() ))

def select_from_opened_sw():
    #
    return select_from_sw( create_lookup_table( add_handler( add_wrks_to_winname( 
        get_opened_scratched_windows(), default_pad_len=0 ), focus ) ))


if  __name__ == "__main__":
    from pprint import pformat
    tree = Connection().get_tree()
    scratch_con = tree.scratchpad()
    count = len(scratch_con.focus)
    print("Count of scratchpad containers", count)
    # pprint.pprint( tree)
    print("Tota arboro:\n", pformat(tree, compact=True))

    # focused = [tree.find_focused()]
    # print("Focus on:\n", pformat(focused))
    # print("Scratch-containers id:", scratch_con.get("focus"))

