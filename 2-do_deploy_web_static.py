#!/usr/bin/python3

"""Fabric script that distributes an archive to your web servers"""

import os.path
from fabric.api import env
from fabric.api import put
from fabric.api import run

env.hosts = ["52.87.235.175", "100.25.192.241"]


def do_deploy(archive_path):
    """Distributes an archive to a web server"""

    if os.path.isfile(archive_path) is False:
        return False

    file = archive_path.split("/")[-1]
    name = file.split(".")[0]

    if put(archive_path, "/tmp/{}".format(file)).failed:
        return False

    if run("rm -rf /data/web_static/releases/{}/".format(name)).failed:
        return False

    if run("mkdir -p /data/web_static/releases/{}/".format(name)).failed:
        return False

    if run(
        "tar -xzf /tmp/{} -C /data/web_static/releases/{}/".format(file, name)
    ).failed:
        return False

    if run("rm /tmp/{}".format(file)).failed:
        return False

    if run(
        "mv /data/web_static/releases/{}/web_static/* "
        "/data/web_static/releases/{}/".format(name, name)
    ).failed:
        return False

    if run("rm -rf /data/web_static/releases/{}/web_static".format(name)).failed:
        return False

    if run("rm -rf /data/web_static/current").failed:
        return False

    if run(
        "ln -s /data/web_static/releases/{}/ /data/web_static/current".format(name)
    ).failed:
        return False

    return True