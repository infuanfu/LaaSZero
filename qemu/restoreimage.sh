#!/bin/sh
#
# restores changes applied by prepareimage.sh
#

if [[ $EUID -ne 0 ]]; then
    echo "must be run as root"
    exit 1
fi

if [[ -z $1 ]]; then
    echo "must provide image file as param"
    exit 1
fi

echo "enable etc/ld.so.preload and unbend /etc/fstab in image"

IMG=$1
MOUNTOFFSET=$(file "$IMG"|sed 's/;/\n/g'|grep "partition 2"|sed 's/, /\n/g'|grep startsector|awk '{print $2 " * 512"}'|bc)

MOUNT=$(mktemp -d)
mount $(pwd)"/$IMG" -o offset=$MOUNTOFFSET $MOUNT
echo $(cat $MOUNT/etc/ld.so.preload | awk -F# '{print $1$2}') >$MOUNT/etc/ld.so.preload
echo $(cat $MOUNT/etc/fstab | sed 's/sda/mmcblk0p/g') >$MOUNT/etc/fstab

echo "set /etc/ld.so.preload to:"
cat $MOUNT/etc/ld.so.preload

echo "set /etc/fstab to:"
cat $MOUNT/etc/fstab

umount $MOUNT
rmdir $MOUNT
