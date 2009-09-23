from google.appengine.ext import db


class Image(db.Model):
    """
    DB storage for images
    """
    data = db.BlobProperty(default=None)
