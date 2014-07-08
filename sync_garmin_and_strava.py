import config
import requests
import re


#
## Shamelessly stolen and modified from https://github.com/cpfair/tapiriik/blob/master/tapiriik/services/GarminConnect/garminconnect.py#L188
#

def _rate_limit():
  import fcntl, struct, time

  min_period = 1 # I appear to been banned from Garmin Connect while determining this.

  try:
    if not last_req_start:
        last_req_start = 0
  except:
    last_req_start = 0

  try:
    print("Have lock")


    wait_time = max(0, min_period - (time.time() - last_req_start))
    time.sleep(wait_time)

    last_req_start = time.time()

    print("Rate limited for %f" % wait_time)
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
## End Stolen Code
#


session = requests.Session()

_get_session()

import json

activities = session.get( 'http://connect.garmin.com/proxy/activity-search-service-1.0/json/activities?&limit=1' ).text
meow = json.loads( activities )

activity_id = meow['results']['activities'][0]['activity']['activityId']
activity_name = meow['results']['activities'][0]['activity']['activityName']['value']
activity_type = meow['results']['activities'][0]['activity']['activityType']['key']

gpx_file = session.get( 'http://connect.garmin.com/proxy/activity-service-1.1/gpx/activity/' + activity_id + '?full=true' ).text

# Replace Garmin Connect metadata with metadata for the device I'm using
gpx_file = gpx_file.replace( 'Garmin Connect', 'Garmin Edge 810' )

moo = open( 'test.gpx', 'w' )
moo.write( gpx_file )
moo.close()

gpx_file = open( 'test.gpx', 'r' )


from stravalib import Client, unithelper
strava = Client( access_token=config.STRAVA_ACCESS_TOKEN)

strava.upload_activity( gpx_file, 'gpx' )
