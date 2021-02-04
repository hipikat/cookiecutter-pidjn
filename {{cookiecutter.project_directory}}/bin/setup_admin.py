#!/usr/bin/env python
"""
Install a "SECRET_KEY=..." line in the .env file in the root project directory.
If '--print' is passed, just print a suitable key to stdout.
"""

import logging
import os
import re
import sys
import random


SECRET_KEY_LENGTH = 50
SECRET_KEY_CHARS = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'


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


def secret_key():
    """Return a string of random characters suited to a Django `SECRET_KEY`."""
    return ''.join(
        [random.SystemRandom().choice(SECRET_KEY_CHARS)
         for _ in range(SECRET_KEY_LENGTH)])


if __name__ == "__main__":

    # Just print the key to stdio, if they called us with '--print'
    if sys.argv[-1] == '--print':
        print(secret_key()),

    # Otherwise, check to see if a SECRET_KEY exists in .env
    env_file = os.path.join(PROJECT_DIR, '.env')
    try:
        with open(env_file) as fp:
            env_lines = fp.readlines()
    except FileNotFoundError:
        logging.error("No .env file installed at %s; aborting" % (os.getcwd(),))
        sys.exit(1)

    key_re = re.compile(r"^SECRET_KEY=[^#]+")
    for line in env_lines:
        if re.match(key_re, line.strip()):
            logging.debug("SECRET_KEY already exists in .env; aborting")
            sys.exit(0)

    # No un-commented SECRET_KEY found in .env; append one
    with open(env_file, "a") as fp:
        fp.write("SECRET_KEY=%s\n" % (secret_key(),))
    logging.debug("Successfully wrote SECRET_KEY line to .env")
