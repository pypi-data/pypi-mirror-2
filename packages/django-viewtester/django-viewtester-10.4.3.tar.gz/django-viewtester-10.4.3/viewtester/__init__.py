
from django.contrib.auth.models import AnonymousUser

class AlreadyExists(Exception):
    pass

# Keep track of state
class ViewtesterState(object):
    app_label = ''
    app = None
    context = {}
    context_keys = []
    classname = ''
    class_list = []
    class_testlist = []
    fixtures_available = []
    fixtures_loaded = []
    initialised = False
    password = ''
    testname = ''
    user = AnonymousUser()
    view = ''

    def __setattr__(self, name, value):
        if name == 'classname':
            if value in self.class_list:
                raise AlreadyExists('Classname `%s` already exists' % value)
            self.class_list.append(value)
            # reset the list of tests in this class
            self.class_testlist = []
        if name == 'testname':
            if value in self.class_testlist:
                raise AlreadyExists('Testname `%s` already exists' % value)
            self.class_testlist.append(value)
        super(ViewtesterState, self).__setattr__(name, value)


viewtesterstate = ViewtesterState()
