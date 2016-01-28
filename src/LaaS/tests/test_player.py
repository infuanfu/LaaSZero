import pytest


class TestPlayer:

    def test_player_reads_trackid_from_filehandle(self, mocker):
        # assert reading from handle (mocked stdin)
        pass

    def test_player_tells_sdl_to_load_complete_audio_folder(self):
        # Mix_LoadWAV gets correct path
        pass

    def test_player_changes_track_on_receiving_new_track_id(self, mocker):
        pass

    def test_player_keeps_playing_on_receiving_same_track_id(self):
        pass

    def test_player_fades_out_on_track_end(self):
        pass

    def test_player_shuts_down_when_filehandle_is_closed(self):
        pass


class TestMapping:
    def test_player_ignores_unmapped_track_ids(self):
        pass

    def test_player_drops_track_id_from_mapping_for_missing_file(self):
        pass
