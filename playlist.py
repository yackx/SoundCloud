# -*- coding: utf-8 -*-

import requests, os.path, soundcloud
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

    # Stats
    print "Playlist downloaded to %s" % playlist_title
    print "Downloaded: %d, Skipped: %d, Errors: %d" % (downloaded, skipped, errors)
