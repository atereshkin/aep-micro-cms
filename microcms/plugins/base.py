from django.utils import simplejson

class SimplePlugin(object):
    def __init__(self, name, page):
        """
        @param name - name of the placeholder
        """
        self.name = name
        self.page = page

    def render(self):
        return getattr(self.page, self.name, 'Edit me')
    
    def save_url(self):
        return '.'

    def options(self):
        return simplejson.dumps({})

class RichPlugin(SimplePlugin):
    def options(self):
        return simplejson.dumps({ 'type' : 'wym',
                                  'submit' : 'OK',
                                  'cancel' : 'Cancel',
                                  'wym' : { 'basePath' : '123',
                                            'loadSkin' : False,
                                            'updateSelector' : 'button'}})
