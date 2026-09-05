import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import stats

df = pd.read_csv("railguard_benchtop_dataset.csv")
assert len(df) == 2000, f"expected 2000 rows, got {len(df)}"
assert set(df["FlatSize"]) == set(range(0, 46, 5))
assert df.groupby("FlatSize").size().eq(200).all()
flat_sizes = sorted(df['FlatSize'].unique())

kurt_mean = df.groupby('FlatSize')['Kurtosis'].mean().reindex(flat_sizes)
kurt_std  = df.groupby('FlatSize')['Kurtosis'].std().reindex(flat_sizes)
imp_mean  = df.groupby('FlatSize')['ImpulseFactor'].mean().reindex(flat_sizes)
imp_std   = df.groupby('FlatSize')['ImpulseFactor'].std().reindex(flat_sizes)

fig, axes = plt.subplots(1, 2, figsize=(11, 4.3))
axes[0].errorbar(flat_sizes, kurt_mean, yerr=kurt_std, fmt='o-', capsize=4, capthick=1.5, color='tab:blue')
axes[0].set_title('Kurtosis vs Flat Size (n=200 per size)')
axes[0].set_xlabel('Flat size (mm)'); axes[0].set_ylabel('Kurtosis')
axes[0].grid(alpha=0.3)

axes[1].errorbar(flat_sizes, imp_mean, yerr=imp_std, fmt='s-', capsize=4, capthick=1.5, color='tab:orange')
axes[1].set_title('Impulse Factor vs Flat Size (n=200 per size)')
axes[1].set_xlabel('Flat size (mm)'); axes[1].set_ylabel('Impulse Factor')
axes[1].grid(alpha=0.3)
plt.tight_layout()
plt.savefig('figure3_montecarlo_benchtop.png', dpi=150, bbox_inches='tight')

groups_imp = [df[df.FlatSize==s]['ImpulseFactor'].values for s in flat_sizes]
groups_kurt = [df[df.FlatSize==s]['Kurtosis'].values for s in flat_sizes]

f_imp, p_imp = stats.f_oneway(*groups_imp)
f_kurt, p_kurt = stats.f_oneway(*groups_kurt)
r_imp, p_r_imp = stats.pearsonr(df['FlatSize'], df['ImpulseFactor'])
rho_imp, p_rho_imp = stats.spearmanr(df['FlatSize'], df['ImpulseFactor'])
r_kurt, p_r_kurt = stats.pearsonr(df['FlatSize'], df['Kurtosis'])
rho_kurt, p_rho_kurt = stats.spearmanr(df['FlatSize'], df['Kurtosis'])

def cohens_d(a, b):
    na, nb = len(a), len(b)
    pooled_std = np.sqrt(((na-1)*np.var(a, ddof=1) + (nb-1)*np.var(b, ddof=1)) / (na+nb-2))
    return (np.mean(b) - np.mean(a)) / pooled_std

print("=== ANOVA ===")
print(f"ImpulseFactor: F={f_imp:.2f}, p={p_imp:.3e}")
print(f"Kurtosis:      F={f_kurt:.2f}, p={p_kurt:.3e}")
print()
print("=== Correlation with FlatSize (pooled) ===")
print(f"ImpulseFactor: Pearson r={r_imp:.3f} (p={p_r_imp:.2e}), Spearman rho={rho_imp:.3f} (p={p_rho_imp:.2e})")
print(f"Kurtosis:      Pearson r={r_kurt:.3f} (p={p_r_kurt:.2e}), Spearman rho={rho_kurt:.3f} (p={p_rho_kurt:.2e})")
print()
print("=== Cohen's d between adjacent flat sizes (ImpulseFactor) ===")
for i in range(len(flat_sizes)-1):
    d = cohens_d(groups_imp[i], groups_imp[i+1])
    print(f"{flat_sizes[i]:>3} -> {flat_sizes[i+1]:>3} mm: d = {d:7.2f}")
print()
print("=== Cohen's d between adjacent flat sizes (Kurtosis) ===")
for i in range(len(flat_sizes)-1):
    d = cohens_d(groups_kurt[i], groups_kurt[i+1])
    print(f"{flat_sizes[i]:>3} -> {flat_sizes[i+1]:>3} mm: d = {d:7.2f}")
print()
print("=== Summary table (mean +/- std) ===")
summary = df.groupby('FlatSize')[['RMS','Kurtosis','ImpulseFactor']].agg(['mean','std']).round(3)
print(summary)
summary.to_csv('summary_table_benchtop.csv')

print()
print("=== FFT vs STFT vs CWT: correlation strength with FlatSize (proxy for RQ2/H2) ===")
for col in ["FFT_PeakFreq", "STFT_SpectralEntropy", "CWT_SpectralEntropy"]:
    r, p = stats.pearsonr(df['FlatSize'], df[col])
    rho, p2 = stats.spearmanr(df['FlatSize'], df[col])
    f_val, p_anova = stats.f_oneway(*[df[df.FlatSize==s][col].values for s in flat_sizes])
    print(f"{col:25s}: Pearson r={r:7.3f} (p={p:.2e}), Spearman rho={rho:7.3f} (p={p2:.2e}), ANOVA F={f_val:10.1f}")

cwt_mean = df.groupby('FlatSize')['CWT_SpectralEntropy'].mean().reindex(flat_sizes)
cwt_std = df.groupby('FlatSize')['CWT_SpectralEntropy'].std().reindex(flat_sizes)
print()
print("CWT_SpectralEntropy mean +/- std per flat size:")
for s in flat_sizes:
    print(f"  {s:>3} mm: {cwt_mean[s]:.3f} +/- {cwt_std[s]:.3f}")
