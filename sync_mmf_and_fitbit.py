from mapmyfitness import MapMyFitness
import fitbit

from config import *

mmf = MapMyFitness(api_key=MMF_CLIENT_KEY, access_token=MMF_ACCESS_TOKEN)

fitbit_client = fitbit.Fitbit( FITBIT_CLIENT_KEY, FITBIT_CLIENT_SECRET, user_key=FITBIT_USER_KEY, user_secret=FITBIT_USER_SECRET)

# Grab all bike workouts from map my fitness
workouts = mmf.workout.search(user=MMF_USER_ID,activity_type=MMF_ACTIVITY_TYPE)

for workout in workouts:
  print workout.name
  print "\t" + str( workout.start_datetime )
  print "\t" + str( workout.distance_total )
  print "\t" + str( workout.elapsed_time_total )

# TODO:
# 1. Implement startTime conversion
# 2. Implement date conversion
# 3. Test to make sure duplication doesn't happen

  # Log the activity in FitBit
  #fitbit_client.log_activity( {'activityId':FITBIT_ACTIVITY_ID, 'startTime':"12:00", 'durationMillis': 1000 * 60 * 60, 'date' : "2014-04-13", 'distance':"1.23"} )
  
