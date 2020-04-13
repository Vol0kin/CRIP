import Utilidades as utils
import random
import time

### Problema logaritmo discreto ####################################################################
# Encontrar una solución (si existe) de log_a(b) mod p, donde:
#   - p primo
#   - b entero, 1 <= b <= p-1
#   - a entero, 2 <= a <= p-2

# 1 - Fuerza bruta


def logaritmo_fuerza_bruta(a, b, p):
    # Si b es 1, la solución es 0
    if b == 1:
        return 0
    else:
        # En caso contrario, realizar la potencia modular de base a y módulo p
        # con todos los valores posibles (excepto 0).
        for i in range(1, p-1):
            potencia = utils.potencia_modular(a, i, p)
            # Si la potencia es b, tenemos una solución
            if potencia == b:
                return i
            # Si alguna potencia es 1, no existe solución
            if potencia == 1:
                break

    print("No existe el logaritmo")
    return -1


# 2 - Algoritmo paso enano - paso gigante

def logaritmo_pasoenano_pasogigante(a, b, p):
    s = utils.raiz(p) + 1

    # Generación de la tabla
    T = [b]

    for i in range(1, s):
        T.append(T[i - 1] * a % p)

    # Probar potencias s potencias de a, terminando si alguna está en la tabla
    for t in range(1, s+1):
        e = utils.potencia_modular(a, s*t, p)
        if e in T:
            return t*s - T.index(e)

    print("No existe el logaritmo")
    return -1

# 3 - Algoritmo p de Pollard


def logaritmo_ro_pollard(a, b, p):

    # Función para obtener el siguiente valor de una sucesión.
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

    # Resolver congruencia
    sols = utils.congruencia(a_cong, b_cong, p - 1)
    sols = tuple(filter(lambda x: utils.potencia_modular(a, x, p) == b, sols))

    if len(sols) == 0:
        print("No existe el logaritmo")
        return -1
    else:
        return sols[0]

### Problema factorización #########################################################################
# Dado un número n no primo, encontrar un divisor del mismo (distinto de 1 y n)

# 1 - División por tentativa


def factorizacion_tentativa(n):
    p = 2

    # Probar a dividir n por todos los números primos hasta que alguno sea divispr
    while n % p != 0:
        p = utils.siguiente_primo(p+1)

    return p

# 2 - Método de Fermat


def factorizacion_fermat(n):
    x = utils.raiz(n)  # x raíz entera de n

    # Si n es un número cuadrado, su raíz entera es un divisor
    if utils.escuadrado(n):
        return x

    # En caso contrario, incrementar x (queremos entero igual o inmediatamente superior a la raíz)
    x += 1
    y_cuadrado = x*x - n

    # Incrementar x hasta que x² - n sea un cuadrado
    while not utils.escuadrado(y_cuadrado):
        x += 1
        y_cuadrado = x*x - n

    y = utils.raiz(y_cuadrado)
    return x+y

# 3 - Algoritmo p de Pollard


def factorizacion_ro_pollard(n):
    incremento = 1

    # Función para obtener el siguiente valor de una sucesión. Esta función varía según un incremento.
    def siguiente_pollard(x):
        return (x*x + incremento) % n

    max_iter = utils.raiz(n)  # Número máximo de funciones diferentes a probar
    mcd = n

    # Mientras no se haya probado el número máximo de funciones
    while incremento < max_iter:
        x = siguiente_pollard(0)
        y = siguiente_pollard(x)

        mcd = utils.mcd(y-x, n)

        # Continuar obteniendo valores de la sucesión hasta obtener mcd != 1
        while mcd == 1:
            x = siguiente_pollard(x)
            y_aux = siguiente_pollard(y)
            y = siguiente_pollard(y_aux)

            mcd = utils.mcd(y - x, n)

        # Si el mcd es n, no se ha encontrado divisor: probar otra función
        if mcd == n:
            incremento += 1
        # Si mcd != n, tenemos un divisor: fin del algoritmo
        else:
            break

    return mcd


### Medición de tiempos ############################################################################

# Función para obtener elemento primitivo a partir de primo fuerte

def primer_primitivo(p):
    q = (p - 1) // 2

    a = random.randint(2, p - 2)

    while not utils.potencia_modular(a, q, p) == p - 1:
        a = random.randint(2, p - 2)

    return a

# Función para obtener un número impar no primo de n bits


def impar_noprimo_nbits(n):
    r = random.randint(2**(n-1), 2**n - 1)
    while r % 2 == 0 or utils.probable_primo(r, 20):
        r = random.randint(2**(n-1), 2**n - 1)

    return r

# Función para obtener un número de n bits a partir del producto de primos pequeños


def producto_primos_pequeños(n):
    objetivo = 2**(n-1)
    p = 137
    r = p

    while r < objetivo:
        p = utils.siguiente_primo(p+1)
        r *= p

    return r

# Tiempos logaritmo discreto


def medir_tiempo_log_discreto(algoritmo, repeticiones, inicio, fin, incremento):
    lista_tiempos = []
    lista_n = []

    for n in range(inicio, fin+1, incremento):
        print(f"Inicio con {n} bits")
        p = utils.primofuerte_bits(n)
        # a elemento primitivo: el logaritmo debe tener solución
        a = primer_primitivo(p)

        t_tam = 0

        for i in range(repeticiones):
            b = random.randint(2, p-2)
            t1 = time.clock()
            algoritmo(a, b, p)
            t2 = time.clock()
            t_tam += t2 - t1

        print(f"{t_tam / repeticiones}")

        lista_tiempos.append(t_tam / repeticiones)
        lista_n.append(n)

    return lista_tiempos, lista_n

# Tiempos factorizacion


def medir_tiempo_factorizacion(algoritmo, repeticiones, inicio, fin, incremento):
    lista_medias = []
    lista_max = []
    lista_n = []

    for n in range(inicio, fin+1, incremento):
        print(f"Inicio con {n} bits")
        tiempos_n = []

        # Producto de primos pequeños
        b = producto_primos_pequeños(n)
        t1 = time.clock()
        algoritmo(b)
        t2 = time.clock()
        tiempos_n.append(t2 - t1)

        # Producto de primos de tamaño la mitad
        p1 = utils.primofuerte_bits(n//2)
        p2 = utils.primofuerte_bits(n//2)
        t1 = time.clock()
        algoritmo(p1 * p2)
        t2 = time.clock()
        tiempos_n.append(t2 - t1)

        # Resto de repeticiones
        for i in range(2, repeticiones):
            b = impar_noprimo_nbits(n)
            t1 = time.clock()
            algoritmo(b)
            t2 = time.clock()
            tiempos_n.append(t2 - t1)

        print(tiempos_n)
        print(f"{sum(tiempos_n) / repeticiones}")

        lista_medias.append(sum(tiempos_n) / repeticiones)
        lista_max.append(max(tiempos_n))
        lista_n.append(n)

    return lista_medias, lista_max, lista_n
