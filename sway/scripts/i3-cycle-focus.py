#!/usr/bin/env python3
#
# provides alt+tab functionality between windows, switching
# between n windows; example i3 conf to use:
#     exec_always --no-startup-id i3-cycle-focus.py --history 2
#     bindsym $mod1+Tab exec --no-startup-id i3-cycle-focus.py --switch

from os import _exit, remove
from os.path import exists as is_exist
from socket \
    import ( socket
           , AF_UNIX
           , SOCK_STREAM )
from selectors import DefaultSelector, EVENT_READ
from threading \
    import ( RLock
           , Timer
           , Thread )
from argparse import ArgumentParser
from i3ipc import Connection

SOCKET_FILE = '/tmp/.i3-cycle-focus.sock'
MAX_WIN_HISTORY = 16
UPDATE_DELAY = 2.0


def on_shutdown(i3_conn, e):
    _exit(0)

class FocusWatcher:
    def __init__(self):
        self.i3 = Connection()
        self.i3.on('window::focus', self.on_window_focus)
        self.i3.on('shutdown', on_shutdown)
        self.listening_socket = socket(AF_UNIX, SOCK_STREAM)
        if is_exist(SOCKET_FILE):
            remove(SOCKET_FILE)
        self.listening_socket.bind(SOCKET_FILE)
        self.listening_socket.listen(1)
        self.window_list = []
        self.window_list_lock = RLock()
        self.focus_timer = None
        self.window_index = 1

    def update_windowlist(self, window_id):
        with self.window_list_lock:
            if window_id in self.window_list:
                self.window_list.remove(window_id)
            self.window_list.insert(0, window_id)
            if len(self.window_list) > MAX_WIN_HISTORY:
                del self.window_list[MAX_WIN_HISTORY:]
            self.window_index = 1

    def get_valid_windows(self):
        tree = self.i3.get_tree()
        if args.active_workspace:
            return set(w.id for w in tree.find_focused().workspace().leaves())
        elif args.visible_workspaces:
            ws_list = []
            w_set = set()
            for item in self.i3.get_outputs():
                ws_list.append(item.current_workspace)
            for ws in tree.workspaces():
                if str(ws.num) in ws_list:
                    for w in ws.leaves():
                        w_set.add(w.id)
            return w_set
        else:
            return set(w.id for w in tree.leaves())

    def on_window_focus(self, i3conn, event):
        if args.ignore_float and (event.container.floating == "user_on"
                                  or event.container.floating == "auto_on"):
            return
        if UPDATE_DELAY != 0.0:
            if self.focus_timer is not None:
                self.focus_timer.cancel()
            self.focus_timer = Timer(UPDATE_DELAY, self.update_windowlist,
                                               [event.container.id])
            self.focus_timer.start()
        else:
            self.update_windowlist(event.container.id)

    def launch_i3(self):
        self.i3.main()

    def launch_server(self):
        selector = DefaultSelector()

        def accept(sock):
            conn, addr = sock.accept()
            selector.register(conn, EVENT_READ, read)

        def read(conn):
            data = conn.recv(1024)
            if data == b'switch':
                with self.window_list_lock:
                    windows = self.get_valid_windows()
                    for window_id in self.window_list[self.window_index:]:
                        if window_id not in windows:
                            self.window_list.remove(window_id)
                        else:
                            if self.window_index < (len(self.window_list) - 1):
                                self.window_index += 1
                            else:
                                self.window_index = 0
                            self.i3.command('[con_id=%s] focus' % window_id)
                            break
            elif not data:
                selector.unregister(conn)
                conn.close()

        selector.register(self.listening_socket, EVENT_READ, accept)

        while True:
            for key, event in selector.select():
                callback = key.data
                callback(key.fileobj)

    def run(self):
        t_i3 = Thread(target=self.launch_i3)
        t_server = Thread(target=self.launch_server)
        for t in (t_i3, t_server):
            t.start()


if __name__ == '__main__':
    parser = ArgumentParser(prog='i3-cycle-focus.py',
                            description="""
        Cycle backwards through the history of focused windows (aka Alt-Tab).
        This script should be launched from ~/.xsession or ~/.xinitrc.
        Use the `--history` option to set the maximum number of windows to be
        stored in the focus history (Default 16 windows).
        Use the `--delay` option to set the delay between focusing the
        selected window and updating the focus history (Default 2.0 seconds).
        Use a value of 0.0 seconds to toggle focus only between the current
        and the previously focused window. Use the `--ignore-floating` option
        to exclude all floating windows when cycling and updating the focus
        history. Use the `--visible-workspaces` option to include windows on
        visible workspaces only when cycling the focus history. Use the
        `--active-workspace` option to include windows on the active workspace
        only when cycling the focus history.

        To trigger focus switching, execute the script from a keybinding with
        the `--switch` option.""")
    parser.add_argument('--history',
                        dest='history',
                        help='Maximum number of windows in the focus history',
                        type=int)
    parser.add_argument('--delay',
                        dest='delay',
                        help='Delay before updating focus history',
                        type=float)
    parser.add_argument('--ignore-floating',
                        dest='ignore_float',
                        action='store_true',
                        help='Ignore floating windows '
                        'when cycling and updating the focus history')
    parser.add_argument('--visible-workspaces',
                        dest='visible_workspaces',
                        action='store_true',
                        help='Include windows on visible '
                        'workspaces only when cycling the focus history')
    parser.add_argument('--active-workspace',
                        dest='active_workspace',
                        action='store_true',
                        help='Include windows on the '
                        'active workspace only when cycling the focus history')
    parser.add_argument('--switch',
                        dest='switch',
                        action='store_true',
                        help='Switch to the previous window',
                        default=False)
    args = parser.parse_args()

    if args.history:
        MAX_WIN_HISTORY = args.history
    if args.delay:
        UPDATE_DELAY = args.delay
    else:
        if args.delay == 0.0:
            UPDATE_DELAY = args.delay
    if not args.switch:
        focus_watcher = FocusWatcher()
        focus_watcher.run()
    else:
        client_socket = socket(AF_UNIX, SOCK_STREAM)
        client_socket.connect(SOCKET_FILE)
        client_socket.send(b'switch')
        client_socket.close()
