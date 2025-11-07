"""
UHS SOTP VALUATION MODEL v2.0
Four-Part Sum-of-the-Parts Valuation with Real 10-K Data

Purpose: Calculate intrinsic value by separately valuing:
1. Behavioral Health Operations (OpCo)
2. Behavioral Health Real Estate (PropCo)
3. Acute Care Operations (OpCo)
4. Acute Care Real Estate (PropCo)

Author: Investment Analysis Team
Date: October 29, 2025
"""

import pandas as pd
import numpy as np
import json
from datetime import datetime

# ============================================================================
# STEP 1: LOAD COMPREHENSIVE 10-K DATA
# ============================================================================

def load_10k_data():
    """Load extracted 10-K data from comprehensive JSON"""
    with open('data/UHS_10K_2024_comprehensive_data.json', 'r') as f:
        data = json.load(f)
    return data

# ============================================================================
# STEP 2: CALCULATE PRO-FORMA OPERATING EBITDAS (ADD BACK IMPUTED RENT)
# ============================================================================

def calculate_proforma_ebitdas(data):
    """
    Calculate pro-forma OpCo EBITDAs by adding back imputed rent

    Logic:
    - Owned facilities don't pay rent in reported EBITDA
    - To value OpCo separately from PropCo, we must add back market rent
    - Use cap rate method: Imputed Rent = Real Estate Value × Cap Rate
    """

    # Extract segment data (all values in actual dollars, convert to millions)
    behavioral = data['segment_financials']['behavioral_health']['2024']
    acute = data['segment_financials']['acute_care']['2024']

    behavioral_revenue = behavioral['revenue'] / 1_000_000  # Convert to $M
    behavioral_ebitda = behavioral['adjusted_ebitda'] / 1_000_000  # Convert to $M
    behavioral_margin = behavioral['ebitda_margin']  # 22.7%
    behavioral_beds = 24121

    acute_revenue = acute['revenue'] / 1_000_000  # Convert to $M
    acute_ebitda = acute['adjusted_ebitda'] / 1_000_000  # Convert to $M
    acute_margin = acute['ebitda_margin']  # 13.5%
    acute_beds = 6436

    # REAL ESTATE ALLOCATION (convert to millions)
    # We'll use 3 methods and average them
    total_ppe_net = data['balance_sheet']['2024']['assets']['non_current_assets']['property_plant_equipment']['net_ppe'] / 1_000_000  # $6,572M

    # Method 1: By beds (more weighted to behavioral - 79% of beds)
    behavioral_re_beds = (behavioral_beds / (behavioral_beds + acute_beds)) * total_ppe_net
    acute_re_beds = (acute_beds / (behavioral_beds + acute_beds)) * total_ppe_net

    # Method 2: By revenue (56% acute, 44% behavioral)
    total_revenue = behavioral_revenue + acute_revenue
    behavioral_re_revenue = (behavioral_revenue / total_revenue) * total_ppe_net
    acute_re_revenue = (acute_revenue / total_revenue) * total_ppe_net

    # Method 3: By EBITDA (56% behavioral, 44% acute)
    total_ebitda = behavioral_ebitda + acute_ebitda
    behavioral_re_ebitda = (behavioral_ebitda / total_ebitda) * total_ppe_net
    acute_re_ebitda = (acute_ebitda / total_ebitda) * total_ppe_net

    # Average the three methods
    behavioral_re = (behavioral_re_beds + behavioral_re_revenue + behavioral_re_ebitda) / 3
    acute_re = (acute_re_beds + acute_re_revenue + acute_re_ebitda) / 3

    # CALCULATE IMPUTED RENT (Cap Rate × Real Estate Value)
    cap_rate_base = 0.065  # 6.5% base case
    cap_rate_bear = 0.075  # 7.5% bear case (higher cap rate = lower RE value)
    cap_rate_bull = 0.055  # 5.5% bull case (lower cap rate = higher RE value)

    # Base case imputed rent
    behavioral_imputed_rent = behavioral_re * cap_rate_base
    acute_imputed_rent = acute_re * cap_rate_base

    # PRO-FORMA OPCO EBITDAS (Reported + Imputed Rent)
    behavioral_opco_ebitda = behavioral_ebitda + behavioral_imputed_rent
    acute_opco_ebitda = acute_ebitda + acute_imputed_rent

    results = {
        'behavioral': {
            'reported_ebitda': behavioral_ebitda,
            'real_estate_value': behavioral_re,
            'imputed_rent': behavioral_imputed_rent,
            'proforma_opco_ebitda': behavioral_opco_ebitda,
            'beds': behavioral_beds,
            'revenue': behavioral_revenue,
            'margin': behavioral_margin
        },
        'acute': {
            'reported_ebitda': acute_ebitda,
            'real_estate_value': acute_re,
            'imputed_rent': acute_imputed_rent,
            'proforma_opco_ebitda': acute_opco_ebitda,
            'beds': acute_beds,
            'revenue': acute_revenue,
            'margin': acute_margin
        },
        'total_ppe': total_ppe_net
    }

    return results

