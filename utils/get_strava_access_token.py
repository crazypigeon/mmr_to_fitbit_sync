from config import *

from stravalib import Client
import sys

client = Client()

if len( sys.argv ) == 1:

  url = client.authorization_url(client_id=STRAVA_CLIENT_ID,
                                           redirect_uri='http://localhost' )
  print "Paste this URL in your browser:"
  print
  print url
  print
  print "And then re-run this script like so: "
  print "\t" + sys.argv[0] + " <code>"

else:
  code = sys.argv[1]
  access_token = client.exchange_code_for_token(client_id=STRAVA_CLIENT_ID,
                                                client_secret=STRAVA_CLIENT_SECRET,
                                                code=code)
  print "Your Strava access token is: " + access_token
