from typing import Tuple
import random

################################################################################
# Funciones base
################################################################################

def potencia_modular(a, b, m):
    """
    Calculo de la potencia modular a^b mod m

    Orden de eficiencia log(b)
    """
    p = 1

    while b > 0:
        if b % 2 == 1:
            p = (p * a) % m
        
        # Tambien se podria hacer un shift a la derecha
        # b = b >> 1
        b = b // 2
        
        a = (a * a) % m
    
    return p


def test_fermat(n, a):
    """
    Test de primalidad de Fermat
    """
    return potencia_modular(a, n-1, n) == 1


def raices_uno(p):
    """
    Funcion que encuentra todas las soluciones de la ecuacion x^2 - 1 = 0 en Z_p
    """
    l = []

    for i in range(1, p):
        if (i * i) % p == 1:
            l.append(i)
    
    return l


################################################################################
# Ejercicio 1: Test de Miller-Rabin para un numero (n) y un testigo (a) dado
################################################################################

def descomposicion(n: int) -> Tuple[int, int]:
    """
    Funcion para el calculo de la descomposicion de un numero como producto
    de 2^u * s, siendo s un numero impar.

    :param n: Numero del que calcular la descomposicion

    :return Devuelve una tupla con u y s    
    """
    # Inicializar u y s
    u = 0
    s = n
    
    while s % 2 == 0:
        u += 1
        s = s // 2
    
    return u, s


def miller_rabin(n: int, a: int) -> bool:    
    """
    Funcion que realiza el test de primalidad de Miller-Rabin sobre un numero n
    dado utilizando un testigo a dado.

    :param n: Numero que se quiere determinar si es posible primo o no.
    :param a: Testigo que a utilizar para determinar si el numero es posible primo o no.

    :return Devuelve True si el numero es posible primo y False en caso contrario.
    """
    # 1. Descomponer n-1 como 2^u * s con s impar
    u, s = descomposicion(n-1)
    
    # 2. Calcular a = a^s mod n
    a = potencia_modular(a, s, n)
    
    # Si a == 1 o a == n-1, el numero es posible primo
    if a == 1 or a == n-1:
        return True
    
    for i in range(1, u):
        a = potencia_modular(a, 2, n)
        
        # Si a == 1 sin haber pasado por n-1, el numero no es primo ya que tiene mas
        # de una solucion a x^2 - 1 = 0
        if a == 1:
            return False
        
        """
        Si a == n-1, el siguiente valor sera 1, por lo tanto, cumpliria el test
        de Fermat y tendria solo dos soluciones a la ecuacion x^2 - 1 = 0. Puede
        ser primo
        """
        if a == n-1:
            return True
    
    return False


################################################################################
# Ejercicio 2: Test de Miller-Rabin para un numero (n) con (m) numeros aleatorios
################################################################################

def test_miller_rabin(n: int, m: int) -> bool:
    """
    Funcion que realiza el test de Miller-Rabin sobre un numero n para determinar
    si es posible primo o no utilizando m testigos aleatorios.

    :param n: Numero que se quiere determinar si es posible primo o no.
    :param m: Numero de testigos aleatorios que utilizar.

    :return Devuelve True si ha superado el test con todos los testigos y False
            en caso de que falle alguno de los tests.
    """
    for i in range(m):
        # Escoger testigo tal que 2 <= a <= n-2
        a = random.randint(2, n-2)
        
        es_prob_primo = miller_rabin(n, a)
        
        print(f"Para el testigo a: {a} el resultado del test es {es_prob_primo}")
        
        if not es_prob_primo:
            return False
    
    return True


################################################################################
# Ejercicio 3: Dado un numero (n), calcular el primer numero, mayor o igual que 
# (n) que sea probable primo
################################################################################

def primer_probable_primo(n: int, m: int) -> int:
    es_posible_primo = False

    while not es_posible_primo:
        print(f"Probando con n = {n}")
        es_posible_primo = test_miller_rabin(n, m)

        if es_posible_primo:
            posible_primo = n
        
        n += 1
    
    return posible_primo


