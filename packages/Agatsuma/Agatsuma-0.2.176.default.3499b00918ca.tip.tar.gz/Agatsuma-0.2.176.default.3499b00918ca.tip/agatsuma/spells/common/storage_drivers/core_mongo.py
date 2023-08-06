from agatsuma.core import Core
if Core.internal_state.get("mode", None) == "normal":
    import pymongo

import re

from agatsuma import log
from agatsuma import Settings

from agatsuma.interfaces import AbstractSpell, IInternalSpell
from agatsuma.interfaces import IStorageSpell, ISetupSpell

from agatsuma.commons.types import Atom

class MongoDBSpell(AbstractSpell, IInternalSpell, IStorageSpell, ISetupSpell):
    def __init__(self):
        config = {'info' : 'MongoDB support',
                  'deps' : (),
                  'provides': (Atom.storage_driver, ),
                 }
        AbstractSpell.__init__(self, Atom.agatsuma_mongodb, config)

    def pre_configure(self, core):
        core.register_option("!mongo.uri", unicode, "MongoDB host URI")
        core.register_option("!mongo.db_collections", list, "MongoDB databases to use")

    def post_configure(self, core):
        self.init_connection()

    def init_connection(self):
        log.storage.info("Initializing MongoDB connections on URI '%s'" % Settings.mongo.uri)
        connData = MongoDBSpell._parse_mongo_uri(Settings.mongo.uri)
        self.connection = pymongo.Connection(connData[0], connData[1])
        for dbCollectionName in Settings.mongo.db_collections:
            # TODO: XXX: why unicode only?
            #assert type(dbCollectionName) is unicode
            setattr(self, dbCollectionName, self.connection[dbCollectionName])

    @staticmethod
    def _parse_mongo_uri(uri):
        # mongodb://host:port
        match = re.match(r'^mongodb://([\S|\.]+?)?(?::(\d+))?$', uri)
        if match.group(2):
            return  match.group(1), int(match.group(2)) # host, port
        return  match.group(1), None

    def requirements(self):
        return {"mongo" : ["pymongo>=0.6"],
               }
