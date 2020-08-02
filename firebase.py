import pyrebase
from credentials.firebase_config import config

firebase = pyrebase.initialize_app(config)

# Get a reference to the auth service
auth = firebase.auth()

# Log the user in
token = auth.create_custom_token("kopi-chan-admin")
user = auth.sign_in_with_custom_token(token)

# Get a reference to the database service
db = firebase.database()


def PushData(data, dbName):
    results = db.child(dbName).push(data)


def QueryMenu():
    return db.child("menu").get().val().items()
