#!/usr/bin/python3
"""
Fabric script that creates and distributes ann archive to web servers
"""

from fabric.api import env, local, run
from fabric.operations import put
from datetime import datetime
from os.path import exists

# define the servers
env.hosts = ['34.232.65.42', '54.227.224.76']
env.user = 'ubuntu'
env.key_filename = ['~/.ssh/school']


def do_pack():
    """ Creates a .tgz archive from the contents of the web_static folder """
    # Create the 'versions' folder if it doesn't exist
    if not exists('versions'):
        local('mkdir -p versions')

    # Get the current time for the archive name
    now = datetime.now()
    timestamp = now.strftime('%Y%m%d%H%M%S')

    # Set the name of the archive
    archive_name = 'versions/web_static_{}.tgz'.format(timestamp)

    # Create the .tgz archive
    result = local('tar -cvzf {} web_static'.format(archive_name))

    # Check if the archive was created successfully
    if result.succeeded:
        return archive_name
    else:
        return None


def do_deploy(archive_path):
    """ Distributes an archive to the web servers """
    if not exists(archive_path):
        return False

    try:
        # Upload the archive to the /tmp/ directory of the web server
        put(archive_path, '/tmp/')

        # Extract the archive to the appropriate folder
        filename = archive_path.split('/')[-1]
        folder_name = '/data/web_static/releases/{}'.format(filename[:-4])
        run('mkdir -p {}'.format(folder_name))
        run('tar -xzf /tmp/{} -C {}'.format(filename, folder_name))

        # Delete the archive from the web server
        run('rm /tmp/{}'.format(filename))

        # Move the contents of the extracted folder to the appropriate location
        run('mv {}/web_static/* {}'.format(folder_name, folder_name))

        # Delete the extracted folder
        run('rm -rf {}/web_static'.format(folder_name))

        # Delete the symbolic link /data/web_static/current
        run('rm -rf /data/web_static/current')

        # Create a new symbolic link to the new version
        run('ln -s {} /data/web_static/current'.format(folder_name))

        print("New version deployed!")
        return True

    except Exception as e:
        print(e)
        return False


def deploy():
    """Creates and distributes an archive to web servers"""
    # Call do_pack to create the archive
    archive_path = do_pack()

    # If archive_path is None, do_pack failed to create the archive
    if archive_path is None:
        return False

    # call do_deploy to distribute the archive to web servers
    return do_deploy(archive_path)
