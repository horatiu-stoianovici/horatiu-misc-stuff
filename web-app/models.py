from google.appengine.ext import ndb

class MiscData(ndb.Model):
    key = ndb.StringProperty(indexed=True)
    value = ndb.StringProperty(indexed=False)
    date = ndb.DateTimeProperty(indexed=False,auto_now=True)