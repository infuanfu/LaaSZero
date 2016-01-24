# Raspberry Pi in QEMU
## Prerequisites
### Install QEMU ARM system
    sudo dnf install qemu-system-arm

### Download Raspian
Download latest Raspbian image from [raspberrypi.org/downloads/raspbian/](https://www.raspberrypi.org/downloads/raspbian/).

### Download QEMU kernel
Get the kernel suitable for your image at [github.com/dhruvvyas90/qemu-rpi-kernel](https://github.com/dhruvvyas90/qemu-rpi-kernel)

### Prepare image
The entry in `/etc/ld.so.preload` needs to be commented out. There's a script for that

    sudo ./prepareimage.sh 2015-11-21-raspbian-jessie.img

### Fix partitions
First time you boot the image up, you might end up in a root console. You can scroll through systemd's log to find out what went wrong using

    journalctl -xb
    umount /dev/sdb2
    fdisk /dev/sdb2
    shutdown -r now


## Start Raspian in QEMU

    ./startqemu.sh kernel-qemu-4.1.7-jessie 2015-11-21-raspbian-jessie.img

