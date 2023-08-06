import datetime, yaml

import couchdbkit as couch
from couchdbkit.loaders import FileSystemDocsLoader

from vogeler.exceptions import VogelerPersistenceException

class SystemRecord(couch.Document):
    system_name = couch.StringProperty()
    created_at = couch.DateTimeProperty()
    updated_at = couch.DateTimeProperty()

class VogelerStore(object):

    def __init__(self, **kwargs):
        try:
            host, port = kwargs['host'], kwargs['port']
            db = kwargs['db']
            connection_string = "http://%s:%s" % (host, port)
            self.server = couch.Server(uri=connection_string)
            self.dbname = db
        except:
            raise

    def create_db(self, dbname=''):
        try:
            if dbname == '':
                dbname = self.dbname

            self.db = self.server.get_or_create_db(dbname)
            SystemRecord.set_db(self.db)
        except:
            raise

    def drop_db(self, dbname=''):
        try:
            if dbname == '':
                dbname = self.dbname

            self.server.delete_db(dbname)
        except:
            raise

    def use_db(self, dbname=''):
        try:
            if dbname == '':
                dbname = self.dbname

            self.db = self.server.get_or_create_db(dbname)
            SystemRecord.set_db(self.db)
        except:
            raise

    def create(self, node_name):
        try:
            node = SystemRecord.get_or_create(node_name)
            node.system_name = node_name
            node.created_at = datetime.datetime.utcnow()
            node.save()
        except:
            raise

    def get(self, node_name):
        try:
            node = SystemRecord.get(node_name)
            self.node = node
            return node
        except:
            raise

    def touch(self, node_name):
        try:
            node = SystemRecord.get(node_name)
            node.updated_at = datetime.datetime.utcnow()
            node.save()
        except:
            raise

    def update(self, node_name, key, value, datatype):
        node = SystemRecord.get_or_create(node_name)

        if datatype == 'output':
            v = [z.strip() for z in value.split("\n")]
            node[key] = v
        if datatype == 'pylist':
            v = value
            node[key] = v
        if datatype == 'pydict':
            v = value
            node[key] = v
        if datatype == 'yaml':
            v = yaml.load(value)
            node[key] = v
        if datatype == 'string':
            v = value
            node[key] = v
        if datatype == 'raw':
            v = value
            node[key] = v
        node.updated_at = datetime.datetime.utcnow()
        node.save()

    def load_views(self, lp):
        self.loadpath = lp
        try:
            print "Loading design docs from %s" % lp
            loader = FileSystemDocsLoader(self.loadpath)
            loader.sync(self.db, verbose=True)
            print "Design docs loaded"
            return 0
        except:
            raise VogelerPersistenceException("Document load path not found: %s" % lp)

# vim: set ts=4 et sw=4 sts=4 sta filetype=python :
