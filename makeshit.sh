#!/bin/sh
./remap.sh
sleep 2
#echo setting up tty
#./LaaS/bt/setuptty.sh

#echo waiting...
#sleep 10
echo GO
python ./LaaS/bt/scan_bt.py
