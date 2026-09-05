# RailGuard Data Dictionary

The final file `railguard_benchtop_dataset.csv` contains one row per simulation. The released dataset should contain 2,000 rows: 200 repetitions for each flat size from 0 to 45 mm in 5 mm steps.

## Extracted signal features

| Column | Meaning | Unit |
|---|---|---|
| `RMS` | Root mean square of the acceleration signal | m/s² |
| `Peak` | Largest absolute acceleration value | m/s² |
| `CrestFactor` | Peak divided by RMS | dimensionless |
| `Kurtosis` | Fourth standardized moment of the signal | dimensionless |
| `Skewness` | Third standardized moment of the signal | dimensionless |
| `ShapeFactor` | RMS divided by mean absolute signal value | dimensionless |
| `ImpulseFactor` | Peak divided by mean absolute signal value | dimensionless |
| `SpectralEntropy` | Shannon entropy of the normalized FFT/Welch power distribution | bits |
| `BandEnergy_0_200` | Normalized spectral energy from 0 to 200 Hz | dimensionless |
| `BandEnergy_200_1000` | Normalized spectral energy from 200 to 1,000 Hz | dimensionless |
| `BandEnergy_1000_3000` | Normalized spectral energy from 1,000 to 3,000 Hz | dimensionless |
| `FFT_PeakFreq` | Frequency with the largest FFT magnitude | Hz |
| `STFT_SpectralEntropy` | Mean spectral entropy across STFT time frames | bits |
| `CWT_SpectralEntropy` | Spectral entropy derived from PyWavelets CWT energy | bits |

## Run-condition and model-parameter columns

The generation script should also write the flat size, rolling speed, repetition identifier, randomized physical parameters, and sensor-noise setting used for each row. Preserve the exact column names emitted by `gen_chunk.py` and add them to this table before the public release if they are not already documented in the script.

## Dataset checks before release

- Exactly 2,000 rows in the combined CSV.
- Exactly 200 rows for each flat size.
- Flat sizes: 0, 5, 10, 15, 20, 25, 30, 35, 40, and 45 mm.
- No missing values in the 14 feature columns.
- Units and names match the generation and analysis scripts.
