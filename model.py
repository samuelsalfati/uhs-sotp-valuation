"""
UHS Sum-of-the-Parts Valuation Model
CONFIDENTIAL & PROPRIETARY - Do Not Distribute

This model analyzes Universal Health Services through a sum-of-the-parts
framework to identify hidden value in the current market valuation.
"""

import pandas as pd
import numpy as np
from dataclasses import dataclass
from typing import Dict, Optional

# ==========================================
# CONFIDENTIALITY BANNER
# ==========================================

CONFIDENTIALITY_NOTICE = """
⚠️ CONFIDENTIAL & PROPRIETARY ANALYSIS ⚠️
This valuation model contains confidential financial projections and investment strategies.
Unauthorized distribution or disclosure is strictly prohibited.
© 2025 - All Rights Reserved
"""

# ==========================================
# 1. DATA CONFIGURATION
# ==========================================

@dataclass
class SegmentData:
    """Operating segment financial data"""
    name: str
    revenue: float  # LTM Revenue
    ebitda: float   # LTM Adjusted EBITDA
    ebitda_margin: float
    facilities: int
    growth_rate: float  # Expected annual growth

@dataclass
class RealEstateData:
    """Real estate holdings data"""
    book_value: float           # PP&E book value
    owned_sqft: float          # Square footage owned
    leased_sqft: float         # Square footage leased
    market_value_per_sqft: float  # Estimated market value/sqft
    cap_rate: float            # Capitalization rate for REIT valuation
    annual_rent_potential: float  # Pro-forma annual rent at market rates

@dataclass
class CapitalStructure:
    """Capital structure and share data"""
    total_debt: float
    cash: float
    shares_outstanding: float  # Basic shares
    diluted_shares: float      # Fully diluted
    class_a_shares: float      # If multiple classes
    class_b_shares: float
    share_price: float         # Current market price

    @property
    def net_debt(self) -> float:
        return self.total_debt - self.cash

    @property
    def market_cap(self) -> float:
        return self.shares_outstanding * self.share_price

    @property
    def enterprise_value(self) -> float:
        return self.market_cap + self.net_debt

def default_uhs_data():
    """
    UHS financial data from latest 10-K.

    PLACEHOLDER VALUES - REPLACE WITH ACTUAL 10-K DATA
    """
    return {
        "segments": {
            "acute_care": SegmentData(
                name="Acute Care Hospitals",
                revenue=7_500_000_000,      # $7.5B (PLACEHOLDER)
                ebitda=1_200_000_000,       # $1.2B (PLACEHOLDER)
                ebitda_margin=0.16,         # 16% (PLACEHOLDER)
                facilities=26,               # PLACEHOLDER
                growth_rate=0.03            # 3% annual growth
            ),
            "behavioral": SegmentData(
                name="Behavioral Health",
                revenue=6_000_000_000,      # $6.0B (PLACEHOLDER)
                ebitda=1_400_000_000,       # $1.4B (PLACEHOLDER)
                ebitda_margin=0.23,         # 23% (PLACEHOLDER)
                facilities=340,              # PLACEHOLDER
                growth_rate=0.05            # 5% annual growth
            )
        },
        "real_estate": RealEstateData(
            book_value=5_500_000_000,       # $5.5B PP&E (PLACEHOLDER)
            owned_sqft=25_000_000,          # 25M sqft (PLACEHOLDER)
            leased_sqft=5_000_000,          # 5M sqft (PLACEHOLDER)
            market_value_per_sqft=400,      # $400/sqft market value
            cap_rate=0.065,                 # 6.5% cap rate
            annual_rent_potential=650_000_000  # $650M annual rent
        ),
        "capital_structure": CapitalStructure(
            total_debt=11_500_000_000,      # $11.5B (PLACEHOLDER)
            cash=500_000_000,               # $500M (PLACEHOLDER)
            shares_outstanding=70_000_000,   # 70M shares (PLACEHOLDER)
            diluted_shares=72_000_000,      # 72M diluted
            class_a_shares=70_000_000,      # If applicable
            class_b_shares=0,
            share_price=180.00              # Current price (PLACEHOLDER)
        ),
        "corporate_overhead": {
            "current_annual": 450_000_000,   # $450M annual (PLACEHOLDER)
            "public_company_costs": 50_000_000,  # $50M (audit, IR, legal)
            "excess_overhead": 100_000_000,  # $100M reducible overhead
            "optimized_annual": 300_000_000  # $300M pro-forma
        }
    }

