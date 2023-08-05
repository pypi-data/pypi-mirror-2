# -*- coding: utf-8 -*-
import pymongo
from pymongo import Connection
from pymongo.son_manipulator import AutoReference, NamespaceInjector
import cherrypy

conn = Connection()

class Mongo(cherrypy.Tool):
    _name = 'mongo'
    _db = {}

    def __init__(self):
        pass
    
    def _setup(self):
        pass
    
    @property
    def models(self):
        conf = self._merged_args()
        db = self._db.get(conf['db'], None)
        if db is None:
            self._db[conf['db']] = db = getattr(conn, conf['db'])
            db.add_son_manipulator(NamespaceInjector())
            db.add_son_manipulator(AutoReference(db))
        return db