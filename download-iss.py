import requests
import datetime
from datetime import timedelta

requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += 'HIGH:!DH:!aNULL'
try:
    requests.packages.urllib3.contrib.pyopenssl.DEFAULT_SSL_CIPHER_LIST += 'HIGH:!DH:!aNULL'
except AttributeError:
    # no pyopenssl support used / needed / available
    pass
# I need this because the site of ISS apparently uses a small DH key.
# The code is taken from https://stackoverflow.com/questions/38015537/python-requests-exceptions-sslerror-dh-key-too-small

page = requests.get('https://www.epicentro.iss.it/coronavirus/dashboard/inizio.html', verify=False)
# I thank Gianluca Bonifazi @Biuni for helping me find this page
lines = (page.text).splitlines()

# collect data from "Data inizio sintomi"
dailyy = []

for line in lines:
 if "\"width\":[23328,23328,23328" in line:
  fields = line.split(',')
  writing = False
  for word in fields:
   if '\"y\":[20' in word:
    dailyy.append("20")
    writing = True
    continue
   if writing == True and ']' in word:
    dailyy.append(word[0:word.index("]")])
    break
   if writing == True:
    dailyy.append(word)
  break

f = open('sympdatadl.csv', 'w')
day0 = datetime.date(2020, 1, 28)

for i, n in enumerate(dailyy):
 print((day0+timedelta(days=i)),n, sep=',', file=f)
 
# collect data from "Data inizio sintomi (casi sintomatici)"
dailyy2 = []

for line in lines:
 if "\"width\":[23328,23328,23328" in line:
  fields = line.split(',')
  writing = False
  for word in fields:
   if '\"y\":[16' in word:
    dailyy2.append("16")
    writing = True
    continue
   if writing == True and ']' in word:
    dailyy2.append(word[0:word.index("]")])
    break
   if writing == True:
    dailyy2.append(word)
  break

f2 = open('sympdatadates.csv', 'w')
day0 = datetime.date(2020, 1, 28)

for i, n in enumerate(dailyy2):
 print((day0+timedelta(days=i)),n, sep=',', file=f2)
