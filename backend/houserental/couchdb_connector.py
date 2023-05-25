# connect to the couchdb
import couchdb
from django.conf import settings

admin = settings.COUCHDB_USER
password = settings.COUCHDB_PASSWORD


# def connect_to_db(db_name):
#     # send request to couchdb
#     url = f'http://{admin}:{password}@172.26.134.0:5984/'
#     couch = couchdb.Server(url)
#     db_name = db_name
#     if db_name not in couch:
#         db = couch.create(db_name)
#     else:
#         db = couch[db_name]
#     return db
def connect_to_db(db_name):
    cluster = couchdb.Cluster(['http://172.26.134.0:5984', 'http://172.26.136.55:5984'])
    db = cluster[db_name]
    return db
