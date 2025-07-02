# Twitch API Vibe-Coding Project
# Goal: Fetch and display top live Valorant streams using the Twitch API

import os
import requests
from dotenv import load_dotenv

load_dotenv()

# ----- Setup -----
# You (the mentor) will need to create a Twitch Developer app and get:
# 1. A Client ID
# 2. A Client Secret
# 3. A Bearer Token (via OAuth2 Client Credentials Flow)

# Replace these with actual values
CLIENT_ID = os.environ.get("TWITCH_CLIENT_ID")
BEARER_TOKEN = os.environ.get("TWITCH_ACCESS_TOKEN")

# API base
TWITCH_API_URL = 'https://api.twitch.tv/helix'

# Headers required for Twitch API calls
HEADERS = {
    'Client-ID': CLIENT_ID,
    'Authorization': f'Bearer {BEARER_TOKEN}'
}

# ----- Get Game ID for Valorant -----
def get_game_id(game_name):
    response = requests.get(
        f'{TWITCH_API_URL}/games',
        headers=HEADERS,
        params={'name': game_name}
    )
    data = response.json()
    if 'data' in data and data['data']:
        return data['data'][0]['id']
    else:
        print(f"Error fetching game ID for '{game_name}': {data}")
        return None

# ----- Get Live Streams for Game -----
def get_live_streams(game_id, max_results=10):
    response = requests.get(
        f'{TWITCH_API_URL}/streams',
        headers=HEADERS,
        params={
            'game_id': game_id,
            'first': max_results,
            'language': 'en'
        }
    )
    return response.json()['data']

# ----- Main Function -----
def main():
    print("Fetching live Valorant streams on Twitch...\n")
    game_id = get_game_id("Valorant")
    if not game_id:
        return

    streams = get_live_streams(game_id)

    for stream in streams:
        print(f"{stream['user_name']} is live: {stream['title']}")
        print(f"Viewers: {stream['viewer_count']}")
        print(f"Link: https://twitch.tv/{stream['user_login']}")
        print("-" * 40)

if __name__ == '__main__':
    main()
