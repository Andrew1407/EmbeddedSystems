import matplotlib.pyplot as plt
from random import random
import math
from time import perf_counter as getTime

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


def memoize(calcFn):
  def wrapper(*args):
    p = args[0]
    memVal = memoize.memoized.get(p)
    if memVal is not None:
      return memVal

    res = calcFn(*args)
    memoize.memoized[p] = res
    return res

  return wrapper

memoize.memoized = dict()


@memoize
def getCoef(p, N):
  calcComplex = lambda x: complex(math.cos(x), math.sin(x))
  calcCoef = lambda x: calcComplex(x * (2 * math.pi / N))
  return calcCoef(p)


def calcFFT(xVals):
  N = len(xVals)
  EVEN_INC, ODD_INC = 0, 1
  halfN = int(N / 2)
  halfNRange = range(halfN)
  fArr = [0] * N
  calcF = lambda p, inc: sum([ xVals[2 * k + inc] * getCoef(k * p, halfN) for k in halfNRange ])

  for p in halfNRange:
    f1 = calcF(p, ODD_INC)
    f2 = calcF(p, EVEN_INC)
    coef = getCoef(p, N)
    fArr[p] = abs(f2 + coef * f1)
    fArr[p + halfN] = abs(f2 - coef * f1)

  return fArr


def calcDTF(xVals):
  N = len(xVals)
  Nrange = range(N)
  Wcoefs = dict()           # memoizing collection
  fArr = list()

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

      f += xVals[k] * w

    fArr.append(abs(f))

  return fArr


def calcComplexity(iterable, amount):
  harmonics = [ iterable * i for i in range(1, amount) ]
  timeArr = list()

  for n in harmonics:
    _, xArr = calcSignal(dCalls=int(n))
    start = getTime()
    calcFFT(xArr)
    end = getTime()
    timeArr.append(end - start)

  return harmonics, timeArr


def draw(coords, labels=("x", "y", "y(x)")):
  xlabel, ylabel, title = labels
  plt.plot(*coords)
  plt.xlabel(xlabel)
  plt.ylabel(ylabel)
  plt.title(title)


# results output
(tArr, xArr) = calcSignal()
startFFT = getTime()
fArr = calcFFT(xArr)
endFFT = getTime()
calcDTF(xArr)
endDFT = getTime()

print("FFT time:", endFFT - startFFT)
print("DFT time:", endDFT - endFFT)

cmpN, cmpTime = calcComplexity(10, DCALLS)

draw((tArr, xArr), ("time", "x value", "Signal values"))
plt.figure()
draw((tArr, fArr), ("p", "F(p)", "Spectre"))
plt.figure()
draw((cmpN, cmpTime), ("log(n)", "O(log(n))", "Complexity"))
plt.show()
