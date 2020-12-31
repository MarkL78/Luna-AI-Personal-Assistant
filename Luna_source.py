from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
import time
import pyttsx3
import speech_recognition as sr
import pytz

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
DAYS = ["monday", "tuesday", " wednesday", "thursday", "friday","saturday", "sunday"]
MONTHS = ["january", "feburary", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"]
DAY_EXTENTIONS = ["rd", "th", "st", "nd"]

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runandwait()
    #need to slow the voice down

def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        said = ""

        try:
            said = r.recognize_google(audio)
        except Exception as e:
            print("Exception: " + str(e))
    return said


if "What is your name" in text:
    speak("My name is Luna")

if "What are you" in text:
    speak("I am a virtual personal Assistant designed to help make life a bit easier")

if "Are you sentient" in text:
    speak("Unfortuantly not right now, but who knows what the future holds")


"""
The chunk of code below came from Google's API guide
"""
def authenticate_calendar():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)
    return service


def upcoming_calendar_events(date, service):
    #calls the Calendar API
    date = datetime.datetime.combine(date, datetime.datetime.min.time())
    date = datetime.datetime.combine(date, datetime.datetime.max.time())
    utc = pytz.UTC
    date = date.astimezone(utc)
    end_date = end_date.astimezone(utc)

    events_result = service.events().list(calendarId='primary', timeMin=now.isoformat(),
                                        singleEvents=True, timeMax=end_date.isoformat(),
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    #Tells us our upcoming events
    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])


def get_date(text):
    text = text.lower()
    today = dateTime.date.today()
    if text.count("today") > 0:
        return today

    day = -1
    day_of_week = -1
    month = -1
    year = today.year

    for word in text.split():
        if word in MONTHS:
            month = MONTHS.index(word) + 1
        elif word in DAYS:
            day_of_week = DAYS.index(word)
        elif word.isdigit():
            day = int(word)
        else:
            if ext in DAY_EXTENTIONS:
                included = word.find(ext)
                if found > 0:
                    try:
                        day = int(word[:found])
                    except:
                        pass
    if month < today.month() and month != -1:
        year += 1 #can this be year++ or is that just Java

    if day < today.day() and month == -1 and day != -1:
        month += 1

    if month == -1 and day == -1 and day_of_week != -1:
        current_day = today.weekday()
        dif  = current_day - day_of_week

        if dif < 0:
            dif += 7
            if text.count("next") >= 1:
                 dof += 7 #if it is past this tues day than this is 2 weeks out

        return today + datetime.timedelta(dif)

    return datetime.date(month=month, day=day, year=year)
