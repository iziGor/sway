#!/usr/bin/env python3
import i3ipc

i3 = i3ipc.Connection()
last = ''

# Font Awesome 5 Free:style=Solid
# layouts = {"tabbed":"\uf24d", "stacked":"\uf0c9", "splitv":"\uf103", "splith":"\uf101"}
# layouts = { "tabbed":"%{F#61bbf6}\uf24d%{F-}"
          # , "stacked":"%{F#00AA00}\uf5fd%{F-}"
          # , "splitv":"%{F#82B8DF}\uf103%{F-}"
          # , "splith":"%{F#CF4F88}\uf101%{F-}"
          # }

# layouts = { "tabbed":  ("61bbf6", "\uf24d")
          # , "stacked": ("00AA00", "\uf5fd")
          # , "splitv":  ("82B8DF", "\uf103")
          # , "splith":  ("CF4F88", "\uf101")
          # }

layouts = { "tabbed":  ("61bbf6", "\uf24d")
          , "stacked": ("00AA00", "\uf5fd")
          , "splitv":  ("82B8DF", "\u2b9f")
          , "splith":  ("CF4F88", "\u2b9e")
          }

# Material Icons
# layouts = {"tabbed":"\ue8d8", "stacked":"\ue3c7", "splitv":"\ue947", "splith":"\ue949"}


def on_event(self, _):
    global last
    layout = i3.get_tree().find_focused().parent.layout
    if  not layout == last:
        # print("%{{F#{}}}{}%{{F-}}".format(*layouts.get(layout, ("888800", "?"))))
        print("<span color='#{}'>{}</span>".format(*layouts.get(layout, ("888800", "?"))))
    last = layout


# Subscribe to events
i3.on("window::focus", on_event)
i3.on("binding", on_event)

# Start the main loop and wait for events to come in.
i3.main()
