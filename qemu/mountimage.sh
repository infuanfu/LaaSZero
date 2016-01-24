#!/bin/sh
# simply mount an image to "mnt/" in the local folder
#
if [[ $EUID -ne 0 ]]; then
    echo "must be run as root"
    exit 1
fi

if [[ -z $1 ]]; then
    echo "must provide image file as param"
    exit 1
fi

IMG=$1
MOUNTOFFSET=$(file "$IMG"|sed 's/;/\n/g'|grep "partition 2"|sed 's/, /\n/g'|grep startsector|awk '{print $2 " * 512"}'|bc)

MOUNT=mnt
mkdir mnt
mount $(pwd)"/$IMG" -o offset=$MOUNTOFFSET $MOUNT
