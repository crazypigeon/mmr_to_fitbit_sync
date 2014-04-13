## Overview

This is a short script that will take data from the Map My Ride service and transfer it over to FitBit as activity records.

While most of this stuff should work with all activity types in Map My Fitness, I am only focused on the "Road Cycling" activity type because it maps directly to the "Bicycling" FitBit activity and I'm too lazy to implement anything else :).

## Getting Started

1. Populate the config.py file with the API keys for FitBit and MapMyFitness

You can generate the user key and secret for the FitBit API by running this script:

> venv/lib/python2.7/site-packages/fitbit/gather\_keys\_cli.py \<client\_key\> \<client\_secret\>
