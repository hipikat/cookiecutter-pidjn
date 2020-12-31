#!/usr/bin/env python

import os
import shutil
from subprocess import check_call as call

import click
from click import echo as echo


COOKIECUTTER_PIDJN_UPSTREAM = 'https://github.com/hipikat/cookiecutter-pidjn.git'


def _get_project_dir():
    """Search towards the root directory for package.json, and return the
    directory which contains it."""
    cwd = os.path.realpath(os.getcwd())
    while cwd is not os.path.dirname(cwd):
        if 'package.json' in os.listdir(cwd):
            return cwd
        cwd = os.path.dirname(cwd)
    raise RuntimeError("No 'package.json' in cwd (%s) or parent directories." %
                       (os.getcwd(),))


PROJECT_DIR = _get_project_dir()


@click.group()
def cli():
    pass


@click.command()
@click.option('--rebuild', default=False, help="Teardown virtualenv and node_modules first")
@click.option('--dev/--prod', default=False, help="Install developer packages")
@click.argument('environment', default="prod", envvar="{{ cookiecutter.project_env_prefix }}_DJANGO_ENVIRONMENT")
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


@click.command()
@click.option('--clean/--cached', default=False)
def bake(clean):
    echo('Baking project from Cookiecutter template...')
    from cookiecutter.main import cookiecutter

    # Path to the locally cached cookiecutter template
    cc_template = COOKIECUTTER_PIDJN_UPSTREAM
    local_template = os.path.join(PROJECT_DIR, 'var/cookiecutter-pidjn')
    template_is_cached = os.path.exists(os.path.join(local_template, 'cookiecutter.json'))
    if template_is_cached and clean:
        shutil.rmtree(local_template)
    elif template_is_cached:
        cc_template = local_template

    # Let cookiecutter do its thing
    cookiecutter(
        template=cc_template,
        checkout='main',
        no_input=True,
        overwrite_if_exists=True,
        output_dir=os.path.realpath(os.path.join(PROJECT_DIR, '..')),
        config_file=os.path.join(PROJECT_DIR, 'var/pidjn/cookiecutter-config.yaml'),
    )


list(map(cli.add_command, [
    init, teardown, bake
]))


if __name__ == '__main__':
    cli()
