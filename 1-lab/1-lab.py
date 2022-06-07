import matplotlib.pyplot as plt
from random import random
from math import sin, log
from time import perf_counter as getTime

# input parameters
HARMONICS = 12
W_MAX = 1800
DCALLS = 1024

# calc functions
getMx = lambda xArr: sum(xArr) / len(xArr)
getDx = lambda xArr, Mx, dc: sum([ (x - Mx) ** 2 for x in xArr ]) / (dc - 1)

def calcSignal(harmonics=HARMONICS, wMax=W_MAX, dCalls=DCALLS):
  w0 = wMax / harmonics
  tArr = [ t for t in range(dCalls) ]
  xArr = [0] * dCalls

  for hi in range(harmonics):
    w = w0 + w0 * hi
    amp = random()
    phase = random()
    for t in tArr:
      xArr[t] += amp * sin(w * t + phase)

  return tArr, xArr


def getComplexityParams(iterable, amount):
  harmonics = [ iterable * i for i in range(1, amount) ]
  timeArr = list()
  timeChArr = list()

  for n in harmonics:
    start = getTime()
    _, xArr = calcSignal(harmonics=int(n))
    signalEnd = getTime()
    timeArr.append(signalEnd - start)
    getDx(xArr, getMx(xArr), DCALLS)
    paramsEnd = getTime()
    timeChArr.append(signalEnd - paramsEnd)

  return harmonics, timeArr, timeChArr


def draw(coords, labels):
  xlabel, ylabel, title = labels
  plt.plot(*coords)
  plt.xlabel(xlabel)
  plt.ylabel(ylabel)
  plt.title(title)


# results output
tArr, xArr = calcSignal()
Mx = getMx(xArr)
Dx = getDx(xArr, Mx, DCALLS)

print("M(x) =", Mx)
print("D(x) =", Dx)

cmpHarmonics, cpmTime, cpmTimeCh  = getComplexityParams(10e2, 10)
lnHarmonics = [ log(n) for n in cmpHarmonics ]

draw((tArr, xArr), ("time", "x value", "Signal values"))
plt.figure()
draw((cmpHarmonics, cpmTime), ("harmonics (n)", "time","O(n)"))
plt.figure()
draw((lnHarmonics, cpmTime), ("harmonics (ln(n))", "time","O(ln(n))"))
plt.figure()
draw((cpmTime, cpmTimeCh), ("generating signal", "calculating M(x), D(x)", "time"))
plt.show()