# ==========================================
# 2. VALUATION MULTIPLES
# ==========================================

def default_valuation_multiples():
    """
    Industry-standard EBITDA multiples for each segment.
    Based on public comps and recent transactions.
    """
    return {
        "acute_care": {
            "low": 6.0,      # Conservative multiple
            "base": 7.0,     # Base case
            "high": 8.5      # Optimistic
        },
        "behavioral": {
            "low": 9.0,      # Higher quality, more stable
            "base": 10.5,    # Base case
            "high": 12.0     # Premium for growth
        },
        "real_estate_cap_rate": {
            "low": 0.070,    # 7.0% cap rate (conservative)
            "base": 0.065,   # 6.5% cap rate (base)
            "high": 0.060    # 6.0% cap rate (aggressive)
        },
        "real_estate_sqft": {
            "low": 300,      # $300/sqft
            "base": 400,     # $400/sqft
            "high": 500      # $500/sqft
        }
    }

# ==========================================
# 3. SOTP VALUATION CALCULATION
# ==========================================

def calculate_sotp(data: dict, multiples: dict, scenario: str = "base"):
    """
    Calculate Sum-of-the-Parts valuation.

    Args:
        data: UHS financial data dictionary
        multiples: Valuation multiples dictionary
        scenario: 'low', 'base', or 'high'

    Returns:
        Dictionary with SOTP components and total value
    """
    segments = data["segments"]
    real_estate = data["real_estate"]
    capital = data["capital_structure"]
    overhead = data["corporate_overhead"]

    # 1. Acute Care Valuation (EV)
    acute_multiple = multiples["acute_care"][scenario]
    acute_ev = segments["acute_care"].ebitda * acute_multiple

    # 2. Behavioral Health Valuation (EV)
    behavioral_multiple = multiples["behavioral"][scenario]
    behavioral_ev = segments["behavioral"].ebitda * behavioral_multiple

    # 3. Real Estate Valuation (use higher of two methods)
    # Method A: Cap rate on annual rent
    cap_rate = multiples["real_estate_cap_rate"][scenario]
    re_value_cap_rate = real_estate.annual_rent_potential / cap_rate

    # Method B: Per-square-foot market value
    sqft_value = multiples["real_estate_sqft"][scenario]
    re_value_sqft = real_estate.owned_sqft * sqft_value

    # Take the higher of the two methods (conservative approach)
    real_estate_value = max(re_value_cap_rate, re_value_sqft)

    # 4. Corporate Overhead Adjustment (NPV of savings)
    # Assume 10x multiple on annual overhead reduction
    overhead_savings_annual = overhead["current_annual"] - overhead["optimized_annual"]
    overhead_value_creation = overhead_savings_annual * 10

    # 5. Sum of Operating Values
    total_operating_value = acute_ev + behavioral_ev

    # 6. Add Real Estate Value
    total_enterprise_value = total_operating_value + real_estate_value

    # 7. Subtract Net Debt to get Equity Value
    equity_value = total_enterprise_value - capital.net_debt

    # 8. Add Overhead Value Creation
    total_equity_value = equity_value + overhead_value_creation

    # 9. Per-Share Value
    value_per_share = total_equity_value / capital.shares_outstanding

    # Current Market Metrics
    current_market_cap = capital.market_cap
    current_ev = capital.enterprise_value
    current_price = capital.share_price

    # Implied Upside
    implied_upside_pct = (value_per_share - current_price) / current_price
    implied_upside_dollars = value_per_share - current_price

    return {
        "components": {
            "Acute Care EV": acute_ev,
            "Behavioral Health EV": behavioral_ev,
            "Real Estate Value": real_estate_value,
            "Overhead Value Creation": overhead_value_creation,
            "Total EV": total_enterprise_value,
            "Less: Net Debt": -capital.net_debt,
            "Equity Value": total_equity_value,
        },
        "metrics": {
            "SOTP Equity Value": total_equity_value,
            "SOTP Value per Share": value_per_share,
            "Current Market Cap": current_market_cap,
            "Current Share Price": current_price,
            "Current EV": current_ev,
            "Implied Upside ($)": implied_upside_dollars,
            "Implied Upside (%)": implied_upside_pct,
            "Shares Outstanding": capital.shares_outstanding,
        },
        "multiples_used": {
            "Acute Care Multiple": acute_multiple,
            "Behavioral Multiple": behavioral_multiple,
            "RE Cap Rate": cap_rate,
            "RE $/SqFt": sqft_value,
        },
        "real_estate_methods": {
            "Cap Rate Method": re_value_cap_rate,
            "Per SqFt Method": re_value_sqft,
            "Value Used": real_estate_value,
        }
    }

