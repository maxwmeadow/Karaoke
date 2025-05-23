#Makes a request to lrclib.net to get the LRC file lyrics which we can then use to display the karaoke
import requests
import re
import syllables

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

def get_current_word(progress, interpolated_lyrics):
    current = interpolated_lyrics[0]
    for i in range(len(interpolated_lyrics)):
        if interpolated_lyrics[i][0] <= progress:
            current = interpolated_lyrics[i]
        if interpolated_lyrics[i][0] > progress:
            break

    return current

def interpolate_lyrics(lyrics):

    interpolated_lyrics = []

    for i in range(len(lyrics) - 1):
        current_start = lyrics[i][0]
        next_line_start = lyrics[i + 1][0]
        total_time = next_line_start - current_start

        word_split = re.split(r'\s+', lyrics[i][1])
        syllable_count = []
        for word in word_split:
            syllable_count.append(syllables.estimate(word))

        total = sum(syllable_count)
        running_time = current_start

        for j in range(len(syllable_count)):
            word_time = (syllable_count[j] / total) * total_time

            interpolated_lyrics.append((running_time, word_split[j], lyrics[i][1]))
            running_time += word_time

    print(interpolated_lyrics)
    return interpolated_lyrics