################################################################################
# Ejercicio 4: Dado un numero (n), calcular el primer numero, mayor o igual que 
# (n) que sea probable primo fuerte (tanto n como (n-1)/2 son primos)
################################################################################

def test_primo_fuerte(n, m):
    return test_miller_rabin((n - 1) / 2, m)

def primer_probable_primo_fuerte(n: int, m: int) -> int:
    es_primo_fuerte = False

    while not es_primo_fuerte:
        n = primer_probable_primo(n, m)
        print(f"siguiente test con {(n-1)//2}")
        es_primo_fuerte = test_primo_fuerte(n, m)

        if es_primo_fuerte:
            primo_fuerte = n
        
        n += 1
    
    return primo_fuerte


################################################################################
# Ejercicio 5: Dado un numero natural (n), calcular el primer numero primo fuerte (p)
# de n bits (es decir, en el rango 2^(n-1) <= p <= 2^n-1)
################################################################################

def primo_fuerte_n_bits(n, m):
    p = 2 ** (n - 1)
    limite = 2 ** n - 1
    es_primo_fuerte = False

    while not es_primo_fuerte and p <= limite:
        p = primer_probable_primo(p, m)

        if p <= limite:
            es_primo_fuerte = test_primo_fuerte(p, m)
            
            if es_primo_fuerte:
                primo_fuerte = p
            
            p += 1
    
    return primo_fuerte


################################################################################
# Ejercicio 6: elegir tres numeros (n1), (n2) y (n3). Obtener todos los falsos
# testigos para el primero y 200 para los dos siguientes
################################################################################

def calcular_todos_falsos_testigos(n):
    falsos_testigos = []

    for a in range(2, n - 1):
        if miller_rabin(n, a):
            falsos_testigos.append(a)
    
    return falsos_testigos


def calcular_m_falsos_testigos(n, m):
    falsos_testigos = []

    print(n)

    for _ in range(m):
        a = random.randint(2, n - 2)
        print(a)

        if miller_rabin(n, a):
            falsos_testigos.append(a)

    return falsos_testigos


def calcular_proporcion_falsos_testigos(falsos_testigos, m):
    return len(falsos_testigos) / m


################################################################################
# Ejercicio 8: estudiar si 100 numeros aleatorios son falsos testigos segun el
# test de Fermat y el de Miller-Rabin
################################################################################

def falsos_testigos_fermat_miller_rabin(n, m):
    falsos_testigos_fermat = []
    falsos_testigos_miller_rabin = []

    print(n)

    for _ in range(m):
        a = random.randint(2, n - 2)

        if test_fermat(n, a):
            falsos_testigos_fermat.append(a)
        
        if miller_rabin(n, a):
            falsos_testigos_miller_rabin.append(a)

    return falsos_testigos_fermat, falsos_testigos_miller_rabin


if __name__ == "__main__":
    """
    print(test_miller_rabin(1729, 10))

    p = primer_probable_primo(1729, 10)
    print(p)

    fuerte = primer_probable_primo_fuerte(12, 10)
    print(fuerte)
    """

    #primo_fuerte_n_bits(25, 10)

    #falsos_testigos = calcular_todos_falsos_testigos(121)
    #falsos_testigos = calcular_m_falsos_testigos(11 * 13 * 17 * 19 * 23, 200)
    #falsos_testigos = calcular_m_falsos_testigos(primer_probable_primo(10000000, 10) * primer_probable_primo(50000000, 10) , 200)
    #print(falsos_testigos)
    #print(calcular_proporcion_falsos_testigos(falsos_testigos, 200))
    #print(calcular_proporcion_falsos_testigos(falsos_testigos, len(range(2, 124))))

    """
    falsos_testigos = calcular_m_falsos_testigos(3215031751, 200)
    print(falsos_testigos)
    print(calcular_proporcion_falsos_testigos(falsos_testigos, 200))
    """

    fermat, mr = falsos_testigos_fermat_miller_rabin(2199733160881, 100)
    print(fermat)
    print(mr)

    print(calcular_proporcion_falsos_testigos(fermat, 100))
    print(calcular_proporcion_falsos_testigos(mr, 100))