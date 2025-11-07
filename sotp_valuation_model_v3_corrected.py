"""
UHS SOTP VALUATION MODEL v3.0 - CORRECTED
OpCo/PropCo Split with Proper EBITDA → EBITDAR → Normalized OpCo EBITDA Flow

METHODOLOGY:
1. Start with reported EBITDA (AFTER actual rent on leased facilities)
2. Add back actual rent → EBITDAR
3. Impute market rent on owned facilities
4. Subtract total rent (actual + imputed) → Normalized OpCo EBITDA (post-rent)
5. PropCo NOI = Total rent (actual + imputed)

ALL NUMBERS TRACED TO 10-K WITH DOCUMENTATION

Author: Investment Analysis Team
Date: October 30, 2025
"""

import pandas as pd
import numpy as np
import json
from datetime import datetime

# ============================================================================
# STEP 1: LOAD 10-K DATA WITH FULL TRACEABILITY
# ============================================================================

def load_10k_data():
    """Load extracted 10-K data with source references"""
    with open('data/UHS_10K_2024_comprehensive_data.json', 'r') as f:
        data = json.load(f)
    return data

# ============================================================================
# STEP 2: BUILD EBITDA → EBITDAR → NORMALIZED OPCO EBITDA
# ============================================================================

def normalize_ebitda_for_sotp(data):
    """
    Normalize segment EBITDAs for OpCo/PropCo split

    Flow:
    1. Reported EBITDA (from 10-K segment reporting)
    2. + Actual Rent Expense (from 10-K income statement)
    3. = EBITDAR (earnings before rent)
    4. Calculate Imputed Rent on Owned Facilities
    5. Normalized OpCo EBITDA = EBITDAR - Total Rent (actual + imputed)
    6. PropCo NOI = Total Rent (actual + imputed)

    SOURCE DOCUMENTATION:
    - Segment EBITDA: 10-K Note 15 (Segment Reporting)
    - Actual Rent: 10-K Consolidated Income Statement
    - Owned/Leased Mix: 10-K Note 9 (Related Party Transactions)
    - PPE Values: 10-K Consolidated Balance Sheet
    """

    # EXTRACT BASELINE DATA FROM 10-K
    behavioral = data['segment_financials']['behavioral_health']['2024']
    acute = data['segment_financials']['acute_care']['2024']
    real_estate = data['real_estate']

    # -------------------------------------------------------------------
    # ACUTE CARE NORMALIZATION
    # -------------------------------------------------------------------

    # Source: 10-K Note 15 (Segment Reporting)
    acute_revenue = acute['revenue'] / 1_000_000  # $8,922M
    acute_reported_ebitda = acute['adjusted_ebitda'] / 1_000_000  # $1,208M
    acute_ebitda_margin = acute['ebitda_margin']  # 13.5%

    # Source: 10-K Income Statement (Acute Care segment detail)
    # Note: Found in segment income statement detail
    acute_actual_rent = 99.1  # $99.1M (lease and rental expense)

    # Source: 10-K Note 9 (Owned vs Leased)
    acute_owned_beds = real_estate['owned_vs_leased']['acute_care']['owned_beds']  # 5,190
    acute_leased_beds = real_estate['owned_vs_leased']['acute_care']['leased_beds']  # 1,246
    acute_total_beds = acute_owned_beds + acute_leased_beds  # 6,436
    acute_owned_pct = acute_owned_beds / acute_total_beds  # 80.6%
    acute_leased_pct = acute_leased_beds / acute_total_beds  # 19.4%

    # STEP 1: Calculate EBITDAR (add back actual rent)
    acute_ebitdar = acute_reported_ebitda + acute_actual_rent  # $1,307M

    # STEP 2: Impute market rent on owned facilities
    # Method: Use actual rent on leased facilities to calculate $/bed, then apply to owned
    acute_rent_per_leased_bed = acute_actual_rent / acute_leased_beds  # $/bed/year
    acute_imputed_rent_owned = acute_rent_per_leased_bed * acute_owned_beds

    # STEP 3: Total rent (actual + imputed)
    acute_total_rent = acute_actual_rent + acute_imputed_rent_owned

    # STEP 4: Normalized OpCo EBITDA (post-rent)
    acute_opco_ebitda_normalized = acute_ebitdar - acute_total_rent

    # STEP 5: PropCo NOI (= total rent under NNN assumption)
    acute_propco_noi = acute_total_rent

    # -------------------------------------------------------------------
    # BEHAVIORAL HEALTH NORMALIZATION
    # -------------------------------------------------------------------

    # Source: 10-K Note 15 (Segment Reporting)
    behavioral_revenue = behavioral['revenue'] / 1_000_000  # $6,895M
    behavioral_reported_ebitda = behavioral['adjusted_ebitda'] / 1_000_000  # $1,567M
    behavioral_ebitda_margin = behavioral['ebitda_margin']  # 22.7%

    # Source: 10-K Income Statement (Behavioral segment detail)
    behavioral_actual_rent = 47.0  # $47.0M (lease and rental expense)

    # Source: 10-K Note 9 (Owned vs Leased)
    behavioral_owned_beds = real_estate['owned_vs_leased']['behavioral_health']['owned_beds']  # 22,465
    behavioral_leased_beds = real_estate['owned_vs_leased']['behavioral_health']['leased_beds']  # 1,656
    behavioral_total_beds = behavioral_owned_beds + behavioral_leased_beds  # 24,121
    behavioral_owned_pct = behavioral_owned_beds / behavioral_total_beds  # 93.1%
    behavioral_leased_pct = behavioral_leased_beds / behavioral_total_beds  # 6.9%

    # STEP 1: Calculate EBITDAR (add back actual rent)
    behavioral_ebitdar = behavioral_reported_ebitda + behavioral_actual_rent  # $1,614M

    # STEP 2: Impute market rent on owned facilities
    behavioral_rent_per_leased_bed = behavioral_actual_rent / behavioral_leased_beds  # $/bed/year
    behavioral_imputed_rent_owned = behavioral_rent_per_leased_bed * behavioral_owned_beds

    # STEP 3: Total rent (actual + imputed)
    behavioral_total_rent = behavioral_actual_rent + behavioral_imputed_rent_owned

    # STEP 4: Normalized OpCo EBITDA (post-rent)
    behavioral_opco_ebitda_normalized = behavioral_ebitdar - behavioral_total_rent

    # STEP 5: PropCo NOI (= total rent under NNN assumption)
    behavioral_propco_noi = behavioral_total_rent

    # -------------------------------------------------------------------
    # CALCULATE IMPLIED REAL ESTATE VALUES (VALIDATION)
    # -------------------------------------------------------------------

    # Using base case 6.5% cap rate
    cap_rate_base = 0.065

    acute_implied_re_value = acute_propco_noi / cap_rate_base
    behavioral_implied_re_value = behavioral_propco_noi / cap_rate_base
    total_implied_re_value = acute_implied_re_value + behavioral_implied_re_value

    # Compare to actual PPE (net) from balance sheet
    total_ppe_net = real_estate['property_plant_equipment']['total_ppe_net'] / 1_000_000  # $6,572M

    # -------------------------------------------------------------------
    # PACKAGE RESULTS
    # -------------------------------------------------------------------

    results = {
        'acute': {
            # Source data
            'revenue': acute_revenue,
            'reported_ebitda': acute_reported_ebitda,
            'ebitda_margin': acute_ebitda_margin,
            'actual_rent': acute_actual_rent,
            'total_beds': acute_total_beds,
            'owned_beds': acute_owned_beds,
            'leased_beds': acute_leased_beds,
            'owned_pct': acute_owned_pct,

            # Normalization flow
            'ebitdar': acute_ebitdar,
            'rent_per_leased_bed': acute_rent_per_leased_bed,
            'imputed_rent_owned': acute_imputed_rent_owned,
            'total_rent': acute_total_rent,
            'opco_ebitda_normalized': acute_opco_ebitda_normalized,
            'propco_noi': acute_propco_noi,

            # Implied values
            'implied_re_value_6_5_cap': acute_implied_re_value,

            # 10-K references
            'sources': {
                'ebitda': '10-K Note 15 (Segment Reporting)',
                'rent': '10-K Income Statement (Acute segment detail)',
                'owned_leased': '10-K Note 9 (Related Party Transactions)',
            }
        },
        'behavioral': {
            # Source data
            'revenue': behavioral_revenue,
            'reported_ebitda': behavioral_reported_ebitda,
            'ebitda_margin': behavioral_ebitda_margin,
            'actual_rent': behavioral_actual_rent,
            'total_beds': behavioral_total_beds,
            'owned_beds': behavioral_owned_beds,
            'leased_beds': behavioral_leased_beds,
            'owned_pct': behavioral_owned_pct,

            # Normalization flow
            'ebitdar': behavioral_ebitdar,
            'rent_per_leased_bed': behavioral_rent_per_leased_bed,
            'imputed_rent_owned': behavioral_imputed_rent_owned,
            'total_rent': behavioral_total_rent,
            'opco_ebitda_normalized': behavioral_opco_ebitda_normalized,
            'propco_noi': behavioral_propco_noi,

            # Implied values
            'implied_re_value_6_5_cap': behavioral_implied_re_value,

            # 10-K references
            'sources': {
                'ebitda': '10-K Note 15 (Segment Reporting)',
                'rent': '10-K Income Statement (Behavioral segment detail)',
                'owned_leased': '10-K Note 9 (Related Party Transactions)',
            }
        },
        'consolidated': {
            'total_revenue': acute_revenue + behavioral_revenue,
            'total_reported_ebitda': acute_reported_ebitda + behavioral_reported_ebitda,
            'total_actual_rent': acute_actual_rent + behavioral_actual_rent,
            'total_ebitdar': acute_ebitdar + behavioral_ebitdar,
            'total_imputed_rent': acute_imputed_rent_owned + behavioral_imputed_rent_owned,
            'total_rent_normalized': acute_total_rent + behavioral_total_rent,
            'total_opco_ebitda_normalized': acute_opco_ebitda_normalized + behavioral_opco_ebitda_normalized,
            'total_propco_noi': acute_propco_noi + behavioral_propco_noi,
            'total_implied_re_value_6_5_cap': total_implied_re_value,
            'actual_ppe_net': total_ppe_net,
            're_value_reconciliation': (total_implied_re_value / total_ppe_net) - 1  # % difference
        }
    }

    return results

