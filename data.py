import requests
import json
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from google.colab import files
import numpy as np

gs_cred = {
  "type": "service_account",
  "project_id": "",
  "private_key_id": "",
  "private_key": "",
  "client_email": "",
  "client_id": "",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "",
  "client_x509_cert_url": ""
}

with open('gs_cred.json', 'w') as outfile:
    json.dump(gs_cred, outfile)

#EXTRACT DEALS DATA FROM PIPEDRIVE CRM
more = True
start = 0
full_res = []

while more == True:
  url = "https://api.pipedrive.com/v1/deals?api_token='YOUR_TOKEN'&start="+str(start)

  payload={}
  headers = {
    'Accept': 'application/json'
  }

  response = requests.request("GET", url, headers=headers, data=payload)
  r1 = json.loads(response.text.encode('utf8'))
  full_res.extend(r1['data'])
  more = r1['additional_data']['pagination']['more_items_in_collection']
  if more == True:
    start = r1['additional_data']['pagination']['next_start']
  else:
    print('End')
    break
  print(start, more)

#CLEAN IT TO BE EXPORTABLE TO A GOOGLE SHEET
data1 = pd.DataFrame(full_res)
j1 = data1.to_json(orient="records")
j2 = json.loads(j1)
data2 = pd.json_normalize(j2)
data2 = data2.drop(columns=['person_id.phone','person_id.email'])
data2 = data2.fillna('')

file = r'gs_cred.json'
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name(file, scope)
client = gspread.authorize(creds)

#EXPORT DATA TO A GOOGLE SHEETS
gs_book='YOUR_BOOK'
gs_url = 'https://docs.google.com/spreadsheets/d/'+gs_book+'/edit'
gs_sheet = 'data'

sheet = client.open_by_url(gs_url).worksheet(gs_sheet)
sheet.clear()
sheet.insert_rows([data2.columns.values.tolist()],row=1, value_input_option='RAW')
sheet.insert_rows(data2.values.tolist(),row=2, value_input_option='RAW')
