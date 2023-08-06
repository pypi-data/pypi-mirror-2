#!/bin/bash

# make_krzlistings.sh - Generate a separate listing in text format for each
#      KRZ/K25/K26 file under the directory given on the command line.
#      Each listing will be created  in the same directory as the input file,
#      taking care not to overwrite existing files.
#
#      If you run this script with the '-f' option it will only print which
#      file would be generated, but not actually create them.

if [ "x$1" = "x-f" ]; then
    DOIT=true
    shift
fi

ROOTDIR="$1"

if [ -z "$ROOTDIR" ]; then
    echo "Usage: make_krzlistings.sh <root directory>" >&2
fi

find "$ROOTDIR" -iregex '.*\.\(krz\|k25\|k26\)$' | \
while read fn; do
    # Do not strip off the extension to distinguish between
    # .KRZ, .K25 and .K26 files with the same basename!
    base="${fn##*/}"
    path="${fn%/*}"

    if [ ! -e "$path/$base.txt" ]; then
        echo "Generating listing '$path/base.txt'..."
        if [ "x$DOIT" = "xtrue" ]; then
            k2list -o "$path/$base.txt" "$fn"
        fi
    else
        echo "Output file '$path/$base.txt' exists." >&2
    fi
done
