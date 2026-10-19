# Quantitative Neuropathology & Progression Modeling in Alzheimer’s Disease: Multi-Cohort Analysis of Continuous Pseudo-Progression Scores (CPS)

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Data Source: SEA-AD](https://img.shields.io/badge/Data-SEA--AD%20Atlas-green.svg)](https://data.sea-ad.org/)

---

## 📌 Project Overview

Traditional staging systems for Alzheimer’s Disease (AD) rely on discrete clinical or neuropathological categorizations (e.g., Braak staging, CERAD scores), which often fail to capture the continuous, non-linear spectrum of neurodegenerative progression. The **Seattle Alzheimer’s Disease Brain Cell Atlas (SEA-AD)** introduced the **Continuous Pseudo-progression Score (CPS)**—a continuous metric derived from quantitative neuropathology using Bayesian disease pseudo-progression modeling. 

This repository presents a rigorous computational and statistical framework to evaluate CPS distributions, regional pathology progression, and cross-dataset metrics across three flagship SEA-AD studies:
* **Travaglini et al. (2026)**: Global and local region-specific CPS ($A\beta$ vs. $pTau$).
* **Kana et al. (2026)**: Comparative analysis of immunohistochemistry-derived CPS metrics (AT8 for $pTau$ vs. 6E10 for $A\beta$).
* **Gabitto et al. (2024)**: Donor-level baseline pseudo-progression scores.

---

## 🔬 Key Scientific Questions & Analytical Objectives

1. **Selective Vulnerability & Spatial Pathology:** How does local pathological burden (`CPS_Local`) vary across cortical and subcortical regions (e.g., Middle Temporal Gyrus `MTG`, Hippocampus `HIP`, Entorhinal Cortex `MEC`, Visual Cortex `V1C`) compared to global burden (`CPS_Global`)?
2. **Proteinopathy Dissociation:** Do Amyloid-$\beta$ (`CPS_ABeta` / `6E10`) and hyperphosphorylated Tau (`CPS_pTau` / `AT8`) exhibit distinct trajectory distributions across pseudo-progression space?
3. **Robust Statistical Inference:** How do non-parametric distribution comparisons and bootstrap estimation validate regional heterogeneity without making strict Gaussian assumptions?

---

## 🛠️ Methodology & Statistical Pipeline

### 1. Data Integrity & Automated Sanity Checks
* **Range Validation:** Bounded sanity verification ($0.0 \le \text{CPS} \le 1.0$) across all datasets.
* **Completeness & Duplication:** Null value detection and strict donor-ID uniqueness checks per brain region.
* **Structural Consistency:** Verification of brain region codes (`MTG`, `STG`, `HIP`, `DFC`, `V1C`, `MEC`, `FI`, `AnG`, `ITG`).

### 2. Distributional & Exploratory Data Analysis (EDA)
* **Study-Level EDA:** Global boxplots and Kernel Density Estimation (KDE) distributions across study methods (`Travaglini 2026`, `Kana 2026`, `Gabitto 2024`).
* **Intra-Method Breakdown:** Region-stratified box plots comparing local vs. global pathology distributions.

### 3. Non-Parametric Hypothesis Testing & Bootstrapping
* **Paired & Unpaired Wilcoxon Tests:** Wilcoxon signed-rank tests for matched regional metrics (e.g., `CPS_Local_ABeta` vs. `CPS_Local_pTau` within donor) and Mann-Whitney U tests across regions.
* **Effect Size Metrics:** Calculation of median difference ($\Delta \text{Median}$) as a robust measure of location shift.
* **Bootstrap Resampling:** 1,000–10,000 iteration bias-corrected bootstrap estimation to compute 95% Confidence Intervals (95% CI) for medians and paired differences.

---

## 📁 Repository Structure

```text
.
├── data/
│   └── sea-ad_global_and_local_cps_050126.xlsx   # SEA-AD primary dataset
├── notebooks/
│   ├── 01_data_validation_and_cleaning.ipynb    # Automated security & range checks
│   ├── 02_exploratory_data_analysis.ipynb       # Regional & methodological boxplots
│   └── 03_statistical_inference_bootstrap.ipynb # Wilcoxon tests & 95% Bootstrap CIs
├── src/
│   ├── __init__.py
│   ├── data_loader.py                           # Multi-tab data ingestion pipeline
│   ├── stats.py                                 # Custom bootstrapping & non-parametric tests
│   └── visualization.py                         # Publication-ready Seaborn/Matplotlib style
├── outputs/
│   ├── figures/                                 # Generated high-resolution plots (PNG/SVG)
│   └── tables/                                  # Statistical summary export (CSV)
├── requirements.txt                             # Python dependencies
├── LICENSE                                      # MIT License
└── README.md                                    # Project documentation

📊 Summary of Findings (Dataset Overview)
| Study Cohort | Donors (n) | Primary Metrics Analyzed | Core Analytical Focus |
|---|---|---|---|
| Travaglini 2026 | 84 (632 tissue samples) | CPS_Global, CPS_Local, A\beta, pTau | Regional vulnerability across 9 brain regions (HIP, MEC, V1C, etc.) |
| Kana 2026 | 41 | CPS, CPS_AT8 (pTau), CPS_6E10 (A\beta) | Immunohistochemistry marker concordance |
| Gabitto 2024 | 84 | CPS | Benchmark single-cell trajectory donor cohort |
🚀 Quick Start & Installation
Prerequisites
 * Python 3.10 or higher
 * pip package manager
Installation
 * Clone the repository:
   git clone [https://github.com/your-username/emory-sea-ad-cps-analysis.git](https://github.com/your-username/emory-sea-ad-cps-analysis.git)
cd emory-sea-ad-cps-analysis

 * Create and activate a virtual environment:
   python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

 * Install dependencies:
   pip install -r requirements.txt

 * Run the pipeline:
   python src/data_loader.py
python src/stats.py

🧪 Dependencies
 * Pandas – Data wrangling and tabular processing
 * NumPy – High-performance array operation and bootstrapping
 * SciPy – Non-parametric statistical testing (scipy.stats)
 * Matplotlib & Seaborn – Publication-ready data visualization
 * OpenPyXL – Excel sheet parsing
 * Data Credit: All data sourced from the Seattle Alzheimer’s Disease Brain Cell Atlas (SEA-AD).
This repository was built as an independent computational biology project demonstrating workflow reproducibility, rigorous non-parametric statistics, and data processing skills applied to neurodegenerative pathology datasets.

