class BluetoothToTrackMapper:
    def __init__(self, config=None):
        if not config:
            config = {}

        self.map = dict(config)

    def resolve(self, bt_id):
        return self.map.get(bt_id, None)
