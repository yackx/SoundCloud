# -*- coding: utf-8 -*-

"""
Download tracks from SoundCloud using their API.

See https://developers.soundcloud.com/.

You need to register your "app" to get your CLIENT_ID.
No password needed.

Install this friendly soundcloud wrapper:
https://github.com/soundcloud/soundcloud-python

pip install soundcloud
"""

import argparse, requests, urllib2
import track, playlist

parser = argparse.ArgumentParser(description='Download a SoundCloud tracks and playlists')
parser.add_argument('--track', '-t', help="Track URL")
parser.add_argument('--playlist', '-p', help="Public or shared playlist URL")
parser.add_argument('--all', '-a', help="User URL. Download all tracks for all public playlists")
parser.add_argument('--id', help='Client ID', required=True)
parser.add_argument(
        '--override', '-d', action='store_true',
        help='Override file if it exists. Defaults to false')
args = parser.parse_args()

dir = 'mp3'

error_msg = None
try:
    if args.track:
        error_msg = 'Error: track not found'
        track.download_from_url(args.id, args.track, dir=dir, override=args.override)
    elif args.playlist:
        error_msg = 'Error: Playlist not found. Make sure it is public or use its share URL'
        playlist.download_from_url(args.id, args.playlist, base_dir=dir, override=args.override)
    elif args.all:
        error_msg = 'Error: User not found'
        playlist.download_all(args.id, args.all, base_dir=dir, override=args.override)
    else:
        parser.print_help()
        print '\nError: you must specify either a track, a public (or shared) playlist or a user'
        exit(1)
except urllib2.HTTPError, err:
    if err.code == 404:
        print error_msg
        exit(1)
    else:
        raise
