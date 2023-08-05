# -*- coding: utf-8 -*-
import cherrypy

import toolbox
import namespace

import apps

import os
loc = os.getcwd()

# TODO find a better place for this
import daml
###


def session(name):
    """
    use in app.conf to specify file-based session location, ie:
    
        tools.sessions.storage_type = 'file'
        tools.sessions.storage_path = main.session('app_name')
    """
    s = os.path.join(loc, 'sessions', name)
    not os.path.isdir(s) and os.makedirs(s)
    return s

toolbox.dae.sqla.create_all()

