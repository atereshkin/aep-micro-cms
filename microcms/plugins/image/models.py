from google.appengine.ext import db


class Image(db.Model):
    data = db.BlobProperty(default=None)
