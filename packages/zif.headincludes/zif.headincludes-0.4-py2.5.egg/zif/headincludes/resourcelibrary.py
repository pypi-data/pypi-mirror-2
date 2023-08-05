# changed for using wsgi headincludes filter 7may06 jmw
# using utility 12may06 jmw

from zope.component import getUtility
from interfaces import IHeadIncludeRegistration

library_info = {}

class LibraryInfo(object):
    def __init__(self):
        self.included = []
        self.required = []

def _required(required_list, req):
    if req not in required_list:
        required_list.append(req)
        for r in getRequired(req):
            _required(required_list, r)

def need(library_name):
    registrar = getUtility(IHeadIncludeRegistration)
    if registrar:
        myList = []
        try:
            _required(myList, library_name)
        except KeyError:
            raise RuntimeError('Unknown resource library: %s' % library_name)
        myList.reverse()
        for lib in myList:
            included = getIncluded(lib)
            for file_name in included:
                url = '/@@/%s/%s' % (lib, file_name)
                registrar.register(url)

def getRequired(name):
    return library_info[name].required

def getIncluded(name):
    return library_info[name].included

# register cleanup with zope.testing if available
try:
    from zope.testing.cleanup import addCleanUp
except ImportError:
    pass
else:
    addCleanUp(lambda: library_info.clear())
    del addCleanUp
