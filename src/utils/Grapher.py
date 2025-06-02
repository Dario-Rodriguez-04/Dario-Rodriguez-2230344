import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

def onda_senoidal():
    Ts = 0.05
    x = np.linspace(-1, 5, 1000)
    y = np.sin(4 * np.pi * x)
    # Muestreo
    N = int((5 - (-1)) / Ts) + 1
    n = np.arange(N)
    t_n = -1 + n * Ts
    y_disc = np.sin(4 * np.pi * t_n)
    plt.plot(x, y,)
    plt.stem(t_n, y_disc, linefmt='r-', markerfmt='ro', basefmt=' ', label="Muestreada")
    plt.grid(True)
    plt.legend()
    plt.show()

def onda_exponencial():
    Ts = 0.05
    t = np.linspace(-1, 5, 1000)
    u = np.where(t >= 0, 1, 0)
    y = np.exp(-2 * t) * u
    # Muestreo
    N = int((5 - (-1)) / Ts) + 1
    n = np.arange(N)
    t_n = -1 + n * Ts
    u_n = np.where(t_n >= 0, 1, 0)
    y_disc = np.exp(-2 * t_n) * u_n
    plt.plot(t, y, label="Continua")
    plt.stem(t_n, y_disc, linefmt='r-', markerfmt='ro', basefmt=' ', label="Muestreada")
    plt.grid(True)
    plt.legend()
    plt.show()

def onda_triangular():
    Ts = 0.05
    t = np.linspace(-1, 5, 1000)
    y = signal.sawtooth(2 * np.pi * 2 * t, width=0.5)
    # Muestreo
    N = int((5 - (-1)) / Ts) + 1
    n = np.arange(N)
    t_n = -1 + n * Ts
    y_disc = signal.sawtooth(2 * np.pi * 2 * t_n, width=0.5)
    plt.plot(t, y, label="Continua")
    plt.stem(t_n, y_disc, linefmt='r-', markerfmt='ro', basefmt=' ', label="Muestreada")
    plt.grid(True)
    plt.legend()
    plt.show()

def onda_cuadrada():
    Ts = 0.05
    t = np.linspace(-1, 5, 1000)
    y = signal.square(2 * np.pi * 2 * t)
    # Muestreo
    N = int((5 - (-1)) / Ts) + 1
    n = np.arange(N)
    t_n = -1 + n * Ts
    y_disc = signal.square(2 * np.pi * 2 * t_n)
    plt.plot(t, y, label="Continua")
    plt.stem(t_n, y_disc, linefmt='r-', markerfmt='ro', basefmt=' ', label="Muestreada")
    plt.grid(True)
    plt.legend()
    plt.show()


