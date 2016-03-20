"""
"AT Interface"

Scans the BT spectrum for available BT ids.
"""


from enum import Enum

import serial


class AtException(RuntimeError):
    pass


class BtRole(Enum):
    slave = 0
    master = 1
    slave_loop = 2


class InquiryAccessMode(Enum):
    standard = 0
    rssi = 1


class BtDevice:
    def setup(self):
        try:
            self.at()
        except AtException:
            self.at_init()

        self.at_role()
        self.at_inqm()

    def list_device_ids(self):
        # Todo make this more pythonic; list comprehension or so
        device_ids = []
        for line in self.at_inq():
            if line.startswith('+INQ'):
                device_ids.append(self._convert_rssi(self._parse(line)))

        return device_ids

    def __init__(self, port='/dev/ttyAMA0'):
        self.bt_device = serial.Serial(
            port=port,
            baudrate=38400,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS
        )
        if not self.bt_device.isOpen():
            self.bt_device.open()

    @staticmethod
    def _parse(line):
        import re
        m = re.search(r'^\+INQ:(?P<addr>[^,]+),\d,(?P<rssi>[0-9a-fA-F]{4})', line)
        return m.group('addr', 'rssi')  # m.group('addr'), m.group('rssi')

    @staticmethod
    def _convert_rssi(addr_rssi_tuple):
        # TODO: testme
        return addr_rssi_tuple[0], (int(addr_rssi_tuple[1], 16) - 2 ** 16)

    def _execute_cmd(self, cmd):
        self.bt_device.write(cmd + '\r\n')

        bt_repls = []
        bt_repl = ""
        while True:
            bt_repl += self.bt_device.read()
            if bt_repl[-1] == '\n':
                bt_repls.append(bt_repl)
                if bt_repl.startswith("OK"):
                    break
                if bt_repl.startswith("ERROR"):
                    raise AtException(bt_repl)
                bt_repl = ""

        return bt_repls

    def at(self):
        return self._execute_cmd('AT')

    def at_init(self):
        return self._execute_cmd('AT+INIT')

    def at_role(self, role_type=BtRole.master):
        return self._execute_cmd('AT+ROLE={}'.format(role_type))

    def at_inqm(self, access_mode=InquiryAccessMode.rssi, max_devices=20, time_out=3):
        return self._execute_cmd('AT+INQM={},{},{}'.format(
            access_mode, max_devices, time_out
        ))

    def at_inq(self):
        # TODO: abort wait after a few seconds (TIMEOUT)
        return self._execute_cmd('AT+INQ')
