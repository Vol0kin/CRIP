from random import randint
from math import sqrt, floor

def factoriza2(n):
    [u,s]=[0,n]
    while (s%2 == 0):
        [u,s] = [u+1,s>>1]
    return([u,s])

def potenciamodular(a,b,m):
    p = 1
    while b > 0:
        if (b%2 == 1):
            p = (p*a)%m
        b = b//2
        a = (a*a)%m
    return p

def mcd(a,b):
    if b == 0:
        return(abs(a))
    while b!=0:
        (a,b) = (b,a%b)
    return a

def mcd_ex(a,b):
    (u0,u1)=(1,0)
    (v0,v1)=(0,1)
    while b > 0:
        (c,r) = (a//b, a%b)
        (u0,u1) = (u1,u0-c*u1)
        (v0,v1) = (v1,v0-c*v1)
        (a,b) = (b, r)
    return [a,u0,v0]

def inverso(a,n):
    u = mcd_ex(a,n)
    if u[0] == 1:
        return(u[1])
    else:
        print('No existe el inverso')
        return(0)

def mraux(u,p,a):
    if (a == 1 or a == (p-1)):
        return True
    for i in range(u-1):
        a = (a*a)%p
        if a == p-1:
            return True
        if a == 1:
            return False
    return False
    
def MillerRabin(p,n):
    if (p%2) == 0:
        print('El numero es par')
        return False
    [u,s] = factoriza2(p-1)
    i = 0
    while i<n:
        a = randint(2,p-2)
        b = potenciamodular(a,s,p)
        i+=1
        bool = mraux(u,p,b)
        if bool == False:
            return False
    return True

def raicesuno(p):
    l = []
    for i in range(1,p):
        if (i**2)%p == 1:
            l = l + [i]
    return l
    
def siguienteprimo(n):
    n = n + 1 - n%2
    while not(MillerRabin(n,20)):
        n+=2
    return n

def siguienteprimofuerte(n):
    n = n + 3 - n%4
    q = (n-1)//2
    while not(MillerRabin(q,10)) or not(MillerRabin(2*q+1,10)):
        q+=2
    return 2*q+1

def legendre2(p):
    if (p%8) == 1 or (p%8) == 7:
        return 1
    else:
        return -1

def legendre(m,n):
    if m == 1:
         return 1
    elif m == -1:
         return (-1)**((n-1)//2)
    elif (m%2) == 0:
         return legendre2(n)*legendre(m//2,n)
    elif (m%4) == 3 and (n%4) == 3:
         return (-1)*legendre(n%m,m)
    else:
         return legendre(n%m,m)

def raizmod(a,p):
    if legendre(a,p) == -1:
        print('No existe la raíz')
        return 0
    x = 2
    while legendre(x,p) == 1:
        x+=1
    u,s = 0,p-1
    while s%2 == 0:
        u+=1
        s = s//2
    if u == 1:
        r = potenciamodular(a,(p+1)//4,p)
        if r > (p-1)//2:
             return(p-r)
        return r
    b = potenciamodular(x,s,p)
    inva = inverso(a,p)
    r = potenciamodular(a,(s+1)//2,p)
    aux = (inva*r*r)%p
    exp = 2**(u-2)
    for j in range(u-1):
        aux2 = potenciamodular(aux,exp,p)
        if aux2 == p-1:
             r = (r*b)%p
             aux = (aux*b*b)%p
        b = (b*b)%p
        exp = exp//2
    if r > (p-1)//2:
        return (p-r)
    return r

def congruencia(a,b,m):
    d = mcd_ex(a,m)
    if b%d[0] == 0:
        m1 = m//d[0]
        a1 = (d[1]*b//d[0])%m1
        return([a1,m1])
    return([0,0])

def sistema(l):
    sol = [0,1]
    for y in l:
        z = congruencia(y[0]*sol[1],(y[1]-y[0]*sol[0])%y[2],y[2])
        sol = [sol[0]+sol[1]*z[0],sol[1]*z[1]]
    return(sol)

def raizmodular(v,p,q):
    n = p*q
    u1 = raizmod(v,p)
    u2 = raizmod(v,q)
    r1 = sistema([[1,u1,p],[1,u2,q]])[0]
    if r1 > (n-1)//2:
        r1 = n-r1
    r2 = sistema([[1,u1,p],[1,q-u2,q]])[0]
    if r2 > (n-1)//2:
        r2 = n-r2
    return([r1,r2])

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

def primo_bits(n):
    while True:
        r = randint(2**(n-1), 2**n - 1)
        p = siguienteprimo(r)
        if p <= 2**n - 1:
            return p

def primofuerte_bits(n):
    while True:
        r = randint(2**(n-1), 2**n - 1)
        p = siguienteprimofuerte(r)
        if p <= 2**n - 1:
            return p