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


def pushData(data, dbName):
    results = db.child(dbName).push(data)


def updateMenu(all_menu, menu_prices, today_menu):
    db.child("menu").child("all_menu").update(all_menu)
    db.child("menu").child("menu_prices").update(menu_prices)
    db.child("menu").child("today_menu").update(today_menu)


def getTodayMenu():
    today_menu = db.child("menu").child("today_menu").get()
    return today_menu.val()
