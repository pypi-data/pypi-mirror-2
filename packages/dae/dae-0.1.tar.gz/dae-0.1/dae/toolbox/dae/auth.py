# -*- coding: utf-8 -*-
import cherrypy
import urllib
import re

p = re.compile('(?<=\ ).*(?=\ )')
def get_request_line():
    return p.search(cherrypy.request.request_line).group(0)

def auth(redirect='/users', redirect_type='external'):
    if not cherrypy.session.get('auth'):
        redirect += '/login?redirect='+urllib.quote_plus(get_request_line())
        if redirect_type == 'internal':
            raise cherrypy.InternalRedirect(cherrypy.url(redirect))
        elif redirect_type == 'external':
            raise cherrypy.HTTPRedirect(cherrypy.url(redirect))

