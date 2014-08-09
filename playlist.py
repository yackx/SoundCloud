# -*- coding: utf-8 -*-

import urllib2, requests, os.path
from bs4 import BeautifulSoup
import utils, song


url_prefix = 'https://soundcloud.com'


def scrape(url):
    """Scrape the song urls from the playlist"""
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


def download(client_id, url, base_dir, override=False):
    """Download the given playlist"""
    downloaded = 0
    skipped = 0
    errors = 0

    # Retrieve playlist data
    scraped = scrape(url)

    # Create dir
    playlist_title = scraped['playlist_title']
    dir = os.path.join(base_dir, playlist_title)
    utils.create_dir(dir)

    # Download songs
    for song_url in scraped['song_urls']:
        try:
            done = song.download(client_id, song_url, dir, override)
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
