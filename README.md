SoundCloud Downloader
=====================

A simple Python script to download music from SoundCloud, using either their API or by scraping HTML where it makes sense.


## Install

You need Python 2.7.5 or above and the following libraries:

* [SoundCloud client](https://github.com/soundcloud/soundcloud-python): `pip install soundcloud`

Refer to their documentation for alternate installation methods (`easy_install`, `apt-get`, ...).

You also need a *CLIENT ID* from SoundCloud.
It is as simple as [registering your "app"](https://developers.soundcloud.com/).


## Download a song

    youri:SoundCloud $ python download.py -h
    usage: download.py [-h] [--song SONG] [--playlist PLAYLIST] --id ID
                       [--override]

    Download a SoundCloud sound or a complete playlist

    optional arguments:
      -h, --help            show this help message and exit
      --song SONG, -s SONG  Download a single song
      --playlist PLAYLIST, -p PLAYLIST
                            Download all songs from a public playlist
      --id ID, -i ID        Client ID
      --override, -d        Override file if it exists. Defaults to false

To download a song, copy the song page URL from your browser:

    youri:SoundCloud $ python download.py --id my_id --song https://soundcloud.com/dj-crontab/indiscriminate-killers
    Found: 'Indiscriminate Killers'

The song will be downloaded to a `mp3` folder under the current directory.


## Download a playlist

To download all songs from a playlist, make sure the playlist URL is accessible without password:

* Either by making the playlist public or
* By using its "sharing URL". To do so, go to the playlist and click on the "Share" button. Copy the "Private Share" URL that appears.

Example:

    youri:SoundCloud $ python download.py --id my_id --playlist https://soundcloud.com/its-me/sets/my-list/sharecode
    Found: 'Execute Every Minute'
    File already exists, skipped
    Found: 'Indiscriminate Killers'
    Found: 'Above & Beyond pres. OceanLab - Satellite (ilan Bluestone Remix) [Out Now]'
    Error: could not download
    Found: 'Missiles at a Wedding - Heavy'
    Found: 'CASHMERE'
    Downloaded: 3, Skipped: 1, Errors: 1

Notice that, for some reason, some titles cannot be downloaded, probably due to restriction set by the author or poster.

The song will be downloaded to a folder named `mp3/playlist_title` under the current directory.


## Unit tests

Close to zero at the time. Use `py.test`:

    youri:SoundCloud $ py.test -q tests
    .
    1 passed in 0.08 seconds
