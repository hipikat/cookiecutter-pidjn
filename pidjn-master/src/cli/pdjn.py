#!/usr/bin/env python

from subprocess import check_call as call

import click
from click import echo as echo


@click.group()
def cli():
    pass


@click.command()
@click.option('--rebuild', default=False, help="Teardown virtualenv and node_modules first")
@click.option('--dev/--prod', default=False, help="Install developer packages")
@click.argument('environment', default="prod", envvar="MYSITE_DJANGO_ENVIRONMENT")
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
