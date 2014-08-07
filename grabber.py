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

import sys, re, os.path
import soundcloud

url_prefix = 'https://soundcloud.com'


def create_dir(dir):
    """Create directory if it does not exist"""
    if not os.path.exists(dir):
        os.makedirs(dir)


def build_file_name(dir, title):
    """Build the file name"""
    import re, os.path
    file_name = re.sub('/', '', title) + ".mp3"
    return os.path.join(dir, file_name)


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


def download_song(client_id, track_url, dir, override=False):
    """Download a song using the API"""
    import urllib

    client = soundcloud.Client(client_id=client_id)
    track = client.get('/resolve', url=track_url)
    print "Found: '%s'" % track.title

    #from pprint import pprint
    #pprint (vars(track))

    if not dir: dir = 'mp3'
    create_dir(dir)

    title = fix_title(track.title, track.user['username'])
    file_name = build_file_name(dir, title)

    if not override and os.path.exists(file_name):
        print "File already exists, skipped"
        return False

    stream_url = client.get(track.stream_url, allow_redirects=False)
    urllib.urlretrieve(stream_url.location, file_name)

    return True


def scrape_playlist(url):
    """Scrape the song urls from the playlist"""
    import urllib2
    from bs4 import BeautifulSoup

    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page)

    playlist_title = soup.find('meta', attrs={'property': 'twitter:title'})['content']
    last_part = url.split('/')[-1]    # Last part of URL if the playlist short id
    anchors = soup.find_all('a', class_='set-track-title')
    song_urls = []
    for anchor in anchors:
        # Prepend scheme+host and remove the list name from url
        song_urls.append(url_prefix + anchor['href'].rstrip(last_part))

    return {'playlist_title': playlist_title, 'song_urls': song_urls}


def dowload_playlist(client_id, url, base_dir, override=False):
    """Download the given playlist"""
    import requests

    downloaded = 0
    skipped = 0
    errors = 0

    # Retrieve playlist data
    scrape = scrape_playlist(url)

    # Create dir
    playlist_title = scrape['playlist_title']
    dir = os.path.join(base_dir, playlist_title)
    create_dir(dir)

    # Download songs
    for song_url in scrape['song_urls']:
        try:
            done = download_song(client_id, song_url, dir, override)
            if done: downloaded = downloaded + 1
            else: skipped = skipped + 1
        except requests.exceptions.HTTPError, err:
            if err.response.status_code == 404:
                print 'Error: could not download'
                errors = errors + 1
            else:
                raise

    print "Playlist downloaded to %s" % playlist_title
    print "Downloaded: %d, Skipped: %d, Errors: %d" % (downloaded, skipped, errors)
