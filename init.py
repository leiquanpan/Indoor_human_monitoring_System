import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate('/home/ubuntu/json_file/bigbrother-187c7-firebase-adminsdk-kbahd-ca4e377409.json')
default_app = firebase_admin.initialize_app(cred)
