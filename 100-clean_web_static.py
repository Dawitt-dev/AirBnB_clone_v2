#!/usr/bin/python3
"""
Fabric script that deletes out-of-date archives
"""

from fabric.api import env, run, local
from datetime import datetime
from os.path import exists

# Define the servers
env.hosts = ['34.232.65.42', '54.227.224.76']
env.user = 'ubuntu'
env.key_filename = ['~/.ssh/school']


def do_clean(number=0):
    """Deletes out-of-date archives"""
    # Convert number to an integer
    number = int(number)

    # Get the list of archives in the versions folder
    archives = local('ls -1t versions', capture=True).split('\n')

    # Delete all archives except the most recent "number" archives
    for archive in archives[number:]:
        local('rm versions/{}'.format(archive))

    # Get the list of archives in the /data/web_static/releases folder
    releases = run('ls -1t /data/web_static/releases').split()

    # Delete all archives in except the most recent "number" archives
    for release in releases[number:]:
        run('rm -rf /data/web_static/releases/{}'.format(release))