# ============================================================================
# STEP 3: APPLY VALUATION MULTIPLES (SOTP)
# ============================================================================

def calculate_sotp_valuation(normalized_data, scenario='base'):
    """
    Calculate four-part SOTP valuation using normalized EBITDAs

    MULTIPLES SOURCES:
    - Behavioral OpCo: 8-11x (comps: ACHC, PSYT, AMED)
    - Acute Care OpCo: 6-8x (comps: THC, CYH, LPNT)
    - PropCo Cap Rate: 5.5-7.5% (healthcare REIT comps: VTR, HR, MPW)

    Scenarios:
    - Bear: Conservative multiples (low OpCo, high cap rate)
    - Base: Mid-range multiples
    - Bull: Optimistic multiples (high OpCo, low cap rate)
    """

    # Define scenario parameters
    multiples = {
        'bear': {
            'behavioral_opco_multiple': 8.0,
            'acute_opco_multiple': 6.0,
            'cap_rate': 0.075,  # Higher cap = lower PropCo value
        },
        'base': {
            'behavioral_opco_multiple': 9.5,
            'acute_opco_multiple': 7.0,
            'cap_rate': 0.065,
        },
        'bull': {
            'behavioral_opco_multiple': 11.0,
            'acute_opco_multiple': 8.0,
            'cap_rate': 0.055,  # Lower cap = higher PropCo value
        }
    }

    params = multiples[scenario]

    # PART 1: BEHAVIORAL OPCO
    behavioral_opco_ebitda = normalized_data['behavioral']['opco_ebitda_normalized']
    behavioral_opco_value = behavioral_opco_ebitda * params['behavioral_opco_multiple']

    # PART 2: BEHAVIORAL PROPCO
    behavioral_propco_noi = normalized_data['behavioral']['propco_noi']
    behavioral_propco_value = behavioral_propco_noi / params['cap_rate']

    # PART 3: ACUTE OPCO
    acute_opco_ebitda = normalized_data['acute']['opco_ebitda_normalized']
    acute_opco_value = acute_opco_ebitda * params['acute_opco_multiple']

    # PART 4: ACUTE PROPCO
    acute_propco_noi = normalized_data['acute']['propco_noi']
    acute_propco_value = acute_propco_noi / params['cap_rate']

    # TOTAL ENTERPRISE VALUE
    total_enterprise_value = (
        behavioral_opco_value +
        behavioral_propco_value +
        acute_opco_value +
        acute_propco_value
    )

    # EQUITY VALUE
    # Source: 10-K Balance Sheet & Debt Schedule
    net_debt = 4378.5  # $4,378.5M (from 10-K)
    equity_value = total_enterprise_value - net_debt

    # PER SHARE VALUE
    # Source: 10-K Capital Structure
    shares_outstanding = 64.98  # Million shares
    value_per_share = equity_value / shares_outstanding

    # CURRENT MARKET (as of valuation date)
    current_price = 208.39
    current_market_cap = current_price * shares_outstanding
    current_ev = current_market_cap + net_debt

    # UPSIDE ANALYSIS
    upside_pct = ((value_per_share - current_price) / current_price) * 100
    ev_upside_pct = ((total_enterprise_value - current_ev) / current_ev) * 100

    results = {
        'scenario': scenario,
        'multiples': params,

        # OpCo values
        'behavioral_opco_ebitda': behavioral_opco_ebitda,
        'behavioral_opco_value': behavioral_opco_value,
        'acute_opco_ebitda': acute_opco_ebitda,
        'acute_opco_value': acute_opco_value,
        'total_opco_value': behavioral_opco_value + acute_opco_value,

        # PropCo values
        'behavioral_propco_noi': behavioral_propco_noi,
        'behavioral_propco_value': behavioral_propco_value,
        'acute_propco_noi': acute_propco_noi,
        'acute_propco_value': acute_propco_value,
        'total_propco_value': behavioral_propco_value + acute_propco_value,

        # Enterprise & equity
        'total_enterprise_value': total_enterprise_value,
        'net_debt': net_debt,
        'equity_value': equity_value,
        'shares_outstanding': shares_outstanding,
        'value_per_share': value_per_share,

        # Market comparison
        'current_price': current_price,
        'current_market_cap': current_market_cap,
        'current_ev': current_ev,
        'upside_pct': upside_pct,
        'ev_upside_pct': ev_upside_pct,

        # Mix analysis
        'opco_pct_of_ev': (behavioral_opco_value + acute_opco_value) / total_enterprise_value * 100,
        'propco_pct_of_ev': (behavioral_propco_value + acute_propco_value) / total_enterprise_value * 100,
    }

    return results

