import config
import requests
import re
import pickle
import os
import json
import stravalib
import fcntl, struct, time

#
## "Borrowed" and modified from https://github.com/cpfair/tapiriik/blob/master/tapiriik/services/GarminConnect/garminconnect.py#L188
#

def _rate_limit():

  min_period = 1 # I appear to been banned from Garmin Connect while determining this.

  try:
    if not last_req_start:
        last_req_start = 0
  except:
    last_req_start = 0

  try:
    #print("Have lock")


    wait_time = max(0, min_period - (time.time() - last_req_start))
    time.sleep(wait_time)

    last_req_start = time.time()

    #print("Rate limited for %f" % wait_time)
  finally:
    last_req_start = time.time()

def _get_session():
  data = {
      "username": config.GARMIN_EMAIL,
      "password": config.GARMIN_PASSWORD,
      "_eventId": "submit",
      "embed": "true",
  }
  params = {
      "service": "http://connect.garmin.com/post-auth/login",
      "clientId": "GarminConnect",
      "consumeServiceTicket": "false",
  }
# I may never understand what motivates people to mangle a perfectly good protocol like HTTP in the ways they do...
  preResp = session.get("https://sso.garmin.com/sso/login", params=params)

  if preResp.status_code != 200:
      raise APIException("SSO prestart error %s %s" % (preResp.status_code, preResp.text))
  data["lt"] = re.search("name=\"lt\"\s+value=\"([^\"]+)\"", preResp.text).groups(1)[0]

  ssoResp = session.post("https://sso.garmin.com/sso/login", params=params, data=data, allow_redirects=False)
  if ssoResp.status_code != 200:
      raise APIException("SSO error %s %s" % (ssoResp.status_code, ssoResp.text))

  ticket_match = re.search("ticket=([^']+)'", ssoResp.text)
  if not ticket_match:
      raise APIException("Invalid login", block=True, user_exception=UserException(UserExceptionType.Authorization, intervention_required=True))
  ticket = ticket_match.groups(1)[0]

# ...AND WE'RE NOT DONE YET!

  _rate_limit()
  gcRedeemResp1 = session.get("http://connect.garmin.com/post-auth/login", params={"ticket": ticket}, allow_redirects=False)
  if gcRedeemResp1.status_code != 302:
      raise APIException("GC redeem 1 error %s %s" % (gcRedeemResp1.status_code, gcRedeemResp1.text))

  _rate_limit()
  gcRedeemResp2 = session.get(gcRedeemResp1.headers["location"], allow_redirects=False)
  if gcRedeemResp2.status_code != 302:
      raise APIException("GC redeem 2 error %s %s" % (gcRedeemResp2.status_code, gcRedeemResp2.text))

#
## End "borrowed" Code
#

# Setup Garmin
session = requests.Session()
_get_session()

# Setup Strava
strava = stravalib.Client( access_token=config.STRAVA_ACCESS_TOKEN)

# Load Already Uploaded IDs
pickle_filename = 'data.pkl'

try:
  pickle_file = open( pickle_filename, 'rb' )
  uploaded_ids = pickle.load(pickle_file)
  pickle_file.close()
except:
    uploaded_ids = []


# Grab the last 10 activities from Garmin Connect
number_of_activities = 10
activities = session.get( 'http://connect.garmin.com/proxy/activity-search-service-1.0/json/activities?&limit=' + str( number_of_activities ) ).text
response = json.loads( activities )['results']['activities']

# Iterate through each of the returned activities and upload the ones that aren't already there
for activity_record in response:
    temporary_gpx_filename = 'temp.gpx'

    activity_id = activity_record['activity']['activityId']
    #activity_name = activity_record['activity']['activityName']['value']
    #activity_type = activity_record['activity']['activityType']['key']

    # Got this URL through the Garmin connect website
    gpx_stream = session.get( 'http://connect.garmin.com/proxy/activity-service-1.1/gpx/activity/' + activity_id + '?full=true' ).text

    # Replace Garmin Connect metadata with metadata for the device I'm using
    # This allows it to show up on the Strava page, and for Strava to actually trust the Barometric data in the file
    gpx_stream = gpx_stream.replace( 'Garmin Connect', 'Garmin Edge 810' )

    # Stravalib requires that a file be passed to it...
    # There is probably a better way to do this then to write/read/delete a file on the actual filesystem
    gpx_file = open( temporary_gpx_filename, 'w' )
    gpx_file.write( gpx_stream )
    gpx_file.close()

    gpx_file = open( temporary_gpx_filename, 'r' )


    # Skip if we've already uploaded it
    if activity_id in uploaded_ids:
        print "Already Uploaded Garmin Activity ID: " + activity_id + '...skipping...'
        continue

    try:
        strava.upload_activity( gpx_file, 'gpx' )
        uploaded_ids.append( activity_id )
        print "Uploaded Garmin Activity ID: " + activity_id
    except stravalib.exc.ActivityUploadFailed:
        uploaded_ids.append( activity_id )
        print "Problem Uploading Garmin Activity ID: " + activity_id + "....probably a dupe...skipping...."

    gpx_file.close()
    os.unlink( temporary_gpx_filename )

pickle_file = open( pickle_filename, 'wb' )
pickle.dump( uploaded_ids, pickle_file )
pickle_file.close()
