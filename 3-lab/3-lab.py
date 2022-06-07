import matplotlib.pyplot as plt
from random import random
import math
from time import perf_counter as getTime
from array import array

# input parameters
HARMONICS = 12
W_MAX = 1800
DCALLS = 64

# calc functions
def calcSignal(harmonics=HARMONICS, wMax=W_MAX, dCalls=DCALLS):
  w0 = wMax / harmonics
  tArr = [ t for t in range(dCalls) ]
  xArr = [0] * dCalls

  for hi in range(harmonics):
    w = w0 + w0 * hi
    amp = random()
    phase = random()
    for t in tArr:
      xArr[t] += amp * math.sin(w * t + phase)

  return tArr, xArr


def calcDTF(xVals, containerType="list"):
  N = len(xVals)
  Nrange = range(N)
  Wcoefs = dict()           # memoizing collection
  fArr = list()
  xArr = xVals.copy()
  if containerType == "array":
    xArr = array('f', xArr)
    fArr = array('f', fArr)

  calcComplex = lambda x: complex(math.cos(x), math.sin(x))
  calcCoef = lambda x: calcComplex(x * (2 * math.pi / N))

  for p in Nrange:
    f = 0
    for k in Nrange:
      pk = p * k
      w = Wcoefs.get(pk)
      if w is None:
        w = calcCoef(pk)
        Wcoefs[pk] = w

      f += xArr[k] * w

    fArr.append(abs(f))

  return fArr


def calcComplexity(iterable, amount):
  harmonics = [ iterable * i for i in range(1, amount) ]
  timeList = list()
  timeArr = list()

  for n in harmonics:
    _, xArr = calcSignal(dCalls=int(n))
    startList = getTime()
    calcDTF(xArr)
    endList = getTime()
    calcDTF(xArr, containerType="array")
    endArr = getTime()
    timeList.append(endList - startList)
    timeArr.append(endArr - endList)

  return harmonics, timeList, timeArr


def draw(coords, labels=("x", "y", "y(x)")):
  xlabel, ylabel, title = labels
  plt.plot(*coords)
  plt.xlabel(xlabel)
  plt.ylabel(ylabel)
  plt.title(title)


# results output
(tArr, xArr) = calcSignal()
startTimeList = getTime()
fArrList = calcDTF(xArr)
endTimeList = getTime()
calcDTF(xArr, containerType="array")
endTimeArr = getTime()

print("DTF time for list:", endTimeList - startTimeList)
print("DTF time for array:", endTimeArr - endTimeList)

cmpN, cmpList, cmpArr = calcComplexity(10, DCALLS)

draw((tArr, xArr), ("time", "x value", "Signal values"))
plt.figure()
draw((tArr, fArrList), ("p", "F(p)", "Spectre"))
plt.figure()
draw((cmpN, cmpList))
draw((cmpN, cmpArr), ("n^2 + n", "O(n^2 + n)", "Complexity (blue - list, red - array)"))
plt.show()
