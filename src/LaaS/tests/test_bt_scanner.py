import pytest


@pytest.mark.parametrize('expected_id', [
    'bt_1',
])
def test_btid_extractor_finds_all_ids(mocked_spectrum_scan, expected_id):
    from bt.extracting import extract_ids

    bt_ids = extract_ids(mocked_spectrum_scan)
    assert expected_id in bt_ids


@pytest.mark.parametrize('line, addr_rssi', [
    ('+INQ:11:5:180086,0,FFBF', ('11:5:180086', 'FFBF')),
    ('+INQ:11:6:180086,0,FFC4', ('11:6:180086', 'FFC4')),
    ('+INQ:11:7:180088,0,FFB0', ('11:7:180088', 'FFB0')),
    ('+INQ:13:5:130086,0,FFB8', ('13:5:130086', 'FFB8')),
    ('+INQ:12:5:140086,0,FFC5', ('12:5:140086', 'FFC5')),
])
def test_bt_device_parser(line, addr_rssi):
    from bt.scanner import BtDevice

    # noinspection PyProtectedMember
    result = BtDevice._parse(None, line)

    assert result == addr_rssi
