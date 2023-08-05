import cherrypy
from .. import toolbox

class HostsNamespace(object):
    apps = {}
    domains = {}
    default = None
    vhost = None

    @classmethod
    def hosts_namespace(self, k, v):
        if k == 'apps':
            self.apps.update(v)
            self.load_all()

    @classmethod
    def load_all(self):
        for name, config in self.apps.items():
            if config.get('on', False):
                apps = __import__('apps.%s' % name)
                domain = config.get('domain', None)
                if domain is not None:
                    conf = config.get('conf', {})
                    self.domains[domain] = dm = cherrypy.Application(\
                        getattr(apps, name).controllers.Root(), config=conf)
                    if config.get('default', False):
                        self.default = dm
                    dm.toolboxes.update(toolbox.toolboxes)
        self.vhost = cherrypy._cpwsgi.VirtualHost(self.default, \
            domains=self.domains)
        cherrypy.tree.graft(self.vhost)
    
    @classmethod
    def refresh_all(self):
        pass
