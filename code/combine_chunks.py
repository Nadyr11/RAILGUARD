import os
import glob
import numpy as np
import pandas as pd

base_dir = r"C:\Projects\RAILGUARD\CODE\code"
chunk_files = sorted(glob.glob(os.path.join(base_dir, "chunk_*.csv")))

df = pd.concat([pd.read_csv(f) for f in chunk_files], ignore_index=True)

# 1. Структурные проверки
assert len(df) == 2000, f"Expected 2000 rows, got {len(df)}"
assert set(df["FlatSize"]) == set(range(0, 46, 5))
assert set(df["Speed"]) == {5, 10, 15, 20}
assert df.groupby("FlatSize").size().eq(200).all()
assert df.groupby(["FlatSize", "Speed"]).size().eq(50).all()
assert df.isnull().sum().sum() == 0, "Dataset contains missing values!"

# 2. Математические проверки
assert np.isfinite(df.select_dtypes(include=np.number)).all().all(), "Dataset contains NaN or Inf!"
assert (df["CWT_SpectralEntropy"] >= 0).all(), "Entropy cannot be negative!"
assert (df["CWT_SpectralEntropy"] <= np.log2(48) + 1e-9).all(), "Entropy exceeds max theoretical value log2(48)!"

# Сохранение готового датасета
out_path = os.path.join(base_dir, "railguard_benchtop_dataset.csv")
df.to_csv(out_path, index=False)
print(f"Dataset successfully built and verified: {out_path}")
