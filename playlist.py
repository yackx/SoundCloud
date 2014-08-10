# -*- coding: utf-8 -*-

import requests, os.path, soundcloud
from collections import Counter
import utils, track


def download_from_url(client_id, url, base_dir, override=False):
    """Download the given playlist"""
    downloaded = 0
    skipped = 0
    errors = 0

    # Retrieve playlist data
    client = soundcloud.Client(client_id=client_id)
    playlist = client.get('/resolve', url=url)

    # Create dir
    playlist_title = playlist.title
    dir = os.path.join(base_dir, playlist_title)
    utils.create_dir(dir)

    # Download tracks
    for trak in playlist.tracks:
        try:
            #done = song.down(client, track, dir, override)
            done = track.download_from_id(client_id, trak['id'], dir, override)
            if done: downloaded = downloaded + 1
            else: skipped = skipped + 1
        except requests.exceptions.HTTPError, err:
            if err.response.status_code == 404:
                print 'Error: could not download'
                errors = errors + 1
            else:
                raise

    print 'Playlist downloaded to "%s"' % playlist_title
    return Counter({
        'downloaded': downloaded, 'skipped': skipped, 'errors': errors
    })


def download_all(client_id, user_url, base_dir, override=False):
    """Download all playlist from the given user URL"""
    client = soundcloud.Client(client_id=client_id)
    user = client.get('/resolve', url=user_url)
    playlists = client.get('/users/%d/playlists' % user.id)
    stats = Counter()

    for playlist in playlists:
        print 'Playlist: "%s"' % playlist.title
        playlist_stats = download_from_url(client_id, playlist.permalink_url, base_dir, override)
        stats = stats + playlist_stats

    return stats
