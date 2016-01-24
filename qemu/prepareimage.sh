#!/bin/sh
#
# prepares raspbian image for use with qemu
#
# tested with raspbian jessie
#

if [[ $EUID -ne 0 ]]; then
    echo "must be run as root"
    exit 1
fi

if [[ -z $2 ]]; then
    echo "Usage: $0 <image file> <kernel version>"
    exit 1
fi

IMG=$1
MOUNTOFFSET=$(file "$IMG"|sed 's/;/\n/g'|grep "partition 2"|sed 's/, /\n/g'|grep startsector|awk '{print $2 " * 512"}'|bc)

echo "mount offset is $MOUNTOFFSET"

MOUNT=$(mktemp -d)
echo "mounting to $MOUNT"
mount $(pwd)"/$IMG" -o offset=$MOUNTOFFSET $MOUNT

echo "commenting out entry in /etc/ld.so.preload"
COMMENTED=$(cat $MOUNT/etc/ld.so.preload | awk -F# '{print "#" $1$2}')
echo "$COMMENTED" >$MOUNT/etc/ld.so.preload

echo "remapping /etc/fstab and disabling /boot"
SDAMAPPED=$(cat $MOUNT/etc/fstab | sed 's/mmcblk0p/sda/g' | sed 's|.*/dev/sda1|#/dev/sda1|')
echo "$SDAMAPPED" >$MOUNT/etc/fstab

echo "cleaning up /lib/modules"
# cleanup links
find $MOUNT/lib/modules -type l -exec rm {} ";"

echo "adding symlink for kernel modules $2 in /etc/modules"
# set new link
ln -s $(ls $MOUNT/lib/modules|head -n1) "$MOUNT/lib/modules/$2+"

echo "done."

echo -e "\nset /etc/ld.so.preload to:"
cat $MOUNT/etc/ld.so.preload

echo -e "\nset /etc/fstab to:"
cat $MOUNT/etc/fstab

echo -e "\nset symlink for kernel modules"
find $MOUNT/lib/modules -type l -exec ls -l {} ";"

umount $MOUNT
rmdir $MOUNT
