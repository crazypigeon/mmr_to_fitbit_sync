## Overview

This repo contains a small collection of scripts I use to copy my fitness data between services.

I have each script run every 15 minutes offset (GC->Strava and then Strava->Fitbit) using a cron job on my Raspberry Pi.

Right now the main focus is Garmin Connect to Strava and then Strava to FitBit.

In the past it was MapMyRide to Fitbit.

Most of the scripts are for copying cycling related data, however the MapMyFitness scripts contain information for transferring hiking activities as well.

## Requirements

Most requirements are in the __requirements.txt__ file.

This script also requires the [mapmyfitness-python module](https://github.com/JasonSanford/mapmyfitness-python).

## Getting Started

Everything this script needs to run is contained in the __config.py__ file.

There is a template of this file is called __config\_template.py__ in the root directory of this repo.

### Getting API Keys

#### FitBit

1. Populate the config.py file with the API keys for FitBit and MapMyFitness

You can generate the user key and secret for the FitBit API by running this script:

> venv/lib/python2.7/site-packages/fitbit/gather\_keys\_cli.py \<client\_key\> \<client\_secret\>

#### MapMyFitness

MapMyFitness authorization tokens can be generated using the [MapMyFitness API Explorer](https://www.mapmyapi.com/io-docs)

#### Strava

Use the get_strava_access_token.py script to generate a token.