# ==========================================
# 4. SCENARIO ANALYSIS
# ==========================================

def run_all_scenarios(data: dict, multiples: dict):
    """
    Run Bear, Base, and Bull scenarios.

    Returns DataFrame with scenario comparison.
    """
    scenarios = {}

    for scenario in ["low", "base", "high"]:
        result = calculate_sotp(data, multiples, scenario)
        scenario_name = {"low": "Bear", "base": "Base", "high": "Bull"}[scenario]

        scenarios[scenario_name] = {
            "SOTP Value per Share": result["metrics"]["SOTP Value per Share"],
            "Implied Upside (%)": result["metrics"]["Implied Upside (%)"] * 100,
            "Acute Care EV": result["components"]["Acute Care EV"] / 1e9,
            "Behavioral EV": result["components"]["Behavioral Health EV"] / 1e9,
            "Real Estate Value": result["components"]["Real Estate Value"] / 1e9,
            "Total Equity Value": result["metrics"]["SOTP Equity Value"] / 1e9,
        }

    df = pd.DataFrame(scenarios).T
    df["Current Price"] = data["capital_structure"].share_price

    return df

# ==========================================
# 5. SENSITIVITY ANALYSIS
# ==========================================

def sensitivity_analysis(data: dict, multiples: dict):
    """
    Create sensitivity table for key drivers.

    Returns DataFrame with sensitivity matrix.
    """
    base_result = calculate_sotp(data, multiples, "base")
    base_value = base_result["metrics"]["SOTP Value per Share"]

    # Sensitivity on Behavioral Multiple (biggest driver)
    behavioral_multiples = np.arange(8.0, 13.0, 0.5)
    acute_multiples = np.arange(5.0, 9.0, 0.5)

    sensitivity_data = []

    for behav_mult in behavioral_multiples:
        for acute_mult in acute_multiples:
            # Temporarily adjust multiples
            temp_multiples = multiples.copy()
            temp_multiples["behavioral"]["base"] = behav_mult
            temp_multiples["acute_care"]["base"] = acute_mult

            result = calculate_sotp(data, temp_multiples, "base")
            value_per_share = result["metrics"]["SOTP Value per Share"]

            sensitivity_data.append({
                "Behavioral Multiple": behav_mult,
                "Acute Multiple": acute_mult,
                "Value per Share": value_per_share,
                "vs Base": value_per_share - base_value,
            })

    return pd.DataFrame(sensitivity_data)

# ==========================================
# USAGE EXAMPLE
# ==========================================

if __name__ == "__main__":
    print(CONFIDENTIALITY_NOTICE)
    print("\n" + "="*60)
    print("UHS SUM-OF-THE-PARTS VALUATION MODEL")
    print("="*60 + "\n")

    data = default_uhs_data()
    multiples = default_valuation_multiples()

    # Run base case
    base_case = calculate_sotp(data, multiples, "base")

    print("BASE CASE VALUATION:")
    print(f"SOTP Value per Share: ${base_case['metrics']['SOTP Value per Share']:.2f}")
    print(f"Current Price: ${base_case['metrics']['Current Share Price']:.2f}")
    print(f"Implied Upside: {base_case['metrics']['Implied Upside (%)']:.1%}")

    print("\nCOMPONENTS:")
    for component, value in base_case["components"].items():
        print(f"  {component}: ${value/1e9:.2f}B")

    print("\n" + "="*60)
    print("ALL SCENARIOS:")
    scenarios_df = run_all_scenarios(data, multiples)
    print(scenarios_df)
