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

today_menu = {
    0: 'Pour-over Coffee',
    1: 'Cold-brew Tea',
    2: 'Hot Tea',
    3: 'Matcha Latte',
}

suggested_donations = {
    'Pour-over Coffee': 1.70,
    'Black Coffee': 1.00,
    'Mocha': 1.50,
    'Cold-brew Coffee': 1.50,
    'Cold-brew Tea': 0.60,
    'Hot Tea': 0.50,
    'Thai Milk Tea': 1.00,
    'Matcha Latte': 1.50,
    'Brown Sugar Milk Tea': 1.80,
}

def updateMenu(suggested_donations, today_menu):
    db.child("menu").child("suggested_donations").update(suggested_donations)
    db.child("menu").child("today_menu").update(today_menu)

def pushData(data, dbName):
    results = db.child(dbName).push(data)

updateMenu(suggested_donations, today_menu)

menu_items = db.child("menu").child("today_menu").get().val()
suggested_donation = db.child("menu").child("suggested_donations").get().val()
