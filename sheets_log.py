import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
client = gspread.authorize(creds)

def insert_order(row):
  sheet = client.open('Order Records').worksheet("Orders")
  index = len(sheet.get_all_records()) + 2
  sheet.insert_row(row, index)

def insert_feedback(row):
  sheet = client.open('Order Records').worksheet("Feedbacks")
  index = len(sheet.get_all_records()) + 2
  sheet.insert_row(row, index)