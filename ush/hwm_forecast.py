"""hwm_forecast.py: predictive json files for HWM DAILY and LIVE charts"""
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
__author__ = 'Floyd Fayton'
__credits__ = ["Floyd Fayton"]
__version__ = "1.0.0"
__maintainer__ = "Floyd Fayton"
__email__ = "floyd.fayton@noaa.gov"
__status__ = "test"
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
import sys
import json as json
import time
from datetime import datetime, timedelta, date
import os
import numpy as np

#setting vars, ii is wcossii
iifile = sys.argv[1] 
fcst_ctrl = os.environ["FCST_CTRL"]
workdir = os.environ["DATA"] + '/'

#jiif = open(iifile)
jiif = open('cactus_daily_nid_nodes_p1.json')
ljsonf = json.load(jiif)
for i in ljsonf:
    print(i[0]['name'])






