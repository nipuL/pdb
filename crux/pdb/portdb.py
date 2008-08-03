from xmlobj import XMLObject, XMLResult

class XMLIndex(XMLObject):
    ROOT = "repo"
    ATTRS = ["name", "maintainer", "type", "url", "ports"]

class XMLFiles(XMLObject):
    ROOT = "files"
    ATTRS = ["pkgfile", "footprint", "md5sum"]

class XMLPort(XMLObject):
    ROOT = "port"
    ATTRS = ["name", "repo", "command", "files"]

    def _process_files(self, node):
        self.files = XMLResult().feed(XMLFiles, node)

    
