import matplotlib.pyplot as plt
from random import random
from math import sin
from time import perf_counter as getTime
from array import array

# input parameters
HARMONICS = 12
W_MAX = 1800
DCALLS = 64

getInterval = lambda x: int(x / 2) - 1

T_INTERVAL = getInterval(DCALLS)

# calc functions
getMx = lambda x: sum(x) / len(x)

def calcSignal(harmonics=HARMONICS, wMax=W_MAX, dCalls=DCALLS, arrType="list"):
  w0 = wMax / harmonics
  tArr = [ t for t in range(dCalls) ]
  xArr = [0] * dCalls

  if arrType == "array":
    tArr = array('i', tArr)
    xArr = array('f', xArr)

  for hi in range(harmonics):
    w = w0 + w0 * hi
    amp = random()
    phase = random()
    for t in tArr:
      xArr[t] += amp * sin(w * t + phase)

  return tArr, xArr

def calcCorrelation(vals, Mvals, tInterval=T_INTERVAL):
  x, y = vals if len(vals) == 2 else (vals[0], vals[0])
  Mx, My = Mvals if len(Mvals) == 2 else (Mvals[0], Mvals[0])
  tIntArr = [ i for i in range(tInterval) ]
  rArr = list()

  for i in tIntArr:
    Rxy = 0
    for t in tIntArr:
      Rxy += (x[t] - Mx) * (y[t + i] - My)
    Rxy /= 2 * tInterval + 1
    rArr.append(Rxy)

  return tIntArr, rArr


def getCorrelationComplexity(iterable, amount, self=True, arrType="list"):
  dCalls = [ iterable * i for i in range(1, amount) ]
  cmpTimeArr = list()
  corTimeArr = list()

  for dc in dCalls:
    corTimeIntervals = [0, 0]
    tInterval = getInterval(dc)
    start = getTime()
    _, xArr = calcSignal(dCalls=int(dc), arrType=arrType)
    Mx = getMx(xArr)
    if self:
      cor1Start = getTime()
      calcCorrelation((xArr,), (Mx,), tInterval)
      cor1End = getTime()
      corTimeIntervals[0] = cor1End - cor1Start
    else:
      _, yArr = calcSignal(dCalls=int(dc), arrType=arrType)
      My = getMx(yArr)
      cor2Start = getTime()
      calcCorrelation((xArr, yArr), (Mx, My), tInterval)
      cor2End = getTime()
      corTimeIntervals[1] = cor2End - cor2Start
    end = getTime()
    cmpTimeArr.append(end - start)
    # taking correlation calc. time for two signals only
    corTimeArr.append(sum(corTimeIntervals))

  return dCalls, cmpTimeArr, corTimeArr


def draw(coords, labels):
  xlabel, ylabel, title = labels
  plt.plot(*coords)
  plt.xlabel(xlabel)
  plt.ylabel(ylabel)
  plt.title(title)


# results output
tArr1, xArr1 = calcSignal()
Mx1 = getMx(xArr1)

tArr2, xArr2 = calcSignal()
Mx2 = getMx(xArr2)

corrCoords1 = calcCorrelation((xArr1,), (Mx1,))             # seft
listCorTimeStart = getTime()
corrCoords2 = calcCorrelation((xArr1, xArr2), (Mx1, Mx2))   # first and second
listCorTimeEnd = getTime()
calcCorrelation((array('f', xArr1), array('f', xArr2)), (Mx1, Mx2))
arrCorTimeEnd = getTime()

# calculated once for two types log
print("Time for correlation calculating for list type:", listCorTimeEnd - listCorTimeStart)
print("Time for correlation calculating for array type:", arrCorTimeEnd - listCorTimeEnd)

cmp1 = getCorrelationComplexity(10, HARMONICS)
cmp2 = getCorrelationComplexity(10, HARMONICS, False)
# complexity for array type
_, _, corTimeArray = getCorrelationComplexity(10, HARMONICS, False, "array")
corTimeDifTypes = (cmp2[2], corTimeArray)                                       # calc. correlation for list and array

draw((tArr1, xArr1), ("time", "x value", ""))
draw((tArr2, xArr2), ("time", "x value", "Signals 1, 2"))
plt.figure()
draw(corrCoords1, ("t interval", "Rxx", "Autocorrelation"))
plt.figure()
draw(corrCoords2, ("t interval", "Rxy", "Correlation for signals 1, 2"))
plt.figure()
draw(cmp1[:2], ("dCalls", "O(n)", "Complexity (self)"))
plt.figure()
draw(cmp2[:2], ("dCalls", "O(n)", "Complexity (2 signals)"))
plt.figure()
draw(corTimeDifTypes, ("list time", "array time", "array/list calc. correlation time"))
plt.show()
