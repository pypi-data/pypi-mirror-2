import urlparse
import vogeler.db.couch as couch

from vogeler.exceptions import VogelerPersistenceException

"""
vogeler.persisistence is used like so:

>>> import vogeler.persistence as engine
>>> c = engine.create_engine('couch://127.0.0.1:5984/system_records')
>>> c.create_db()
>>> c.create('nodename')
>>> package_list = some_shell_command_output
>>> c.update('nodename', 'packages', 'package_list', 'output')
>>> mylist = ['foo','bar','baz']
>>> c.update('nodename', 'my_python_list', mylist, 'pylist')
>>> mydict = {'foo' : 1, 'bar' : 2, 'baz' : 'shoe'}
>>> c.update('nodename', 'my_python_dict', mydict, 'pydict')
>>> myyaml = some_yaml_data
>>> c.update('nodename', 'my_yaml_data', myyaml, 'yaml')
>>> c.update('nodename', 'my_string', 'some sting data', 'string')
>>> myxml = some_xml_data
>>> c.update('nodename', 'my_raw_data', myxml, 'raw')
>>> myjson = some_json_data
>>> c.update('nodename', 'my_json_data', myjson, 'json')
>>> c.drop_db()
"""
def create_engine(dsn):
    """
    Create a connection to a persistence backend.

    :param string dsn: A :class:`urlparse` parseable url defining a persistence backend

        e.g. `couch://127.0.0.1:5984/system_records`

    :returns: engine. instance of :class:`VogelerPersistence`

    """
    try:
        scheme, params = _parse_url(dsn)
        connect_string = "%s.VogelerStore(%s)" % (scheme, params)
        engine = eval(connect_string)
        return engine
    except:
        raise VogelerPersistenceException("Unable to connect to backend database: %s" % connect_string)

def _parse_url(url):
    parsed = urlparse.urlparse(url)
    s = parsed.scheme
    h, p = parsed.netloc.split(':')
    d = parsed.path.split("/")[1]
    params = "host='%s', port='%s', db='%s'" % (h, p, d)
    return (s, params)

# vim: set ts=4 et sw=4 sts=4 sta filetype=python :
