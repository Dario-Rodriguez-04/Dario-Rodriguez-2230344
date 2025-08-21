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

def generate_clean_signal(n, fs, f1=8, f2=20):
    Ts = 1 / fs
    return np.sin(2 * np.pi * f1 * n * Ts) + 0.5 * np.sin(2 * np.pi * f2 * n * Ts)

def add_noise_signal(clean_signal, n, fs, noise_freq=50, noise_amp=0.3):
    Ts = 1 / fs
    noise = noise_amp * np.sin(2 * np.pi * noise_freq * n * Ts)
    return clean_signal + noise

def plot_signal_and_spectrum(x, fs, title_prefix):
    N = len(x)
    
    plt.figure(figsize=(15, 10))
    
    plt.subplot(2, 2, 1)
    plt.plot(x[:200], 'b-', linewidth=1)
    plt.title(f'{title_prefix} - Señal Temporal (primeras 200 muestras)')
    plt.xlabel('Muestra (n)')
    plt.ylabel('Amplitud')
    plt.grid(True, alpha=0.3)
    
    plt.subplot(2, 2, 2)
    plt.stem(range(50), x[:50], linefmt='r-', markerfmt='ro', basefmt=' ')
    plt.title(f'{title_prefix} - Señal Discreta (primeras 50 muestras)')
    plt.xlabel('Muestra (n)')
    plt.ylabel('Amplitud')
    plt.grid(True, alpha=0.3)
    
    X = dft_implementation(x)
    frequencies = np.fft.fftfreq(N, 1/fs)
    magnitude = np.abs(X)
    
    positive_freq_idx = frequencies >= 0
    freq_positive = frequencies[positive_freq_idx]
    mag_positive = magnitude[positive_freq_idx]
    
    plt.subplot(2, 2, 3)
    plt.plot(freq_positive, mag_positive, 'g-', linewidth=2)
    plt.title(f'{title_prefix} - Espectro de Magnitud Completo')
    plt.xlabel('Frecuencia (Hz)')
    plt.ylabel('Magnitud')
    plt.grid(True, alpha=0.3)
    plt.xlim(0, fs/2)
    
    plt.subplot(2, 2, 4)
    plt.plot(freq_positive, mag_positive, 'g-', linewidth=2)
    plt.title(f'{title_prefix} - Espectro de Magnitud (0-60 Hz)')
    plt.xlabel('Frecuencia (Hz)')
    plt.ylabel('Magnitud')
    plt.grid(True, alpha=0.3)
    plt.xlim(0, 60)
    
    plt.tight_layout()
    plt.show()
    
    return X, frequencies, magnitude

def find_peaks_with_noise(magnitude, frequencies, threshold=0.15):
    max_magnitude = np.max(magnitude)
    
    peak_indices = []
    for i in range(2, len(magnitude) - 2):
        if (magnitude[i] > magnitude[i-1] and 
            magnitude[i] > magnitude[i+1] and 
            magnitude[i] > threshold * max_magnitude):
            peak_indices.append(i)
    
    peak_freqs = frequencies[peak_indices]
    peak_amps = magnitude[peak_indices]
    
    return peak_freqs, peak_amps

def compare_spectra(clean_mag, noisy_mag, frequencies):
    positive_freq_idx = frequencies >= 0
    freq_positive = frequencies[positive_freq_idx]
    clean_mag_pos = clean_mag[positive_freq_idx]
    noisy_mag_pos = noisy_mag[positive_freq_idx]
    
    plt.figure(figsize=(12, 8))
    
    plt.subplot(2, 1, 1)
    plt.plot(freq_positive, clean_mag_pos, 'b-', linewidth=2, label='Señal Limpia')
    plt.plot(freq_positive, noisy_mag_pos, 'r-', linewidth=2, alpha=0.7, label='Señal con Ruido')
    plt.title('Comparación de Espectros - Vista Completa')
    plt.xlabel('Frecuencia (Hz)')
    plt.ylabel('Magnitud')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.xlim(0, 128)
    
    plt.subplot(2, 1, 2)
    plt.plot(freq_positive, clean_mag_pos, 'b-', linewidth=2, label='Señal Limpia')
    plt.plot(freq_positive, noisy_mag_pos, 'r-', linewidth=2, alpha=0.7, label='Señal con Ruido')
    plt.title('Comparación de Espectros - Zoom (0-60 Hz)')
    plt.xlabel('Frecuencia (Hz)')
    plt.ylabel('Magnitud')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.xlim(0, 60)
    
    plt.tight_layout()
    plt.show()

def mostrar():
    print("=== Análisis de Señales Discretas con Ruido usando DFT ===")
    
    fs = 256
    duration = 6
    N = int(fs * duration)
    delta_f = fs / N
    
    f1 = 8
    f2 = 20
    noise_freq = 50
    noise_amp = 0.3
    
    print(f"Parámetros de la señal:")
    print(f"Frecuencia de muestreo: {fs} Hz")
    print(f"Duración: {duration} s")
    print(f"Número de muestras: {N}")
    print(f"Resolución en frecuencia: {delta_f:.4f} Hz")
    print(f"Frecuencias de la señal: f1 = {f1} Hz, f2 = {f2} Hz")
    print(f"Frecuencia del ruido: {noise_freq} Hz")
    
    n = np.arange(N)
    
    print("\n1. Generando señal limpia...")
    clean_signal = generate_clean_signal(n, fs, f1, f2)
    
    print("2. Añadiendo ruido...")
    noisy_signal = add_noise_signal(clean_signal, n, fs, noise_freq, noise_amp)
    
    print("3. Analizando señal limpia...")
    X_clean, freq_clean, mag_clean = plot_signal_and_spectrum(clean_signal, fs, "Señal Limpia")
    
    print("4. Analizando señal con ruido...")
    X_noisy, freq_noisy, mag_noisy = plot_signal_and_spectrum(noisy_signal, fs, "Señal con Ruido")
    
    print("5. Identificando picos espectrales...")
    
    peaks_clean, amps_clean = find_peaks_with_noise(mag_clean, freq_clean, 0.1)
    positive_clean = peaks_clean >= 0
    print(f"\nPicos en señal limpia (frecuencias positivas):")
    for i, (freq, amp) in enumerate(zip(peaks_clean[positive_clean], amps_clean[positive_clean])):
        print(f"  Pico {i+1}: {freq:.3f} Hz, Amplitud: {amp:.1f}")
    
    peaks_noisy, amps_noisy = find_peaks_with_noise(mag_noisy, freq_noisy, 0.1)
    positive_noisy = peaks_noisy >= 0
    print(f"\nPicos en señal con ruido (frecuencias positivas):")
    for i, (freq, amp) in enumerate(zip(peaks_noisy[positive_noisy], amps_noisy[positive_noisy])):
        print(f"  Pico {i+1}: {freq:.3f} Hz, Amplitud: {amp:.1f}")
    
    print("6. Comparando espectros...")
    compare_spectra(mag_clean, mag_noisy, freq_clean)
    
    print("\n=== Análisis completado ===")
    print("Observaciones:")
    print("- La señal limpia muestra picos claros en 8 Hz y 20 Hz")
    print("- El ruido añade un pico adicional en 50 Hz")
    print("- La resolución permite distinguir las frecuencias individuales")
    print(f"- Resolución mínima distinguible: {delta_f:.4f} Hz")
