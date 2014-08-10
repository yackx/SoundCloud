SoundCloud Downloader
=====================

A simple Python script to download music from SoundCloud, using either their API.


## Install

1° Download the code

Clone this repository:

    git clone https://github.com/YouriAckx/SoundCloud.git

2° Install libraries

You need Python 2.7.5 or above and the following library:

* [SoundCloud client](https://github.com/soundcloud/soundcloud-python): `pip install soundcloud`. Refer to their documentation for alternate installation methods (`easy_install`, `apt-get`, ...).

3° Get your client id

You also need a *CLIENT ID* from SoundCloud. It is as simple as [registering your "app"](https://developers.soundcloud.com/).


## Download a track

    youri:SoundCloud $ python download.py -h
    usage: download.py [-h] [--track TRACK] [--playlist PLAYLIST] --id ID
                       [--override]

    Download a SoundCloud sound or a complete playlist

    optional arguments:
      -h, --help            show this help message and exit
      --track TRACK, -s TRACK  Download a single track
      --playlist PLAYLIST, -p PLAYLIST
                            Download all tracks from a public playlist
      --id ID, -i ID        Client ID
      --override, -d        Override file if it exists. Defaults to false

To download a track, copy the track page URL from your browser:

    youri:SoundCloud $ python download.py --id my_id --track https://soundcloud.com/dj-crontab/indiscriminate-killers
    Found: 'Indiscriminate Killers'

The track will be downloaded to a `mp3` folder under the current directory.


## Download a playlist

To download all tracks from a playlist, make sure the playlist URL is accessible without password:

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

The track will be downloaded to a folder named `mp3/playlist_title` under the current directory.


## Download all playlists

To download all tracks from all playlists of a user:

    youri:SoundCloud $ python download.py --id my_id --all http://soundcloud.com/some-user

The playlists must be public.


## Unit tests

Close to zero at the time. Use `py.test`:

    youri:SoundCloud $ py.test -q tests
    .
    1 passed in 0.08 seconds
