import os
import sys

dirname = os.path.dirname(__file__)

for testfile in os.listdir(dirname):
    testname, ext = os.path.splitext(testfile)
    if ext=='.py' and testname != "__init__":
        classnames = []
        fp = open(os.path.join(dirname, testfile), "rb")
        # TODO: just import?
        for line in fp:
            if line.startswith('class ') and line.rstrip().endswith('(TestCase):'):
                classname = line[6:line.find('(')]
                classnames.append(classname)
        fp.close()
        testmodule = '%s.%s' % (__name__, testname)
        _testmod = __import__(testmodule, fromlist=classnames)
        self = sys.modules[__name__]
        for classname in classnames:
            myclassname = classname
            while getattr(self, myclassname, None):
                myclassname = myclassname + "_"
            setattr(self, myclassname, getattr(_testmod, classname))
