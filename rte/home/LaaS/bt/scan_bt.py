#!/usr/bin/env python
import time
import serial
from operator import itemgetter
import sys

ser = serial.Serial(
    port='/dev/ttyAMA0',
    baudrate=38400,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
)

#ser.open()
ser.isOpen()


devmap = {
"11:5:180086": 1,
"11:5:180124": 2,
"11:3:140071": 3,
"11:3:140118": 4,
}


def readser():
    bt_repls = []
    bt_repl = ""
    while True:
        bt_repl += ser.read()
        if bt_repl[-1] == '\n':
            bt_repls.append(bt_repl)
            if bt_repl.startswith("OK") or bt_repl.startswith("ERROR"):
                break;
            bt_repl = ""
    return (bt_repls, bt_repl.startswith("OK"))

def execcmd(cmd):
    ser.write(cmd+"\r\n")
    return readser()

if __name__ == "__main__":
    bt_init = [
    "AT",
    "AT+INIT",          # initilize bt stack
    "AT+ROLE=1",        # set master
    "AT+INQM=1,20,3",   # inquiry mode RSSI, list 20 devices, timeout after 3*1.25 sec
    ]

    for cmd in bt_init:
        (repls,status) = execcmd(cmd)
        #print status

    while True:
        (repls,status) = execcmd("AT+INQ")
        #print status

        devs = {}
        for line in repls:
            #print line[:-2]
            if line.startswith("+INQ:"):
                (addr,dclass,rssi) = line[5:-2].split(',')
		devs[addr] = int(rssi, 16) - 2**16
        
	raw = ["%s/%s" % (x[0],x[1]) for x in sorted(devs.items(),key=itemgetter(1))]
	seen = ["%s/%s" % (devmap[x[0]],x[1]) for x in sorted(devs.items(),key=itemgetter(1)) if x[0] in devmap]
	print "map "+(" ".join(seen))
	print "raw "+(" ".join(raw))
	sys.stdout.flush()
