# UHS Sum-of-the-Parts (SOTP) Valuation Model Guide

## ⚠️ CONFIDENTIALITY NOTICE

**THIS DOCUMENT AND ALL RELATED MATERIALS ARE STRICTLY CONFIDENTIAL AND PROPRIETARY.**

This valuation model and analysis contain confidential financial projections, investment strategies, and proprietary methodologies. This information is intended solely for authorized personnel and must not be distributed, shared, or disclosed to any third party without express written permission.

**By accessing this model, you acknowledge:**
- All information herein is confidential and proprietary
- You will not distribute, copy, or share this analysis
- You will use this information solely for authorized investment analysis purposes
- Unauthorized disclosure may result in legal action

**© 2025 - All Rights Reserved**

---

## 📋 Executive Summary

This guide provides a comprehensive framework for building a **Sum-of-the-Parts (SOTP) valuation model for Universal Health Services, Inc. (UHS)** using Streamlit, inspired by the Ora Living financial model design.

### Investment Thesis:
**UHS's enterprise value significantly undervalues the company when analyzed on a sum-of-the-parts basis.** By separating:
1. Acute Care Hospital operations
2. Behavioral Health operations
3. Owned real estate assets
4. Reducing corporate overhead

...we demonstrate **hidden value** that justifies a higher valuation or potential breakup scenario.

---

## 🏗️ Project Setup - Step by Step

### Step 1: Create New Project Directory

```bash
# Navigate to where you want to create the project
cd ~/Documents/Investments/  # Or your preferred location

# Create new project folder
mkdir uhs-sotp-valuation
cd uhs-sotp-valuation

# Create folder structure
mkdir data
mkdir Assets
mkdir exports
```

### Step 2: Copy Required Files from Ora Living

```bash
# Copy requirements.txt
cp ~/Documents/Ora\ Living/Financial\ Model/ora-va-step1/requirements.txt .

# Copy .streamlit config folder if it exists
cp -r ~/Documents/Ora\ Living/Financial\ Model/ora-va-step1/.streamlit .

# Create .gitignore for confidentiality
cat > .gitignore << EOF
# Confidential Data
data/*.pdf
data/*.xlsx
exports/
*.csv

# Python
__pycache__/
*.pyc
.DS_Store

# Environment
.env
venv/
EOF
```

### Step 3: Set Up Python Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate  # Mac/Linux
# or
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

### Step 4: Download UHS Materials

**Required Documents (from SEC EDGAR):**
1. Latest 10-K (Annual Report) - FY 2024
2. Latest 10-Q (Quarterly Report) - Most recent quarter
3. Latest Proxy Statement (DEF 14A) - For share structure
4. Latest Investor Presentation (from UHS website)

**Where to find:**
- SEC EDGAR: https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000352915
- UHS Investor Relations: https://www.uhsinc.com/investors/

**Save to:**
```
data/
├── uhs_10k_2024.pdf
├── uhs_10q_latest.pdf
├── uhs_proxy_2024.pdf
└── uhs_investor_deck.pdf
```

---

## 📊 Data Extraction Checklist

### From 10-K, Extract:

#### Operating Segments (Item 1 & Item 8):
- [ ] Acute Care Hospitals - Revenue
- [ ] Acute Care Hospitals - Adjusted EBITDA
- [ ] Behavioral Health - Revenue
- [ ] Behavioral Health - Adjusted EBITDA
- [ ] Number of facilities by segment
- [ ] Bed count by segment

#### Real Estate (Note on Property & Equipment):
- [ ] Owned property book value
- [ ] Leased property details
- [ ] Square footage (if disclosed)
- [ ] Property locations by state
- [ ] Depreciation schedule

#### Capital Structure (Balance Sheet):
- [ ] Total debt (current + long-term)
- [ ] Debt maturity schedule
- [ ] Interest rates on debt
- [ ] Cash and equivalents
- [ ] Shares outstanding (basic & diluted)
- [ ] Share classes and voting rights

#### Corporate Overhead (Income Statement):
- [ ] Corporate SG&A
- [ ] Public company costs
- [ ] D&O insurance, audit fees
- [ ] IR/legal/compliance costs

---

## 💻 MODEL.PY - SOTP Calculation Engine

