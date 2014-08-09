# -*- coding: utf-8 -*-

import urllib, re, os.path, soundcloud
import utils

def download(client_id, track_url, dir, override=False):
    """Download a song using the API"""
    client = soundcloud.Client(client_id=client_id)
    track = client.get('/resolve', url=track_url)
    print "Found: '%s'" % track.title

    #from pprint import pprint
    #pprint (vars(track))

    if not dir: dir = 'mp3'
    utils.create_dir(dir)

    title = fix_title(track.title, track.user['username'])
    file_name = utils.build_file_name(dir, title)

    if not override and os.path.exists(file_name):
        print "File already exists, skipped"
        return False

    stream_url = client.get(track.stream_url, allow_redirects=False)
    urllib.urlretrieve(stream_url.location, file_name)

    return True


def fix_title(title, user_name):
    """Fix title (missing space, illegal chars, missing author)"""
    # Add missing dash
    title = re.sub(r"^(.*\S)- (.*)$", r"\1 - \2", title)

    # Remove adds
    title = title.split('//', 1)[0]

    # Prepend username if author seems to be missing
    if ' - ' not in title:
        title = '%s - %s' % (user_name, title)

    return title.strip()
