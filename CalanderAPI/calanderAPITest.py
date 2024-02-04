import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]

def write_file(data):
  with open('events.txt','a+') as file:
    file.write(data)

'''
RUN ONLY IN COLAB 

from google.colab import drive
from google.colab import files

# Mount Google Drive to Colab
drive.mount('/content/gdrive')

# Define the local file path
local_file_path = 'path/to/your/local/file.txt'

# Define the destination folder and file name on Google Drive
drive_folder = '/content/gdrive/My Drive/'
drive_file_name = 'uploaded_file.txt'

# Copy the local file to Google Drive
!cp "{local_file_path}" "{drive_folder}{drive_file_name}"
'''

def main():

  creds = None
   
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "./Config/credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  try:
    service = build("calendar", "v3", credentials=creds)

    now = datetime.datetime.utcnow().isoformat() + "Z"  
    print("Getting the upcoming 10 events")
    events_result = (
        service.events()
        .list(
            calendarId="primary",
            timeMin=now,
            maxResults=10,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )
    events = events_result.get("items", [])

    if not events:
      print("No upcoming events found.")
      return

    for event in events:
      start = event["start"].get("dateTime", event["start"].get("date"))
      print(start, event["summary"])
      
      filestream = start+event['summary']+"\n"
      write_file(filestream)
  
  except HttpError as error:
    print(f"An error occurred: {error}")


if __name__ == "__main__":
  main()