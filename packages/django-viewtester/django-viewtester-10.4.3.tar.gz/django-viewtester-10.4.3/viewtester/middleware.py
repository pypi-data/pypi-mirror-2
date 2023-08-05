import imp
import logging

from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.core import urlresolvers
from django.template import Template, Context
from django.template.loader import render_to_string
from django.test.client import Client
from django.test.utils import setup_test_environment
from django.utils.encoding import smart_unicode

from utils import safe_dict

from viewtester import viewtesterstate
from viewtester.views import get_viewtester_div

_HTML_TYPES = ('text/html', 'application/xhtml+xml')

VIEWTESTER_DISCARD_CONTEXT_KEYS = getattr(
    settings, 'VIEWTESTER_DISCARD_CONTEXT_KEYS', ['LANGUAGES',
                                                 'LANGUAGE_BIDI',
                                                 'LANGUAGE_CODE'])


def replace_insensitive(string, target, replacement):
    """
    Similar to string.replace() but is case insensitive
    Code borrowed from: http://forums.devshed.com/python-programming-11/case-insensitive-string-replace-490921.html
    """
    no_case = string.lower()
    index = no_case.rfind(target.lower())
    if index >= 0:
        return string[:index] + replacement + string[index + len(target):]
    else: # no results so return the original string
        return string


class Viewtester(object):
    
    def __init__(self):
        self.log = logging.getLogger('viewtester')
        if not viewtesterstate.initialised:
            viewtesterstate.classname = 'ViewtesterStart'
            viewtesterstate.testname = 'test_start'
            self.log.info(render_to_string('viewtester/boilerplate.txt').rstrip())
            context = Context({
                    'classname': viewtesterstate.classname,
                    'fixtures': viewtesterstate.fixtures_loaded,
                    })
            self.log.info(render_to_string('viewtester/class.txt', context).rstrip())
        viewtesterstate.initialised = True

    def _get_context_keys(self, context):
        """Get the keys from the (possible nested) context(s)"""
        keys = []
        for d in context.dicts:
            if isinstance(d, Context):
                keys += self._get_context_keys(d)
            else:
                keys += d.keys()
        return keys

    def _log_context(self, context):
        keys = []
        if isinstance(context, list):
            for c in context:
                keys += self._get_context_keys(c)
        else:
            keys = self._get_context_keys(context)

        keys = set(keys)

        # Skip some keys
        for discardkey in VIEWTESTER_DISCARD_CONTEXT_KEYS:
            keys.discard(discardkey)

        keys = list(keys)
        keys.sort()

        viewtesterstate.context = context
        viewtesterstate.context_keys = keys

    def _log_request(self, request):
        method = request.method.lower()
        request_str = "'%s', {" % request.path
        for dikt in request.REQUEST.dicts:
            for arg in dikt:
                request_str += "'%s': '%s', " % (arg, request.REQUEST[arg])
        request_str += "}"
        context = {
            'method': method,
            'request_str': request_str,
        }
        context = Context(safe_dict(context))
        self.log.info(render_to_string('viewtester/request.txt', context).rstrip())

    def _log_status(self, response):
        context = {
            'status_code': response.status_code,
        }
        context = Context(safe_dict(context))
        self.log.info(render_to_string('viewtester/status.txt', context).rstrip())

    def _should_process(self, request):
        # is the callback function in the current app?
        try:
            callback, callback_args, callback_kwargs = urlresolvers.resolve(
                request.path_info)
        except urlresolvers.Resolver404:
            return False

        if 'test_client_true' in request.REQUEST:
            return False

        return callback in viewtesterstate.app_views.__dict__.values()

    def process_request(self, request):
        if not self._should_process(request):
            return
        self._log_request(request)

    def process_response(self, request, response):

        # Check for login/logout
        lastuser = viewtesterstate.user

        # When the db is new/recreated there is no request.session
        # (and therefore no request.user)
        try:
            req_user = request.user
        except AttributeError:
            req_user = AnonymousUser()

        if lastuser != req_user:
            viewtesterstate.user = req_user
            if req_user.is_anonymous():
                self.log.info(render_to_string('viewtester/logout.txt').rstrip())
            else:
                viewtesterstate.password = request.POST['password']
                context = Context(safe_dict({
                            'username': req_user.username,
                            'password': viewtesterstate.password,
                            }))
                self.log.info(render_to_string('viewtester/login.txt',
                                               context).rstrip())

        if not self._should_process(request):
            return response

        self._log_status(response)
        
        # For GET-requests, do the get and get the context. See
        # test_utils.viewtester.middleware
        if request.method == "GET":
            # The setup_test_environment is *required* (to listen to the
            # template_rendered signal and get the context)
            setup_test_environment()
            c = Client()
            if not req_user.is_anonymous():
                assert c.login(username=viewtesterstate.user.username, 
                               password=viewtesterstate.password)
            getdict = request.GET.copy()
            getdict['test_client_true'] = 'yes' #avoid recursion
            test_response = c.get(request.path, getdict)
            context = test_response.context
            if context and test_response.status_code != 404:
                self._log_context(context)

        # do not inject the div in ajax-calls. It's very confusing...
        if request.is_ajax():
            return response

        # inject viewtester-div and -extrahead
        extrahead = render_to_string('viewtester/extrahead.html')

        # Credits for this bit: django-debug-toolbar. Thanks!
        if response['Content-Type'].split(';')[0] in _HTML_TYPES:
            response.content = replace_insensitive(
                smart_unicode(response.content), 
                u'</head>', 
                extrahead + u'</head>')
            response.content = replace_insensitive(
                smart_unicode(response.content), 
                u'</body>', 
                get_viewtester_div() + u'</body>')

        return response
