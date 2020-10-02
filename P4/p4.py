'''
Autores
    Roberto García Pérez
    Vladislav Nikolov Vasilev
    Víctor Alejandro Vargas Pérez
'''

import utils
from random import randint
from os import system
from hashlib import sha256

################################################################################

def obtener_p(q, exponente):
    # Elegir c al azar de *exponente* bits y lo multiplicamos por 2 para
    # que sea par
    c = randint(2**(exponente-1), 2**exponente - 1)
    c *= 2

    # p = q*c+1
    # Mientras p no es primo: p = p + 2q
    p = q*c + 1
    while not utils.MillerRabin(p, 20):
        p += 2 * q

    return p

def obtener_alfa(p, q):
    alfa = 1
    while alfa == 1:
        a = randint(2, p-2)
        alfa = utils.potenciamodular(a, (p-1)//q, p)

    return alfa


def generar_claves_DSS(N, L):
    q = utils.primo_bits(N)
    p = obtener_p(q, L - N)
    alfa = obtener_alfa(p, q)
    x = randint(2, q - 2)
    y = utils.potenciamodular(alfa, x, p)

    return q, p, alfa, x, y


################################################################################

def firmar_DSS(mensaje, p, q, alfa, x):
    # Obtener resumen como string hexadecimal y convertirlo a entero
    resumen = sha256(open(mensaje, "rb").read()).hexdigest()
    z = int(resumen, 16)

    r = 0
    s = 0

    while r == 0 or s == 0:
        k = randint(2, q-2)
        r = utils.potenciamodular(alfa,k, p) % q
        s = (utils.inverso(k, q) * (z + x*r)) % q

    return r, s

################################################################################

def verificar_firma_DSS(mensaje, r, s, p, q, alfa, y):
    w = utils.inverso(s, q)

    # Obtener resumen como string hexadecimal y convertirlo a entero
    resumen = sha256(open(mensaje, "rb").read()).hexdigest()
    z = int(resumen, 16)

    u = z*w % q
    v = r*w % q
    r2 = ((utils.potenciamodular(alfa, u, p) * utils.potenciamodular(y, v, p)) % p) % q

    return r == r2

################################################################################

# Ejecución

print('FIRMA DIGITAL')
print('¿Qué quieres hacer?')

opcion = 0

while opcion != 1 and opcion != 2 and opcion != 3:
    opcion = int(input("1 (Generar claves)\n2 (Firmar mensaje)\n3 (Verificar firma)\n\nEntrada: "))


N = 256
L = 1024

# Generar Claves
if opcion == 1:
    q, p, alfa, x, y = generar_claves_DSS(N, L)
    pub_key = (p, q, alfa, y)
    priv_key = (p, q, alfa, x, y)

    with open("clave_publica.pub", "w") as f:
        for k in pub_key:
            f.write(f"{k}\n")

    with open("clave_privada.priv", "w") as f:
        for k in priv_key:
            f.write(f"{k}\n")

    print("\nClaves generadas en los ficheros clave_publica.pub y clave_privada.priv\n")

# Firmar mensaje
elif opcion == 2:

    f_mensaje = input("\nIntroduce el fichero con el mensaje a firmar: ")

    clave_privada = input("\nIntroduce el fichero con la clave privada: ")

    with open(clave_privada) as f:
        (p, q, alfa, x, y) = tuple(map(lambda x: int(x), f.read().splitlines()))


    r, s = firmar_DSS(f_mensaje, p, q, alfa, x)

    with open("firma.sign", "w") as f:
        f.write(f"{r}\n")
        f.write(f"{s}\n")

    print("\nSe ha firmado el mensaje. El resultado está en firma.sign")

# Verificar firma
else:

    f_mensaje = input("\nIntroduce el fichero con el mensaje que se ha firmado: ")

    firma = input("\nIntroduce el fichero con la firma: ")

    with open(firma) as f:
        (r, s) = tuple(map(lambda x: int(x), f.read().splitlines()))

    clave_publica = input("\nIntroduce el fichero con la clave pública: ")

    with open(clave_publica) as f:
        (p, q, alfa, y) = tuple(map(lambda x: int(x), f.read().splitlines()))

    es_valida = verificar_firma_DSS(f_mensaje, r, s, p, q, alfa, y)

    if es_valida:
        print("La firma es válida")
    else:
        print("La firma no es válida")
