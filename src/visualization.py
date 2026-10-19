"""
Visualization Module for SEA-AD CPS Analysis.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os

class CPSVisualizer:
    """Generates publication-grade figures for global and regional CPS evaluations."""

    def __init__(self, output_dir: str = "outputs/figures"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self._set_publication_style()

    def _set_publication_style(self):
        """Configures clean aesthetic settings for academic plotting."""
        sns.set_theme(style="ticks", font="sans-serif")
        plt.rcParams['figure.dpi'] = 300
        plt.rcParams['axes.labelsize'] = 12
        plt.rcParams['axes.titlesize'] = 14
        plt.rcParams['xtick.labelsize'] = 10
        plt.rcParams['ytick.labelsize'] = 10

    def plot_study_comparison(self, datasets: dict) -> None:
        """Plots global CPS distribution across the three distinct studies."""
        fig, ax = plt.subplots(figsize=(8, 6))
        
        plot_data = []
        for study_name, df in datasets.items():
            cps_col = 'CPS_Global' if 'CPS_Global' in df.columns else 'CPS'
            temp_df = df[['Donor ID', cps_col]].copy()
            temp_df['Study'] = study_name
            temp_df.rename(columns={cps_col: 'CPS'}, inplace=True)
            plot_data.append(temp_df)
            
        combined_df = pd.concat(plot_data, ignore_index=True)
        
        sns.boxplot(data=combined_df, x='Study', y='CPS', palette='Set2', ax=ax, width=0.4, fliersize=3)
        sns.stripplot(data=combined_df, x='Study', y='CPS', color='black', alpha=0.3, jitter=0.2, size=4, ax=ax)
        
        ax.set_title("Cross-Study Comparison of Continuous Pseudo-Progression Scores", pad=15, weight='bold')
        ax.set_xlabel("Study Cohort")
        ax.set_ylabel("Continuous Pseudo-Progression Score (CPS)")
        ax.set_ylim(-0.05, 1.05)
        sns.despine()
        
        out_path = os.path.join(self.output_dir, "cross_study_cps_comparison.png")
        plt.tight_layout()
        plt.savefig(out_path)
        plt.close()
        print(f"[*] Saved study comparison plot to {out_path}")

    def plot_travaglini_regional_breakdown(self, trav_df: pd.DataFrame) -> None:
        """Plots regional local vs global CPS breakdown for Travaglini 2026."""
        fig, ax = plt.subplots(figsize=(12, 6))
        
        melted = trav_df.melt(
            id_vars=['Donor ID', 'Brain Region'], 
            value_vars=['CPS_Global', 'CPS_Local'],
            var_name='Metric Type', 
            value_name='CPS'
        )
        
        sns.boxplot(data=melted, x='Brain Region', y='CPS', hue='Metric Type', palette='Pastel1', ax=ax)
        ax.set_title("Regional Vulnerability: Global vs. Local CPS (Travaglini et al. 2026)", pad=15, weight='bold')
        ax.set_xlabel("Brain Region")
        ax.set_ylabel("CPS Value")
        ax.set_ylim(-0.05, 1.05)
        plt.legend(title='Metric Tier', frameon=False)
        sns.despine()
        
        out_path = os.path.join(self.output_dir, "travaglini_regional_cps.png")
        plt.tight_layout()
        plt.savefig(out_path)
        plt.close()
        print(f"[*] Saved regional vulnerability plot to {out_path}")

if __name__ == "__main__":
    from data_loader import SEAADDataLoader
    loader = SEAADDataLoader("data/sea-ad_global_and_local_cps_050126.xlsx")
    dsets = loader.load_all_sheets()
    viz = CPSVisualizer()
    viz.plot_study_comparison(dsets)
    if 'Travaglini 2026' in dsets:
        viz.plot_travaglini_regional_breakdown(dsets['Travaglini 2026'])
      
