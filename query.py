import urllib

class Request(object):
    def __init__(self, url, parameters):
        self.parameters = {'f':'xml'}
        self.parameters.update(parameters)
        self.url = url

    def read(self):
        return urllib.urlopen('?'.join((
                    self.url,
                    urllib.urlencode(self.parameters)
                    ))).read()

class Index(Request):
    def __init__(self, url):
        super(Index, self).__init__(url, {'a':'index'})

class Repo(Request):
    def __init__(self, url, repo):
        super(Repo, self).__init__(url, {'a':'repo', 'q':repo})

class Search(Request):
    def __init__(self, url, query, strict=False):
        super(Search, self).__init__(url, {'a':'search', 'q':query})
        if strict:
            self.parameters.update({'strict':'true'})
