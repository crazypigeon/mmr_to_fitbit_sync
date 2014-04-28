from mapmyfitness import MapMyFitness
import fitbit
from datetime import datetime
from pytz import timezone

from config import *

debug = False

METERS_IN_A_MILE = 1609.34

pacific_timezone = timezone('America/Los_Angeles')

mmf = MapMyFitness(api_key=MMF_CLIENT_KEY, access_token=MMF_ACCESS_TOKEN)

fitbit_client = fitbit.Fitbit( FITBIT_CLIENT_KEY, FITBIT_CLIENT_SECRET, user_key=FITBIT_USER_KEY, user_secret=FITBIT_USER_SECRET)

# Grab all bike workouts from map my fitness
workouts = []

# Iterate through all valid activity types
for activity_id in MMF_BIKE_ACTIVITY_TYPES: 
  workouts = workouts + mmf.workout.search(user=MMF_USER_ID,activity_type=activity_id)

for workout in workouts:

  start_time = workout.start_datetime.astimezone( pacific_timezone ).strftime( '%H:%M' )
  start_date = workout.start_datetime.astimezone( pacific_timezone ).strftime( '%Y-%m-%d' )
  duration_milliseconds = int( 1000 * workout.elapsed_time_total )
  distance = workout.distance_total / METERS_IN_A_MILE
  
  dupe = False

  # Make sure we didn't already log this activity
  for activity in fitbit_client.activities( date = start_date )['activities']:
    if start_time == activity['startTime'] and duration_milliseconds == activity['duration']:
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
    print "Created an activity record in FitBit for the workout named: " + workout.name 
  # Otherwise, skip
  else:
    if debug:
      print 'Activity record for the workout named "'+ workout.name + '" already exists in FitBit!'
      print "Fitbit raw data"
      print activity['startTime']
      print start_date
      print activity['duration']
      print activity['distance']

  if debug:
    print "MMR raw data"
    print start_time
    print start_date
    print duration_milliseconds
    print distance
