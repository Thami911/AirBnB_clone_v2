#!/usr/bin/python3
""" Fabric script that creates and distributes an archive to your web servers
    using the function deploy: """

from fabric.api import *
from datetime import datetime
from os.path import exists
# do_pack = __import__('1-pack_web_static').do_pack
# do_deploy = __import__('2-do_deploy_web_static').do_deploy

env.hosts = ['54.165.88.198', '100.26.255.115']  # <IP web-01>, <IP web-02>

def do_pack():
    """generates a .tgz archive from the contents of the web_static folder"""
    local("sudo mkdir -p versions")
    date = datetime.now().strftime("%Y%m%d%H%M%S")
    file_name = "versions/web_static_{}.tgz".format(date)
    result = local("sudo tar -cvzf {} web_static".format(file_name))
    if result.succeeded:
        return file_name
    else:
        return None


def do_deploy(archive_path):
    """ distributes an archive to my web servers"""
    if exists(archive_path) is False:
        return False
    file_name = archive_path.split('/')[-1]
    no_tgz = '/data/web_static/releases/' + "{}".format(file_name.split('.')[0])
    tmp = "/tmp/" + file_name

    try:
        put(archive_path, "/tmp/")
        run("mkdir -p {}/".format(no_tgz))
        run("tar -xzf {} -C {}/".format(tmp, no_tgz))
        run("rm {}".format(tmp))
        run("mv {}/web_static/* {}/".format(no_tgz, no_tgz))
        run("rm -rf {}/web_static".format(no_tgz))
        run("rm -rf /data/web_static/current")
        run("ln -s {}/ /data/web_static/current".format(no_tgz))
        return True
    except:
        return False


def deploy():
    """ creates and distributes an archive to your web servers"""
    new_archive_path = do_pack()
    if exists(new_archive_path) is False:
        return False
    result = do_deploy(new_archive_path)
    return result
