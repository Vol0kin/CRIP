'''
Fichero con funciones auxiliares dadas para realizar 
esta práctica o implementadas en prácticas anteriores 
'''

import random

### 1 - Funciones auxiliares implementadas en la práctica 1 ########################################


def potencia_modular(base, exponente, modulo):
    a = base
    b = exponente

    p = 1
    while b > 0:
        if b % 2 == 1:
            p = (p * a) % modulo
        b //= 2
        a = (a * a) % modulo

    return p


def descomponer(n):
    u = 0
    s = n
    while s % 2 == 0:
        u += 1
        s = s // 2
    return u, s


def test_miller_rabin(n, a):
    u, s = descomponer(n-1)
    a = potencia_modular(a, s, n)
    if a == 1 or a == n - 1:
        return True
    else:
        for i in range(1, u):
            a = (a*a) % n
            if a == 1:
                return False
            if a == n - 1:
                return True
    return False


def probable_primo(n, m):
    for i in range(m):
        r = random.randint(2, n-1)
        primo = test_miller_rabin(n, r)
        if not primo:
            return False

    return True


def siguiente_primo(n):
    if n % 2 == 0:
        i = n+1
    else:
        i = n

    while True:
        if probable_primo(i, 5):
            return i
        i += 2


def primer_primo_fuerte(n):
    if n % 2 == 0:
        i = n+1
    else:
        i = n

    while True:
        if probable_primo(i, 10) and probable_primo((i-1)//2, 10):
            return i
        i += 2


def primofuerte_bits(n):
    while True:
        r = random.randint(2**(n-1), 2**n - 1)
        p = primer_primo_fuerte(r)
        if p <= 2**n - 1:
            return p


### 2 - Funciones auxiliares específicas de la práctica 3 ##########################################

# Calcula el máximo común divisor de dos números.


def mcd(a, b):
    while b != 0:
        (a, b) = (b, a % b)
    return a

# Calcula el inverso de a módulo b (si existe). Si no existe, lo dice y devuelve 0.


def inversomodular(a, b):
    (u0, u1) = (1, 0)
    while b > 0:
        (u0, u1) = (u1, u0-(a//b)*u1)
        (a, b) = (b, a % b)
    if a == 1:
        return u0
    else:
        print("No existe el inverso")
        return 0

# Resuelve la congruencia ax = b mod m. Da todas las soluciones comprendidas entre 0 y m-1 (por tanto, m debe ser mayor que.


def congruencia(a, b, m):
    d = mcd(a, m)
    if b % d == 0:
        n = m//d
        u = inversomodular(a//d, n)
        x = (u*(b//d)) % n
        sol = []
        for i in range(d):
            sol.append(x)
            x += n
        return sol
    print("La congruencia no tiene solución")
    return([0])

# Calcula la raíz cuadrada entera de un número natural.


def raiz(n):
    m = (len(bin(n))-1) // 2
    x = 1 << m  # x=2^m
    y = (x**2+n)//(2*x)
    while x > y:
        (x, y) = (y, (y**2+n)//(2*y))
    return x

# Comprueba si un número natural es cuadrado perfecto.


def escuadrado(n):
    y = raiz(n)
    return(y**2 == n)
