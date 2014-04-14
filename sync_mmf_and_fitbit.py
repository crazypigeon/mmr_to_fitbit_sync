from mapmyfitness import MapMyFitness
import fitbit
from datetime import datetime
from pytz import timezone

from config import *

METERS_IN_A_MILE = 1609.34

mmf = MapMyFitness(api_key=MMF_CLIENT_KEY, access_token=MMF_ACCESS_TOKEN)

fitbit_client = fitbit.Fitbit( FITBIT_CLIENT_KEY, FITBIT_CLIENT_SECRET, user_key=FITBIT_USER_KEY, user_secret=FITBIT_USER_SECRET)

# Grab all bike workouts from map my fitness
workouts = mmf.workout.search(user=MMF_USER_ID,activity_type=MMF_ACTIVITY_TYPE)

for workout in workouts:
  # 2014-04-10 16:24:12+00:00

  meh = workout.start_datetime.strftime( '%Y-%m-%d %H:%M:%S%z' )

  print meh

  print workout.name
  print "\t" + str( workout.start_datetime )
  print "\t" + str( workout.distance_total )
  print "\t" + str( workout.elapsed_time_total )

  pacific_timezone = timezone('America/Los_Angeles')

  start_time = workout.start_datetime.astimezone( pacific_timezone ).strftime( '%H:%M' )
  start_date = workout.start_datetime.astimezone( pacific_timezone ).strftime( '%Y-%m-%d' )

  # Log the activity in FitBit
  fitbit_client.log_activity(
     { 
        'activityId' : FITBIT_ACTIVITY_ID, 
        'startTime' : start_time,
        'durationMillis': int( 1000 * workout.elapsed_time_total ),
        'date' : start_date,
        'distance' : workout.distance_total / METERS_IN_A_MILE
     }
  )
  

  