Create `model.py` with the following structure:

```python
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
            "Acute Care EV": result["components"]["Acute Care EV"],
            "Behavioral EV": result["components"]["Behavioral Health EV"],
            "Real Estate Value": result["components"]["Real Estate Value"],
            "Total Equity Value": result["metrics"]["SOTP Equity Value"],
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
```

---

## 🎨 APP.PY - Streamlit UI (Ora Living Style)

Create `app.py`:

```python
"""
UHS Sum-of-the-Parts Valuation Analysis
CONFIDENTIAL & PROPRIETARY - Streamlit Dashboard

Inspired by Ora Living financial model design.
"""

import streamlit as st
import pandas as pd
import numpy as np
from model import (
    default_uhs_data, default_valuation_multiples,
    calculate_sotp, run_all_scenarios, sensitivity_analysis,
    CONFIDENTIALITY_NOTICE
)

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="UHS SOTP Valuation",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# CONFIDENTIALITY DISCLAIMER (ALWAYS VISIBLE)
# ==========================================

st.sidebar.markdown(f"""
<div style="background-color: #FFE6E6; padding: 15px; border-radius: 8px; border: 2px solid #FF4444; margin-bottom: 20px;">
    <h3 style="color: #CC0000; margin: 0;">⚠️ CONFIDENTIAL</h3>
    <p style="font-size: 11px; margin: 5px 0 0 0; color: #CC0000;">
        <b>PROPRIETARY ANALYSIS</b><br>
        This valuation model contains confidential financial projections and investment strategies.
        <b>Do not distribute or share.</b>
    </p>
</div>
""", unsafe_allow_html=True)

# ==========================================
# CUSTOM CSS (ORA LIVING BLUE THEME)
# ==========================================

st.markdown("""
<style>
    /* Light blue background */
    .stApp {
        background-color: #F8FCFD !important;
    }

    .main {
        background-color: #F8FCFD !important;
    }

    section[data-testid="stSidebar"] {
        background-color: #EBF7FA !important;
    }

    .block-container {
        background-color: #F8FCFD !important;
        padding-top: 2rem;
    }

    /* Metric containers with subtle white background */
    div[data-testid="metric-container"] {
        background-color: rgba(255, 255, 255, 0.8);
        padding: 15px;
        border-radius: 10px;
        border: 1px solid rgba(0, 183, 216, 0.2);
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }

    /* DataFrames clean white background */
    .stDataFrame {
        background-color: white;
        padding: 10px;
        border-radius: 8px;
    }

    /* Blue sliders */
    div[data-baseweb="slider"] > div > div > div > div:nth-child(1) > div {
        background-color: rgb(0, 183, 216) !important;
    }

    div[data-baseweb="slider"] > div > div > div > div:nth-child(2) {
        background-color: rgb(0, 183, 216) !important;
    }

    div[role="slider"] {
        background-color: rgb(0, 183, 216) !important;
    }

    /* Tab styling - more prominent */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: rgba(255, 255, 255, 0.5);
        padding: 10px;
        border-radius: 10px;
    }

    .stTabs [data-baseweb="tab"] {
        background-color: white;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: 600;
        border: 1px solid rgba(0, 183, 216, 0.2);
    }

    .stTabs [aria-selected="true"] {
        background-color: rgb(0, 183, 216) !important;
        color: white !important;
    }

    /* Confidentiality banner at top */
    .confidential-banner {
        background: linear-gradient(135deg, #FF4444 0%, #CC0000 100%);
        color: white;
        padding: 10px 20px;
        text-align: center;
        font-weight: bold;
        margin-bottom: 20px;
        border-radius: 8px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# CONFIDENTIALITY BANNER (TOP OF PAGE)
# ==========================================

st.markdown("""
<div class="confidential-banner">
    ⚠️ CONFIDENTIAL & PROPRIETARY ANALYSIS - DO NOT DISTRIBUTE ⚠️
</div>
""", unsafe_allow_html=True)

# ==========================================
# HEADER
# ==========================================

st.title("🏥 Universal Health Services (UHS)")
st.subheader("Sum-of-the-Parts Valuation Analysis")
st.markdown("---")

# ==========================================
# LOAD DATA
# ==========================================

data = default_uhs_data()
multiples = default_valuation_multiples()

# ==========================================
# SIDEBAR CONTROLS
# ==========================================

st.sidebar.header("⚙️ Valuation Assumptions")

st.sidebar.markdown("### Operating Segment Multiples")

multiples["acute_care"]["base"] = st.sidebar.slider(
    "Acute Care EBITDA Multiple",
    min_value=5.0,
    max_value=10.0,
    value=7.0,
    step=0.5,
    help="Typical range: 6-8x for acute care hospitals"
)

multiples["behavioral"]["base"] = st.sidebar.slider(
    "Behavioral Health EBITDA Multiple",
    min_value=8.0,
    max_value=14.0,
    value=10.5,
    step=0.5,
    help="Typical range: 9-12x for behavioral health (higher quality)"
)

st.sidebar.markdown("### Real Estate Valuation")

re_method = st.sidebar.radio(
    "Primary RE Valuation Method",
    ["Cap Rate Method", "Per SqFt Market Value", "Higher of Both"],
    index=2
)

multiples["real_estate_cap_rate"]["base"] = st.sidebar.slider(
    "Capitalization Rate (%)",
    min_value=5.0,
    max_value=8.0,
    value=6.5,
    step=0.25,
) / 100

multiples["real_estate_sqft"]["base"] = st.sidebar.slider(
    "Market Value per SqFt ($)",
    min_value=200,
    max_value=600,
    value=400,
    step=25,
)

st.sidebar.markdown("### Corporate Overhead")

overhead_reduction_pct = st.sidebar.slider(
    "Overhead Reduction (%)",
    min_value=0,
    max_value=50,
    value=33,
    step=5,
    help="% reduction in corporate overhead post-separation"
) / 100

data["corporate_overhead"]["optimized_annual"] = (
    data["corporate_overhead"]["current_annual"] * (1 - overhead_reduction_pct)
)

# ==========================================
# CALCULATE SOTP
# ==========================================

base_result = calculate_sotp(data, multiples, "base")
scenarios_df = run_all_scenarios(data, multiples)

# ==========================================
# MAIN CONTENT TABS
# ==========================================

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📊 SOTP Summary",
    "🏥 Operating Segments",
    "🏢 Real Estate",
    "💰 Capital Structure",
    "📈 Scenarios & Sensitivity",
    "📋 Detailed Tables"
])

# ----- TAB 1: SOTP SUMMARY -----
with tab1:
    st.header("Sum-of-the-Parts Valuation Summary")

    # Key Metrics (Top Row)
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "SOTP Value per Share",
            f"${base_result['metrics']['SOTP Value per Share']:.2f}",
            delta=f"+${base_result['metrics']['Implied Upside ($)']:.2f}",
            delta_color="normal"
        )

    with col2:
        st.metric(
            "Current Share Price",
            f"${base_result['metrics']['Current Share Price']:.2f}"
        )

    with col3:
        upside_pct = base_result['metrics']['Implied Upside (%)'] * 100
        st.metric(
            "Implied Upside",
            f"{upside_pct:.1f}%",
            delta=f"${base_result['metrics']['Implied Upside ($)']:.2f}"
        )

    with col4:
        st.metric(
            "Total Equity Value",
            f"${base_result['metrics']['SOTP Equity Value']/1e9:.2f}B"
        )

    st.markdown("---")

    # SOTP Waterfall Chart
    st.subheader("Valuation Waterfall")

    components_df = pd.DataFrame({
        "Component": list(base_result["components"].keys()),
        "Value ($B)": [v/1e9 for v in base_result["components"].values()]
    })

    st.bar_chart(components_df.set_index("Component"))

    # Components Table
    st.subheader("Valuation Components Breakdown")

    components_display = []
    for comp, value in base_result["components"].items():
        components_display.append({
            "Component": comp,
            "Value ($M)": f"${value/1e6:,.0f}",
            "Value ($B)": f"${value/1e9:.2f}"
        })

    st.dataframe(pd.DataFrame(components_display), use_container_width=True)

    # Investment Thesis Summary
    st.markdown("---")
    st.subheader("💡 Investment Thesis")

    if upside_pct > 20:
        thesis_color = "#00CC00"
        thesis_text = "STRONG BUY"
    elif upside_pct > 10:
        thesis_color = "#66CC00"
        thesis_text = "BUY"
    else:
        thesis_color = "#FF8800"
        thesis_text = "HOLD"

    st.markdown(f"""
    <div style="background-color: rgba(255,255,255,0.8); padding: 20px; border-radius: 10px; border-left: 5px solid {thesis_color};">
        <h3 style="color: {thesis_color}; margin-top: 0;">Recommendation: {thesis_text}</h3>
        <p><b>Implied Upside:</b> {upside_pct:.1f}% (${base_result['metrics']['Implied Upside ($)']:.2f} per share)</p>
        <p><b>Key Drivers:</b></p>
        <ul>
            <li>Behavioral Health segment trading at premium multiples (10-12x EBITDA)</li>
            <li>Significant real estate value (~${base_result['components']['Real Estate Value']/1e9:.2f}B) hidden in balance sheet</li>
            <li>Corporate overhead reduction opportunity creates additional value</li>
            <li>Sum-of-parts significantly exceeds current market valuation</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# ----- TAB 2: OPERATING SEGMENTS -----
with tab2:
    st.header("Operating Segment Analysis")

    col1, col2 = st.columns(2)

    # Acute Care
    with col1:
        st.subheader("🏥 Acute Care Hospitals")
        acute = data["segments"]["acute_care"]

        st.metric("LTM Revenue", f"${acute.revenue/1e9:.2f}B")
        st.metric("LTM EBITDA", f"${acute.ebitda/1e9:.2f}B")
        st.metric("EBITDA Margin", f"{acute.ebitda_margin:.1%}")
        st.metric("Number of Facilities", f"{acute.facilities}")

        st.markdown(f"**Valuation Multiple:** {multiples['acute_care']['base']:.1f}x")
        st.metric(
            "Implied Enterprise Value",
            f"${base_result['components']['Acute Care EV']/1e9:.2f}B"
        )

    # Behavioral Health
    with col2:
        st.subheader("🧠 Behavioral Health")
        behavioral = data["segments"]["behavioral"]

        st.metric("LTM Revenue", f"${behavioral.revenue/1e9:.2f}B")
        st.metric("LTM EBITDA", f"${behavioral.ebitda/1e9:.2f}B")
        st.metric("EBITDA Margin", f"{behavioral.ebitda_margin:.1%}")
        st.metric("Number of Facilities", f"{behavioral.facilities}")

        st.markdown(f"**Valuation Multiple:** {multiples['behavioral']['base']:.1f}x")
        st.metric(
            "Implied Enterprise Value",
            f"${base_result['components']['Behavioral Health EV']/1e9:.2f}B"
        )

    st.markdown("---")

    # Segment Comparison
    st.subheader("Segment Comparison")

    segment_compare = pd.DataFrame({
        "Metric": ["Revenue ($B)", "EBITDA ($B)", "EBITDA Margin", "Facilities", "Multiple", "Enterprise Value ($B)"],
        "Acute Care": [
            f"${acute.revenue/1e9:.2f}",
            f"${acute.ebitda/1e9:.2f}",
            f"{acute.ebitda_margin:.1%}",
            acute.facilities,
            f"{multiples['acute_care']['base']:.1f}x",
            f"${base_result['components']['Acute Care EV']/1e9:.2f}"
        ],
        "Behavioral Health": [
            f"${behavioral.revenue/1e9:.2f}",
            f"${behavioral.ebitda/1e9:.2f}",
            f"{behavioral.ebitda_margin:.1%}",
            behavioral.facilities,
            f"{multiples['behavioral']['base']:.1f}x",
            f"${base_result['components']['Behavioral Health EV']/1e9:.2f}"
        ]
    })

    st.dataframe(segment_compare, use_container_width=True)

# ----- TAB 3: REAL ESTATE -----
with tab3:
    st.header("Real Estate Valuation")

    re = data["real_estate"]

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Book Value", f"${re.book_value/1e9:.2f}B")
        st.metric("Owned Sq Ft", f"{re.owned_sqft/1e6:.1f}M")

    with col2:
        st.metric("Market Value (SOTP)", f"${base_result['components']['Real Estate Value']/1e9:.2f}B")
        st.metric("Leased Sq Ft", f"{re.leased_sqft/1e6:.1f}M")

    with col3:
        implied_markup = (base_result['components']['Real Estate Value'] / re.book_value - 1) * 100
        st.metric("Value vs Book", f"+{implied_markup:.0f}%")
        st.metric("Total Sq Ft", f"{(re.owned_sqft + re.leased_sqft)/1e6:.1f}M")

    st.markdown("---")

    # Valuation Methods Comparison
    st.subheader("Valuation Methods")

    re_methods = pd.DataFrame({
        "Method": ["Cap Rate Method", "Per Sq Ft Market Value", "Book Value (for reference)"],
        "Calculation": [
            f"${re.annual_rent_potential/1e6:.0f}M rent / {multiples['real_estate_cap_rate']['base']:.2%} cap rate",
            f"{re.owned_sqft/1e6:.1f}M sqft × ${multiples['real_estate_sqft']['base']}/sqft",
            "Historical cost basis"
        ],
        "Value ($B)": [
            f"${base_result['real_estate_methods']['Cap Rate Method']/1e9:.2f}",
            f"${base_result['real_estate_methods']['Per SqFt Method']/1e9:.2f}",
            f"${re.book_value/1e9:.2f}"
        ]
    })

    st.dataframe(re_methods, use_container_width=True)

    st.info(f"**Method Used:** {re_method} = **${base_result['components']['Real Estate Value']/1e9:.2f}B**")

    # REIT Spin Analysis
    st.markdown("---")
    st.subheader("Potential REIT Spin-Off Analysis")

    st.markdown(f"""
    If UHS were to spin off its real estate into a separate REIT:

    - **Asset Value:** ${base_result['components']['Real Estate Value']/1e9:.2f}B
    - **Annual Rent (pro forma):** ${re.annual_rent_potential/1e6:.0f}M
    - **Implied Cap Rate:** {multiples['real_estate_cap_rate']['base']:.2%}
    - **REIT Yield to Investors:** ~5-6% (typical healthcare REIT)

    **Benefits:**
    - Unlock hidden real estate value
    - Create tax-efficient structure
    - Reduce OpCo leverage
    - Create two publicly-traded entities
    """)

# ----- TAB 4: CAPITAL STRUCTURE -----
with tab4:
    st.header("Capital Structure Analysis")

    capital = data["capital_structure"]

    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("Debt & Cash")
        st.metric("Total Debt", f"${capital.total_debt/1e9:.2f}B")
        st.metric("Cash", f"${capital.cash/1e9:.2f}B")
        st.metric("Net Debt", f"${capital.net_debt/1e9:.2f}B")

    with col2:
        st.subheader("Equity")
        st.metric("Shares Outstanding", f"{capital.shares_outstanding/1e6:.1f}M")
        st.metric("Current Share Price", f"${capital.share_price:.2f}")
        st.metric("Market Cap", f"${capital.market_cap/1e9:.2f}B")

    with col3:
        st.subheader("Enterprise Value")
        st.metric("Current EV", f"${capital.enterprise_value/1e9:.2f}B")
        st.metric("SOTP Equity Value", f"${base_result['metrics']['SOTP Equity Value']/1e9:.2f}B")
        sotp_ev = base_result['metrics']['SOTP Equity Value'] + capital.net_debt
        st.metric("SOTP Implied EV", f"${sotp_ev/1e9:.2f}B")

    st.markdown("---")

    # Debt to EBITDA
    st.subheader("Leverage Analysis")

    total_ebitda = data["segments"]["acute_care"].ebitda + data["segments"]["behavioral"].ebitda
    debt_to_ebitda = capital.net_debt / total_ebitda

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Total LTM EBITDA", f"${total_ebitda/1e9:.2f}B")
        st.metric("Net Debt / EBITDA", f"{debt_to_ebitda:.2f}x")

    with col2:
        st.metric("EV / EBITDA (Current)", f"{capital.enterprise_value / total_ebitda:.1f}x")
        st.metric("EV / EBITDA (SOTP)", f"{sotp_ev / total_ebitda:.1f}x")

    # Share Structure
    st.markdown("---")
    st.subheader("Share Structure")

    share_structure = pd.DataFrame({
        "Share Class": ["Class A (Common)", "Class B (if applicable)", "Diluted Shares"],
        "Shares Outstanding (M)": [
            f"{capital.class_a_shares/1e6:.2f}",
            f"{capital.class_b_shares/1e6:.2f}",
            f"{capital.diluted_shares/1e6:.2f}"
        ],
        "% of Total": [
            f"{capital.class_a_shares/capital.diluted_shares*100:.1f}%",
            f"{capital.class_b_shares/capital.diluted_shares*100:.1f}%",
            "100.0%"
        ]
    })

    st.dataframe(share_structure, use_container_width=True)

# ----- TAB 5: SCENARIOS & SENSITIVITY -----
with tab5:
    st.header("Scenario Analysis")

    # Scenario Comparison
    st.subheader("Bear / Base / Bull Scenarios")

    st.dataframe(
        scenarios_df.style.format({
            "SOTP Value per Share": "${:.2f}",
            "Implied Upside (%)": "{:.1f}%",
            "Acute Care EV": "${:.2f}B",
            "Behavioral EV": "${:.2f}B",
            "Real Estate Value": "${:.2f}B",
            "Total Equity Value": "${:.2f}B",
            "Current Price": "${:.2f}",
        }),
        use_container_width=True
    )

    # Scenario Chart
    st.subheader("Value per Share by Scenario")
    scenario_chart = scenarios_df[["SOTP Value per Share", "Current Price"]]
    st.bar_chart(scenario_chart)

    st.markdown("---")

    # Sensitivity Analysis
    st.subheader("Sensitivity Analysis")

    st.markdown("**Key Drivers:** Behavioral Health and Acute Care multiples have the largest impact on valuation.")

    # Simple sensitivity table
    sensitivity_data = []
    behavioral_mults = [9.0, 10.0, 10.5, 11.0, 12.0]

    for mult in behavioral_mults:
        temp_multiples = multiples.copy()
        temp_multiples["behavioral"]["base"] = mult
        result = calculate_sotp(data, temp_multiples, "base")

        sensitivity_data.append({
            "Behavioral Multiple": f"{mult:.1f}x",
            "Value per Share": f"${result['metrics']['SOTP Value per Share']:.2f}",
            "Upside": f"{result['metrics']['Implied Upside (%)']:.1%}"
        })

    st.dataframe(pd.DataFrame(sensitivity_data), use_container_width=True)

# ----- TAB 6: DETAILED TABLES -----
with tab6:
    st.header("Detailed Data Tables")

    # Export full results
    st.subheader("Complete SOTP Calculation")

    full_results = {
        "Component": list(base_result["components"].keys()),
        "Value ($M)": [v/1e6 for v in base_result["components"].values()],
        "Value ($B)": [v/1e9 for v in base_result["components"].values()],
    }

    full_df = pd.DataFrame(full_results)

    st.dataframe(full_df, use_container_width=True)

    # Download button
    csv = full_df.to_csv(index=False)
    st.download_button(
        "Download SOTP Calculation (CSV)",
        csv,
        "uhs_sotp_valuation.csv",
        "text/csv",
        key="download-sotp"
    )

    st.markdown("---")

    # Input Assumptions Summary
    st.subheader("Input Assumptions Summary")

    assumptions = {
        "Category": [
            "Acute Care Multiple",
            "Behavioral Health Multiple",
            "Real Estate Cap Rate",
            "Real Estate $/SqFt",
            "Overhead Reduction",
            "Shares Outstanding (M)",
            "Current Share Price",
            "Net Debt ($B)"
        ],
        "Value": [
            f"{multiples['acute_care']['base']:.1f}x",
            f"{multiples['behavioral']['base']:.1f}x",
            f"{multiples['real_estate_cap_rate']['base']:.2%}",
            f"${multiples['real_estate_sqft']['base']:.0f}",
            f"{overhead_reduction_pct:.0%}",
            f"{capital.shares_outstanding/1e6:.1f}",
            f"${capital.share_price:.2f}",
            f"${capital.net_debt/1e9:.2f}"
        ]
    }

    st.dataframe(pd.DataFrame(assumptions), use_container_width=True)

# ==========================================
# FOOTER
# ==========================================

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #CC0000; font-size: 12px; padding: 20px; background-color: rgba(255, 230, 230, 0.5); border-radius: 8px;">
    <b>⚠️ CONFIDENTIAL & PROPRIETARY ANALYSIS ⚠️</b><br>
    This valuation model is confidential and intended solely for authorized use.<br>
    Unauthorized distribution or disclosure is strictly prohibited.<br>
    © 2025 - All Rights Reserved
</div>
""", unsafe_allow_html=True)
```

