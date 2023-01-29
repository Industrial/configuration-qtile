import os
import subprocess

from libqtile import bar, extension, hook, layout, widget
from libqtile.config import Click, Drag, Group, Match, Screen, EzKey
from libqtile.lazy import lazy
from libqtile.log_utils import logger
from libqtile.utils import guess_terminal

mod = "mod4"
terminal = guess_terminal()


def move_window_to_screen(qtile, window, screen):
    window.togroup(screen.group.name)
    qtile.focus_screen(screen.index)
    screen.group.focus(window, True)


@lazy.function
def move_window_to_prev_screen(qtile):
    index = qtile.current_screen.index
    index = index - 1 if index > 0 else len(qtile.screens) - 1
    move_window_to_screen(qtile, qtile.current_window, qtile.screens[index])


@lazy.function
def move_window_to_next_screen(qtile):
    index = qtile.current_screen.index
    index = index + 1 if index < len(qtile.screens) - 1 else 0
    move_window_to_screen(qtile, qtile.current_window, qtile.screens[index])


keys = [
    EzKey("M-C-t", lazy.spawn(terminal), desc="Launch terminal"),
    EzKey(
        "M-C-p",
        lazy.run_extension(
            extension.DmenuRun(
                dmenu_bottom=True,
                dmenu_ignorecase=True,
                dmenu_prompt=">",
                font="sans",
                fontsize=10,
                foreground="#FFFFFF",
                background="#000000",
                selected_background="#4488AA",
                selected_foreground="#FFFFFF",
            )
        ),
        desc="Spawn Command",
    ),
    EzKey("M-C-q", lazy.window.kill(), desc="Kill window"),
    EzKey("M-C-S-r", lazy.reload_config(), desc="Reload config"),
    EzKey("M-C-S-q", lazy.shutdown(), desc="Shutdown Qtile"),
    EzKey("M-C-S-z", lazy.spawn("slock"), desc="Lock Screen"),
    # Focus Window
    EzKey("M-h", lazy.layout.left(), desc="Focus Window Left"),
    EzKey("M-j", lazy.layout.down(), desc="Focus Window Down"),
    EzKey("M-k", lazy.layout.up(), desc="Focus Window Up"),
    EzKey("M-l", lazy.layout.right(), desc="Focus Window Right"),
    # Move Window
    EzKey("M-C-h", lazy.layout.shuffle_left(), desc="Move Window Left"),
    EzKey("M-C-j", lazy.layout.shuffle_down(), desc="Move Window Down"),
    EzKey("M-C-k", lazy.layout.shuffle_up(), desc="Move Window Up"),
    EzKey("M-C-l", lazy.layout.shuffle_right(), desc="Move Window Right"),
    # Focus Screen
    EzKey("M-S-h", lazy.next_screen(), desc="Focus Screen Left"),
    EzKey("M-S-l", lazy.prev_screen(), desc="Focus Screen Right"),
    # Move Screen
    EzKey("M-C-S-h", move_window_to_next_screen(), desc="Move Screen Left"),
    EzKey("M-C-S-l", move_window_to_prev_screen(), desc="Move Screen Right"),
    # Grow Window
    EzKey("M-C-A-S-h", lazy.layout.grow_left(), desc="Grow Window Left"),
    EzKey("M-C-A-S-j", lazy.layout.grow_down(), desc="Grow Window Down"),
    EzKey("M-C-A-S-k", lazy.layout.grow_up(), desc="Grow Window Up"),
    EzKey("M-C-A-S-l", lazy.layout.grow_right(), desc="Grow Window Right"),
    EzKey("M-C-A-S-n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Layout
    EzKey("M-<space>", lazy.next_layout(), desc="Next Layout"),
    EzKey(
        "M-S-<space>",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
]

groups = [Group(i) for i in "123456789"]

for i in groups:
    keys.extend(
        [
            EzKey(
                f"M-{i.name}",
                lazy.group[i.name].toscreen(),
                desc=f"Switch to group {i.name}",
            ),
            EzKey(
                f"M-C-{i.name}",
                lazy.window.togroup(i.name, switch_group=True),
                desc=f"Switch to group {i.name}",
            ),
        ]
    )

layouts = [
    layout.Columns(border_focus_stack=["#4488AA", "#336699"], border_width=3),
    layout.Matrix(),
    layout.MonadTall(),
    layout.MonadWide(),
    layout.Max(),
]

widget_defaults = dict(
    font="sans",
    fontsize=12,
    padding=3,
)
extension_defaults = widget_defaults.copy()

bar_background_color = "#222222"

def widget_group_box():
    return widget.GroupBox(
        hide_unused=True,
        highlight_method="border",

        # Active Text Color
        active="FFFFFF",

        # Inactive Text Color
        inactive="FFFFFF",

        # foreground="FF0000",

        # Other Screen Border
        other_screen_border="666666",
        this_screen_border="CCCCCC",

        other_current_screen_border="336699",
        this_current_screen_border="99CCFF",

        urgent_alert_method="border",
        urgent_border="FF0000",
        urgent_text="FF0000",
    )

# TODO: Set the order / name / id correctly from left to right
screens = [
    Screen(
        bottom=bar.Bar(
            [
                widget_group_box(),
                widget.CurrentLayoutIcon(),
                widget.TaskList(),
            ],
            32,
            background=bar_background_color,
        ),
    ),
    Screen(
        bottom=bar.Bar(
            [
                widget_group_box(),
                widget.CurrentLayoutIcon(),
                widget.TaskList(),
            ],
            32,
            background=bar_background_color,
        ),
    ),
    Screen(
        bottom=bar.Bar(
            [
                widget_group_box(),
                widget.CurrentLayoutIcon(),
                widget.Prompt(),
                widget.TaskList(),
                widget.Chord(
                    chords_colors={
                        "launch": ("#ff0000", "#ffffff"),
                    },
                    name_transform=lambda name: name.upper(),
                ),
                widget.ThermalZone(),
                widget.CryptoTicker(),
                widget.Systray(),
                widget.DF(),
                # widget.HDDBusyGraph(),
                widget.NetGraph(),
                # widget.Net(),
                widget.MemoryGraph(),
                # widget.Memory(),
                widget.CPUGraph(),
                # widget.CPU(),
                # widget.BatteryIcon(),
                # widget.Battery(),
                widget.Clock(format="%Y-%m-%d %a %H:%M:%S"),
                # widget.QuickExit(),
            ],
            32,
            background=bar_background_color,
        ),
    ),
    Screen(
        bottom=bar.Bar(
            [
                widget_group_box(),
                widget.CurrentLayoutIcon(),
                widget.TaskList(),
            ],
            32,
            background=bar_background_color,
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag(
        [mod],
        "Button1",
        lazy.window.set_position_floating(),
        start=lazy.window.get_position(),
    ),
    Drag(
        [mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()
    ),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.run([home])

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
