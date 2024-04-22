#!/usr/bin/python3
"""
Fabric script that generates a .tgz archive from the contents of the\
web_static folder of your AirBnB Clone repo
"""

from fabric.api import local
from datetime import datetime
import os


def do_pack():
    """ Creates a .tgz archive from the contents of the web_static folder """
    # Create the 'versions' folder if it doesn't exist
    if not os.path.exists('versions'):
        os.makedirs('versions')

    # Get the current time for the archive name
    now = datetime.now()
    timestamp = now.strftime('%Y%m%d%H%M%S')

    # Set the name of the archive
    archive_name = 'versions/web_static_' + timestamp + '.tgz'

    # Create the .tgz archive
    result = local('tar -cvzf {} web_static'.format(archive_name))

    # Check if the archive was created successfully
    if result.succeeded:
        return archive_name
    else:
        return None