# ============================================================================
# STEP 3: APPLY INDUSTRY MULTIPLES (FROM COMPS RESEARCH)
# ============================================================================

def calculate_sotp_valuation(proforma_data, scenario='base'):
    """
    Calculate four-part SOTP valuation

    Multiples from industry research:
    - Behavioral Health OpCo: 8-11x EBITDA (pure-plays like ACHC)
    - Acute Care OpCo: 6-8x EBITDA (THC, CYH range)
    - Real Estate: Cap rate method (6-7% cap rates for healthcare RE)

    Scenarios:
    - Bear: Conservative multiples
    - Base: Middle of range
    - Bull: Optimistic multiples
    """

    # Define multiples by scenario
    multiples = {
        'bear': {
            'behavioral_opco_multiple': 8.0,
            'acute_opco_multiple': 6.0,
            'cap_rate': 0.075,  # Higher cap rate = lower RE value
        },
        'base': {
            'behavioral_opco_multiple': 9.5,
            'acute_opco_multiple': 7.0,
            'cap_rate': 0.065,
        },
        'bull': {
            'behavioral_opco_multiple': 11.0,
            'acute_opco_multiple': 8.0,
            'cap_rate': 0.055,  # Lower cap rate = higher RE value
        }
    }

    params = multiples[scenario]

    # PART 1: BEHAVIORAL OPCO VALUE
    behavioral_opco_ebitda = proforma_data['behavioral']['proforma_opco_ebitda']
    behavioral_opco_value = behavioral_opco_ebitda * params['behavioral_opco_multiple']

    # PART 2: BEHAVIORAL PROPCO VALUE (Cap Rate Method)
    # Value = NOI / Cap Rate, where NOI = Imputed Rent
    behavioral_propco_noi = proforma_data['behavioral']['imputed_rent']
    behavioral_propco_value = behavioral_propco_noi / params['cap_rate']

    # PART 3: ACUTE CARE OPCO VALUE
    acute_opco_ebitda = proforma_data['acute']['proforma_opco_ebitda']
    acute_opco_value = acute_opco_ebitda * params['acute_opco_multiple']

    # PART 4: ACUTE CARE PROPCO VALUE
    acute_propco_noi = proforma_data['acute']['imputed_rent']
    acute_propco_value = acute_propco_noi / params['cap_rate']

    # TOTAL ENTERPRISE VALUE
    total_enterprise_value = (
        behavioral_opco_value +
        behavioral_propco_value +
        acute_opco_value +
        acute_propco_value
    )

    # EQUITY VALUE (EV - Net Debt)
    net_debt = 4378.5  # From 10-K: $4,378.5M net debt
    equity_value = total_enterprise_value - net_debt

    # PER SHARE VALUE
    shares_outstanding = 64.98  # From capital structure
    value_per_share = equity_value / shares_outstanding

    # Current market price
    current_price = 208.39
    upside_pct = ((value_per_share - current_price) / current_price) * 100

    results = {
        'scenario': scenario,
        'multiples': params,
        'behavioral_opco_value': behavioral_opco_value,
        'behavioral_propco_value': behavioral_propco_value,
        'acute_opco_value': acute_opco_value,
        'acute_propco_value': acute_propco_value,
        'total_enterprise_value': total_enterprise_value,
        'net_debt': net_debt,
        'equity_value': equity_value,
        'shares_outstanding': shares_outstanding,
        'value_per_share': value_per_share,
        'current_price': current_price,
        'upside_pct': upside_pct,
        # Additional metrics
        'behavioral_opco_ebitda': behavioral_opco_ebitda,
        'behavioral_propco_noi': behavioral_propco_noi,
        'acute_opco_ebitda': acute_opco_ebitda,
        'acute_propco_noi': acute_propco_noi,
    }

    return results

