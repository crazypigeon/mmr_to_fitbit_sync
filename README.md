## Overview

This is a short script that will take data from the Map My Ride service and transfer it over to FitBit as activity records.

While most of this stuff should work with all activity types in Map My Fitness, I am only focused on the "Road Cycling" activity type because it maps directly to the "Bicycling" FitBit activity and I'm too lazy to implement anything else :).

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
