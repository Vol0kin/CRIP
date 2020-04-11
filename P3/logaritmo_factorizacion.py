import Practica3 as utils
import time
import random


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
    if n % 2 == 0 :
        i = n+1
    else :
        i = n

    while True:
        if probable_primo(i,10) and probable_primo((i-1)//2,10) :
            return i
        i += 2        
        
        
def primofuerte_bits(n) :
    while True :
        r = random.randint(2**(n-1), 2**n - 1)
        p = primer_primo_fuerte(r)
        if p <= 2**n - 1 :
            return p        

          
def orden(a, n):
    i = 1
    b = a
    while not b == 1:
        b = (b*a) % n
        i += 1

    return i


def es_primitivo(a, n):
    return orden(a, n) == n - 1


def primer_primitivo(n):
    for i in range(1, n-1):
        if es_primitivo(i, n):
            return i
    
    return None
  
# Problema logaritmo discreto

# 1 - Fuerza bruta


def fuerza_bruta(a, b, p):
    if b == 1:
        return 0
    else:
        for i in range(1, p-1):
            potencia = potencia_modular(a, i, p)
            if potencia == b:
                return i
            if potencia == 1:
                return -1
    return -1


# 2 - Algoritmo paso enano - paso gigante
def pasoenano_pasogigante(a, b, p):
    s = utils.raiz(p) + 1
    T = []
    for i in range(s):
        T.append((potencia_modular(a, i, p) * b) % p)

    for t in range(1, s):
        e = potencia_modular(a, s*t, p)
        if e in T:
            return t*s - T.index(e)

    print("No existe el logaritmo")
    return -1


# 3 - Algoritmo p de Pollard
def logaritmo_ro_pollard(a, b, p):
    print(a, b, p)
    def siguiente_pollard(x, alfa, beta):
        if x % 3 == 0:
            return x**2 % p, (2*alfa % (p - 1), 2*beta % (p - 1))
        elif x % 3 == 1:
            return x*b % p, (alfa, beta + 1)
        else:
            return x*a % p, (alfa + 1, beta)

    x_n, alfa_beta_n = siguiente_pollard(1, 0, 0)
    x_2n, alfa_beta_2n = siguiente_pollard(x_n, *alfa_beta_n)

    while x_n != x_2n:
        x_n, alfa_beta_n = siguiente_pollard(x_n, *alfa_beta_n)
        x_aux, alfa_beta_aux = siguiente_pollard(x_2n, *alfa_beta_2n)
        x_2n, alfa_beta_2n = siguiente_pollard(x_aux, *alfa_beta_aux)

    a_cong = alfa_beta_2n[1] - alfa_beta_n[1]
    b_cong = alfa_beta_n[0] - alfa_beta_2n[0]

    sols = utils.congruencia(a_cong, b_cong, p - 1)
    sols = tuple(filter(lambda x: potencia_modular(a, x, p) == b, sols))

    return sols[0]

# Problema factorización

# 1 - División por tentativa


def factorizacion_tentativa(n):
    p = 2
    while n % p != 0:
        p = siguiente_primo(p+1)

    return p, n//p

# 2 - Método de Fermat


def factorizacion_fermat(n):
    x = raiz(n)
    y = x*x - n
    while not utils.escuadrado(y):
        x+=1
        y = x*x - n

    return x+y, x-y

# 3 - Algoritmo p de Pollard


def factorizacion_ro_pollard(n):
    def siguiente_pollard(x):
        return (x*x + 1) % n

    x = siguiente_pollard(0)
    y = siguiente_pollard(x)

    mcd = utils.mcd(y-x, n)
    while mcd == 1 or mcd == n:
        x = siguiente_pollard(x)
        y_aux = siguiente_pollard(y)
        y = siguiente_pollard(y_aux)

        mcd = utils.mcd(y - x, n)

    return mcd

  
## Medición de tiempos 

# Tiempos logaritmo discreto 

def medir_tiempo_log_discreto(algoritmo):
    lista_tiempos = []
    lista_n = []
    
    n = 10
    n_b = 10
    
    while True:
        print(f"Inicio con {n} bits")
        p = primofuerte_bits(n)
        a = primer_primitivo(p)
        
        t_tam = 0
        
        for i in range(n_b):
            b = random.randint(2, p-2)
            
            t1 = time.time()
            algoritmo(a, b, p) 
            t2 = time.time()
            
            t_tam += t2 - t1
        
        lista_tiempos.append(t_tam / n_b)
        lista_n.append(n)
        n += 5
        
        print(f"{t_tam / n_b}")
      
  
    return lista_tiempos, lista_n

medir_tiempo_log_discreto(logaritmo_ro_pollard)
