import optparse
from xml.dom import minidom

import portdb
import query
from xmlobj import XMLResult

class CLI(optparse.OptionParser):
    def __init__(self):
        optparse.OptionParser.__init__(self)
        self.add_options()

    def add_options(self):
        for opt in self.OPTIONS:
            kwargs = opt[2]
            if kwargs.has_key('callback'):
                callback = kwargs['callback']
                if isinstance(callback,str):
                    kwargs['callback'] = getattr(self, callback)
            self.add_option(opt[0],opt[1],**opt[2])

class Action(XMLResult):
    def __init__(self, xmlcls):
        self.xmlcls = xmlcls

    def query(self):
        self.result = self.feed(self.xmlcls, minidom.parseString(self.read()))
        

class Index(Action, query.Index):
    def __init__(self, options):
        Action.__init__(self, portdb.XMLIndex)
        query.Index.__init__(self, options.url)

    def display(self):
        for repo in self.result:
            print repo.name
 
class Search(Action, query.Search):
    def __init__(self, options):
        Action.__init__(self, portdb.XMLPort)
        query.Search.__init__(self, options.url, options.query)

    def display(self):
        for port in self.result:
            print "[%s] %s" % (port.repo, port.name)

class Repo(Action, query.Repo):
    def __init__(self, options):
        Action.__init__(self, portdb.XMLPort)
        query.Repo.__init__(self, options.url, options.query)

    def display(self):
        for port in self.result:
            print port.name
    
class PDB(CLI):
    OPTIONS = [
        ['-a',
         '--action',
         { 'dest': 'action',
           'default': 'index',
           'help': 'specify the action to do on the portdb',
           'metavar':'TYPE',
           'type':'str',
           'action':'callback',
           'callback': 'set_action' }],
        ['-u',
         '--url',
         { 'dest': 'url',
           'default': 'http://crux.nu/~lucas/portdb/',
           'help': 'set the url of the portdb' }]]

    ACTIONS = {'index': Index, 'search': Search, 'repo': Repo}

    def run(self, args):
        self.parse_args(args)
        if self.largs:
            self.values.query = self.largs[0]
        action = self.ACTIONS[self.values.action](self.values)
        action.query()
        action.display()

    def set_action(self, option, opt_str, value, parser):
        if value not in self.ACTIONS.keys():
            raise optparse.OptionValueError, "invalid action '%s'" % value
        parser.values.action = value
