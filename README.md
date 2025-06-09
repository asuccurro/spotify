# Spotify Playlist Exporter

A simple command-line tool to export Spotify playlist tracks (titles and artists) to CSV or TXT files.

## Setup

1. Create a Spotify Developer account and application at https://developer.spotify.com/dashboard/
2. Get your Client ID and Client Secret from the Spotify Developer Dashboard
3. Add `https://localhost:8888/callback` as a Redirect URI in your app settings
4. Set up your environment:

```bash
# Install dependencies
pip install -r requirements.txt

# Update .env file with your Spotify credentials
# Edit the .env file and fill in your:
# - SPOTIFY_CLIENT_ID
# - SPOTIFY_CLIENT_SECRET
# - SPOTIFY_REDIRECT_URI (must match exactly what you entered in the developer dashboard)
```

## Usage

```bash
# Export to CSV (default)
python public_exporter.py "https://open.spotify.com/playlist/your_playlist_id"

# Export to TXT
python public_exporter.py "https://open.spotify.com/playlist/your_playlist_id" --format txt

# Specify custom output file
python public_exporter.py "https://open.spotify.com/playlist/your_playlist_id" --output my_songs.csv

```

### How to get a Spotify playlist URL (public playlists)

1. Open Spotify
2. Navigate to the playlist you want to export
3. Click the "..." menu
4. Select "Share" and then "Copy link to playlist"

## Features

- Exports track title and artist information
- Supports both CSV and TXT output formats
- Handles large playlists with pagination
- Includes track position numbers
- Provides clean and readable output

## License

MIT License - See LICENSE file for details.
