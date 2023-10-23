"""hwm_forecast.py: predictive json files for HWM charts"""
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
__author__ = "Floyd Fayton"
__credits__ = ["Floyd Fayton"]
__version__ = "1.0.0"
__maintainer__ = "Floyd Fayton"
__email__ = "floyd.fayton@noaa.gov"
__status__ = "para"
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
import sys
import json
import re
from datetime import datetime, timezone
import os
import pandas as pd

def err_exit(msg):
    """Leaving this script hastily"""
    print(msg, file=sys.stderr)
    sys.exit(1)

def mathing(sign, number, row, x1, i):
    """Math by sign"""
    if sign == "*":  # sign * 0 (number) == 0
        nuvalue = max(0, int(x1 * number))
        row[0]["data"][:][i][-1] = nuvalue
    elif sign == "-":  # double meaning if number is 0 or empty
        if number == 0:
            row[0]["data"][:][i][-1] = 0  # value to zero since x1-0
        else:
            nuvalue = max(0, int(x1 - number))
            row[0]["data"][:][i][-1] = nuvalue
    elif sign == "/":
        nuvalue = max(0, int(x1 / number))
        row[0]["data"][:][i][-1] = nuvalue
    elif sign == "+":
        nuvalue = max(0, int(x1 + number))
        row[0]["data"][:][i][-1] = nuvalue
    else:
        err_exit(
            "operand not detected, \
            please fix $PARMhwm/fcst_ctrl file"
        )

def new_value(data, model, sign, number, times):  # generates new values by time
    """Generating new values by time values, or entire chart"""
    if times != "0":
        tarr = []
        split = times.split(sep=",", maxsplit=-1)
        epoch_zero = int(data[0][:][0]["data"][0][0] / 1000)
        epoch = datetime.utcfromtimestamp(epoch_zero)
        epoch = epoch.strftime("%Y%m%d")
        for _, ranget in enumerate(split):
            ranget = ranget.split(sep="-")  # rm dash, split list elements
            ymdhm_s = "".join([epoch, ranget[0]])
            ymdhm_e = "".join([epoch, ranget[1]])
            start = datetime.strptime(ymdhm_s, "%Y%m%d%H%M")
            end = datetime.strptime(ymdhm_e, "%Y%m%d%H%M")

            #.utc is critical for start/end
            start = int(start.replace(tzinfo=timezone.utc).timestamp() * 1000)
            end = int(end.replace(tzinfo=timezone.utc).timestamp() * 1000)
            tarr.append(ranget)
            for row in data:
                mfound = re.fullmatch(model, row[0]["name"])
                if mfound:
                    for t in range(start, end, 60000):
                        for i in range(0, 1439):
                            x1 = row[0]["data"][:][i][-1]
                            if t == row[0]["data"][:][i][0]:
                                mathing(sign, number, row, x1, i)

    else:
        for row in data:
            mfound = re.fullmatch(model, row[0]["name"])
            if mfound:
                for i in range(0, 1439):
                    x1 = row[0]["data"][:][i][-1]
                    mathing(sign, number, row, x1, i)

def hwm_modify(jsonfile, ctrl, nufile):
    """Main script to start modification of existing file"""
    with open(ctrl, "r", encoding="utf-8") as cfile:
        jsonctrl = pd.read_csv(
            cfile,
            sep=" ",
            comment="#",
            header=None,
            skip_blank_lines=True,
            names=["sign", "model", "number", "times"],
        )
        jsonctrl = jsonctrl.fillna("0")  # no NaNs or empty fields,

    with open(jsonfile, "r", encoding="utf-8") as jfile:
        data = json.load(jfile)
        data_str = re.sub(
            r"[\[\]]", "", str(data)
        )  # super step for searching, object --> string

    # Create new models
    for _, cow in jsonctrl.iterrows():
        sign = cow["sign"]
        model = cow["model"]
        modelfound = re.findall("'" + model + "'", data_str)
        number = int(cow["number"])
        times = cow["times"]

        if not modelfound:
            xbegin = data[0][:][0]["data"][0][0]
            modeldata = []
            for _ in range(0, 1439):
                modeldata.append([xbegin, 0])
                xbegin += 60000
            newmodel = json.dumps(
                [{"name": model, "data": modeldata}], indent=4, sort_keys=False
            )
            poo = json.loads(newmodel)
            data.append(poo)
            data_str = re.sub(r"[\[\]]", "", str(data))  # reset vars with updated data
            modelfound = re.findall("'" + model + "'", data_str)

        new_value(data, model, sign, number, times)

    with open(nufile, "w", encoding="utf-8") as final:
        final.write(json.dumps(data, indent=4, sort_keys=False))

################ TESTING INPUTS ################
infile = "cactus_daily_nid_nodes_p1.json"
ctrlfile = "parm/fcst_ctrl"
outfile = "hwm_fcst_nid_nodes_p1.json"
################################################

# ############### PRODUCTION INPUTS #############
# infile = os.environ["IJSON"]
# ctrlfile = os.environ["FCST_CTRL"]
# outfile = os.environ["DATA"] + '/' + os.environ["OJSON"]
# ###############################################

hwm_modify(infile, ctrlfile, outfile)
os.listdir(path=".")
