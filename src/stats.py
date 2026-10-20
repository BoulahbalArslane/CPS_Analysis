import numpy as np
import pandas as pd
from scipy import stats
from typing import Tuple, Dict, Any, Optional

class CPSStatistics:
    """
    Robust non-parametric statistical inference framework for SEA-AD 
    Continuous Pseudo-progression Score (CPS) analyses.
    Avoids Gaussian assumptions by relying on bootstrap resampling and 
    Wilcoxon signed-rank tests tailored strictly per biomarker and regional tier.
    """
    
    @staticmethod
    def bootstrap_median_ci(
        data: np.ndarray, 
        n_iterations: int = 10000, 
        alpha: float = 0.05
    ) -> Tuple[float, float, float]:
        """
        Computes percentile bootstrap confidence intervals for the median 
        of a specific biomarker or regional observation array.
        
        Args:
            data (np.ndarray): Numeric array of observations (e.g., CPS_Global_pTau).
            n_iterations (int): Number of bootstrap resamples (default: 10,000).
            alpha (float): Significance level, e.g., 0.05 for 95% CI.
            
        Returns:
            Tuple[float, float, float]: (observed_median, ci_lower, ci_upper)
        """
        clean_data = data[~np.isnan(data)]
        if len(clean_data) == 0:
            return np.nan, np.nan, np.nan
            
        obs_median = np.median(clean_data)
        n = len(clean_data)
        
        # Vectorized bootstrap resampling
        resampled_indices = np.random.randint(0, n, size=(n_iterations, n))
        resampled_medians = np.median(clean_data[resampled_indices], axis=1)
        
        lower_percentile = (alpha / 2) * 100
        upper_percentile = (1 - alpha / 2) * 100
        
        ci_lower = np.percentile(resampled_medians, lower_percentile)
        ci_upper = np.percentile(resampled_medians, upper_percentile)
        
        return float(obs_median), float(ci_lower), float(ci_upper)

    @staticmethod
    def bootstrap_median_difference_ci(
        group1: np.ndarray, 
        group2: np.ndarray, 
        n_iterations: int = 10000, 
        alpha: float = 0.05
    ) -> Tuple[float, float, float]:
        """
        Computes bootstrap 95% CI for the difference between two biomarker 
        or regional medians (e.g., comparing CPS_Global_ABeta vs CPS_Global_pTau).
        
        Args:
            group1 (np.ndarray): First biomarker group array.
            group2 (np.ndarray): Second biomarker group array.
            n_iterations (int): Number of bootstrap resamples.
            alpha (float): Significance level.
            
        Returns:
            Tuple[float, float, float]: (observed_median_diff, ci_lower, ci_upper)
        """
        c1 = group1[~np.isnan(group1)]
        c2 = group2[~np.isnan(group2)]
        
        if len(c1) == 0 or len(c2) == 0:
            return np.nan, np.nan, np.nan
            
        obs_diff = np.median(c1) - np.median(c2)
        
        # Independent bootstrap resampling for both groups
        idx1 = np.random.randint(0, len(c1), size=(n_iterations, len(c1)))
        idx2 = np.random.randint(0, len(c2), size=(n_iterations, len(c2)))
        
        meds1 = np.median(c1[idx1], axis=1)
        meds2 = np.median(c2[idx2], axis=1)
        diff_distribution = meds1 - meds2
        
        lower_p = (alpha / 2) * 100
        upper_p = (1 - alpha / 2) * 100
        
        ci_lower = np.percentile(diff_distribution, lower_p)
        ci_upper = np.percentile(diff_distribution, upper_p)
        
        return float(obs_diff), float(ci_lower), float(ci_upper)

    @staticmethod
    def perform_wilcoxon_test(
        group1: np.ndarray, 
        group2: np.ndarray, 
        paired: bool = True
    ) -> Tuple[float, float]:
        """
        Performs non-parametric hypothesis testing between biological tiers 
        (Wilcoxon signed-rank for paired regional/biomarker metrics, or Mann-Whitney U).
        
        Args:
            group1 (np.ndarray): First metric vector.
            group2 (np.ndarray): Second metric vector.
            paired (bool): Whether to perform paired Wilcoxon test.
            
        Returns:
            Tuple[float, float]: (test_statistic, p_value)
        """
        c1 = group1[~np.isnan(group1)]
        c2 = group2[~np.isnan(group2)]
        
        if paired:
            min_len = min(len(c1), len(c2))
            stat, p_val = stats.wilcoxon(c1[:min_len], c2[:min_len])
        else:
            stat, p_val = stats.mannwhitneyu(c1, c2, alternative='two-sided')
            
        return float(stat), float(p_val)
