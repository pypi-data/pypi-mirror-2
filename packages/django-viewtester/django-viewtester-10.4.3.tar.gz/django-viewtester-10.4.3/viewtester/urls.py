from django.conf.urls.defaults import *

urlpatterns = patterns('',
                       url(r'^newtest/$',
                           'viewtester.views.newtest',
                           name='viewtester_newtest'),
                       url(r'^newclass/$',
                           'viewtester.views.newclass',
                           name='viewtester_newclass'),
                       url(r'^savefixture/$',
                           'viewtester.views.savefixture',
                           name='viewtester_savefixture'),
                       url(r'^assertequal/$',
                           'viewtester.views.assertequal',
                           name='viewtester_assertequal'),
                       )
