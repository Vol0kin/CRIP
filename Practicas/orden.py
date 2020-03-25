
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

def orden(a, n):
    i = 1
    b = a
    while not b == 1:
        b = (b*a) % n
        i += 1

    return i


def es_primitivo(a, n):
    return orden(a, n) == n - 1

def elementos_primitivos(n):
    sol = []
    for i in range(1, n-1):
        if es_primitivo(i, n):
            sol.append(i)
    return sol


def primitivop1(a):
    div_primos = [2,3,7,19,2021879]
    sol = True
    for i in div_primos:
        j = potencia_modular(a,6453837768//i,6453837769)
        print(j)
        sol = sol and not(j==1)
    return sol

#for i in range(1, 19):
#    print(orden(i, 19))

#print(orden(4, 19))

p = 6453837769
for p in range(2, 50):
    print("p = ", p, " " ,primitivop1(p))

