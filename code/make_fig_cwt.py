import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.signal import welch, stft
from sim_lib import simulate_wheel_flat, morlet_cwt_coefficients, MW, MB, KS, CS, KH, FS

np.random.seed(42)
t_h, a_h = simulate_wheel_flat(0, 10, 0.1, MW, MB, KS, CS, KH)
t_d, a_d = simulate_wheel_flat(10, 10, 0.1, MW, MB, KS, CS, KH)

fig, axes = plt.subplots(2, 4, figsize=(17, 7))

for row, (t, sig, label, color) in enumerate([
    (t_h, a_h, "Healthy (0 mm flat)", "b"),
    (t_d, a_d, "Defective (10 mm flat)", "r"),
]):
    # Time domain
    axes[row, 0].plot(t, sig, color=color, linewidth=0.6)
    axes[row, 0].set_title(f"{label}\nTime Domain")
    axes[row, 0].set_xlabel("Time (s)")
    axes[row, 0].set_ylabel("Acceleration (m/s^2)")

    # FFT (Welch PSD)
    f_w, p_w = welch(sig, fs=FS, nperseg=1024)
    axes[row, 1].semilogy(f_w, p_w, color=color)
    axes[row, 1].set_title("Welch Power Spectrum")
    axes[row, 1].set_xlabel("Frequency (Hz)")
    axes[row, 1].set_ylabel("PSD")
    axes[row, 1].set_xlim([0, 2000])

    # STFT
    f_s, t_s, Z = stft(sig, fs=FS, nperseg=256)
    im1 = axes[row, 2].pcolormesh(t_s, f_s, np.abs(Z), shading="gouraud", cmap="viridis")
    axes[row, 2].set_title("STFT Spectrogram")
    axes[row, 2].set_xlabel("Time (s)")
    axes[row, 2].set_ylabel("Frequency (Hz)")
    axes[row, 2].set_ylim([0, 2000])
    fig.colorbar(im1, ax=axes[row, 2], label="Magnitude")

    # CWT scalogram (same implementation used for CWT_SpectralEntropy feature)
    coeffs, freqs_hz = morlet_cwt_coefficients(sig, FS)
    im2 = axes[row, 3].pcolormesh(t, freqs_hz, np.abs(coeffs), shading="gouraud", cmap="viridis")
    axes[row, 3].set_yscale("log")
    axes[row, 3].set_title("CWT Scalogram (Morlet)")
    axes[row, 3].set_xlabel("Time (s)")
    axes[row, 3].set_ylabel("Frequency (Hz)")
    fig.colorbar(im2, ax=axes[row, 3], label="Magnitude")

plt.tight_layout()
plt.savefig("figure_cwt_comparison.png", dpi=150, bbox_inches="tight")
print("saved")
