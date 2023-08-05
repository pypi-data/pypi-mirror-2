from django.core.management.base import BaseCommand
from mutations.evolution import Evolution
from optparse import make_option


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--interactive', dest='interactive', default=False,
            help='Runs in interactive mode.'),
        make_option('--dry', dest='dry', default=False,
            help='Runs in dry mode.'),
        make_option('--alldone', dest='alldone', default=False,
            help='Marks every mutation as done.'),
    )

    help = 'Runs mutations where they belong.'

    def handle(self, *args, **options):
        opts = ['interactive', 'dry', 'alldone']
        params = {}
        for opt in opts:
            params[opt] = bool(options[opt])
        evolution = Evolution(**params)
        evolution.evolve()

