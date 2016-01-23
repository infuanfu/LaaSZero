#!/usr/bin/env python3

import os
import select
import sys
import time

from sdl2 import *
from sdl2.sdlmixer import *


def play(chid, wav, do_play):
    if Mix_Playing(chid) and not do_play:
        print("fadeout " + str(Mix_FadeOutChannel(chid, 2000)))
    elif not Mix_Playing(chid) and do_play:
        print("fadein " + str(Mix_FadeInChannel(chid, wav, -1, 2000)))
    print("error: " + SDL_GetError())


def main():
    """entry point"""
    SDL_Init(SDL_INIT_AUDIO)

    for i in range(Mix_GetNumMusicDecoders()):
        print("decoder {}: {}".format(i, Mix_GetMusicDecoder(i)))

    print("mixinit " + str(Mix_Init(MIX_INIT_MP3)))
    print("openaudio " + str(Mix_OpenAudio(44100, MIX_DEFAULT_FORMAT, 2, 1024)))
    Mix_VolumeMusic(MIX_MAX_VOLUME)
    Mix_AllocateChannels(4)

    path = os.path.dirname(os.path.realpath(__file__))

    print("path: {}".format(path))

    default_wav = Mix_LoadWAV('{}/data/noise.wav'.format(path))
    track_wav = [Mix_LoadWAV('{}/data/track1.wav'.format(path)),
                 Mix_LoadWAV('{}/data/track2.wav'.format(path)),
                 Mix_LoadWAV('{}/data/track3.wav'.format(path)),
                 ]
    track_counter = [0, 0, 0, 0]

    last_time = int(time.time())
    while True:
        now_time = int(time.time())

        if select.select([sys.stdin, ], [], [], 0.0)[0]:
            c = sys.stdin.read(1)
            if c == 'q':
                break
            elif '1' <= c <= '3':
                print("refresh " + c)
                track_counter[int(c) - 1] = 5

        if now_time > last_time:
            print("Tick")
            last_time = now_time

            track_counter = map(lambda count: max(0, count - 1), track_counter)

            anything_playing = True
            for i, x in enumerate(track_counter):
                play(i + 1, track_wav[i - 1], x > 0)
                anything_playing = anything_playing or x > 0

            play(0, default_wav, not anything_playing)

    Mix_CloseAudio()
    Mix_FreeChunk(default_wav)
    Mix_FreeChunk(track_wav[1])
    Mix_FreeChunk(track_wav[2])
    Mix_FreeChunk(track_wav[3])
    Mix_Quit()

    # SDL_DestroyWindow(window)
    SDL_Quit()
    return 0


if __name__ == '__main__':
    main()
