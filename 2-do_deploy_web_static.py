#!/usr/bin/python3
"""
Fabric script that distributes an archive to your web servers
"""

from fabric.api import env, run, put
from os.path import exists

# Define the servers
env.hosts = ['34.232.65.42', '54.227.224.76']  # Replace with your server IPs
env.user = 'ubuntu'  # Replace with your username
env.key_filename = ['~/.ssh/school']  # Replace with your SSH private key path


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
