#!/usr/bin/env python3
"""
Public Playlist Exporter
------------------------
A minimal script that uses client credentials flow for public playlists only.
This approach doesn't require user authentication for public playlists.
"""

import os
import sys
import csv
import argparse
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Load environment variables
load_dotenv()

def export_playlist(playlist_url, output_format='csv', output_file=None, numbering=False):
    """
    Export tracks from a public Spotify playlist to a file.
    
    Args:
        playlist_url (str): The URL of the Spotify playlist
        output_format (str): The output format ('csv' or 'txt')
        output_file (str, optional): The output file path
        numbering (bool): Whether to include track numbering in the output
    """
    # Get credentials from environment variables
    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
    
    if not all([client_id, client_secret]):
        print("Error: Missing Spotify API credentials in .env file.")
        sys.exit(1)
    
    try:
        # Set up client credentials manager (no user authentication needed)
        auth_manager = SpotifyClientCredentials(
            client_id=client_id,
            client_secret=client_secret
        )
        
        # Create the Spotify client
        spotify = spotipy.Spotify(auth_manager=auth_manager)
        
        # Extract playlist ID from URL
        if "spotify.com" in playlist_url:
            playlist_id = playlist_url.split("/")[-1].split("?")[0]
        else:
            playlist_id = playlist_url
        
        # Get playlist details
        playlist = spotify.playlist(playlist_id)
        playlist_name = playlist['name']
        print(f"Fetching tracks from playlist: {playlist_name}")
        
        # Get all tracks
        results = spotify.playlist_items(playlist_id)
        tracks = results['items']
        
        # Handle pagination
        while results['next']:
            results = spotify.next(results)
            tracks.extend(results['items'])
        
        # Process track information
        track_info = []
        for i, item in enumerate(tracks):
            if not item['track']:
                continue
            
            track = item['track']
            artists = ", ".join([artist['name'] for artist in track['artists']])
            
            track_data = {
                "position": i + 1,
                "title": track['name'],
                "artist": artists,
                "album": track['album']['name']
            }
            track_info.append(track_data)
        
        print(f"Found {len(track_info)} tracks in the playlist.")
        
        # Export to the selected format
        if not output_file:
            # Clean the playlist name for filename
            clean_name = "".join(c if c.isalnum() or c in [' ', '-', '_'] else '_' for c in playlist_name)
            output_file = f"{clean_name}.{output_format}"
        
        if output_format == 'csv':
            export_to_csv(track_info, output_file)
        else:
            export_to_txt(playlist_name, track_info, output_file, numbering)
        
        print(f"\n✅ Export complete!")
        print(f"File saved to: {os.path.abspath(output_file)}")
        
    except Exception as e:
        if "access token could not be validated" in str(e).lower():
            print("Error: Cannot access this playlist. It may be private or require authorization.")
            print("For private playlists, please use the regular playlist_exporter.py script.")
        else:
            print(f"Error: {e}")
        sys.exit(1)

def export_to_csv(tracks, file_path):
    """Export tracks to a CSV file"""
    with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['position', 'title', 'artist', 'album']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for track in tracks:
            writer.writerow({k: track[k] for k in fieldnames})
    
    print(f"Successfully exported {len(tracks)} tracks to {file_path}")

def export_to_txt(playlist_name, tracks, file_path, numbering=False):
    """Export tracks to a text file"""
    with open(file_path, 'w', encoding='utf-8') as txtfile:
        txtfile.write(f"Playlist: {playlist_name}\n")
        txtfile.write("=" * 50 + "\n\n")
        
        for track in tracks:
            if numbering:
                txtfile.write(f"{track['position']:02d}. {track['title']} - {track['artist']}\n")
            else:
                txtfile.write(f"{track['title']} - {track['artist']}\n")

    print(f"Successfully exported {len(tracks)} tracks to {file_path}")

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Export public Spotify playlist tracks to CSV or TXT.')
    parser.add_argument('playlist_url', help='Spotify playlist URL or URI')
    parser.add_argument('--format', choices=['csv', 'txt'], default='csv',
                      help='Output format (default: csv)')
    parser.add_argument('--output', help='Output file path (optional)')
    parser.add_argument('--numbering', action='store_true', help='Enable numbering for tracks')

    args = parser.parse_args()
    
    # Export the playlist
    export_playlist(args.playlist_url, args.format, args.output, args.numbering)

if __name__ == "__main__":
    main()
