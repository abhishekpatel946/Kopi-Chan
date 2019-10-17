import pyrebase

config = {
    "apiKey": "AIzaSyB3uWHGYINp6J6P2f-R-vYpM89kQorb_Uo",
    "authDomain": "uscaffeinatedbot.firebaseapp.com",
    "databaseURL": "https://uscaffeinatedbot.firebaseio.com/",
    "storageBucket": "uscaffeinatedbot.appspot.com",
    "serviceAccount": "./uscaffeinatedbot-firebase-adminsdk-3awke-82b73b167b.json"
}

firebase = pyrebase.initialize_app(config)

# Get a reference to the auth service
auth = firebase.auth()

# Log the user in
token = auth.create_custom_token("kopi-chan-admin")
user = auth.sign_in_with_custom_token(token)

# Get a reference to the database service
db = firebase.database()

menu = {
    'Pour-over Coffee': {
        'name': 'Pour-over Coffee',
        'serving': True,
        'recommended_dontation': 1.70
    },
    'French Press Coffee - Black': {
        'name': 'French Press Coffee - Black',
        'serving': False,
        'recommended_dontation': 1.00
    },
    'French Press Coffee - Mocha': {
        'name': 'French Press Coffee - Mocha',
        'serving': False,
        'recommended_dontation': 1.50
    },
    'Cold-brew Coffee': {
        'name': 'Cold-brew Coffee',
        'serving': False,
        'recommended_dontation': 1.00
    },
    'Cold-brew Tea': {
        'name': 'Cold-brew Tea',
        'serving': True,
        'recommended_dontation': 0.60
    },
    'Hot Tea': {
        'name': 'Hot Tea',
        'serving': True,
        'recommended_dontation': 0.50
    },
    'Thai Milk Tea': {
        'name': 'Thai Milk Tea',
        'serving': False,
        'recommended_dontation': 1.00
    },
    'Matcha Latte': {
        'name': 'Matcha Latte',
        'serving': True,
        'recommended_dontation': 1.50
    },
    'Brown Sugar Milk Tea': {
        'name': 'Brown Sugar Milk Tea',
        'serving': False,
        'recommended_dontation': 1.50
    },
    'Vietnamese Coffee': {
        'name': 'Vietnamese Coffee',
        'serving': False,
        'recommended_dontation': 1.50
    }
}


def pushData(data, dbName):
    results = db.child(dbName).push(data)

# db.child("menu").update(menu)

