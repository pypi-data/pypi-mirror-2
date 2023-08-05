import os
from datetime import datetime
import logging

from django.utils.safestring import mark_safe


def safe_dict(dict):
    new_dic = {}
    for key,val in dict.iteritems():
        new_dic[key] = mark_safe(val)
    return new_dic


def get_app_path(app):
    return os.path.dirname(app.__file__)


def get_tests_dir(app_path):
    return os.path.join(app_path, 'tests')


def format_filename(basefilename, n):
    return "%s_%02d.py" % (basefilename, n)


def get_logfilepath(app_path):
    testdir = get_tests_dir(app_path)
    if not os.path.exists(testdir):
        os.mkdir(testdir)
        import shutil
        source = os.path.join(os.path.dirname(__file__), 'templates', 
                              'viewtester', '__init__.py')
        target = os.path.join(testdir, '__init__.py')
        shutil.copy (source, target)
    filename = os.path.join(testdir, 
                            datetime.today().strftime('tests_dd_%Y%m%d'))
    n = 1
    while os.path.exists(format_filename(filename, n)):
        n = n + 1
    filename = format_filename(filename, n)
    return filename


def get_fixtures_path(app_path):
    return os.path.join(app_path, 'fixtures')


def get_available_fixtures(app_path):
    fixtures_path = get_fixtures_path(app_path)
    if not os.path.exists(fixtures_path):
        os.mkdir(fixtures_path)
    available_fixtures = os.listdir(fixtures_path)
    available_fixtures.sort()
    return available_fixtures


def setup_logging(logfile):
    logging.basicConfig(level=logging.CRITICAL, filename="/dev/null")
    log = logging.getLogger('viewtester')
    [log.removeHandler(h) for h in log.handlers]
    log.setLevel(logging.INFO)
    handler = logging.FileHandler(logfile, 'a')
    handler.setFormatter(logging.Formatter('%(message)s'))
    log.addHandler(handler)
