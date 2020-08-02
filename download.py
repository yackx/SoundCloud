# -*- coding: utf-8 -*-

"""
Download tracks from SoundCloud.

See https://developers.soundcloud.com/ for more info on the API.

You need to register your "app" to get your CLIENT_ID.
No password needed.

Install this friendly soundcloud wrapper:
https://github.com/soundcloud/soundcloud-python
pip install soundcloud
"""

import argparse, requests, urllib2
import track, playlist, likes


def print_download_stats(stats):
    print "Downloaded: %d, Skipped: %d, Errors: %d" % (
            stats['downloaded'], stats['skipped'], stats['errors'])


parser = argparse.ArgumentParser(description='Download a SoundCloud tracks and playlists')
parser.add_argument('--track', '-t', help="Track full URL")
parser.add_argument('--playlist', '-p', help="Public or shared playlist URL")
parser.add_argument('--all', '-a', help="User URL. Download all tracks for all public playlists")
parser.add_argument('--likes', '-l', help="Download all of a user's likes.")
parser.add_argument('--id', help='Client ID', required=True)
parser.add_argument('--dir', help='Output directory.')
parser.add_argument(
        '--override', '-d', action='store_true',
        help='Override file if it exists. Defaults to false')
args = parser.parse_args()

if args.dir:
    dir = args.dir
else:
    dir = 'mp3'

error_msg = None
try:
    if args.track:
        error_msg = 'Error: track not found'
        track.download_from_url(args.id, args.track, dir=dir, override=args.override)
    elif args.playlist:
        error_msg = 'Error: Playlist not found. Make sure it is public or use its share URL'
        stats = playlist.download_from_url(args.id, args.playlist, base_dir=dir, override=args.override)
        print_download_stats(stats)
    elif args.all:
        error_msg = 'Error: User not found'
        stats = playlist.download_all(args.id, args.all, base_dir=dir, override=args.override)
        print_download_stats(stats)
    elif args.likes:
        error_msg = 'Error: User not found'
        stats = likes.download_all_likes(args.id, args.likes, base_dir=dir, override=args.override)
        print_download_stats(stats)
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
