import numpy as np
import matplotlib.pyplot as plt
from src.utils.Grapher import continuous_plotter, discrete_plotter

def dft_implementation(x):
    N = len(x)
    X = np.zeros(N, dtype=complex)
    
    for k in range(N):
        for n in range(N):
            X[k] += x[n] * np.exp(-2j * np.pi * k * n / N)
    
    return X

def calculate_frequency_resolution(fs, N):
    return fs / N

def generate_modulated_signal(t, fm=0.5, fc=8, m=0.5):
    modulator = 1 + m * np.cos(2 * np.pi * fm * t)
    carrier = np.sin(2 * np.pi * fc * t)
    return modulator * carrier

def find_spectral_peaks(X, frequencies, threshold=0.1):
    magnitude = np.abs(X)
    max_magnitude = np.max(magnitude)
    
    peak_indices = []
    for i in range(1, len(magnitude) - 1):
        if (magnitude[i] > magnitude[i-1] and 
            magnitude[i] > magnitude[i+1] and 
            magnitude[i] > threshold * max_magnitude):
            peak_indices.append(i)
    
    peak_freqs = frequencies[peak_indices]
    peak_amps = magnitude[peak_indices]
    
    return peak_freqs, peak_amps

def mostrar():
    print("=== Análisis de la Transformada de Fourier Discreta ===")
    print("Señal: x(t) = [1 + m·cos(2π·fm·t)]·sin(2π·fc·t)")
    print("Parámetros: fm = 0.5 Hz, fc = 8 Hz, m = 0.5")
    
    fm = 0.5
    fc = 8
    m = 0.5
    
    fs = 50
    T = 4
    N = int(fs * T)
    
    t_continuous = np.linspace(0, T, 1000)
    x_continuous = generate_modulated_signal(t_continuous, fm, fc, m)
    
    t_discrete = np.arange(N) / fs
    x_discrete = generate_modulated_signal(t_discrete, fm, fc, m)
    
    delta_f = calculate_frequency_resolution(fs, N)
    print(f"\nParámetros de muestreo:")
    print(f"Frecuencia de muestreo: {fs} Hz")
    print(f"Número de muestras: {N}")
    print(f"Resolución en frecuencia: {delta_f:.3f} Hz")
    
    print("\n1. Visualizando señal continua...")
    continuous_plotter(t_continuous, x_continuous, 
                      "Señal Modulada Continua x(t)")
    
    print("2. Visualizando señal muestreada...")
    discrete_plotter(t_discrete, x_discrete, 
                    "Señal Modulada Muestreada x[n]")
    
    print("3. Calculando DFT...")
    X = dft_implementation(x_discrete)
    
    # Vector de frecuencias
    frequencies = np.fft.fftfreq(N, 1/fs)
    
    # Magnitud del espectro
    magnitude = np.abs(X)
    
    # Mostrar espectro de magnitud (solo frecuencias positivas)
    positive_freq_idx = frequencies >= 0
    freq_positive = frequencies[positive_freq_idx]
    mag_positive = magnitude[positive_freq_idx]
    
    plt.figure(figsize=(12, 8))
    
    # Subplot 1: Espectro completo
    plt.subplot(2, 1, 1)
    plt.plot(freq_positive, mag_positive, 'b-', linewidth=2)
    plt.title('Espectro de Magnitud de la DFT')
    plt.xlabel('Frecuencia (Hz)')
    plt.ylabel('Magnitud')
    plt.grid(True, alpha=0.3)
    plt.xlim(0, fs/2)
    
    # Subplot 2: Zoom en la región de interés
    plt.subplot(2, 1, 2)
    plt.plot(freq_positive, mag_positive, 'b-', linewidth=2)
    plt.title('Espectro de Magnitud (Zoom en región de interés)')
    plt.xlabel('Frecuencia (Hz)')
    plt.ylabel('Magnitud')
    plt.grid(True, alpha=0.3)
    plt.xlim(0, 15)
    
    plt.tight_layout()
    plt.show()
    
    print("4. Identificando picos espectrales...")
    peak_freqs, peak_amps = find_spectral_peaks(X, frequencies)
    
    positive_peaks_idx = peak_freqs >= 0
    peak_freqs_positive = peak_freqs[positive_peaks_idx]
    peak_amps_positive = peak_amps[positive_peaks_idx]
    
    print(f"\nPicos espectrales detectados (frecuencias positivas):")
    for i, (freq, amp) in enumerate(zip(peak_freqs_positive, peak_amps_positive)):
        print(f"Pico {i+1}: Frecuencia = {freq:.3f} Hz, Amplitud = {amp:.2f}")
    
    print(f"\nAnálisis teórico esperado:")
    print(f"- Componente DC: 0 Hz")
    print(f"- Bandas laterales inferiores: {fc-fm:.1f} Hz")
    print(f"- Portadora: {fc:.1f} Hz") 
    print(f"- Bandas laterales superiores: {fc+fm:.1f} Hz")
    
    plt.figure(figsize=(10, 6))
    phase = np.angle(X[positive_freq_idx])
    plt.plot(freq_positive, phase, 'g-', linewidth=2)
    plt.title('Espectro de Fase de la DFT')
    plt.xlabel('Frecuencia (Hz)')
    plt.ylabel('Fase (radianes)')
    plt.grid(True, alpha=0.3)
    plt.xlim(0, 15)
    plt.show()
    
    print("\n=== Análisis completado ===")