# ============================================================================
# STEP 4: SENSITIVITY ANALYSIS
# ============================================================================

def create_sensitivity_table(proforma_data):
    """
    Create sensitivity tables for:
    1. Behavioral OpCo Multiple vs Cap Rate
    2. Acute OpCo Multiple vs Cap Rate
    3. Two-way: Behavioral Multiple vs Acute Multiple
    """

    # Sensitivity ranges
    behavioral_multiples = np.arange(7.0, 12.5, 0.5)
    acute_multiples = np.arange(5.0, 9.5, 0.5)
    cap_rates = np.arange(0.050, 0.085, 0.005)

    # TABLE 1: Value per share vs Behavioral Multiple & Cap Rate
    sensitivity_1 = pd.DataFrame(index=behavioral_multiples, columns=cap_rates)

    for beh_mult in behavioral_multiples:
        for cap_rate in cap_rates:
            # Calculate value with these parameters
            beh_opco = proforma_data['behavioral']['proforma_opco_ebitda'] * beh_mult
            beh_propco = proforma_data['behavioral']['imputed_rent'] / cap_rate
            acute_opco = proforma_data['acute']['proforma_opco_ebitda'] * 7.0  # Hold acute at base
            acute_propco = proforma_data['acute']['imputed_rent'] / cap_rate

            ev = beh_opco + beh_propco + acute_opco + acute_propco
            equity = ev - 4378.5
            per_share = equity / 64.98

            sensitivity_1.loc[beh_mult, cap_rate] = round(per_share, 2)

    # TABLE 2: Value per share vs Behavioral Multiple & Acute Multiple
    sensitivity_2 = pd.DataFrame(index=behavioral_multiples, columns=acute_multiples)

    for beh_mult in behavioral_multiples:
        for acute_mult in acute_multiples:
            beh_opco = proforma_data['behavioral']['proforma_opco_ebitda'] * beh_mult
            beh_propco = proforma_data['behavioral']['imputed_rent'] / 0.065  # Base cap rate
            acute_opco = proforma_data['acute']['proforma_opco_ebitda'] * acute_mult
            acute_propco = proforma_data['acute']['imputed_rent'] / 0.065

            ev = beh_opco + beh_propco + acute_opco + acute_propco
            equity = ev - 4378.5
            per_share = equity / 64.98

            sensitivity_2.loc[beh_mult, acute_mult] = round(per_share, 2)

    return {
        'behavioral_mult_vs_cap_rate': sensitivity_1,
        'behavioral_mult_vs_acute_mult': sensitivity_2
    }

# ============================================================================
# STEP 5: ACQUISITION PREMIUM ANALYSIS
# ============================================================================

def calculate_acquisition_premium(base_value_per_share):
    """
    Calculate acquisition prices at various premiums

    Typical healthcare acquisition premiums: 30-60%
    For family-controlled companies: Often require 50-80% premiums
    """

    current_price = 208.39

    premiums = [0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80]

    results = []

    for premium_pct in premiums:
        # Premium to current market price
        offer_price = current_price * (1 + premium_pct)

        # Premium to intrinsic value
        premium_to_fair = ((offer_price - base_value_per_share) / base_value_per_share) * 100

        # Total equity value at offer price
        total_equity_value = offer_price * 64.98  # Million

        # Miller family proceeds (11% economic ownership)
        miller_family_proceeds = total_equity_value * 0.108

        results.append({
            'premium_pct': premium_pct * 100,
            'offer_price_per_share': round(offer_price, 2),
            'premium_to_fair_value_pct': round(premium_to_fair, 1),
            'total_equity_value_m': round(total_equity_value, 0),
            'miller_family_proceeds_m': round(miller_family_proceeds, 0),
            'enterprise_value_m': round(total_equity_value + 4378.5, 0)
        })

    return pd.DataFrame(results)

