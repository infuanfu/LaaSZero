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


IMG=$1
MOUNTOFFSET=$(file "$IMG"|sed 's/;/\n/g'|grep "partition 2"|sed 's/, /\n/g'|grep startsector|awk '{print $2 " * 512"}'|bc)

echo "mount offset is $MOUNTOFFSET"

MOUNT=$(mktemp -d)
echo "mounting to $MOUNT"
mount $(pwd)"/$IMG" -o offset=$MOUNTOFFSET $MOUNT

echo "restoring entry in /etc/ld.so.preload"
UNCOMMENTED=$(cat $MOUNT/etc/ld.so.preload | awk -F# '{print $1$2}')
echo "$UNCOMMENTED" >$MOUNT/etc/ld.so.preload

echo "restoring original mapping in /etc/fstab and enabling /boot"
MMCMAPPED=$(cat $MOUNT/etc/fstab | sed 's|#/dev/sda1|/dev/sda1|' | sed 's/sda/mmcblk0p/g')
echo "$MMCMAPPED" >$MOUNT/etc/fstab

echo "cleaning up /lib/modules"
find $MOUNT/lib/modules -type l -exec rm {} ";"

echo "done."

echo "set /etc/ld.so.preload to:"
cat $MOUNT/etc/ld.so.preload

echo "set /etc/fstab to:"
cat $MOUNT/etc/fstab

umount $MOUNT
rmdir $MOUNT
