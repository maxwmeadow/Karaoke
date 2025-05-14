from spotify import login, getSpotifyInfo
from lyrics import get_synced_lyrics, get_current_lyric
from overlay import create_overlay
import time

RUNNING = True

def main():
    login()
    track_data = getSpotifyInfo()
    print(track_data)
    lyrics = get_synced_lyrics(
        track_data["song_name"],
        track_data["artist_name"],
        track_data["album_name"],
        track_data["duration"]
    )
    print(lyrics)
    progress = track_data["progress"]
    current = get_current_lyric(progress, lyrics)
    print(current)
    create_overlay(current)

if __name__ == '__main__':
    main()