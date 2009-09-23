from django.utils import simplejson

class SimplePlugin(object):
    def __init__(self, name, page):
        """
        @param name - name of the placeholder
        @param page - microcms.models.Page instance
        """
        self.name = name
        self.page = page

    def render(self):
        """
        Render the plugin to html
        """
        return getattr(self.page, self.name, 'Edit me')
    
    def save_url(self):
        """
        Rreturn url to post the changes to
        """
        return '.'

    def options(self):
        """
        Returns options for jedtable
        """
        return simplejson.dumps({})

class RichPlugin(SimplePlugin):
    def options(self):
        return simplejson.dumps({ 'type' : 'wym',
                                  'submit' : 'OK',
                                  'cancel' : 'Cancel',
                                  'wym' : { 'basePath' : '123',
                                            'loadSkin' : False,
                                            'updateSelector' : 'button'}})
