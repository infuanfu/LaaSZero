#!/bin/sh
if [[ $EUID -ne 0 ]]; then
    echo "must be run as root"
    exit 1
fi

if [[ -z $1 ]]; then
    echo "must provide image file as param"
    exit 1
fi

echo "disabling etc/ld.so.preload in image"

IMG=$1
MOUNTOFFSET=$(file "$IMG"|sed 's/;/\n/g'|grep "partition 2"|sed 's/, /\n/g'|grep startsector|awk '{print $2 " * 512"}'|bc)

MOUNT=$(mktemp -d)
mount $(pwd)"/$IMG" -o offset=$MOUNTOFFSET $MOUNT
COMMENTED=$(cat $MOUNT/etc/ld.so.preload | awk -F# '{print "#" $1$2}')
echo "$COMMENTED" >$MOUNT/etc/ld.so.preload
cat $MOUNT/etc/ld.so.preload
umount $MOUNT
rmdir $MOUNT
