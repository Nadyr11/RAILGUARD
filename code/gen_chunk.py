import sys
import time
import numpy as np
import pandas as pd
from sim_lib import simulate_wheel_flat, extract_features, MW, MB, KS, CS, KH, R, FS

size = int(sys.argv[1])
np.random.seed(42 + size)  # deterministic but distinct per chunk; documented in README

speeds = [5, 10, 15, 20]
repeats = 50
rows = []
t0 = time.time()
for speed in speeds:
    for rep in range(repeats):
        mw_v = MW * np.random.uniform(0.9, 1.1)
        mb_v = MB * np.random.uniform(0.9, 1.1)
        ks_v = KS * np.random.uniform(0.9, 1.1)
        cs_v = CS * np.random.uniform(0.9, 1.1)
        kh_v = KH * np.random.uniform(0.9, 1.1)
        noise_v = np.random.uniform(0.05, 0.2)
        _, sig = simulate_wheel_flat(size, speed, noise_v, mw_v, mb_v, ks_v, cs_v, kh_v)
        feats = extract_features(sig)
        feats.update({"FlatSize": size, "Speed": speed, "Repeat": rep})
        rows.append(feats)

df = pd.DataFrame(rows)
cols = ["FlatSize", "Speed", "Repeat", "RMS", "Peak", "CrestFactor", "Kurtosis", "Skewness",
        "ShapeFactor", "ImpulseFactor", "SpectralEntropy", "BandEnergy_0_200Hz",
        "BandEnergy_200_1000Hz", "BandEnergy_1000_3000Hz", "FFT_PeakFreq",
        "STFT_SpectralEntropy", "CWT_SpectralEntropy"]
df = df[cols]
df.to_csv(f"chunk_{size}.csv", index=False)
print(f"flat_size={size}: {len(df)} rows in {time.time()-t0:.1f}s")
