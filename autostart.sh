#!/usr/bin/env bash

if [ -x "$(command -v pasystray)" ]; then
  pasystray &> /dev/null &
fi

if [ -x "$(command -v blueman-applet)" ]; then
  blueman-applet &> /dev/null &
fi

# firefox &> /dev/null &
# alacritty &> /dev/null &
# element-desktop &> /dev/null &
# discord &> /dev/null &
# spotify &> /dev/null
