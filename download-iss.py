import requests

requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += 'HIGH:!DH:!aNULL'
try:
    requests.packages.urllib3.contrib.pyopenssl.DEFAULT_SSL_CIPHER_LIST += 'HIGH:!DH:!aNULL'
except AttributeError:
    # no pyopenssl support used / needed / available
    pass

page = requests.get('https://www.epicentro.iss.it/coronavirus/dashboard/inizio.html', verify=False)
lines = (page.text).splitlines()

dailyy = []

for line in lines:
 if "<script type=\"application/json\" data-for=\"htmlwidget-5683e312fd82693e76ce\">" in line:
  fields = line.split(',')
  writing = False
  for word in fields:
   if '\"y\":[10' in word:
    dailyy.append("10")
    writing = True
    continue
   if writing == True and ']' in word:
    dailyy.append(word[0:word.index("]")])
    break
   if writing == True:
    dailyy.append(word)
  break

f = open('sympdatadl.csv', 'w')

for i, n in enumerate(dailyy):
 print(n,i, sep=',', file=f)
