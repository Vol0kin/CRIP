from random import randint
from math import sqrt, floor
import time

def mcd_ex(a,b):
    (u0,u1)=(1,0)
    (v0,v1)=(0,1)
    while b > 0:
        (c,r) = (a//b, a%b)
        (u0,u1) = (u1,u0-c*u1)
        (v0,v1) = (v1,v0-c*v1)
        (a,b) = (b, a%b)
    return [a,u0,v0]

def inverso(a,p):
    x = mcd_ex(a,p)
    if x[0] == 1:
        return(x[1]%p)
    print('No existe el inverso')
    return 0

p = 362834280994187030710023991040175206904050711166288420558764425647758819918107404388055611
q = 384824237418077153783358778375943401261871966388487718774447118111259354458598762229755951

#n = p * q
n = 4050162682101453643920823917094627299441695791445831222744846356093660548006570106087173213405211281556146182260820950632356118529

e = 65537

phi = (p - 1) * (q - 1)
d = inverso(e, phi)
#d = 71313179457309239943470500120404374549451526113369387036026205668038373522590874594176606165743883128552003912676253649142683871328810395559211697701634854626126081199168839774873

kpub = (n,e)
kpriv = (n,d)

def potenciamodular(a,b,m):
    p = 1
    while b > 0:
        if (b%2 == 1):
            p = (p*a)%m
        b = b>>1
        a = (a*a)%m
    return p




def textotonumero(tex):
    sol = 0
    pos = 1
    for s in tex:
        x = ord(s)
        if (x>64 and x < 91):
            sol = sol + pos*(x-64)
            pos*=28
        elif x == 209:
            sol = sol + pos*27
            pos*=28
        elif x == 32:
            pos*=28
    return sol

def numerototexto(num):
    texto = ''
    while num > 0:
       aux = num%28
       if aux==0:
           texto = texto + ' '
       elif aux == 27:
           texto = texto + 'Ñ'
       else:
           texto = texto + chr(aux+64)
       num = num//28
    return texto


def cifra_RSA(mensaje):
    m = textotonumero(mensaje)
    cif = potenciamodular(m,kpub[1],kpub[0])
    return(numerototexto(cif))

def descifra_RSA(mensaje_cif):
    c = textotonumero(mensaje_cif)
    m = potenciamodular(c,kpriv[1],kpriv[0])
    return(numerototexto(m))


print(f"p: {p}")
print(f"q: {q}")
print(f'n: {n}')
print(f'e: {e}')
print(f'phi: {phi}')
print(f'd: {d}')
