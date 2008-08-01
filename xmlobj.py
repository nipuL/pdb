class AttributeAsNone(object):
    '''This class let's us handle attributes that might not exist.
The class returns a None object if the attribute is in ATTRS and
is not defined in the instance.'''
    ATTRS = []

    def __getattribute__(self, name):
        def getattr(name):
            return object.__getattribute__(self, name)

        if name in getattr("ATTRS"):
            try:
                return getattr(name)
            except AttributeError:
                return None
        return getattr(name)

class XMLObject(AttributeAsNone):
    '''Converts some XML into a Python object.
You can define how nodes are handled by defining methods with the form:

    def _process_NODENAME(self, node):
        ....
'''
    def __init__(self, node):
        for child in node.childNodes:
            getattr(self, '_process_%s' % child.nodeName,
                    self._process__)(child)
            self.ATTRS.append(child.nodeName)

    def _process__(self, node):
        setattr(self, node.nodeName, self.get_text(node.childNodes))

    def get_text(self, nodeList):
        rc = ''
        for node in nodeList:
            if node.nodeType == node.TEXT_NODE:
                rc += node.data
        return rc

class XMLResult(object):
    def feed(self, cls, node):
        '''Return a list of XMLObject based instances
Your XMLObjects will need to have a ROOT attribute which is the name
of the root node'''
        if node.nodeName != cls.ROOT:
            return [cls(el) for el in node.getElementsByTagName(cls.ROOT)]
        else:
            return cls(node)
