# Cookiecutter hook to be run after generating projects

import logging
import os
from os import getcwd, makedirs, symlink
from os.path import abspath, exists, isdir, join, realpath
import re
import sys


PROJECT_DIR = getcwd()


logging.debug('Starting post_gen_project.py; cwd=' + PROJECT_DIR)

logging.debug("Installing symlinks...")
os.system('bin/install_symlinks.py --env debug')

logging.debug("Ensuring existence of a SECRET_KEY...")
os.system('bin/generate_secret_key.py')

logging.debug("Finished baking " + os.path.basename(PROJECT_DIR))
