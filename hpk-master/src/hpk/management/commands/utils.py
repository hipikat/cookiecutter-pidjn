"""Utilities for Django Management commands."""

from importlib.util import spec_from_file_location, module_from_spec
from os.path import dirname, join as join_paths

from django.conf import settings
from django.core.management.base import BaseCommand


PROJECT_DIR = dirname(dirname(settings.BASE_DIR))


class ScriptCommand(BaseCommand):
    """Base class for management commands that would like to import Python
    files from the scripts/ directory (under this project's base directory).

    Management Commands inheriting from this class should set the class
    variable `script_name` to the name of the script, excluding the '.py'
    extension. After initialisation, they will have a self.module attribute
    representing the namespace defined by the script's instantiation.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.module = self._get_script_module()

    def _get_script_module(self):
        script_path = join_paths(PROJECT_DIR, 'scripts', self.script_name + '.py')
        spec = spec_from_file_location("cmd_utils." + self.script_name,script_path)
        module = module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
