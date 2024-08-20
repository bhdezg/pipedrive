# pipedrive

## Introduction
This Python script extracts deal data from Pipedrive CRM and exports it to a Google Sheet.
1. The script first sets up the Google Sheets credentials.
2. It then makes API calls to Pipedrive to fetch all deal data, paginating through the results.
3. The fetched data is cleaned and formatted using pandas.
4. Finally, the script connects to Google Sheets and exports the cleaned data.

## Setup
Google Sheets Credentials:

Obtain a [service account key file](https://developers.google.com/workspace/guides/create-credentials?hl=en) from the Google Cloud Console.
Save the key file as gs_cred.json.

Update Script:
- Replace YOUR_TOKEN with your actual pipedrive API token.
- Replace YOUR_BOOK with your Google Sheets document ID.
- Update the gs_cred dictionary with your Google service account credentials.
- Update the `gs_sheet` variable with the name of the sheet you want to update in your Google Sheets document.


## Requirements

1. Python 3.x installed on your system.
2. A service account key file
3. An account in https://www.pipedrive.com/
