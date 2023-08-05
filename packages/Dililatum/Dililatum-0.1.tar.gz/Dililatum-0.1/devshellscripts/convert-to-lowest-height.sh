#!/bin/bash
function get_height {
    ffmpeg -i "$1" 2>&1 | grep Stream | cut -d' ' -f10 \
        | cut -d'x' -f2 | cut -d',' -f1
}

function get_smallest_height {
echo $(for x in $pngs; do get_height $x; done) \
    | tr ' ' '\n' | sort -n | head -n 1
}

function convert_heights {
    for x in $pngs; do
        mogrify -resize x$height $x
    done
}

pngs=$(find -name '*.png')
height=$(get_smallest_height)
echo "These files will be used:"
echo $pngs
echo
echo "Smallest height is $height pixels."

convert_heights
echo "All files have been converted."