"""Management command to print a SECRET_KEY string."""

from .utils import ScriptCommand


class Command(ScriptCommand):
    help = 'Print a random SECRET_KEY string'
    script_name = 'generate_secret_key'

    def handle(self, *args, **options):
        print(self.module.secret_key())
