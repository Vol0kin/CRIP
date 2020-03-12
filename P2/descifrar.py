abecedario = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"


def leer_archivo(path):
    with open(path) as f:
        content = f.read()
    
    return content


def descifra_cesar(text, k):
    correspondence = {k: v%len(abecedario) for k in}