import numpy as np
import matplotlib.pyplot as plt

def graficar_logaritmo(n_bits, t_medios):
    n_bits = list(map(lambda x: f'{x}', n_bits))
    
    plt.plot(n_bits, t_medios, 'r-o')
    
    plt.xlabel('Tamaño (núm. bits)')
    plt.ylabel('Tiempo de ejecución (s)')
    
    plt.show()


def graficar_all(n_bits, tiempos, labels):
    for b in n_bits:
        b = list(map(lambda x: f'{x}', b))
    
    for b, t, l in zip(n_bits, tiempos, labels):
        plt.plot(b, t, '-o', label=l)
    
    plt.xlabel('Tamaño (núm. bits)')
    plt.ylabel('Tiempo de ejecución (s)')
    plt.legend()
    
    plt.show()
    

def graficar_factorizacion(n_bits, t_medios, t_max):
    n_bits = list(map(lambda x: f'{x}', n_bits))
    
    plt.plot(n_bits, t_medios, 'r-o', label='Tiempo medio')
    plt.plot(n_bits, t_max, 'b-o', label='Tiempo maximo')
    
    plt.xlabel('Tamaño (núm. bits)')
    plt.ylabel('Tiempo de ejecución (s)')
    plt.legend()
    
    plt.show()

# Datos del problema del logaritmo discreto
log_fb_tiempos = [3.289999999651627e-05, 6.240000000161672e-05, 0.0004239999999981592,
                  0.0016849999999976717, 0.005689900000015768, 0.04919489999999769,
                  0.2382556999999906, 0.677249500000005, 2.956829200000004, 11.27176830000002,
                  101.70763059999999]
log_fb_bits = [5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25]

log_pasos_tiempos = [1.620000000000024e-05, 1.5600000000000335e-05, 2.9600000000002542e-05,
                     7.979999999999862e-05, 0.0001903999999999989, 0.0005393000000000009,
                     0.001259400000000002, 0.005197200000000002, 0.019143700000000003,
                     0.04263840000000003, 0.21767710000000004, 0.5687606000000001,
                     2.4810711999999997, 11.5459092, 41.1283097, 157.9750945999999]

log_pasos_bits = [5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35]

log_pollard_tiempos = [6.699999999000283e-05, 0.0001010999999834894,
                       0.00014440000004469766, 0.0001297000000704429, 0.00014069999997445848,
                       0.00037850000003345483, 0.0007830000000922155, 0.0015563000000383908,
                       0.0034021000000393543, 0.004873399999951289, 0.01632649999996829,
                       0.0254003000000921, 0.045783799999981056, 0.12040650000003553,
                       0.193842099999938, 0.48515189999998254, 0.8358214999999746,
                       2.017601899999954, 3.708842400000003, 7.42329679999998,
                       15.097770699999955, 32.025017100000014, 82.15813870000007]

log_pollard_bits = [5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39, 41, 43, 45, 47, 49]

"""
graficar_logaritmo(log_fb_bits, log_fb_tiempos)
graficar_logaritmo(log_pasos_bits, log_pasos_tiempos)
graficar_logaritmo(log_pollard_bits, log_pollard_tiempos)
graficar_all_logaritmos(log_pollard_bits, [log_fb_tiempos, log_pasos_tiempos, log_pollard_tiempos], ['Fuerza bruta', 'Paso enano - paso gigante', r'$\rho$ de Pollard'])
"""

# Datos del problema de la factorizacion
fact_tent_tiempos = [0.0, 0.0015625, 0.0015625, 0.0015625, 0.0015625, 0.0015625,
                     0.0046875, 0.003125, 0.003125, 0.0046875, 0.009375, 0.0140625,
                     0.025, 0.015625, 0.0265625, 0.065625, 0.0578125, 0.05, 0.128125,
                     0.1609375, 0.275, 0.265625, 0.65, 1.1265625, 1.00625, 3.4046875,
                     1.9703125, 4.5421875, 4.075, 12.98125, 13.4328125]

fact_tent_max = [0.0, 0.015625, 0.015625, 0.015625, 0.015625, 0.015625, 0.03125, 0.03125,
                 0.03125, 0.046875, 0.09375, 0.0625, 0.21875, 0.140625, 0.265625, 0.328125,
                 0.578125, 0.5, 1.28125, 1.59375, 2.640625, 2.46875, 6.5, 6.375, 10.0625,
                 18.8125, 19.59375, 32.671875, 40.6875, 74.9375, 134.328125]

fact_tent_bits = [20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39,
                  40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50]

fact_fermat_tiempos = [0.0015625, 0.0, 0.0015625, 0.0015625, 0.0015625, 0.0015625, 0.0125, 0.009375,
                       0.0296875, 0.0109375, 0.034375, 0.178125, 0.025, 0.1453125, 1.028125, 2.2875,
                       6.0984375, 17.2859375, 19.95, 5.778125, 37.65625, 38.5578125, 80.7984375,
                       83.8015625, 711.8109375]

fact_fermat_max = [0.015625, 0.0, 0.015625, 0.015625, 0.015625, 0.015625, 0.046875, 0.046875,
                   0.078125, 0.03125, 0.234375, 1.234375, 0.1875, 0.84375, 7.75, 17.890625,
                   57.5, 105.3125, 147.4375, 44.765625, 370.34375, 307.765625, 683.140625,
                   695.90625, 2953.125]

fact_fermat_bits = [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34]

fact_pollard_tiempos = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0015625, 0.0, 0.0015625, 0.0046875, 0.0078125, 0.015625, 0.1515625, 0.1328125, 0.0828125, 0.328125, 1.30625, 7.0875, 3.9546875, 48.4328125, 122.88125]
fact_pollard_max = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.015625, 0.0, 0.015625, 0.03125, 0.078125, 0.15625, 0.5625, 1.328125, 0.828125, 3.234375, 13.0625, 64.984375, 39.546875, 484.328125, 1228.8125]
fact_pollard_bits = [10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100, 105, 110]

"""
graficar_factorizacion(fact_tent_bits, fact_tent_tiempos, fact_tent_max)
graficar_factorizacion(fact_fermat_bits, fact_fermat_tiempos, fact_fermat_max)
graficar_factorizacion(fact_pollard_bits, fact_pollard_tiempos, fact_pollard_max)
"""

graficar_all([fact_tent_bits, fact_fermat_bits, fact_pollard_bits], [fact_tent_tiempos, fact_fermat_tiempos, fact_pollard_tiempos], ['Tentativa', 'Fermat', r'$\rho$ de Pollard'])
