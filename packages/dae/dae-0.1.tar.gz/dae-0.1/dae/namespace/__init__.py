import cherrypy
from hosts import HostsNamespace

cherrypy.config.namespaces['hosts'] = HostsNamespace.hosts_namespace