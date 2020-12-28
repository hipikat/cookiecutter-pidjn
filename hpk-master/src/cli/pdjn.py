#!/usr/bin/env python

from subprocess import check_call as call

import click
from click import echo as echo


@click.group()
def cli():
    pass


@click.command()
@click.option('--dev', default=False, help="Install developer dependencies")
def init():
    if dev:     # noqa: F821
        echo("Setting up production environment...")
        call('npm run init', shell=True)
    else:
        echo("Setting up development environment...")
        call('npm run init:dev', shell=True)


@click.command()
def teardown():
    echo('Tearing down Python & Node environments...')
    call('npm run teardown', shell=True)


list(map(cli.add_command, [
    init, teardown
]))


if __name__ == '__main__':
    cli()
