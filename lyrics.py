#Makes a request to lrclib.net to get the LRC file lyrics which we can then use to display the karaoke
from ast import parse

import requests
import re

LRCLIB_URL = 'https://lrclib.net/api/get'


def get_synced_lyrics(track: str, artist: str, album: str, duration_ms: int):

    duration_seconds = int(duration_ms * 0.001)

    params = {
        'track_name': track,
        'artist_name': artist,
        'album_name': album,
        'duration': duration_seconds,
    }
    response = requests.get(LRCLIB_URL, params=params)
    data = response.json()

    lyrics = data.get("syncedLyrics")

    return parse_lrc(lyrics)

def parse_lrc(lyrics):
    parsed_lyrics = []

    lyric_lines = lyrics.splitlines()
    for line in lyric_lines:
        timesplits = re.findall(r'\[(\d{2}):(\d{2})\.(\d{2})\]', line)
        lyric = re.sub(r'\[.*?\]', '', line).strip()
        for i in range(len(timesplits)):
            minute = int(timesplits[i][0])
            second = int(timesplits[i][1])
            millisecond = int(timesplits[i][2])

            time_in_ms = (minute * 60 + second) * 1000 + millisecond * 10
            parsed_lyrics.append((time_in_ms, lyric))

    lyrics_sorted = sorted(parsed_lyrics, key=lambda x: x[0])
    return lyrics_sorted

def get_current_lyric(progress, parsed_lyrics):
    current_lyric = parsed_lyrics[0]
    for i in range(len(parsed_lyrics)):
        if parsed_lyrics[i][0] <= progress:
            current_lyric = parsed_lyrics[i]
        if parsed_lyrics[i][0] > progress:
            break

    return current_lyric