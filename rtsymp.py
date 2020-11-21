import numpy as np
import math

from matplotlib import pyplot as plt

from scipy import stats as sps
from scipy.stats import gamma
from scipy.stats import poisson

def logfactorial(n):
# returns log(n!)
 lf = np.zeros(n.size)
 for i in range(n.size):
   for j in range(int(n[i])+1):
    if j == 0:
     continue
    lf[i] += np.log(j)
 return lf

def percentile(data, p):
# data contain a probability (or likelyhood) distribution, and this returns the p-th percentile position.
  s = data.sum()
  ndata = data/s
  percent = 0.0
  for i in range(len(ndata)):
   percent += ndata[i]
   if percent > p/100.0:
    break
  return i
   

#dailyfile = open('testdata.txt', 'r')
#dailyfile = open('sympdata_it.csv', 'r')
dailyfile = open('sympdatadl.csv', 'r')
daily = []

for line in dailyfile.readlines():
 fields = line.split(',')
# daily.append(float(fields[0]))
 daily.append(int(fields[0]))
dailyfile.close()

days = len(daily)

# the daily data of infection (the number of positive symptomatic based on the date of sympton onset)
I = np.array(daily)
#(days,)

rmin, rmax, rsteps = 0.01,5,500
# candidates for R_t.
r = (np.matrix(np.linspace(rmin, rmax, rsteps))).transpose()
#(1,rsteps)

# parameters for the Gamma distribution
shape = 1.87
rate = 0.28
scale=1/rate

# window of estimate
tau = 7
# cutoff for infection (14 days for quarantine, 30 days should be enough)
Tmax = 30

# the infectivity of a single infected
w = gamma.pdf(np.linspace(0,Tmax,Tmax+1), shape,0,scale)
#(Tmax+1,)


# range of calculation. We have to wait for Tmax in order to accumulate the data
t = np.linspace(Tmax, days-Tmax-tau, days-Tmax-tau+1)
#(days-Tmax-tau,)

Lambda = np.matrix((np.convolve(w,I))[Tmax:days:1])

Ic = I[Tmax:days:1]

#plt.plot(np.linspace(0,days-Tmax-1,days-Tmax),logfactorial(I)[Tmax:days:1],linewidth=2, color='r')
#plt.show()


logP = np.array(np.log(r * Lambda)) * Ic - np.array(r * Lambda) - logfactorial(Ic)


logLt = np.empty((rsteps, days-Tmax-tau+1))
C = np.ones(tau)

for i in range(rsteps):
 logLt[i] = np.convolve(logP[i],C,'valid')


logL = logLt.transpose()



normalizer = np.empty((days-Tmax-tau+1))
normalizedlogL = np.empty((days-Tmax-tau+1,rsteps))

for i in range(days-Tmax-tau+1):
 normalizer[i] = logL[i].max()
 normalizedlogL[i] = logL[i]-normalizer[i]


L = np.exp(normalizedlogL)

Prob = np.empty((days-Tmax-tau+1,rsteps))

for i in range(days-Tmax-tau+1):
 Prob[i] = L[i]/L[i].sum()

R5 = np.empty((days-Tmax-tau+1))
R = np.empty((days-Tmax-tau+1))
R95 = np.empty((days-Tmax-tau+1))
for i in range(days-Tmax-tau+1):
 R5[i] = r[percentile(Prob[i],5)]
 R[i] = r[L[i].argmax()]
 R95[i] = r[percentile(Prob[i],95)-1] # to make 5 and 95-th percentile symmetric

#plt.plot(r,L[10],linewidth=2, color='r')
#plt.savefig('perc.png')

plt.plot(t,R,linewidth=2, color='r')
plt.show()
#plt.savefig('rtsymp.png')


#print(R5)
print(R)
#print(R95)
