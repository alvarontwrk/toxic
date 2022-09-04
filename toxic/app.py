#!/usr/bin/env python3

import click
import toxic
import os


@click.command()
@click.option("-s", "--secret", type=str)
@click.option("-t", "--timeout", type=int)
@click.option("-p", "--pre", type=str)
@click.option("-c", "--command", type=str)
@click.option("--cert", type=str)
@click.option("--key", type=str)
@click.version_option()
def main(secret, timeout, pre, command, cert, key):
    secret = secret if secret else None
    timeout = timeout if timeout else 60
    pre = pre if pre else None
    command = command if command else None
    cert = cert if cert else None
    key = key if key else None

    pid = os.fork()

    if pid:
        toxic.serverapp.config["secret"] = secret
        if cert and key:
            toxic.serverapp.run(ssl_context=(cert,key))
        else:
            toxic.serverapp.run()
    else:
        toxic.handle_connection(timeout, command, pre)
