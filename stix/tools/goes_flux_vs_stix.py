import sys
import math
from pprint import pprint
import pymongo
from datetime import datetime
from stix.spice import datetime as sdt
from matplotlib import pyplot as plt

connect = pymongo.MongoClient(port=9000)
db = connect["stix"]
fdb= db['flares']
rows=fdb.find({'goes.flux':{'$gt':0}})
x=[]
y=[]
for row in rows:
    xx=row['peak_counts']
    yy=row['goes']['flux']
    print(xx,yy)
    x.append(xx/4.)
    y.append(yy)

plt.scatter(y,x)
plt.xlabel('GOES flux')
plt.ylabel('STIX counts')
plt.xscale('log')
plt.yscale('log')
plt.show()



