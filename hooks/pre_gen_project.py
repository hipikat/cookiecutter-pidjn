# Cookiecutter hook to be run after generating projects

import logging
from os import getcwd, listdir, makedirs, symlink
from os.path import abspath, exists, isdir, join, realpath
import re
import sys


MODULE_REGEX = r'^[_a-zA-Z][_a-zA-Z0-9]+$'
PROJECT_DIR = realpath(getcwd())

logging.debug('Starting pre_gen_project.py; cwd=' + PROJECT_DIR)


module_name = re.escape('{{ cookiecutter.project_module_name }}')


# Validate project_module_name is a valid Python name
if not re.match(MODULE_REGEX, module_name):

    raise ValueError('cookiecutter.project_module_name '
                     '"{{ cookiecutter.project_module_name }}" is not a valid '
                     'Python module name.')

    logging.debug('ERROR: %s is not a valid Python module name!' % module_name)
    sys.exit(1)


logging.debug('Finished pre_gen_project.py')
