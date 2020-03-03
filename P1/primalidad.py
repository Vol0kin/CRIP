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


def imprime_separador():
    print("\n" + "*" * 80 + "\n")


################################################################################
# Ejercicio 1: Test de Miller-Rabin para un numero (n) y un testigo (a) dado
################################################################################

def descomposicion(n):
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


def miller_rabin(n, a):    
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

def test_miller_rabin(n, m):
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
        
        if not es_prob_primo:
            return False
    
    return True


################################################################################
# Ejercicio 3: Dado un numero (n), calcular el primer numero, mayor o igual que 
# (n) que sea probable primo
################################################################################

def primer_probable_primo(n, m):
    """
    Funcion que calcula el primer numero mayor o igual a n que sea probable primo.

    :param n: Numero a partir del que se quiere encontrar el siguiente primo.
    :param m: Numero de testigos aleatorios que utilizar.

    :return Devuelve un probable primo mayor o igual que n.
    """
    es_posible_primo = False

    while not es_posible_primo:
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
    """
    Funcion que comprueba si un numero n es un primo fuerte.

    :param n: Numero a partir del que se quiere encontrar el siguiente primo fuerte.
    :param m: Numero de testigos aleatorios que utilizar.

    :return Devuelve True si n es probable primo fuerte y False en caso contrario. 
    """
    return test_miller_rabin((n - 1) // 2, m)


def primer_probable_primo_fuerte(n, m):
    """
    Funcion que calcula el primer numero mayor o igual a n que sea probable
    primo fuerte.

    :param n: Numero a comprobar si es numero primo fuerte.
    :param m: Numero de testigos aleatorios que utilizar.
    """
    es_primo_fuerte = False

    while not es_primo_fuerte:
        n = primer_probable_primo(n, m)
        es_primo_fuerte = test_primo_fuerte(n, m)

        if es_primo_fuerte:
            primo_fuerte = n
        
        n += 1
    
    return primo_fuerte


################################################################################
# Ejercicio 5: Dado un numero natural (n), calcular el primer numero primo fuerte
# (p) de n bits (es decir, en el rango 2^(n-1) <= p <= 2^n-1)
################################################################################

def primo_fuerte_n_bits(n, m):
    """
    Funcion que determina el primer numero que sea probable primo fuerte de n bits.

    :param n: Numero de bits que tiene que tener el probable primo fuerte.
    :param m: Numero de testigos aleatorios que utilizar.

    :return Devuelve el primer probable primo fuerte de n bits.
    """
    return primer_probable_primo_fuerte(2 ** (n-1), m)


################################################################################
# Ejercicio 6: elegir tres numeros (n1), (n2) y (n3). Obtener todos los falsos
# testigos para el primero y 200 para los dos siguientes
################################################################################

def calcular_todos_falsos_testigos(n):
    """
    Funcion que calcula todos los falsos testigos mediante el test de Miller-Rabin
    para un numero n. n no puede ser primo.

    :param n: Numero del que se quieren calcular todos los falsos testigos.

    :return Devuelve una lista con todos los falsos testigos.
    """
    falsos_testigos = []

    for a in range(2, n - 1):
        if miller_rabin(n, a):
            falsos_testigos.append(a)
    
    return falsos_testigos


def calcular_m_falsos_testigos(n, m):
    """
    Funcion que calcula m falsos testigos aleatorios mediante el test de Miller-Rabin
    para un numero n. n no puede ser pirmo.

    :param n: Numero del que se quieren calcular los falsos testigos.
    :param m: Numero de testigos aleatorios que utilizar.

    :return Devuelve una lista con los falsos testigos encontrados.
    """
    falsos_testigos = []

    for _ in range(m):
        a = random.randint(2, n - 2)

        if miller_rabin(n, a):
            falsos_testigos.append(a)

    return falsos_testigos


def calcular_proporcion_falsos_testigos(falsos_testigos, m):
    """
    Funcion que calcula la proporcion de falsos testigos.

    :param falsos_testigos: Lista con los falsos testigos encontrados.
    :param m: Numero maximos de elementos que puede tener la lista.

    :return Devuelve la proporcion de falsos testigos que se han encontrado.
    """
    return len(falsos_testigos) / m


################################################################################
# Ejercicio 8: estudiar si 100 numeros aleatorios son falsos testigos segun el
# test de Fermat y el de Miller-Rabin
################################################################################

def falsos_testigos_fermat_miller_rabin(n, m):
    """
    Funcion que determina los falsos testigos segun los tests de Miller-Rabin
    y Fermat para un numero m de testigos aleatorios.

    :param n: Numero sobre el que se van a hacer los tests.
    :param m: Numero de testigos aleatorios a utilizar.

    :return Devuelve una lista con los falsos testigos para el test de Fermat
            y otra lista con los falsos testigos para el test de Miller-Rabin.
    """
    falsos_testigos_fermat = []
    falsos_testigos_miller_rabin = []

    for _ in range(m):
        a = random.randint(2, n - 2)

        if test_fermat(n, a):
            falsos_testigos_fermat.append(a)
        
        if miller_rabin(n, a):
            falsos_testigos_miller_rabin.append(a)

    return falsos_testigos_fermat, falsos_testigos_miller_rabin


if __name__ == "__main__":

    imprime_separador()

    ############################################################################
    # Ejercicio 1
    print("Ejercicio 1")

    n, a = 341, 2
    print(f"Ejecutando test de Miller-Rabin para n = {n} y a = {a}")
    print("El numero es probable primo? ", miller_rabin(n, a))

    a = 10
    print(f"\nEjecutando test de Miller-Rabin para n = {n} y a = {a}")
    print("El numero es probable primo? ", miller_rabin(n, a))

    imprime_separador()

    ############################################################################
    # Ejercicio 2
    print("Ejercicio 2")

    n, m = 341, 20
    print(f"Ejecutando test de Miller-Rabin para n = {n} y m = {m}")
    print("El numero es probable primo? ", test_miller_rabin(n, m))

    n = 1729
    print(f"\nEjecutando test de Miller-Rabin para n = {n} y m = {m}")
    print("El numero es probable primo? ", test_miller_rabin(n, m))

    n = 203956878356401977405765866929034577280193993314348263094772646453283062722701277632936616063144088173312372882677123879538709400158306567338328279154499698366071906766440037074217117805690872792848149112022286332144876183376326512083574821647933992961249917319836219304274280243803104015000563790123
    print(f"\nEjecutando test de Miller-Rabin para n = {n} y m = {m}")
    print("El numero es probable primo? ", test_miller_rabin(n, m))

    imprime_separador()

    ############################################################################
    # Ejercicio 3
    print("Ejercicio 3")

    n = 14
    print(f"Buscando el primer primo mayor o igual que n = {n}")

    p = primer_probable_primo(n, m)
    print(f"El primer primo mayor o igual encontrado es p = {p}")
    print("El numero es probable primo? ", test_miller_rabin(p, m))

    n= 1729
    print(f"\nBuscando el primer primo mayor o igual que n = {n}")

    p = primer_probable_primo(n, m)
    print(f"El primer primo mayor o igual encontrado es p = {p}")
    print("El numero es probable primo? ", test_miller_rabin(p, m))

    imprime_separador()

    ############################################################################
    # Ejercicio 4
    print("Ejercicio 4")

    n = 12
    print(f"Buscando el primer primo fuerte mayor o igual que n = {n}")

    p = primer_probable_primo_fuerte(n, m)
    print(f"El primer primo fuerte mayor o igual encontrado es p = {p}")
    print("El numero es probable primo? ", test_miller_rabin(p, m))

    n= 1729
    print(f"\nBuscando el primer primo fuerte mayor o igual que n = {n}")

    p = primer_probable_primo_fuerte(n, m)
    print(f"El primer primo fuerte mayor o igual encontrado es p = {p}")
    print("El numero es probable primo? ", test_miller_rabin(p, m))

    imprime_separador()

    ############################################################################
    # Ejercicio 5
    print("Ejercicio 5")

    n = 10
    print(f"Buscando el primer primo fuerte de n = {n} bits")

    p = primo_fuerte_n_bits(n, m)
    print(f"El primer primo fuerte de {n} bits es {p}")
    print("El numero es probable primo? ", test_miller_rabin(p, m))

    n = 25
    print(f"\nBuscando el primer primo fuerte de n = {n} bits")

    p = primo_fuerte_n_bits(n, m)
    print(f"El primer primo fuerte de {n} bits es {p}")
    print("El numero es probable primo? ", test_miller_rabin(p, m))

    n = 50
    print(f"\nBuscando el primer primo fuerte de n = {n} bits")

    p = primo_fuerte_n_bits(n, m)
    print(f"El primer primo fuerte de {n} bits es {p}")
    print("El numero es probable primo? ", test_miller_rabin(p, m))

    n = 100
    print(f"\nBuscando el primer primo fuerte de n = {n} bits")

    p = primo_fuerte_n_bits(n, m)
    print(f"El primer primo fuerte de {n} bits es {p}")
    print("El numero es probable primo? ", test_miller_rabin(p, m))

    n = 500
    print(f"\nBuscando el primer primo fuerte de n = {n} bits")

    p = primo_fuerte_n_bits(n, m)
    print(f"El primer primo fuerte de {n} bits es {p}")
    print("El numero es probable primo? ", test_miller_rabin(p, m))

    imprime_separador()

    ############################################################################
    # Ejercicio 6
    print("Ejercicio 6")

    # Elegir n1 (11^2)
    n1 = 121
    print(f"Valor de n1 = {n1}")

    falsos_testigos = calcular_todos_falsos_testigos(n1)

    print(f"Falsos testigos encontrados: {falsos_testigos}")
    print(f"Proporcion de falsos testigos: {calcular_proporcion_falsos_testigos(falsos_testigos, len(range(2, n1-1)))}")

    # Elegir n2 (11 * 13 * 17 * 19 * 23)
    n2 = 11 * 13 * 17 * 19 * 23
    print(f"\nValor de n2 = {n2}")

    m = 200

    print(f"Numero de testigos que se van a probar m = {m}")

    falsos_testigos = calcular_m_falsos_testigos(n2, m)

    print(f"Falsos testigos encontrados: {falsos_testigos}")
    print(f"Proporcion de falsos testigos: {calcular_proporcion_falsos_testigos(falsos_testigos, m)}")

    # Elegir n3
    p1 = primer_probable_primo(10000000, m)
    p2 = primo_fuerte_n_bits(25, m)
    n3 = p1 * p2
    print(f"\nValor de p1 = {p1}")
    print(f"Valor de p2 = {p2}")
    print(f"Valor de n3 = {n3}")

    print(f"Numero de testigos que se van a probar m = {m}")

    falsos_testigos = calcular_m_falsos_testigos(n2, m)

    print(f"Falsos testigos encontrados: {falsos_testigos}")
    print(f"Proporcion de falsos testigos: {calcular_proporcion_falsos_testigos(falsos_testigos, m)}")

    imprime_separador()

    ############################################################################
    # Ejercicio 7
    print("Ejercicio 7")

    n = 3215031751

    print(f"\nValor de n = {n}")
    print(f"Numero de testigos que se van a probar m = {m}")

    falsos_testigos = calcular_m_falsos_testigos(n, m)

    print(f"Falsos testigos encontrados: {falsos_testigos}")
    print(f"Proporcion de falsos testigos: {calcular_proporcion_falsos_testigos(falsos_testigos, m)}")

    imprime_separador()

    ############################################################################
    # Ejercicio 8
    print("Ejercicio 8")

    n, m = 2199733160881, 100

    print(f"\nValor de n = {n}")
    print(f"Numero de testigos que se van a probar m = {m}")

    testigos_fermat, testigos_miller_rabin = falsos_testigos_fermat_miller_rabin(n, m)

    print(f"Falsos testigos encontrados con el test de Fermat: {testigos_fermat}")
    print(f"Falsos testigos encontrados con el test de Miller-Rabin: {testigos_miller_rabin}")

    print(f"Proporcion de falsos testigos para el tet de Fermat: {calcular_proporcion_falsos_testigos(testigos_fermat, m)}")
    print(f"Proporcion de falsos testigos para el test de Miller-Rabin: {calcular_proporcion_falsos_testigos(testigos_miller_rabin, m)}")

   