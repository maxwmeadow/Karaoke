import audio_grab
from spotify import login, getSpotifyInfo
from lyrics import get_synced_lyrics, get_current_word, interpolate_lyrics
from overlay import create_overlay
from audio_grab import get_mp3, grab_set_up
import time
from datetime import datetime, timedelta


def main():
    login()
    grab_set_up()

    current_title = None
    current_lyric_text = None
    current_mp3 = None

    start_time = datetime.now()

    while True:
        if start_time - datetime.now() > timedelta(minutes=5):
            login()
            start_time = datetime.now()

        try:
            track_data = getSpotifyInfo()

            if current_mp3 is None:
                print("grabbing!")
                current_mp3 = get_mp3(track_data["track_url"],track_data["song_name"],track_data["artist_name"])

            # Handle a new song on start or song change
            if track_data["song_name"] and (current_title is None or track_data["song_name"] != current_title):
                current_title = track_data["song_name"]

                lyrics = get_synced_lyrics(
                    track_data["song_name"],
                    track_data["artist_name"],
                    track_data["album_name"],
                    track_data["duration"]
                )

                word_lyrics = interpolate_lyrics(lyrics)

                if not lyrics:
                    word_lyrics = [(0, '', f"No lyrics found for: {track_data['song_name']}")]
                else:
                    print(f"Found {len(lyrics)} lyric lines")

                current_lyric_text = None

            current = get_current_word(track_data["progress"], word_lyrics)

            #Update lyric overlay if lyric has changed based on progress
            if current and (current_lyric_text is None or current_lyric_text != current[1]):
                current_lyric_text = current[1]
                create_overlay(current)

            time.sleep(0.1)

        except Exception as e:
            create_overlay((0, "Error or Paused, unpause to continue"))
            time.sleep(2)


if __name__ == '__main__':
    main()