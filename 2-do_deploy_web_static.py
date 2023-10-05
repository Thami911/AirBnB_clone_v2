#!/usr/bin/python3
""" a Fabric script that distributes an archive to your web servers using the function do_deploy: """


from fabric.api import *
from datetime import datetime
from os.path import exists


env.hosts = ['54.165.88.198', '100.26.255.115']  # <IP web-01>, <IP web-02>


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
