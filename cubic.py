import math
import matplotlib.pyplot as plt

def printEq(coefs):
    print("Уравнение: ", end='')
    n = len(coefs)
    if n == 0:
        print(0)
        return
    for i in range(n):
        if coefs[i] != 0:
            if coefs[i] > 0 and i != 0:
                print("+", sep='', end='')
            if abs(coefs[i]) != 1.0 or i == n - 1:
                print(coefs[i], sep='', end='')
            elif coefs[i] == -1.0:
                print("-", sep='', end='')
            if i == n - 2:
                print("x", sep='', end='')
            elif i != n - 1:
                print("x^" + str(n - i - 1), sep='', end='')
    print("")


def printRoots(roots, eps):
    k = math.ceil(-math.log10(eps))
    formatStr = "x = {:." + str(int(k)) + "f}"
    for i in range(len(roots)):
        print(formatStr.format(roots[i]))


def solveSquareEq(coefs):
    n = len(coefs)
    if n != 3:
        return []
    D = coefs[1] ** 2 - 4 * coefs[0] * coefs[2]
    if D < 0:
        return []
    if D == 0:
        return [-coefs[1] / (2 * coefs[0])]
    return [(-coefs[1] - math.sqrt(D)) / (2 * coefs[0]), (-coefs[1] + math.sqrt(D)) / (2 * coefs[0])]


def findRoot(coefs, a, b, eps, delta):
    cf = []
    l = a
    r = b
    if not (math.isinf(l)) and not (math.isinf(r)):
        if calcFunc(coefs, l) > 0:
            for i in coefs:
                cf.append(-i)
        else:
            for i in coefs:
                cf.append(i)
        c = (l + r) / 2
        while abs(calcFunc(cf, c)) > eps:
            c = (l + r) / 2
            if calcFunc(cf, c) > eps:
                r = c
            elif calcFunc(cf, c) < -eps:
                l = c
        return c
    if math.isinf(l):
        if calcFunc(coefs, r) > 0:
            for i in coefs:
                cf.append(-i)
        else:
            for i in coefs:
                for i in coefs:
                    cf.append(i)
        dx = delta
        while calcFunc(cf, r - dx) < 0:
            dx += delta
        return findRoot(coefs, r - dx, r - dx + delta, eps, delta)
    if math.isinf(r):
        if calcFunc(coefs, l) > 0:
            for i in coefs:
                cf.append(-i)
        else:
            for i in coefs:
                for i in coefs:
                    cf.append(i)
        dx = delta
        while calcFunc(cf, l + dx) < 0:
            dx += delta
        return findRoot(coefs, l + dx - delta, l + dx, eps, delta)


def calcFunc(coefs, x):
    n = len(coefs)
    if n == 0:
        return float('nan')
    res = 0
    for i in range(n):
        res += coefs[i] * x ** (n - i - 1)
    return res


def solveCubeEq(coefs, eps, delta):
    roots = []
    derCoefs = [3, 2 * coefs[1], coefs[2]]
    D = derCoefs[1] ** 2 - 4 * derCoefs[0] * derCoefs[2]
    if D <= 0:
        f0 = calcFunc(coefs, 0)
        if abs(f0) <= eps:
            roots.append(0)
        elif f0 < -eps:
            roots.append(findRoot(coefs, 0, float('+inf'), eps, delta))
        else:
            roots.append(findRoot(coefs, float('-inf'), 0, eps, delta))
    else:
        derRoots = solveSquareEq(derCoefs)
        fa = calcFunc(coefs, derRoots[0])
        fb = calcFunc(coefs, derRoots[1])
        if fa > eps and fb > eps:
            roots.append(findRoot(coefs, float("-inf"), derRoots[0], eps, delta))
        elif fa < -eps and fb < -eps:
            roots.append(findRoot(coefs, derRoots[1], float("+inf"), eps, delta))
        elif abs(fa) < eps and abs(fb) < eps:
            roots.append((derRoots[0] + derRoots[1]) / 2)
        elif fa > eps > abs(fb):
            roots.append(findRoot(coefs, float("-inf"), derRoots[0], eps, delta))
            roots.append(derRoots[1])
        elif abs(fa) < eps and fb < -eps:
            roots.append(derRoots[0])
            roots.append(findRoot(coefs, derRoots[1], float("+inf"), eps, delta))
        elif fa > eps and fb < -eps:
            roots.append(findRoot(coefs, float("-inf"), derRoots[0], eps, delta))
            roots.append(findRoot(coefs, derRoots[0], derRoots[1], eps, delta))
            roots.append(findRoot(coefs, derRoots[1], float("+inf"), eps, delta))
    return roots

def plotEq(coefs, roots, a, b, step):
    curX = a
    x = []
    y = []
    for i in range(math.ceil((b-a)/step)):
        x.append(curX)
        y.append(calcFunc(coefs, curX))
        curX += step
    plt.plot(x, y)
    plt.axhline(y=0.0, color='black', linestyle='-', linewidth=0.5)
    plt.axvline(x=0.0, color='black', linestyle='-', linewidth=0.5)
    max = calcFunc(coefs, b)
    for i in roots:
        plt.scatter(i, calcFunc(coefs, i))
        k = math.ceil(-math.log10(step))
        formatStr = "{:." + str(int(k)) + "f}"
        plt.annotate(formatStr.format(i), xy=(i, calcFunc(coefs, i)), xycoords='data',
                     xytext=(i, max / 5), textcoords='data',
                     arrowprops=dict(facecolor='g', arrowstyle='->'))
    plt.show()



coefs = [1.0]
eps = 0
delta = 0
print("Введите коэффициенты уравнения x^3 + ax^2 + bx + c:")
i = 0
while i < 3:
    try:
        coefs.append(float(input()))
        i += 1
    except Exception as e:
        print("Повторите ввод:" + str(e))
printEq(coefs)
print("Задайте точность:")
while True:
    try:
        eps = float(input())
        if eps <= 0:
            raise Exception("Точность должна быть строго больше нуля!")
        break
    except Exception as e:
        print("Повторите ввод:" + str(e))
print("Задайте шаг:")
while True:
    try:
        delta = float(input())
        if delta <= 0:
            raise Exception("Шаг должен быть строго больше нуля!")
        break
    except Exception as e:
        print("Повторите ввод:" + str(e))

roots = solveCubeEq(coefs, eps, delta)
a = 0
b = 0
if len(roots) >= 2:
    a = roots[0] - 20.0
    b = roots[len(roots)-1] + 20.0
elif len(roots) == 1:
    a = roots[0] - 20.0
    b = roots[0] + 20.0
else:
    a = -50.0
    b = 50.0
plotEq(coefs, roots, a, b, 0.0001)
printRoots(roots, eps)
