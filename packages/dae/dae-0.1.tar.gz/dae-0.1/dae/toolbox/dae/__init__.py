# -*- coding: utf-8 -*-
import cherrypy
daetoolbox = _d = cherrypy._cptools.Toolbox('dae')

from . import lxmlext
from . import publisher
publisher.Publisher.lxmlext = lxmlext.extensions
_d.publisher = publisher.Publisher()

from . import sqla
_d.sqla = sqla.SQLA()

from . import auth # depends on sqla tool
_d.auth = cherrypy.Tool('before_handler', auth.auth, priority=1)

from . import mongo
_d.mongo = mongo.Mongo()