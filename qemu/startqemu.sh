#!/bin/sh

if [[ $EUID -eq 0 ]]; then
    echo "please run this as a regular user, not root"
    exit 1
fi

if [[ -z $2 ]]; then
    echo "Usage: $0 <kernel image> <boot image>"
    exit 1
fi

qemu-system-arm -kernel $1 -cpu arm1176 -m 256 -M versatilepb -serial stdio -append "root=/dev/sda2 panic=1" -hda $2 -redir tcp:5022::22
