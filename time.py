import re
from datetime import datetime

tarr=[]
times="1230-1450,1634-1700,1900-2040"
split=times.split(sep=",",maxsplit=-1)
for idx,trange in enumerate(split):
    trange=trange.split(sep="-")
    tarr.append(trange)
print(tarr)
