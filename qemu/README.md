# Raspberry Pi in QEMU
## Prerequisites
### Install QEMU ARM system
    sudo dnf install qemu-system-arm

### Download Raspian
Download latest Raspbian image from [raspberrypi.org/downloads/raspbian/](https://www.raspberrypi.org/downloads/raspbian/).

### Download QEMU kernel
Get the kernel suitable for your image at [github.com/dhruvvyas90/qemu-rpi-kernel](https://github.com/dhruvvyas90/qemu-rpi-kernel)

### Prepare image
Now you need to apply a few changes to the image you downloaded:

 * comment out the entry in `/etc/ld.so.preload`
 * change `/etc/fstab` to point to `/dev/sda*` instead of `/dev/mmcblk0p*`
 * comment out the entry for `/boot` in `/etc/fstab`
 * create a symlink in `/etc/modules` matching the QEMU kernel version you're using

Luckily, there's a script for that:

    sudo ./prepareimage.sh 2015-11-21-raspbian-jessie.img 4.1.7

Note: You can revert the changes the script makes using `restoreimage.sh`

## Start Raspian in QEMU

    ./startqemu.sh kernel-qemu-4.1.7-jessie 2015-11-21-raspbian-jessie.img
