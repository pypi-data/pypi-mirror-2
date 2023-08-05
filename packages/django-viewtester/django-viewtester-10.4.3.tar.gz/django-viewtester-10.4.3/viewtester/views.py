import os
import logging
import sys

from django.contrib.auth.models import AnonymousUser
from django.core.management import call_command
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.template import Context
from django.template.loader import render_to_string

from viewtester import viewtesterstate, AlreadyExists
from viewtester.utils import safe_dict, get_fixtures_path

def get_viewtester_div():
    return render_to_string('viewtester/div.html', 
                            {'viewtesterstate': viewtesterstate})


def flush_and_load():
    call_command('flush', verbosity=0, interactive=False)
    if viewtesterstate.fixtures_loaded:
        fixtures = [f.strip() for f in viewtesterstate.fixtures_loaded]
        call_command('loaddata', *fixtures, **{'verbosity': 0})
    

def newtest(request):
    testname = request.POST.get('testname', None)
    if not testname:
        return HttpResponseBadRequest('Missing testname')
    try:
        viewtesterstate.testname = testname
    except AlreadyExists, e:
        return HttpResponseBadRequest(e.message)
    # With each new test the client is no longer logged in
    # TODO: add option to 'remain' logged in
    viewtesterstate.user = AnonymousUser()
    log = logging.getLogger('viewtester')

    if not testname.startswith('test'):
        testname = 'test_'+testname
    context = Context(safe_dict({
                'testname': testname,
                }))
    log.info(render_to_string('viewtester/test.txt', context).rstrip())
    # With each new test-method the db is flushed and any fixtures are loaded
    flush_and_load()
    
    if request.is_ajax():
        return HttpResponse(get_viewtester_div())
    else:
        referer = request.META.get('HTTP_REFERER', '')
        return HttpResponseRedirect(referer)


def newclass(request):
    classname = request.POST.get('classname', None)
    if not classname:
        return HttpResponseBadRequest('Missing classname')
    try:
        viewtesterstate.classname = classname
    except AlreadyExists, e:
        return HttpResponseBadRequest(e.message)
    # With each new test the client is no longer logged in
    # TODO: add option to 'remain' logged in
    viewtesterstate.user = AnonymousUser()
    fixtures = request.POST.getlist('fixtures')
    viewtesterstate.fixtures_loaded = fixtures
    flush_and_load()
    log = logging.getLogger('viewtester')
    context = Context({
                'classname': classname,
                'fixtures': fixtures,
                })
    log.info(render_to_string('viewtester/class.txt', context).rstrip())
    if request.is_ajax():
        return HttpResponse(get_viewtester_div())
    else:
        referer = request.META.get('HTTP_REFERER', '')
        return HttpResponseRedirect(referer)


def savefixture(request):
    fixture = request.POST.get('fixture', None)
    if not fixture:
        return HttpResponseBadRequest('Missing fixturename')

    fixture_path = get_fixtures_path(viewtesterstate.app_path)
    fixture_path = os.path.join(fixture_path, fixture)

    # use the extension to determine the format
    _, ext = os.path.splitext(fixture_path)
    if ext:
        format = ext[1:]
    else:
        format = None

    if not format in ('json', 'xml'):
        return HttpResponseBadRequest(
            "Invalid fixfure format. Expecting 'json' or 'xml'.")

    if os.path.exists(fixture_path):
        return HttpResponseBadRequest(
            "Fixture already exists.")

    # Now actually save the fixture. Thanks go out to:
    # http://www.chrisdpratt.com/2008/02/27/a-django-snippet-to-refresh-your-database/
    sys.stdout = open(fixture_path, "wb")
    call_command('dumpdata', viewtesterstate.app_label, format=format,
                 indent=2, verbosity=0, interactive=False)
    sys.stdout.close()
    # reset stdout to its default
    sys.stdout = sys.__stdout__

    viewtesterstate.fixtures_available.append(os.path.split(fixture_path)[1])
    if request.is_ajax():
        return HttpResponse(get_viewtester_div())
    else:
        referer = request.META.get('HTTP_REFERER', '')
        return HttpResponseRedirect(referer)

def assertequal(request):
    keys = request.POST.getlist('keys')
    log = logging.getLogger('viewtester')
    for key in keys:
        try:
            value = viewtesterstate.context[key]
            log.info(render_to_string('viewtester/context.txt', 
                                      safe_dict({'key': key, 
                                                 'value': value})).rstrip())
        except KeyError:
            # The viewtesterstate.context isn't updated for posts so
            # it can become outdated (especially with 'ajax' views)
            return HttpResponseBadRequest(
                "'%s' does not exist in *current* context. " \
                    "The context *isn't* updated for POST-requests.")
    if request.is_ajax():
        return HttpResponse(get_viewtester_div())
    else:
        referer = request.META.get('HTTP_REFERER', '')
        return HttpResponseRedirect(referer)
