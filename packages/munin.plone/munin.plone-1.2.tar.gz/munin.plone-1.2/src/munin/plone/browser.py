from Products.Five.browser import BrowserView
from logging import getLogger
from time import time
from DateTime import DateTime

log = getLogger('munin.plone').info

def timer(fn):
    def decorator(*args, **kw):
        start = time()
        value = fn(*args, **kw)
        elapsed = time() - start
        if elapsed > 0.1:   # only log when execution took more than 100ms
            log('calling %s took %.3fs', fn.__name__, elapsed)
        return value
    decorator.__doc__ = fn.__doc__
    decorator.__name__ = fn.__name__
    return decorator


class Munin(BrowserView):

    @timer
    def contentcreation(self):
        """ content creation statistics """
        result = []
        pc = self.context.portal_catalog
        result.append('content_created:%.1f' % len(pc(created={'query': [DateTime() - (1.0/(24*60/5)),DateTime()], 'range': 'minmax' })))
        result.append('content_modified:%.1f' % len(pc(modified={'query': [DateTime() - (1.0/(24*60/5)),DateTime()], 'range': 'minmax' })))
        return '\n'.join(result)



