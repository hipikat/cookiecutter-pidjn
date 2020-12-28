#!/usr/bin/env python
"""
Install project symlinks:
 - Links from project libraries to directories under node_modules
 - A link from .env to etc/env.(prod|debug)
 - Optionally, links in etc/ to config & settings files throughout the project
"""


import logging
import os
import sys


DEFAULT_ENV = 'prod'


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


def install_project_symlinks(env, force=False, config=False):
    """Instal symlinks - mostly makes configuring Webpack cleaner and easier.
    - Don't overwrite existing symlinks unless `force` is `True`.
    - The `env` argument should match an etc/env.(env) file.
    - Install superfluous links to config files under etc/ if `config` is `True`"""

    SYMLINKS = {
        'src/sass/lib': {
            'foundation': '../../../node_modules/foundation-sites/scss',
            '_vendor': '../../../node_modules/foundation-sites/_vendor',
            'motion-ui': '../../../node_modules/motion-ui/src',
        },
        'src/sass/lib/fontawesome': {
            'scss': '../../../../node_modules/@fortawesome/fontawesome-free/scss',
            'webfonts': '../../../../node_modules/@fortawesome/fontawesome-free/webfonts',
        },
        'src/js/lib': {
            'foundation': '../../../node_modules/foundation-sites/js',
        }
    }
    CONFIG_SYMLINKS = {
        'etc': {
            'Dockerfile': 'Dockerfile.ubuntu',
            'django-base.py': '../src/hpk/settings/base.py',
            'django-debug.py': '../src/hpk/settings/debug.py',
            'django-prod.py': '../src/hpk/settings/prod.py',
        }
    }

    if config:
        SYMLINKS = {**SYMLINKS, **CONFIG_SYMLINKS}

    logging.debug('Creating symlinks from src/.../lib dirs into ./node_modules/...')
    # Create symlinks from SYMLINKS
    for rel_dest_dir, symlinks in SYMLINKS.items():
        for dest_name, rel_source in symlinks.items():
            dest_dir = os.path.abspath(os.path.join(PROJECT_DIR, rel_dest_dir))
            dest = os.path.join(dest_dir, dest_name)
            src = rel_source
            if not os.path.isdir(dest_dir):
                os.makedirs(dest_dir)
            try:
                if os.readlink(dest) and force:
                    os.remove(dest)
            except FileNotFoundError:
                pass
            try:
                os.symlink(src, dest)
            except FileExistsError:
                pass

    # Hook up an environment file
    env_file = os.path.join(PROJECT_DIR, '.env')

    try:
        if os.readlink(env_file) and force:
            os.remove(env_file)
    except FileNotFoundError:
        pass
    logging.debug('Creating ./.env symlink to ./etc/env.' + env)
    try:
        os.symlink(os.path.join(PROJECT_DIR, 'etc/env.' + env), env_file)
    except FileExistsError:
        logging.debug('Skipping .env; already installed.')


if __name__ == "__main__":
    """$ install_symlinks.py [--force] [--config] [--debug|--env ENVNAME]"""

    # Poor-man's (arg|opt)parse
    args = sys.argv[1:]
    force = True if '--force' in args else False
    config = True if '--config' in args else False
    if '--debug' in args:
        env = 'debug'
    elif '--env' in args:
        try:
            env = args[args.index('--env') + 1]
        except IndexError:
            logging.error("You must supply a value for --env")
            sys.exit(1)
    else:
        env = DEFAULT_ENV

    install_project_symlinks(force=force, env=env, config=config)