# ============================================================================
# STEP 4: PROPCO DIVIDEND YIELD ANALYSIS (CAP RATE VS DIVIDEND YIELD)
# ============================================================================

def analyze_propco_dividend_feasibility(normalized_data, target_dividend_yield=0.08):
    """
    Validate whether 8% dividend yield is feasible given PropCo NOI and leverage

    Formula:
    Equity Yield = (Cap Rate - (Debt Constant × LTV)) / (1 - LTV)

    Where:
    - Cap Rate = NOI / Property Value
    - Debt Constant = Annual Debt Service / Loan Amount (includes interest + amortization)
    - LTV = Loan-to-Value ratio
    - Equity Yield = Cash to Equity / Equity Investment (pre-tax dividend yield)
    """

    # PropCo parameters
    total_propco_noi = normalized_data['consolidated']['total_propco_noi']
    cap_rate = 0.065  # Base case

    # Calculate PropCo value
    propco_value = total_propco_noi / cap_rate

    # Test various leverage scenarios
    scenarios = []

    for ltv in np.arange(0.50, 0.76, 0.05):
        for interest_rate in [0.055, 0.060, 0.065, 0.070]:
            # Assume 25-year amortization for debt constant calculation
            # Debt constant ≈ interest rate + 1% (simplified for 25-year amortization)
            debt_constant = interest_rate + 0.01

            # Calculate equity yield
            equity_yield = (cap_rate - (debt_constant * ltv)) / (1 - ltv)

            # Debt and equity sizing
            debt = propco_value * ltv
            equity = propco_value * (1 - ltv)
            debt_service = debt * debt_constant
            cash_to_equity = total_propco_noi - debt_service

            # DSCR (Debt Service Coverage Ratio)
            dscr = total_propco_noi / debt_service if debt_service > 0 else 0

            # Check if target dividend is achievable
            meets_target = equity_yield >= target_dividend_yield

            scenarios.append({
                'ltv': ltv,
                'interest_rate': interest_rate,
                'debt_constant': debt_constant,
                'equity_yield': equity_yield,
                'propco_value': propco_value,
                'debt': debt,
                'equity': equity,
                'debt_service': debt_service,
                'cash_to_equity': cash_to_equity,
                'dscr': dscr,
                'meets_8pct_target': meets_target
            })

    df = pd.DataFrame(scenarios)

    # Filter to viable scenarios (DSCR > 1.20 and meets target)
    viable_scenarios = df[(df['dscr'] >= 1.20) & (df['meets_8pct_target'] == True)]

    return {
        'all_scenarios': df,
        'viable_scenarios': viable_scenarios,
        'total_propco_noi': total_propco_noi,
        'propco_value_at_6_5_cap': propco_value,
        'target_dividend_yield': target_dividend_yield,
        'is_8pct_feasible': len(viable_scenarios) > 0
    }

