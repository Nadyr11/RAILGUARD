import numpy as np
from scipy.integrate import solve_ivp
from scipy.stats import kurtosis, skew
from scipy.signal import welch, stft

MW, MB, KS, CS, KH, R = 0.7, 2.0, 2e6, 5000, 1.5e8, 0.060
G = 9.81  
FS = 10000
T = 0.6  

def simulate_wheel_flat(flat_length_mm, speed_mps, noise_lvl, mw, mb, ks, cs, kh, R=R, T=T, fs=FS, g=G):
    """
    2-DOF wheel-bogie model with a unilateral Hertzian contact law,
    Fc = kh * max(delta, 0)^1.5, where the contact deflection
        delta(t) = delta_static - uw(t) - p(theta(t))
    is driven by (a) the wheel's own dynamic displacement uw(t) and (b) a
    continuous geometric flat-depth profile p(theta), rather than by a
    hand-set multi-state switch. p(theta) is derived from the actual chord
    geometry of a flat of length flat_length_mm on a wheel of radius R:
    within the flat's half-angle alpha_h of its center, the wheel's local
    rolling radius is R*cos(alpha_h)/cos(phi) (phi = angle from flat
    center), which is less than R; p(theta) = R minus that local radius.

    States (uw, vw, ub, vb) are wheel/bogie displacement and velocity
    measured RELATIVE TO the static equilibrium position under gravity
    (found by solving Fc(delta_static) = (mw+mb)*g for delta_static). This
    substitution removes the m*g terms from the equations of motion below
    algebraically (they cancel against the equilibrium condition), so
    gravity does not appear explicitly, but unlike the previous version
    of this model -- the simulation genuinely starts at static equilibrium:
    the flat is placed at theta=pi so it is away from the contact point at
    t=0 (theta=0), giving delta(0)=delta_static, Fc(0)=Fc_eq, and zero net
    force on both masses at the start.
    """
    L = flat_length_mm / 1000.0
    alpha_h = np.arcsin(min(L / (2 * R), 0.999)) if L > 0 else 0.0
    omega = speed_mps / R

    total_weight = (mw + mb) * g
    delta_static = (total_weight / kh) ** (2.0 / 3.0)
    Fc_eq = total_weight

    def flat_depth(theta):
        phi = theta - np.pi
        phi = (phi + np.pi) % (2 * np.pi) - np.pi
        if alpha_h <= 0 or abs(phi) >= alpha_h:
            return 0.0
        return R - R * np.cos(alpha_h) / np.cos(phi)

    def dynamics(t, y):
        uw, vw, ub, vb = y
        theta = (omega * t) % (2 * np.pi)
        p = flat_depth(theta)
        delta = delta_static - uw - p
        fc = kh * max(delta, 0.0) ** 1.5
        d_fs = ks * (uw - ub) + cs * (vw - vb)
        aw = (fc - Fc_eq - d_fs) / mw
        ab = d_fs / mb
        return [vw, aw, vb, ab]

    t_eval = np.linspace(0, T, int(T * fs))
    sol = solve_ivp(dynamics, (0, T), [0, 0, 0, 0], t_eval=t_eval, method='RK45', rtol=1e-6, atol=1e-8)
    accel = []
    for i in range(len(sol.t)):
        uw, vw, ub, vb = sol.y[:, i]
        theta = (omega * sol.t[i]) % (2 * np.pi)
        p = flat_depth(theta)
        delta = delta_static - uw - p
        fc = kh * max(delta, 0.0) ** 1.5
        d_fs = ks * (uw - ub) + cs * (vw - vb)
        aw = (fc - Fc_eq - d_fs) / mw
        accel.append(aw)
    accel = np.array(accel) + np.random.normal(0, noise_lvl, len(sol.t))
    return sol.t, accel

import pywt


def morlet_cwt_coefficients(
    signal,
    fs,
    freq_min=50,
    freq_max=3000,
    n_scales=48
):
    

   
    wavelet = "cmor1.5-1.0"

  
    target_freqs = np.geomspace(
        freq_min,
        freq_max,
        n_scales
    )

  
    central_frequency = pywt.central_frequency(wavelet)

    
    scales = central_frequency * fs / target_freqs

    coefficients, frequencies = pywt.cwt(
        signal,
        scales,
        wavelet,
        sampling_period=1.0 / fs,
        method="fft"
    )

    return coefficients, frequencies


def morlet_cwt_entropy(
    signal,
    fs,
    freq_min=50,
    freq_max=3000,
    n_scales=48
):
  

    coefficients, _ = morlet_cwt_coefficients(
        signal,
        fs,
        freq_min,
        freq_max,
        n_scales
    )

    energy = np.sum(np.abs(coefficients) ** 2, axis=1)

    total_energy = np.sum(energy)

    if total_energy <= 0:
        return 0.0

    probability = energy / total_energy

    entropy = -np.sum(
        probability * np.log2(probability + 1e-12)
    )

    return float(entropy)


def extract_features(signal, fs=FS):
    abs_sig = np.abs(signal)
    rms = np.sqrt(np.mean(signal ** 2))
    peak = np.max(abs_sig)
    mean_abs = np.mean(abs_sig)
    crest_factor = peak / rms if rms else 0
    kurt = kurtosis(signal) + 3
    skewness = skew(signal)
    shape_factor = rms / mean_abs if mean_abs else 0
    impulse_factor = peak / mean_abs if mean_abs else 0

    freqs, psd = welch(signal, fs=fs, nperseg=min(1024, len(signal) // 4))
    psd_norm = psd / np.sum(psd) if np.sum(psd) > 0 else psd
    spectral_entropy = -np.sum(psd_norm * np.log2(psd_norm + 1e-12))

    b1 = np.sum(psd[(freqs >= 0) & (freqs < 200)])
    b2 = np.sum(psd[(freqs >= 200) & (freqs < 1000)])
    b3 = np.sum(psd[(freqs >= 1000) & (freqs < 3000)])
    tot = b1 + b2 + b3

    fft_vals = np.fft.rfft(signal)
    fft_freqs = np.fft.rfftfreq(len(signal), 1 / fs)
    fft_mag = np.abs(fft_vals)
    pos = fft_freqs > 0
    peak_freq = fft_freqs[pos][np.argmax(fft_mag[pos])] if np.any(pos) else 0

    nperseg_stft = max(8, min(256, len(signal) // 4))
    _, _, Zxx = stft(signal, fs=fs, nperseg=nperseg_stft)
    power_psd = np.mean(np.abs(Zxx) ** 2, axis=1)
    ppn = power_psd / np.sum(power_psd) if np.sum(power_psd) > 0 else power_psd
    stft_entropy = -np.sum(ppn * np.log2(ppn + 1e-12))

    cwt_entropy = morlet_cwt_entropy(signal, fs)

    return {
        "RMS": rms, "Peak": peak, "CrestFactor": crest_factor, "Kurtosis": kurt,
        "Skewness": skewness, "ShapeFactor": shape_factor, "ImpulseFactor": impulse_factor,
        "SpectralEntropy": spectral_entropy,
        "BandEnergy_0_200Hz": b1 / tot if tot > 0 else 0,
        "BandEnergy_200_1000Hz": b2 / tot if tot > 0 else 0,
        "BandEnergy_1000_3000Hz": b3 / tot if tot > 0 else 0,
        "FFT_PeakFreq": peak_freq,
        "STFT_SpectralEntropy": stft_entropy,
        "CWT_SpectralEntropy": cwt_entropy,
    }

