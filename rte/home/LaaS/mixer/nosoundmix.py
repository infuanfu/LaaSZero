#!/usr/bin/env python3

import sys
import select
import time

playing = [False, False, False, ]


def mix_playing(x):
    return playing[x]


def mix_fade_out_channel(x, t):
    playing[x] = False
    return x


def mix_fade_in_channel(x, wav, y, t):
    playing[x] = True
    return x


def play(chid, ch_wav, do_play):
    if mix_playing(chid) and not do_play:
        print("fadeout " + str(mix_fade_out_channel(chid, 2000)))
    elif not mix_playing(chid) and do_play:
        print("fadein " + str(mix_fade_in_channel(chid, ch_wav[chid], -1, 2000)))


def main():
    """entry point"""
    track_wav = [0, 1, 2, 3]
    track_counter = [0, 0, 0, 0]

    last_time = int(time.time())
    while True:
        now_time = int(time.time())

        if select.select([sys.stdin, ], [], [], 0.0)[0]:
            c = sys.stdin.read(1)
            if c == 'q':
                break
            elif '0' <= c <= '3':
                print("refresh " + c)
                track_counter[int(c)] = 5

        if now_time > last_time:
            print("Tick")
            last_time = now_time

            track_counter = map(lambda count: max(0, count - 1), track_counter)

            for i, x in enumerate(track_counter):
                play(i, track_wav, x > 0)

    return 0


if __name__ == '__main__':
    main()
