# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import re
import socket
import subprocess
from libqtile import hook
from libqtile import qtile
from typing import List  
from libqtile import bar, layout, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen, ScratchPad, DropDown
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from libqtile.widget import Spacer, Backlight
from libqtile.widget.image import Image
from libqtile.dgroups import simple_key_binder
from libqtile.bar import Bar
from libqtile.config import Screen
from libqtile.widget import Spacer

from powerline.bindings.qtile.widget import PowerlineTextBox

import colors

#My programmes
mod = "mod4"
myBrowser = 'brave'
myTerminal = 'alacritty'
myTextEditor = 'geany'
myVideoPlayer = 'vlc'
myCmdRun      = 'rofi -show run'

keys = [

    # Switch between windows
    Key([mod], "h", lazy.layout.left(),  desc = "Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc = "Move focus to right"),
    Key([mod], "j", lazy.layout.down(),  desc = "Move focus down"),
    Key([mod], "k", lazy.layout.up(),    desc = "Move focus up"),
    Key([mod], "space", lazy.window.toggle_fullscreen(), desc = "Full screen focused window"),

    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "control"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "control"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "control"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "control"], "k", lazy.layout.shuffle_up(), desc="Move window up"),

    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "shift"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "shift"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "shift"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "shift"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([mod, "shift"], "Return", lazy.layout.toggle_split(),
        desc = "Toggle between split and unsplit sides of stack"),
    Key([mod], "Return", lazy.spawn(myTerminal), desc = "Launch terminal"),

    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc = "Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),

    Key([mod, "control"], "r", lazy.restart(), desc = "Restart Qtile"),
    Key([mod, "control"], "q", lazy.shutdown(), desc = "Shutdown Qtile"),
    Key([mod], "r", lazy.spawn(myCmdRun), desc = "Spawn a command using a prompt widget"),

    #Browser
    Key([mod], "b", lazy.spawn(myBrowser), desc = "Launch browser"),

    #Geany
    Key([mod], "t", lazy.spawn(myTextEditor), desc = "Launch geany"),

    #Sound
    Key([], "XF86AudioRaiseVolume", lazy.spawn("pactl set-sink-volume 0 +5%")),
    Key([], "XF86AudioLowerVolume", lazy.spawn("pactl set-sink-volume 0 -5%")),
    Key([], "XF86AudioMute", lazy.spawn("pactl set-sink-mute 0 toggle")),

    #Brightness
    Key([], "XF86MonBrightnessUp", lazy.spawn("lux -a 10%")),
    Key([], "XF86MonBrightnessDown", lazy.spawn("lux -s 10%")),
]

groups = [Group("", layout='bsp'),
          Group("", layout='bsp'),
          Group("", layout='bsp'),
          Group("", layout='bsp')]

dgroups_key_binder = simple_key_binder(mod)

colors, backgroundColor, foregroundColor, workspaceColor, foregroundColorTwo = colors.doomOne() 

layouts = [
    layout.Bsp(border_focus = colors[4], margin = 2),
    layout.TreeTab(border_focus = colors[4], margin = 2)
]

widget_defaults = dict(
    font = 'Ubuntu Bold',
    fontsize = 16,
    padding = 2,
    background = colors[0]
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top = bar.Bar(
            [
                widget.Image(
                    filename = '~/.config/qtile/archLinux_icon.png',
                    scale = 'False',
                    margin_x = 5,
                    mouse_callbacks = {'Button5': lambda: qtile.cmd_spawn(myCmdRun)}
                    ),
                widget.GroupBox(
					margin_x = 5,
					active = colors[2],
                    inactive = colors[1],
                    highlight_color = [backgroundColor, workspaceColor],
                    highlight_method = 'line',
                    ),       
                widget.TextBox(
                    text='\u25e2',
                    padding=0,
                    fontsize=50,
                    background = backgroundColor,
                    foreground = workspaceColor),
                widget.Wlan(
                    interface = "wlan0",
                    format = '     {essid}   {percent:2.0%}',
                    padding = 2,
                    background = workspaceColor,
                    ), 
                widget.TextBox(
                    text='\u25e2',
                    padding=0,
                    fontsize=50,
                    background = workspaceColor,
                    foreground = backgroundColor),
                widget.WindowName(),
                widget.Chord(
                    chords_colors={
                        "launch": ("#ff0000", "#ffffff"),
                    },
                    name_transform=lambda name: name.lower(),
                ),
                widget.TextBox(
                    text='\u25e2',
                    padding=0,
                    fontsize=50,
                    background = backgroundColor,
                    foreground = foregroundColorTwo),
                widget.Volume(
					fmt = '  {}',
					foreground = colors[8],
                    background = foregroundColorTwo,
					padding = 2
					),
                widget.Spacer(
                     background = foregroundColorTwo,
                     length = 10
                    ),
                widget.Battery(
                    charge_char ='',
                    discharge_char = '',
                    format = '  {percent:2.0%} {char}',
                    foreground = colors[6],
                    background = foregroundColorTwo,
                    padding = 2
                    ),
                widget.TextBox(
                    text='\u25e2',
                    padding=0,
                    fontsize=50,
                    background = foregroundColorTwo,
                    foreground = backgroundColor),
                widget.Clock(
                    format='   %b %d %Y |    %I:%M %p',
					foreground = colors[2],
                    background = backgroundColor,
					padding = 2
					),
                widget.Spacer(
                     background = backgroundColor,
                     length = 10
                    )
            ],
            20,
        ),
    ),
]

#dgroups_key_binder = None
dgroups_app_rules = []  # type: List
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

#Programms to start on log in
@hook.subscribe.startup_once
def autostart ():
    home = os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.call([home])

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

##-- String needed for java apps --##
wmname = "LG3D"