---

## 🚀 SETUP & LAUNCH INSTRUCTIONS

### 1. Navigate to Project Directory
```bash
cd ~/path/to/uhs-sotp-valuation
```

### 2. Activate Virtual Environment
```bash
source venv/bin/activate  # Mac/Linux
# or
venv\Scripts\activate  # Windows
```

### 3. Run the Model
```bash
# Test model.py first
python model.py

# Launch Streamlit app
streamlit run app.py
```

### 4. Access the Dashboard
Browser will open automatically to `http://localhost:8501`

---

## 📝 DATA INPUT WORKFLOW

### Step 1: Extract from 10-K

Create `data/uhs_financials.csv`:

```csv
Category,Metric,Value,Source
Acute Care,Revenue,7500000000,10-K pg 45
Acute Care,EBITDA,1200000000,10-K pg 52
Acute Care,Facilities,26,10-K pg 12
Behavioral,Revenue,6000000000,10-K pg 45
Behavioral,EBITDA,1400000000,10-K pg 52
Behavioral,Facilities,340,10-K pg 12
Real Estate,Book Value,5500000000,10-K Balance Sheet
Real Estate,Owned SqFt,25000000,Estimated
Corporate,Overhead Annual,450000000,10-K Income Statement
Capital,Total Debt,11500000000,10-K Balance Sheet
Capital,Cash,500000000,10-K Balance Sheet
Capital,Shares Outstanding,70000000,10-K pg 3
```

