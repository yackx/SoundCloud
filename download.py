# -*- coding: utf-8 -*-

import argparse, requests, urllib2
from grabber import *

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
        download_song(args.id, args.song, dir=dir, override=args.override)
    except requests.exceptions.HTTPError, err:
        if err.response.status_code == 404:
            print 'Error: song not found'
            exit(1)
        else:
            raise

elif args.playlist != None:
    try:
        dowload_playlist(args.id, args.playlist, base_dir=dir, override=args.override)
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
