#In charge of getting the current track name, artist, progress, and duration of song

import urllib.parse
import requests
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
import pkce
import secrets

#Needed URLs and Client ID
CLIENT_ID = 'cfb9c29efe1949e586417226ff0f358a'
REDIRECT_URL = 'http://localhost:8888/callback'
AUTH_URL = 'https://accounts.spotify.com/authorize'
TOKEN_URL = 'https://accounts.spotify.com/api/token'
CURRENTLYPLAYING_URL = 'https://api.spotify.com/v1/me/player/currently-playing'

#Automatically handles get request and gretrieves the code needed to create access token
#Displays spotify connection in local browser and prompts to close when done
class AuthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_url = urllib.parse.urlparse(self.path)
        query_params = urllib.parse.parse_qs(parsed_url.query)
        self.server.auth_code = query_params.get('code', [None])[0]
        self.server.state = query_params.get('state', [None])[0]

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"<h1>Authorization successful. You can close this tab.</h1>")


#Authorizes user for the API through PKCE Flow
def login():
    #Create PKCE verifier and challenge
    verifier = pkce.generate_code_verifier(length=128)
    challenge = pkce.get_code_challenge(verifier)

    #Creating random urlsafe string to check if request was secure by comparing after
    state = secrets.token_urlsafe(16)

    params = {
        'client_id': CLIENT_ID,
        'response_type': 'code',
        'redirect_uri': REDIRECT_URL,
        'state': state,
        'scope': 'user-read-playback-state',
        'code_challenge_method': 'S256',
        'code_challenge': challenge,
    }

    #(Lines 52-58): Creates URL, opens in browser and returns authorization code to create token
    auth_url = f"{AUTH_URL}?{urllib.parse.urlencode(params)}"
    webbrowser.open(auth_url)

    server = HTTPServer(('localhost', 8888), AuthHandler)
    server.handle_request()

    auth_code = server.auth_code

    #Check for attacks through the state
    if server.state != state:
        print("Potential attack, state mismatch")
        return False

    #(Lines 66-84): Sends post request to spotify authorizer with needed info to create access token. Stores token info globally for other functions access.
    header = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    token_params = {
        'grant_type': 'authorization_code',
        'code': auth_code,
        'redirect_uri': REDIRECT_URL,
        'client_id': CLIENT_ID,
        'code_verifier': verifier,
    }

    response = requests.post(TOKEN_URL, data=token_params, headers=header)
    response = response.json()

    global ACCESS_TOKEN, EXP_TIME, REFRESH_TOKEN
    ACCESS_TOKEN = response.get('access_token')
    EXP_TIME = response.get('expires_in')
    REFRESH_TOKEN = response.get('refresh_token')

    getSpotifyInfo()

def getSpotifyInfo():

    header = {
        'Authorization': f'Bearer {ACCESS_TOKEN}',
    }

    response = requests.get(CURRENTLYPLAYING_URL, headers=header)
    response = response.json()

    if response and "item" in response:

        song_name = response["item"]["name"]
        artist_name = response["item"]["artists"][0]["name"]
        album_name = response["item"]["album"]["name"]
        progress = response.get("progress_ms", 0)
        duration = response["item"].get("duration_ms", 0)
        is_playing = response.get("is_playing", False)

        data = {
            "song_name": song_name,
            "artist_name": artist_name,
            "album_name": album_name,
            "progress": progress,
            "duration": duration,
            "is_playing": is_playing,
        }

        return data


if __name__ == '__main__':
    login()