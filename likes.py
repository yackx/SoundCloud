# -*- coding: utf-8 -*-

import requests, os.path, soundcloud
from collections import Counter
import utils, track

# I need to make an instance of Resource from `soundcloud` but it's not working,
# so, this....
class ResourceDuck(object):
    """Object wrapper for resources.

    Provides an object interface to resources returned by the Soundcloud API.
    """
    def __init__(self, obj):
        self.obj = obj
        if hasattr(self, 'origin'):
            self.origin = Resource(self.origin)

    def __getstate__(self):
        return self.obj.items()

    def __setstate__(self, items):
        if not hasattr(self, 'obj'):
            self.obj = {}
        for key, val in items:
            self.obj[key] = val

    def __getattr__(self, name):
        if name in self.obj:
            return self.obj.get(name)
        raise AttributeError

    def fields(self):
        return self.obj

    def keys(self):
        return self.obj.keys()


def download_all_likes(client_id, user_url, base_dir, override=False):
    """Download all of a user's likes."""
    downloaded = 0
    skipped = 0
    errors = 0

    client = soundcloud.Client(client_id=client_id)
    user = client.get('/resolve', url=user_url)

    print "Finding likes..."

    likes = []
    current_url = '/users/%d/favorites?limit=100&offset=0&linked_partitioning=1' % (user.id)
    while True:
        print "."
        query = client.get(current_url)

        collection = query.fields()['collection']
        wrapped_collection = []
        for item in collection:
            wrapped_collection.append(ResourceDuck(item))

        likes.extend(wrapped_collection)

        if 'next_href' in query.fields():
            next_href = query.fields()['next_href']
            start = next_href.find('/users/')
            current_url = next_href[start:]
        else:
            break

    print 'Downloading %d likes...' % len(likes)

    for like in likes:
        try:
            done = track.download(client, like, base_dir, override)
            if done: downloaded = downloaded + 1
            else: skipped = skipped + 1
        except requests.exceptions.HTTPError, err:
            if err.response.status_code == 404:
                print 'Error: could not download'
                errors = errors + 1
            else:
                raise

    print 'Likes downloaded.'

    return Counter({
        'downloaded': downloaded, 'skipped': skipped, 'errors': errors
    })
