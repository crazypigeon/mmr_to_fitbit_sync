import fitbit
from stravalib import Client, unithelper
from datetime import datetime, timedelta
from pytz import timezone

from config import *

debug = True

METERS_IN_A_MILE = 1609.34

pacific_timezone = timezone('America/Los_Angeles')

#mmf = MapMyFitness(api_key=MMF_CLIENT_KEY, access_token=MMF_ACCESS_TOKEN)

strava = Client( access_token=STRAVA_ACCESS_TOKEN)

fitbit_client = fitbit.Fitbit( FITBIT_CLIENT_KEY, FITBIT_CLIENT_SECRET, user_key=FITBIT_USER_KEY, user_secret=FITBIT_USER_SECRET)

# Only grab the last 10 activities

activities = strava.get_activities( limit = 10 )

#for activity in activities:
#    print activity.type

# Iterate through all valid activity types
#for activity_id in MMF_BIKE_ACTIVITY_TYPES: 
#  workouts = workouts + mmf.workout.search( user=MMF_USER_ID, activity_type=activity_id, started_after=started_after )

for activity in activities:
  if activity.type != 'Ride':
    next

  start_datetime = activity.start_date_local

  start_date = start_datetime.strftime( '%Y-%m-%d' )
  start_time = start_datetime.strftime( '%H:%M' )
  duration_milliseconds = int( 1000 * activity.moving_time.total_seconds() )
  distance = unithelper.miles( activity.distance ).num
  
  dupe = False

  # Make sure we didn't already log this activity
  for fitbit_activity in fitbit_client.activities( date = start_date )['activities']:
    if start_time == fitbit_activity['startTime'] and duration_milliseconds == fitbit_activity['duration']:
      dupe = True
      break

  # Log the activity in FitBit if it's not a duplicate
  if not dupe:
    fitbit_client.log_activity(
       { 
          'activityId' : FITBIT_ACTIVITY_ID, 
          'startTime' : start_time,
          'durationMillis': duration_milliseconds,
          'date' : start_date,
          'distance' : distance
       }
    )
    print "Created an activity record in FitBit for the workout named: " + activity.name 
  # Otherwise, skip
  else:
    if debug:
      print 'Activity record for the workout named "'+ activity.name + '" already exists in FitBit!'
      print "Fitbit raw data"
      print fitbit_activity['startTime']
      print start_date
      print fitbit_activity['duration']
      print fitbit_activity['distance']

  if debug:
    print "MMR raw data"
    print start_time
    print start_date
    print duration_milliseconds
    print distance