# ============================================================================
# STEP 5: GENERATE COMPREHENSIVE REPORT
# ============================================================================

def generate_valuation_report():
    """Generate complete SOTP valuation with full 10-K traceability"""

    print("=" * 100)
    print("UHS SOTP VALUATION MODEL v3.0 - CORRECTED")
    print("OpCo/PropCo Split with Proper Normalization")
    print("=" * 100)
    print()

    # Load 10-K data
    data = load_10k_data()

    # STEP 1: Normalize EBITDAs
    print("STEP 1: EBITDA → EBITDAR → NORMALIZED OPCO EBITDA")
    print("-" * 100)

    normalized = normalize_ebitda_for_sotp(data)

    # Display Acute Care normalization
    acute = normalized['acute']
    print("\nACUTE CARE NORMALIZATION:")
    print(f"  Revenue (10-K):                  ${acute['revenue']:>10,.0f}M")
    print(f"  Reported EBITDA (10-K):          ${acute['reported_ebitda']:>10,.0f}M  ({acute['ebitda_margin']:.1%} margin)")
    print(f"  + Actual Rent (10-K):            ${acute['actual_rent']:>10,.0f}M")
    print(f"  = EBITDAR:                       ${acute['ebitdar']:>10,.0f}M")
    print(f"")
    print(f"  Owned/Leased Mix (10-K):")
    print(f"    Owned:  {acute['owned_beds']:,} beds ({acute['owned_pct']:.1%})")
    print(f"    Leased: {acute['leased_beds']:,} beds ({1-acute['owned_pct']:.1%})")
    print(f"")
    print(f"  Rent per Leased Bed:             ${acute['rent_per_leased_bed']:>10,.0f} /bed/year")
    print(f"  × Owned Beds ({acute['owned_beds']:,}):         ${acute['imputed_rent_owned']:>10,.0f}M (imputed)")
    print(f"  Total Rent (actual + imputed):   ${acute['total_rent']:>10,.0f}M")
    print(f"")
    print(f"  EBITDAR:                         ${acute['ebitdar']:>10,.0f}M")
    print(f"  - Total Rent:                    ${acute['total_rent']:>10,.0f}M")
    print(f"  = Normalized OpCo EBITDA:        ${acute['opco_ebitda_normalized']:>10,.0f}M")
    print(f"")
    print(f"  PropCo NOI (= Total Rent):       ${acute['propco_noi']:>10,.0f}M")
    print(f"  Implied RE Value (6.5% cap):     ${acute['implied_re_value_6_5_cap']:>10,.0f}M")

    # Display Behavioral normalization
    beh = normalized['behavioral']
    print("\n" + "="*100)
    print("BEHAVIORAL HEALTH NORMALIZATION:")
    print(f"  Revenue (10-K):                  ${beh['revenue']:>10,.0f}M")
    print(f"  Reported EBITDA (10-K):          ${beh['reported_ebitda']:>10,.0f}M  ({beh['ebitda_margin']:.1%} margin)")
    print(f"  + Actual Rent (10-K):            ${beh['actual_rent']:>10,.0f}M")
    print(f"  = EBITDAR:                       ${beh['ebitdar']:>10,.0f}M")
    print(f"")
    print(f"  Owned/Leased Mix (10-K):")
    print(f"    Owned:  {beh['owned_beds']:,} beds ({beh['owned_pct']:.1%})")
    print(f"    Leased: {beh['leased_beds']:,} beds ({1-beh['owned_pct']:.1%})")
    print(f"")
    print(f"  Rent per Leased Bed:             ${beh['rent_per_leased_bed']:>10,.0f} /bed/year")
    print(f"  × Owned Beds ({beh['owned_beds']:,}):        ${beh['imputed_rent_owned']:>10,.0f}M (imputed)")
    print(f"  Total Rent (actual + imputed):   ${beh['total_rent']:>10,.0f}M")
    print(f"")
    print(f"  EBITDAR:                         ${beh['ebitdar']:>10,.0f}M")
    print(f"  - Total Rent:                    ${beh['total_rent']:>10,.0f}M")
    print(f"  = Normalized OpCo EBITDA:        ${beh['opco_ebitda_normalized']:>10,.0f}M")
    print(f"")
    print(f"  PropCo NOI (= Total Rent):       ${beh['propco_noi']:>10,.0f}M")
    print(f"  Implied RE Value (6.5% cap):     ${beh['implied_re_value_6_5_cap']:>10,.0f}M")

    # Display consolidated
    cons = normalized['consolidated']
    print("\n" + "="*100)
    print("CONSOLIDATED SUMMARY:")
    print(f"  Total Reported EBITDA:           ${cons['total_reported_ebitda']:>10,.0f}M")
    print(f"  Total Actual Rent:               ${cons['total_actual_rent']:>10,.0f}M")
    print(f"  Total EBITDAR:                   ${cons['total_ebitdar']:>10,.0f}M")
    print(f"  Total Imputed Rent (owned):      ${cons['total_imputed_rent']:>10,.0f}M")
    print(f"  Total Rent (normalized):         ${cons['total_rent_normalized']:>10,.0f}M")
    print(f"  Total Normalized OpCo EBITDA:    ${cons['total_opco_ebitda_normalized']:>10,.0f}M")
    print(f"  Total PropCo NOI:                ${cons['total_propco_noi']:>10,.0f}M")
    print(f"")
    print(f"  Implied Total RE Value (6.5%):   ${cons['total_implied_re_value_6_5_cap']:>10,.0f}M")
    print(f"  Actual PPE (net) from 10-K:      ${cons['actual_ppe_net']:>10,.0f}M")
    print(f"  Reconciliation:                  {cons['re_value_reconciliation']:>10.1%} difference")

    # STEP 2: Calculate SOTP Valuations
    print("\n\n" + "="*100)
    print("STEP 2: SOTP VALUATION - THREE SCENARIOS")
    print("-" * 100)

    scenarios = {}
    for scenario in ['bear', 'base', 'bull']:
        scenarios[scenario] = calculate_sotp_valuation(normalized, scenario)

    # Create summary table
    summary_data = []
    for scenario in ['bear', 'base', 'bull']:
        s = scenarios[scenario]
        summary_data.append({
            'Scenario': scenario.upper(),
            'Behavioral OpCo': f"${s['behavioral_opco_value']:,.0f}M",
            'Behavioral PropCo': f"${s['behavioral_propco_value']:,.0f}M",
            'Acute OpCo': f"${s['acute_opco_value']:,.0f}M",
            'Acute PropCo': f"${s['acute_propco_value']:,.0f}M",
            'Total EV': f"${s['total_enterprise_value']:,.0f}M",
            'Equity Value': f"${s['equity_value']:,.0f}M",
            'Price/Share': f"${s['value_per_share']:.2f}",
            'Upside': f"{s['upside_pct']:+.1f}%"
        })

    summary_df = pd.DataFrame(summary_data)
    print("\n" + summary_df.to_string(index=False))

    # Display base case detail
    base = scenarios['base']
    print("\n" + "="*100)
    print("BASE CASE DETAIL:")
    print(f"  Multiples:")
    print(f"    Behavioral OpCo:               {base['multiples']['behavioral_opco_multiple']:.1f}x EBITDA")
    print(f"    Acute Care OpCo:               {base['multiples']['acute_opco_multiple']:.1f}x EBITDA")
    print(f"    PropCo Cap Rate:               {base['multiples']['cap_rate']:.1%}")
    print(f"")
    print(f"  OpCo Valuation:")
    print(f"    Behavioral OpCo EBITDA:        ${base['behavioral_opco_ebitda']:,.0f}M")
    print(f"    × Multiple:                    {base['multiples']['behavioral_opco_multiple']:.1f}x")
    print(f"    = Behavioral OpCo Value:       ${base['behavioral_opco_value']:,.0f}M")
    print(f"")
    print(f"    Acute Care OpCo EBITDA:        ${base['acute_opco_ebitda']:,.0f}M")
    print(f"    × Multiple:                    {base['multiples']['acute_opco_multiple']:.1f}x")
    print(f"    = Acute Care OpCo Value:       ${base['acute_opco_value']:,.0f}M")
    print(f"")
    print(f"  PropCo Valuation:")
    print(f"    Behavioral PropCo NOI:         ${base['behavioral_propco_noi']:,.0f}M")
    print(f"    ÷ Cap Rate:                    {base['multiples']['cap_rate']:.1%}")
    print(f"    = Behavioral PropCo Value:     ${base['behavioral_propco_value']:,.0f}M")
    print(f"")
    print(f"    Acute Care PropCo NOI:         ${base['acute_propco_noi']:,.0f}M")
    print(f"    ÷ Cap Rate:                    {base['multiples']['cap_rate']:.1%}")
    print(f"    = Acute Care PropCo Value:     ${base['acute_propco_value']:,.0f}M")
    print(f"")
    print(f"  Enterprise Value:")
    print(f"    Total OpCo:                    ${base['total_opco_value']:,.0f}M ({base['opco_pct_of_ev']:.1f}%)")
    print(f"    Total PropCo:                  ${base['total_propco_value']:,.0f}M ({base['propco_pct_of_ev']:.1f}%)")
    print(f"    Total EV:                      ${base['total_enterprise_value']:,.0f}M")
    print(f"")
    print(f"  Equity Value:")
    print(f"    Enterprise Value:              ${base['total_enterprise_value']:,.0f}M")
    print(f"    - Net Debt:                    ${base['net_debt']:,.0f}M")
    print(f"    = Equity Value:                ${base['equity_value']:,.0f}M")
    print(f"")
    print(f"  Per Share:")
    print(f"    Shares Outstanding:            {base['shares_outstanding']:.2f}M")
    print(f"    Fair Value per Share:          ${base['value_per_share']:.2f}")
    print(f"    Current Price:                 ${base['current_price']:.2f}")
    print(f"    Upside:                        {base['upside_pct']:+.1f}%")

    # STEP 3: PropCo Dividend Feasibility
    print("\n\n" + "="*100)
    print("STEP 3: PROPCO DIVIDEND YIELD ANALYSIS (CAP RATE VS DIVIDEND YIELD)")
    print("-" * 100)

    dividend_analysis = analyze_propco_dividend_feasibility(normalized, target_dividend_yield=0.08)

    print(f"\nPropCo Parameters:")
    print(f"  Total PropCo NOI:                ${dividend_analysis['total_propco_noi']:,.0f}M")
    print(f"  PropCo Value (6.5% cap):         ${dividend_analysis['propco_value_at_6_5_cap']:,.0f}M")
    print(f"  Target Dividend Yield:           {dividend_analysis['target_dividend_yield']:.1%}")
    print(f"")
    print(f"Is 8% dividend feasible?           {'YES' if dividend_analysis['is_8pct_feasible'] else 'NO'}")

    if dividend_analysis['is_8pct_feasible']:
        print(f"\nViable Scenarios (DSCR ≥ 1.20 and Equity Yield ≥ 8%):")
        viable = dividend_analysis['viable_scenarios']
        display_cols = ['ltv', 'interest_rate', 'equity_yield', 'dscr', 'debt', 'equity', 'cash_to_equity']
        viable_display = viable[display_cols].copy()
        viable_display['ltv'] = viable_display['ltv'].apply(lambda x: f"{x:.0%}")
        viable_display['interest_rate'] = viable_display['interest_rate'].apply(lambda x: f"{x:.1%}")
        viable_display['equity_yield'] = viable_display['equity_yield'].apply(lambda x: f"{x:.1%}")
        viable_display['dscr'] = viable_display['dscr'].apply(lambda x: f"{x:.2f}x")
        viable_display['debt'] = viable_display['debt'].apply(lambda x: f"${x:,.0f}M")
        viable_display['equity'] = viable_display['equity'].apply(lambda x: f"${x:,.0f}M")
        viable_display['cash_to_equity'] = viable_display['cash_to_equity'].apply(lambda x: f"${x:,.0f}M")

        viable_display.columns = ['LTV', 'Interest Rate', 'Equity Yield', 'DSCR', 'Debt', 'Equity', 'Cash to Equity']
        print(viable_display.head(10).to_string(index=False))

    # STEP 4: Save outputs
    print("\n\n" + "="*100)
    print("STEP 4: SAVING OUTPUTS")
    print("-" * 100)

    # Save normalization detail
    norm_export = []
    for segment in ['acute', 'behavioral']:
        d = normalized[segment]
        norm_export.append({
            'Segment': segment.upper(),
            'Revenue': d['revenue'],
            'Reported_EBITDA': d['reported_ebitda'],
            'EBITDA_Margin': d['ebitda_margin'],
            'Actual_Rent': d['actual_rent'],
            'EBITDAR': d['ebitdar'],
            'Total_Beds': d['total_beds'],
            'Owned_Beds': d['owned_beds'],
            'Leased_Beds': d['leased_beds'],
            'Owned_Pct': d['owned_pct'],
            'Rent_Per_Leased_Bed': d['rent_per_leased_bed'],
            'Imputed_Rent_Owned': d['imputed_rent_owned'],
            'Total_Rent': d['total_rent'],
            'Normalized_OpCo_EBITDA': d['opco_ebitda_normalized'],
            'PropCo_NOI': d['propco_noi'],
            'Implied_RE_Value_6_5_Cap': d['implied_re_value_6_5_cap']
        })

    norm_df = pd.DataFrame(norm_export)
    norm_df.to_csv('data/graphs/ebitda_normalization_detail.csv', index=False)
    print("✓ Saved: data/graphs/ebitda_normalization_detail.csv")

    # Save scenario comparison
    summary_df.to_csv('data/graphs/sotp_valuation_scenarios_v3.csv', index=False)
    print("✓ Saved: data/graphs/sotp_valuation_scenarios_v3.csv")

    # Save dividend analysis
    if dividend_analysis['is_8pct_feasible']:
        dividend_analysis['viable_scenarios'].to_csv('data/graphs/propco_dividend_feasibility.csv', index=False)
        print("✓ Saved: data/graphs/propco_dividend_feasibility.csv")

    print()
    print("="*100)
    print("VALUATION COMPLETE!")
    print("="*100)

    return {
        'normalized': normalized,
        'scenarios': scenarios,
        'dividend_analysis': dividend_analysis
    }

# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    results = generate_valuation_report()