# ============================================================================
# STEP 6: GENERATE COMPREHENSIVE REPORTS
# ============================================================================

def generate_valuation_report():
    """Generate complete SOTP valuation with all scenarios"""

    print("=" * 80)
    print("UHS SOTP VALUATION MODEL v2.0")
    print("Four-Part Sum-of-the-Parts Analysis")
    print("=" * 80)
    print()

    # Load data
    data = load_10k_data()

    # Calculate pro-forma EBITDAs
    print("STEP 1: CALCULATING PRO-FORMA OPCO EBITDAS")
    print("-" * 80)
    proforma = calculate_proforma_ebitdas(data)

    print(f"Behavioral Health:")
    print(f"  Reported EBITDA:        ${proforma['behavioral']['reported_ebitda']:,.0f}M")
    print(f"  Real Estate Allocation: ${proforma['behavioral']['real_estate_value']:,.0f}M")
    print(f"  Imputed Rent (6.5%):    ${proforma['behavioral']['imputed_rent']:,.0f}M")
    print(f"  Pro-Forma OpCo EBITDA:  ${proforma['behavioral']['proforma_opco_ebitda']:,.0f}M")
    print()
    print(f"Acute Care:")
    print(f"  Reported EBITDA:        ${proforma['acute']['reported_ebitda']:,.0f}M")
    print(f"  Real Estate Allocation: ${proforma['acute']['real_estate_value']:,.0f}M")
    print(f"  Imputed Rent (6.5%):    ${proforma['acute']['imputed_rent']:,.0f}M")
    print(f"  Pro-Forma OpCo EBITDA:  ${proforma['acute']['proforma_opco_ebitda']:,.0f}M")
    print()

    # Calculate all three scenarios
    print("STEP 2: SOTP VALUATION - THREE SCENARIOS")
    print("-" * 80)

    scenarios = {}
    for scenario in ['bear', 'base', 'bull']:
        scenarios[scenario] = calculate_sotp_valuation(proforma, scenario)

    # Display summary table
    summary_data = []
    for scenario in ['bear', 'base', 'bull']:
        s = scenarios[scenario]
        summary_data.append({
            'Scenario': scenario.upper(),
            'Behavioral OpCo ($M)': f"${s['behavioral_opco_value']:,.0f}",
            'Behavioral PropCo ($M)': f"${s['behavioral_propco_value']:,.0f}",
            'Acute OpCo ($M)': f"${s['acute_opco_value']:,.0f}",
            'Acute PropCo ($M)': f"${s['acute_propco_value']:,.0f}",
            'Enterprise Value ($M)': f"${s['total_enterprise_value']:,.0f}",
            'Equity Value ($M)': f"${s['equity_value']:,.0f}",
            'Value Per Share': f"${s['value_per_share']:.2f}",
            'Upside %': f"{s['upside_pct']:+.1f}%"
        })

    summary_df = pd.DataFrame(summary_data)
    print(summary_df.to_string(index=False))
    print()

    # Current market comparison
    print("CURRENT MARKET VALUATION:")
    print(f"  Stock Price:           $208.39")
    print(f"  Market Cap:            $13,544M")
    print(f"  Enterprise Value:      $17,923M")
    print(f"  Implied EV/EBITDA:     6.4x")
    print()

    # Base case details
    base = scenarios['base']
    print("BASE CASE BREAKDOWN:")
    print(f"  Behavioral OpCo:       ${base['behavioral_opco_value']:,.0f}M  ({base['behavioral_opco_value']/base['total_enterprise_value']*100:.1f}% of EV)")
    print(f"  Behavioral PropCo:     ${base['behavioral_propco_value']:,.0f}M  ({base['behavioral_propco_value']/base['total_enterprise_value']*100:.1f}% of EV)")
    print(f"  Acute Care OpCo:       ${base['acute_opco_value']:,.0f}M  ({base['acute_opco_value']/base['total_enterprise_value']*100:.1f}% of EV)")
    print(f"  Acute Care PropCo:     ${base['acute_propco_value']:,.0f}M  ({base['acute_propco_value']/base['total_enterprise_value']*100:.1f}% of EV)")
    print(f"  " + "-" * 60)
    print(f"  Total Enterprise:      ${base['total_enterprise_value']:,.0f}M")
    print(f"  Less: Net Debt:        ${base['net_debt']:,.0f}M")
    print(f"  Equity Value:          ${base['equity_value']:,.0f}M")
    print(f"  Shares Outstanding:    {base['shares_outstanding']:.2f}M")
    print(f"  Value Per Share:       ${base['value_per_share']:.2f}")
    print(f"  Upside:                {base['upside_pct']:+.1f}%")
    print()

    # Acquisition premium analysis
    print("STEP 3: ACQUISITION PREMIUM ANALYSIS")
    print("-" * 80)
    acquisition_df = calculate_acquisition_premium(base['value_per_share'])
    print(acquisition_df.to_string(index=False))
    print()
    print("Note: Miller family controls 90.5% voting power with 10.8% economic stake")
    print("      Acquisition requires family approval - likely 60-80% premium needed")
    print()

    # Sensitivity analysis
    print("STEP 4: GENERATING SENSITIVITY TABLES...")
    print("-" * 80)
    sensitivity = create_sensitivity_table(proforma)

    # Save all outputs
    print("STEP 5: SAVING OUTPUTS...")
    print("-" * 80)

    # Save scenario comparison
    summary_df.to_csv('data/graphs/sotp_valuation_scenarios.csv', index=False)
    print("✓ Saved: data/graphs/sotp_valuation_scenarios.csv")

    # Save acquisition premium analysis
    acquisition_df.to_csv('data/graphs/acquisition_premium_analysis.csv', index=False)
    print("✓ Saved: data/graphs/acquisition_premium_analysis.csv")

    # Save sensitivity tables
    sensitivity['behavioral_mult_vs_cap_rate'].to_csv('data/graphs/sensitivity_behavioral_vs_caprate.csv')
    print("✓ Saved: data/graphs/sensitivity_behavioral_vs_caprate.csv")

    sensitivity['behavioral_mult_vs_acute_mult'].to_csv('data/graphs/sensitivity_behavioral_vs_acute.csv')
    print("✓ Saved: data/graphs/sensitivity_behavioral_vs_acute.csv")

    # Save detailed breakdown
    detailed_data = []
    for scenario in ['bear', 'base', 'bull']:
        s = scenarios[scenario]
        detailed_data.append({
            'Scenario': scenario.upper(),
            'Behavioral_OpCo_EBITDA': s['behavioral_opco_ebitda'],
            'Behavioral_OpCo_Multiple': s['multiples']['behavioral_opco_multiple'],
            'Behavioral_OpCo_Value': s['behavioral_opco_value'],
            'Behavioral_PropCo_NOI': s['behavioral_propco_noi'],
            'Behavioral_Cap_Rate': s['multiples']['cap_rate'],
            'Behavioral_PropCo_Value': s['behavioral_propco_value'],
            'Acute_OpCo_EBITDA': s['acute_opco_ebitda'],
            'Acute_OpCo_Multiple': s['multiples']['acute_opco_multiple'],
            'Acute_OpCo_Value': s['acute_opco_value'],
            'Acute_PropCo_NOI': s['acute_propco_noi'],
            'Acute_Cap_Rate': s['multiples']['cap_rate'],
            'Acute_PropCo_Value': s['acute_propco_value'],
            'Enterprise_Value': s['total_enterprise_value'],
            'Net_Debt': s['net_debt'],
            'Equity_Value': s['equity_value'],
            'Shares_Outstanding': s['shares_outstanding'],
            'Value_Per_Share': s['value_per_share'],
            'Current_Price': s['current_price'],
            'Upside_Pct': s['upside_pct']
        })

    detailed_df = pd.DataFrame(detailed_data)
    detailed_df.to_csv('data/graphs/sotp_valuation_detailed.csv', index=False)
    print("✓ Saved: data/graphs/sotp_valuation_detailed.csv")

    print()
    print("=" * 80)
    print("VALUATION COMPLETE!")
    print("=" * 80)

    return {
        'scenarios': scenarios,
        'proforma': proforma,
        'sensitivity': sensitivity,
        'acquisition': acquisition_df
    }

# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    results = generate_valuation_report()
