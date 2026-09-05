# RailGuard

Physics-based railway wheel-flat vibration simulation, Monte Carlo dataset generation, and signal-feature analysis for a planned low-cost benchtop detector.

## Project status

**This is a simulation-only study. No physical hardware has been built. All results in the paper are derived from the code and dataset in this repository.**

The proposed test bench is future work. The repository must not be presented as evidence of real-world detector performance.



## Repository contents

```text
RailGuard/
├── README.md
├── LICENSE
├── LICENSE-DATA
├── CITATION.cff
├── requirements.txt
├── .gitignore
├── paper/
│   └── RailGuard Physics-Based Simulation and Experimental Design for Railway Wheel-Flat.pdf
├── code/
│   ├── sim_lib2.py
│   ├── gen_chunk.py
│   ├── combine_chunks.py
│   ├── analyze_benchtop.py
│   └── make_fig_cwt.py
├── data/
│   ├── raw_chunks/
│   │   ├── chunk_0.csv
│   │   ├── chunk_5.csv
│   │   └── ...
│   ├── railguard_benchtop_dataset.csv
│   └── DATA_DICTIONARY.md
├── results/
│   └── summary_table_benchtop.csv
└── figures/
    ├── figure1_schematic.svg
    ├── figure2_healthy_vs_defective.png
    └── figure3_montecarlo_benchtop.png
```

## Reproduce the study from scratch

Create and activate a Python virtual environment first if desired. Then run:

```bash
pip install -r requirements.txt

python code/gen_chunk.py 0
python code/gen_chunk.py 5
python code/gen_chunk.py 10
python code/gen_chunk.py 15
python code/gen_chunk.py 20
python code/gen_chunk.py 25
python code/gen_chunk.py 30
python code/gen_chunk.py 35
python code/gen_chunk.py 40
python code/gen_chunk.py 45

python code/combine_chunks.py
python code/analyze_benchtop.py
python code/make_fig_cwt.py
```

Expected outputs:

- ten chunk files in `data/raw_chunks/`, with 200 rows per flat size;
- `data/railguard_benchtop_dataset.csv`, with 2,000 rows;
- `results/summary_table_benchtop.csv`;
- regenerated analysis figures in `figures/`.

## Random seeds

`gen_chunk.py` uses the following seed for each flat-size chunk:

```python
np.random.seed(42 + size)
```

For the flat sizes `0, 5, 10, ..., 45`, this makes the Monte Carlo sampling deterministic and reproducible when the same pinned library versions are used.

## Reproducibility environment

The dependency versions recorded for this release are:

| Software | Version |
|---|---:|
| Python | 3.12.13 |
| NumPy | 2.3.5 |
| SciPy | 1.17.0 |
| pandas | 2.2.3 |
| Matplotlib | 3.10.8 |
| PyWavelets | 1.9.0 |

The same versions are pinned in `requirements.txt`. PyWavelets is used with the complex Morlet wavelet `cmor1.5-1.0` and 48 frequencies from 50 to 3,000 Hz.

## Dataset structure

The final dataset contains **2,000 simulation rows**: 200 runs for each of ten wheel-flat sizes (`0, 5, 10, ..., 45 mm`) across four rolling speeds. It contains **14 extracted signal features**, together with the run-condition and parameter columns written by the generation script.

The 14 features are RMS, peak amplitude, crest factor, kurtosis, skewness, shape factor, impulse factor, FFT spectral entropy, three normalized band-energy features, FFT peak frequency, STFT spectral entropy, and CWT spectral entropy. Definitions and units are listed in [`data/DATA_DICTIONARY.md`](data/DATA_DICTIONARY.md).

## Paper

The current manuscript is available at [`paper/RailGuard Physics-Based Simulation and Experimental Design for Railway Wheel-Flat.pdf`](paper/RailGuard Physics-Based Simulation and Experimental Design for Railway Wheel-Flat.pdf).

After publication, add the article DOI here. After archiving the repository on Zenodo, also add the Zenodo DOI to this README and to `CITATION.cff`.

## Licenses

- **Code:** MIT License. See [`LICENSE`](LICENSE).
- **Dataset and derived CSV results:** Creative Commons Attribution 4.0 International (CC BY 4.0). See [`LICENSE-DATA`](LICENSE-DATA).

The manuscript may also be subject to the journal's publication terms. Third-party references and cited works remain under their respective rights.

## AI-use disclosure

AI-assisted tools were used to help debug code and refine figure presentation. All modelling choices, generated outputs, numerical results, citations, and final repository contents were reviewed and approved by the author.

## Citation

GitHub will display citation information from [`CITATION.cff`](CITATION.cff). Until article and Zenodo DOIs are available, cite this release as:

> Nadyr, V. (2026). *RailGuard: Railway Wheel-Flat Vibration Simulation and Feature Analysis* (Version 1.0.0) [Computer software and data set].

## Author

Valiollakh Nadyr  
Nazarbayev Intellectual School of Science and Mathematics  
Nauryzbay District, Almaty, Kazakhstan
