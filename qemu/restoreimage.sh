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
UNCOMMENTED=$(cat $MOUNT/etc/ld.so.preload | awk -F# '{print $1$2}')
echo "$UNCOMMENTED" >$MOUNT/etc/ld.so.preload
MMCMAPPED=$(cat $MOUNT/etc/fstab | sed 's|#/dev/sda1|/dev/sda1|' | sed 's/sda/mmcblk0p/g')
echo "$MMCMAPPED" >$MOUNT/etc/fstab

echo "set /etc/ld.so.preload to:"
cat $MOUNT/etc/ld.so.preload

echo "set /etc/fstab to:"
cat $MOUNT/etc/fstab

umount $MOUNT
rmdir $MOUNT
