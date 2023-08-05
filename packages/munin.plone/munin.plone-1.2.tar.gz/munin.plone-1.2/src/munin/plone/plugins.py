from gocept.munin.client import SimpleMultiGraph, main
from os.path import isdir, basename, abspath, normpath, join, exists
from os import environ, getcwd, symlink
from inspect import isclass
from socket import gethostname
from sys import argv

class contentcreation(SimpleMultiGraph):
    keys = ['content_created', 'content_modified']
    names = ['content_created', 'content_modified']
    title = 'Plone content creation'
    category = 'Zope'
    scales = {'min': 0, 'max': 20}

    def config(self):
        print "graph_title %s (%s)" % (self.title, self.index)
        print "graph_vlabel %s" % (self.vlabel)
        print "graph_category %s" % self.category
        print "graph_info %s (%s) " % (self.title, self.index)
        print "graph_args -l %s -u %s --rigid" % (self.scales['min'], self.scales['max'])

        for name in self.names:
            print "%s.label %s" % (name, name)
            print "%s.min %s" % (name, self.scales['min'])
            print "%s.max %s" % (name, self.scales['max'])

def install(script, cmd, path, prefix=None, suffix=None):
    """ set up plugin symlinks using the given prexix/suffix or the
        current hostname and directory """
    assert isdir(path), 'please specify an existing directory'
    if prefix is None:
        prefix = gethostname()
    if suffix is None:
        suffix = basename(getcwd())
    source = abspath(script)
    for name, value in globals().items():
        if isclass(value) and value.__module__ == __name__:
            plugin = '_'.join((prefix, name, suffix))
            target = normpath(join(path, plugin))
            if not exists(target):
                symlink(source, target)
                print 'installed symlink %s' % target
            else:
                print 'skipped existing %s' % target


def run(ip_address='localhost', http_address=8080, port_base=0, user=None, plone='plone'):
    if 3 <= len(argv) <= 5 and argv[1] == 'install':
        return install(*argv)
    if not 'URL' in environ:
        port = int(http_address) + int(port_base)
        host = '%s:%d' % (ip_address, port)
        environ['URL'] = 'http://%s/%s/@@munin.plone.plugins/%%s' % (host,plone)
    if not 'AUTH' in environ and user is not None:
        environ['AUTH'] = user
    main()