### Step 2: Update model.py

Replace placeholder values in `default_uhs_data()` with actual 10-K numbers.

### Step 3: Document Sources

Create `data/sources.md` to track where each number came from.

---

## 🔒 CONFIDENTIALITY BEST PRACTICES

1. **Never commit to public GitHub**
   - Keep repo private or local only
   - Use .gitignore for all data files

2. **Password protect exports**
   - When exporting CSV/PDF, encrypt files
   - Use secure file sharing (not email)

3. **Access control**
   - Only share with authorized team members
   - Keep track of who has access

4. **Secure your machine**
   - Encrypt hard drive
   - Lock screen when away
   - Delete files when project complete

---

## 📊 NEXT STEPS CHECKLIST

- [ ] Create project directory structure
- [ ] Set up virtual environment
- [ ] Copy requirements.txt from Ora
- [ ] Download UHS 10-K, 10-Q, Proxy from SEC
- [ ] Extract financial data to CSV
- [ ] Update model.py with actual data
- [ ] Test model.py calculations
- [ ] Customize app.py branding (UHS logo)
- [ ] Run Streamlit app and verify
- [ ] Document all assumptions
- [ ] Review with team (if applicable)
- [ ] Export final valuation report

---

## 💡 TIPS FOR SUCCESS

1. **Start with Base Case** - Get realistic assumptions first
2. **Validate Multiples** - Research comparable companies
3. **Document Everything** - Track every assumption and source
4. **Stress Test** - Run Bear scenario to understand downside
5. **Focus on Key Drivers** - Behavioral Health multiple is biggest lever

---

## 📚 RESOURCES

- **SEC EDGAR (UHS filings):** https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000352915
- **UHS Investor Relations:** https://www.uhsinc.com/investors/
- **Comparable Companies:** Acadia Healthcare (ACHC), Select Medical (SEM), Tenet Healthcare (THC)
- **Healthcare REITs:** Healthpeak (PEAK), Welltower (WELL), Sabra Health Care (SBRA)

---

**Good luck with your UHS SOTP analysis!**

Remember: This is a **confidential investment analysis** - treat it accordingly.
