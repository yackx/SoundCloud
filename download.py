# -*- coding: utf-8 -*-

"""
Download songs from SoundCloud using their API,
or scraping HTML page when it makes sense.

See https://developers.soundcloud.com/.

You need to register your "app" to get your CLIENT_ID.
No password needed.

Install this friendly soundcloud wrapper:
https://github.com/soundcloud/soundcloud-python

pip install soundcloud
pip install beautifulsoup4
"""

import argparse, requests, urllib2
import song, playlist

parser = argparse.ArgumentParser(description='Download a SoundCloud sound or a complete playlist')
parser.add_argument('--song', '-s', help="Download a single song")
parser.add_argument('--playlist', '-p', help="Download all songs from a public playlist")
parser.add_argument('--id', '-i', help='Client ID', required=True)
parser.add_argument(
        '--override', '-d', action='store_true',
        help='Override file if it exists. Defaults to false')
args = parser.parse_args()

dir = 'mp3'

if args.song != None:
    try:
        song.download(args.id, args.song, dir=dir, override=args.override)
    except requests.exceptions.HTTPError, err:
        if err.response.status_code == 404:
            print 'Error: song not found'
            exit(1)
        else:
            raise

elif args.playlist != None:
    try:
        playlist.download(args.id, args.playlist, base_dir=dir, override=args.override)
    except urllib2.HTTPError, err:
        if err.code == 404:
            print 'Error: Playlist not found. Make sure it is public or use its share URL'
            exit(1)
        else:
            raise

else:
    parser.print_help()
    print '\nError: you must specify either a song or a public playlist'
    exit(1)
