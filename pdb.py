#!/usr/bin/env python
import optparse
import sys
from xml.dom import minidom

from crux.pdb import portdb, query
from crux.pdb.xmlobj import XMLResult

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
        self.options = options

    def display(self):
        for repo in self.result:
            if not self.options.repo or repo.name in self.options.repo:
                if not self.options.info:
                    self.options.info = ["name"]
                for field in self.options.info:
                    print getattr(repo, field),
                print
 
class Search(Action, query.Search):
    def __init__(self, options):
        Action.__init__(self, portdb.XMLPort)
        query.Search.__init__(self, options.url, options.query, options.strict)
        self.options = options

    def display(self):
        for port in self.result:
            if not self.options.repo or port.repo in self.options.repo:
                if not self.options.info:
                    self.options.info = ["name"]
                for field in self.options.info:
                    print getattr(port, field),
                print

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
         { 'default': 'index',
           'help': 'specify the action to do on the portdb',
           'type': 'str',
           'action':'callback',
           'callback': 'set_action' }],
        ['-u',
         '--url',
         { 'default': 'http://crux.nu/~lucas/portdb/',
           'help': 'set the url of the portdb' }],
        ['-i',
         '--info',
         { 'help': 'print extended information',
           'type': 'str',
           'action': 'callback',
           'callback': 'varargs' }],
        ['-r',
         '--repo',
         { 'help': 'only display from given repos',
           'type': 'str',
           'action': 'callback',
           'callback': 'varargs'}],
        ['-s',
         '--strict',
         { 'default': False,
           'action': 'store_true',
           'help': 'perform a strict search (only for search action)' }]]

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

    def varargs(self, option, opt_str, value, parser):
        value = [value]
        rargs = parser.rargs
        while rargs:
            arg = rargs[0]
            if ((arg[:2] == "--" and len(arg) > 2) or
                (arg[:1] == "-" and len(arg) > 1 and arg[1] != "-")):
                break
            else:
                value.append(arg)
                del rargs[0]
        setattr(parser.values, option.dest, value)
 
def main():
    PDB().run(sys.argv[1:])

if __name__ == '__main__':
    sys.exit(main())
