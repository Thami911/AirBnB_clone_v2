#!/usr/bin/python3
"""Fabric script that deletes out-of-date archives"""

from fabric.api import *

env.hosts = env.hosts = ['54.165.88.198', '100.26.255.115']
env.user = 'ubuntu'

def do_clean(number=0):
    """Delete out-of-date archives"""
    number = int(number)
    if number < 1:
        number = 1

    with lcd("versions"):
        local("ls -t | tail -n +{} | xargs rm -rf".format(number + 1))

    with cd("/data/web_static/releases"):
        run("ls -t | tail -n +{} | xargs rm -rf".format(number + 1))
