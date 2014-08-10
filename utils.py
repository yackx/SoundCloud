# -*- coding: utf-8 -*-

import re, os.path


def create_dir(dir):
    """Create directory if it does not exist"""
    if not os.path.exists(dir):
        os.makedirs(dir)


def build_file_name(dir, title):
    """Build the file name"""
    file_name = re.sub('/', '', title) + ".mp3"
    return os.path.join(dir, file_name)
