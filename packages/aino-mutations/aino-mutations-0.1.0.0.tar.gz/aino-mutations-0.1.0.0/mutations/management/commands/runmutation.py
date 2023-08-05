from django.core.management.base import BaseCommand
from django.db import connections, transaction
from optparse import make_option
from os.path import abspath


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--dry', dest='dry', default=False,
            help='Runs in dry mode.'),
    )
    help = 'Runs a mutation script in te current revision, does not mark it as run.'

    def handle(self, path, *args, **options):
        path = abspath(path)
        db_alias = path.split('/')[-2]
        execfile(path, {}, {
            'cursor': connections[db_alias].cursor(),
            'commit_unless_managed': transaction.commit_unless_managed,
            'dry': bool(options['dry']),
        })

