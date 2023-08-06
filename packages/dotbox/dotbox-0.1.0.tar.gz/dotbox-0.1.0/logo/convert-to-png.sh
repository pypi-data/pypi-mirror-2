#!/bin/sh
base="dotbox-logo"
source="$base".svg
size="$1"

if [ ! "$size" ]; then
    echo "usage: $0 WIDTH (example: $0 320 returns a png of 320x160 pixels)"
else
    newpng="$base-$1.png"
    echo "Converting $source to $newpng..."
    inkscape "--export-png=$newpng" "--export-width=$size" "$source"
fi
