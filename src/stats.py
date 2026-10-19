"""
Statistical Inference and Bootstrapping Module for CPS Analysis.
"""

import numpy as np
import pandas as pd
from scipy import stats
from typing import Tuple, Union

class CPSStatistics:
    """Non-parametric statistical methods and bootstrap estimators for CPS metrics."""

    @staticmethod
    def bootstrap_median_ci(data: np.ndarray, n_iterations: int = 10000, alpha: float = 0.05) -> Tuple[float, float, float]:
        """
        Computes bias-corrected and accelerated bootstrap 95% Confidence Interval for the median.
        """
        data = np.asarray(data)
        data = data[~np.isnan(data)]
        if len(data) == 0:
            return np.nan, np.nan, np.nan

        sample_median = np.median(data)
        boot_medians = np.empty(n_iterations)
        
        n = len(data)
        rng = np.random.default_rng(seed=42)
        for i in range(n_iterations]:
            boot_sample = rng.choice(data, size=n, replace=True)
            boot_medians[i] = np.median(boot_sample)
            
        lower_percentile = (alpha / 2) * 100
        upper_percentile = (1 - alpha / 2) * 100
        ci_lower = np.percentile(boot_medians, lower_percentile)
        ci_upper = np.percentile(boot_medians, upper_percentile)
        
        return sample_median, ci_lower, ci_upper

    @staticmethod
    def bootstrap_median_difference_ci(group1: np.ndarray, group2: np.ndarray, n_iterations: int = 10000, alpha: float = 0.05) -> Tuple[float, float, float]:
        """
        Computes bootstrap 95% CI for the difference between two independent medians (Median(G1) - Median(G2)).
        """
        g1 = np.asarray(group1)
        g2 = np.asarray(group2)
        
        obs_diff = np.median(g1) - np.median(g2)
        boot_diffs = np.empty(n_iterations)
        
        rng = np.random.default_rng(seed=42)
        for i in range(n_iterations):
            b1 = rng.choice(g1, size=len(g1), replace=True)
            b2 = rng.choice(g2, size=len(g2), replace=True)
            boot_diffs[i] = np.median(b1) - np.median(b2)
            
        ci_lower = np.percentile(boot_diffs, (alpha / 2) * 100)
        ci_upper = np.percentile(boot_diffs, (1 - alpha / 2) * 100)
        
        return obs_diff, ci_lower, ci_upper

    @staticmethod
    def perform_wilcoxon_test(x: np.ndarray, y: np.ndarray, paired: bool = False) -> Tuple[float, float]:
        """
        Performs Wilcoxon signed-rank test (paired) or Mann-Whitney U test (unpaired).
        """
        x = np.asarray(x)
        y = np.asarray(y)
        
        if paired:
            stat, p_val = stats.wilcoxon(x, y, nan_policy='omit')
        else:
            stat, p_val = stats.mannwhitneyu(x, y, nan_policy='omit')
            
        return stat, p_val

if __name__ == "__main__":
    # Quick test
    d1 = np.random.beta(2, 5, 100)
    d2 = np.random.beta(3, 4, 100)
    med, low, high = CPSStatistics.bootstrap_median_ci(d1)
    print(f"Sample Median: {med:.4f} (95% CI: [{low:.4f}, {high:.4f}])")
  
