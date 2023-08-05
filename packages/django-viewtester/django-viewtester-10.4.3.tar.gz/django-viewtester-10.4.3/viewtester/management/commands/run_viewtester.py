from optparse import make_option

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from django.utils.importlib import import_module

from viewtester import viewtesterstate
from viewtester import utils


class Command(BaseCommand):
    help = 'Runs the test server with viewtester output enabled'
    args = 'appname'
    option_list = BaseCommand.option_list + (
        make_option('-f', '--fixture', dest='fixtures',action='append', default=[],
            help='Fixtures to load upon server startup (use multiple --fixture to load multiple fixtures).'),
        make_option('-l', '--logfile', dest='logfile', default=None,
            help='(Log)file to write the tests to. '),
        )

    def handle(self, app_label, **options):
        from django.db.models import get_app

        # a suspenders-and-a-belt pattern?
        fixtures = options.get('fixtures', [])
        logfile = options.get('logfile', None)

        # This loads the models module into app. 
        try:
            app = get_app(app_label)
        except ImproperlyConfigured:
           raise CommandError('Could not find app: %s' % app_label) 

        app_path = utils.get_app_path(app)

        app_views = import_module('.views', app_label)

        if not logfile:
            logfile = utils.get_logfilepath(app_path)

        utils.setup_logging(logfile)

        fixtures_available = utils.get_available_fixtures(app_path)

        # store some info
        viewtesterstate.app_label = app_label
        viewtesterstate.app = app
        viewtesterstate.app_views = app_views
        viewtesterstate.app_path = app_path
        viewtesterstate.fixtures_loaded = fixtures
        viewtesterstate.fixtures_available = fixtures_available

        # Wrap the viewtester middleware around the existing middleware
        if 'viewtester.middleware.Viewtester' not in settings.MIDDLEWARE_CLASSES:
            settings.MIDDLEWARE_CLASSES += ('viewtester.middleware.Viewtester',)

        # run the testserver and load the fixtures provided on the
        # commandline. Note that these fixtures are NOT the same
        # fixtures that are available when creating a new class
        call_command('testserver', *fixtures, **options)
