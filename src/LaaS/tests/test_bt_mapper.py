import pytest


class TestBluetoothMapping:

    @pytest.mark.parametrize('map_input,bt_id,expected', [
        ({'bt_1': 'track_a'}, 'bt_1', 'track_a'),
        ({'bt_1': 'track_a'}, 'bt_2', None),
        (None, 'something', None),
    ])
    def test_maptool_resolves_to_expected_value(self, map_input, bt_id, expected):
        """
        `maptool` should not raise an Exception, ever.
        """
        from bt import BluetoothToTrackMapper
        assert BluetoothToTrackMapper(config=map_input).resolve(bt_id) == expected
