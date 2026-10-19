"""
Data Ingestion and Integrity Check Module for SEA-AD CPS Datasets.
"""

import pandas as pd
import numpy as np
from typing import Dict, Tuple

class SEAADDataLoader:
    """Loader and security validation pipeline for SEA-AD CPS datasets."""
    
    EXPECTED_RANGES = {
        'CPS': (0.0, 1.0),
        'CPS_Global': (0.0, 1.0),
        'CPS_Global_ABeta': (0.0, 1.0),
        'CPS_Global_pTau': (0.0, 1.0),
        'CPS_Local': (0.0, 1.0),
        'CPS_Local_ABeta': (0.0, 1.0),
        'CPS_Local_pTau': (0.0, 1.0),
        'CPS_AT8': (0.0, 1.0),
        'CPS_6E10': (0.0, 1.0)
    }

    def __init__(self, excel_path: str):
        self.excel_path = excel_path
        self.xls = pd.ExcelFile(excel_path)

    def load_all_sheets(self) -> Dict[str, pd.DataFrame]:
        """Loads all relevant study sheets, excluding the README."""
        sheets = [s for s in self.xls.sheet_names if s != 'README']
        dataframes = {}
        for sheet in sheets:
            df = pd.read_excel(self.xls, sheet_name=sheet)
            self._validate_security_and_integrity(df, sheet)
            dataframes[sheet] = df
        return dataframes

    def _validate_security_and_integrity(self, df: pd.DataFrame, sheet_name: str) -> None:
        """Performs automated security and data hygiene checks."""
        print(f"[*] Running integrity check for sheet: '{sheet_name}' (Shape: {df.shape})")
        
        # 1. Check for missing values
        null_counts = df.isnull().sum().sum()
        if null_counts > 0:
            print(f"    [WARNING] Found {null_counts} missing values in {sheet_name}.")
        else:
            print(f"    [PASS] No missing values detected.")

        # 2. Check numerical column bounds [0.0, 1.0]
        for col in df.columns:
            if col in self.EXPECTED_RANGES:
                min_val, max_val = df[col].min(), df[col].max()
                expected_min, expected_max = self.EXPECTED_RANGES[col]
                if min_val < expected_min or max_val > expected_max:
                    raise ValueError(
                        f"    [SECURITY ERROR] Column '{col}' in {sheet_name} out of bounds! "
                        f"Found [{min_val}, {max_val}], expected [{expected_min}, {expected_max}]."
                    )
        print(f"    [PASS] All CPS metrics verified within valid biological range [0.0, 1.0].")

        # 3. Check Donor ID presence
        if 'Donor ID' not in df.columns:
            raise KeyError(f"    [ERROR] 'Donor ID' column missing from {sheet_name}.")
        print(f"    [PASS] Donor ID schema validated. Unique donors: {df['Donor ID'].nunique()}\n")

if __name__ == "__main__":
    loader = SEAADDataLoader("data/sea-ad_global_and_local_cps_050126.xlsx")
    datasets = loader.load_all_sheets()
    print("Successfully ingested and verified all study cohorts.")
  
