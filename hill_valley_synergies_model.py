"""
HILL VALLEY ACQUISITION OF UHS - SYNERGIES MODEL

Purpose: Model cost and revenue synergies from integrating UHS into Hill Valley

Components:
1. Corporate overhead elimination
2. Procurement synergies
3. IT/systems consolidation
4. Facility rationalization
5. Revenue synergies
6. Pro-forma financials with synergies
7. Updated valuation with synergy value

Author: Hill Valley Investment Team
Date: October 29, 2025
"""

import pandas as pd
import numpy as np
import json
from datetime import datetime

# ============================================================================
# STEP 1: LOAD UHS BASELINE DATA
# ============================================================================

def load_uhs_data():
    """Load UHS financial data from 10-K"""
    with open('data/UHS_10K_2024_comprehensive_data.json', 'r') as f:
        data = json.load(f)

    # Key metrics (in millions)
    metrics = {
        'revenue': 15_827.9,
        'total_ebitda': 2_775.6,
        'behavioral_revenue': 6_895.1,
        'behavioral_ebitda': 1_567.2,
        'acute_revenue': 8_922.3,
        'acute_ebitda': 1_208.5,
        'operating_income': 1_681.8,
        'net_income': 1_142.1,
        'total_opex': 14_146.1,
        'sg_and_a': 7_518.7 + 4_308.4,  # Salaries + other opex
        'depreciation': 584.8,
        'interest_expense': 186.1,
        'facilities_count': 352,
        'employees': None,  # Will estimate
    }

    return metrics

# ============================================================================
# STEP 2: MODEL COST SYNERGIES
# ============================================================================

def calculate_cost_synergies(baseline):
    """
    Calculate cost synergies from Hill Valley integration

    Categories:
    1. Corporate overhead elimination
    2. Procurement synergies
    3. IT & systems consolidation
    4. Facility rationalization
    5. Other operating efficiencies
    """

    total_revenue = baseline['revenue']
    total_opex = baseline['sg_and_a']

    synergies = {}

    # ========================================================================
    # 1. CORPORATE OVERHEAD ELIMINATION
    # ========================================================================

    """
    UHS Corporate Functions to Eliminate:
    - C-Suite (CEO, CFO, COO, General Counsel)
    - Corporate Finance (FP&A, Treasury, Tax, Accounting)
    - Corporate HR & Benefits Administration
    - Corporate Legal
    - Corporate IT (Infrastructure, Security, ERP)
    - Corporate Development & Strategy
    - Investor Relations
    - Corporate Real Estate Management

    Estimated Corporate Headcount: ~500-700 employees
    Average Loaded Cost: $150K-200K per employee
    Total Corporate Overhead: $75-140M

    Post-Acquisition:
    - Eliminate entire corporate function (consolidate into Hill Valley)
    - Keep divisional presidents and regional operators
    - Savings: 80-90% of corporate overhead
    """

    # Conservative estimate: UHS corporate overhead = 1.0% of revenue
    estimated_corporate_overhead = total_revenue * 0.010  # $158M

    # Eliminate 85% (keep minimal transition team for 12 months)
    corporate_synergy_pct = 0.85

    synergies['corporate_overhead'] = {
        'description': 'Eliminate UHS corporate functions (C-suite, finance, legal, HR, IT)',
        'baseline_cost': estimated_corporate_overhead,
        'synergy_pct': corporate_synergy_pct,
        'annual_savings': estimated_corporate_overhead * corporate_synergy_pct,
        'implementation_cost': 50,  # Severance, retention bonuses
        'time_to_realize_months': 12,
        'year_1_run_rate': 0.65,  # 65% realized in Year 1
        'year_2_run_rate': 1.00,  # 100% by Year 2
    }

    # ========================================================================
    # 2. PROCUREMENT SYNERGIES
    # ========================================================================

    """
    Categories:
    a) Medical Supplies & Pharmaceuticals
    b) Food Services
    c) Linen & Housekeeping
    d) Professional Services (IT, legal, consulting)
    e) Insurance (medical malpractice, D&O, property)

    UHS Purchasing Power: $15.8B revenue
    Hill Valley + UHS: ~$30-40B combined (assuming Hill Valley similar size)

    Healthcare GPO benchmarks: 10-15% cost reduction on supplies
    UHS already in GPO, but Hill Valley may have better rates
    Conservative: 5% reduction on supplies spend
    """

    # Supplies expense from 10-K: $1,588M
    supplies_expense = 1_588

    # Procurement synergy: 5% on supplies
    procurement_synergy_pct = 0.05

    # Also apply to other operating expenses (food, services)
    # Other opex: $4,308M, but only ~30% is procurable
    other_procurable = 4_308 * 0.30

    total_procurable = supplies_expense + other_procurable

    synergies['procurement'] = {
        'description': 'Medical supplies, pharmaceuticals, food, services at Hill Valley rates',
        'baseline_cost': total_procurable,
        'synergy_pct': procurement_synergy_pct,
        'annual_savings': total_procurable * procurement_synergy_pct,
        'implementation_cost': 10,  # Contract renegotiation, systems integration
        'time_to_realize_months': 18,
        'year_1_run_rate': 0.40,
        'year_2_run_rate': 0.80,
        'year_3_run_rate': 1.00,
    }

    # ========================================================================
    # 3. IT & SYSTEMS CONSOLIDATION
    # ========================================================================

    """
    UHS IT Spend (estimated):
    - EHR Licenses (Epic, Cerner, etc): $50-75M/year
    - Data Centers & Cloud: $30-40M/year
    - Cybersecurity: $20-30M/year
    - Help Desk & Support: $25-35M/year
    - Software Licenses (Office, etc): $15-20M/year
    Total: ~$140-200M/year = 0.9-1.3% of revenue

    Post-Acquisition:
    - Consolidate EHR platforms (eliminate redundant licenses)
    - Migrate to Hill Valley data centers
    - Consolidate help desk & support
    - Volume discounts on software licenses

    Savings: 30-40% of IT spend
    """

    # Estimate IT spend at 1.0% of revenue
    it_spend = total_revenue * 0.010  # $158M

    # Synergy: 35% reduction
    it_synergy_pct = 0.35

    synergies['it_systems'] = {
        'description': 'Consolidate EHR, data centers, help desk, software licenses',
        'baseline_cost': it_spend,
        'synergy_pct': it_synergy_pct,
        'annual_savings': it_spend * it_synergy_pct,
        'implementation_cost': 75,  # Migration costs, new hardware
        'time_to_realize_months': 24,
        'year_1_run_rate': 0.20,
        'year_2_run_rate': 0.60,
        'year_3_run_rate': 1.00,
    }

    # ========================================================================
    # 4. FACILITY RATIONALIZATION
    # ========================================================================

    """
    Strategy: Close underperforming acute care hospitals

    UHS Acute Care: 28 hospitals, $8.9B revenue, 13.5% EBITDA margin
    Industry: 15-16% EBITDA margin target

    Identify bottom quartile (7 hospitals) with <10% margins
    Estimated: $1.5B revenue, $50M EBITDA, $100M in losses/stranded costs

    Options:
    a) Close and sell real estate ($300-400M proceeds)
    b) Convert to behavioral facilities (better use of RE)
    c) Divest to regional operator

    Conservative: Close 3-5 hospitals, save $40M in annual losses
    """

    synergies['facility_rationalization'] = {
        'description': 'Close/divest 3-5 underperforming acute care hospitals',
        'baseline_cost': 40,  # Annual losses eliminated
        'synergy_pct': 1.00,
        'annual_savings': 40,
        'implementation_cost': 20,  # Closure costs, employee severance
        'time_to_realize_months': 18,
        'year_1_run_rate': 0.00,  # No savings in Year 1 (takes time to close)
        'year_2_run_rate': 0.75,
        'year_3_run_rate': 1.00,
        'one_time_gain': 350,  # Sale of real estate
    }

    # ========================================================================
    # 5. OTHER OPERATING EFFICIENCIES
    # ========================================================================

    """
    Additional opportunities:
    - Revenue cycle management (faster collections)
    - Labor scheduling optimization (reduce overtime, agency staff)
    - Shared services (centralized billing, coding)
    - Marketing & advertising consolidation

    Industry benchmarks: 1-2% of operating expenses
    Conservative: 0.5% of opex
    """

    other_synergy_pct = 0.005

    synergies['other_efficiencies'] = {
        'description': 'Labor optimization, RCM improvements, shared services',
        'baseline_cost': total_opex,
        'synergy_pct': other_synergy_pct,
        'annual_savings': total_opex * other_synergy_pct,
        'implementation_cost': 30,
        'time_to_realize_months': 24,
        'year_1_run_rate': 0.30,
        'year_2_run_rate': 0.70,
        'year_3_run_rate': 1.00,
    }

    # ========================================================================
    # TOTAL COST SYNERGIES
    # ========================================================================

    total_annual_savings = sum(s['annual_savings'] for s in synergies.values())
    total_implementation_cost = sum(s['implementation_cost'] for s in synergies.values())

    synergies['total'] = {
        'total_annual_savings': total_annual_savings,
        'total_implementation_cost': total_implementation_cost,
        'year_1_savings': sum(s['annual_savings'] * s['year_1_run_rate'] for s in synergies.values() if 'year_1_run_rate' in s),
        'year_2_savings': sum(s['annual_savings'] * s['year_2_run_rate'] for s in synergies.values() if 'year_2_run_rate' in s),
        'year_3_savings': sum(s['annual_savings'] * s.get('year_3_run_rate', 1.0) for s in synergies.values() if 'year_1_run_rate' in s),
    }

    return synergies

# ============================================================================
# STEP 3: MODEL REVENUE SYNERGIES (UPSIDE)
# ============================================================================

def calculate_revenue_synergies(baseline):
    """
    Revenue synergies are UPSIDE (not included in base case)

    Categories:
    1. Cross-referrals between Hill Valley and UHS
    2. Payor contract optimization
    3. De novo expansion in underserved markets
    4. Telehealth and virtual care expansion
    """

    total_revenue = baseline['revenue']

    revenue_synergies = {
        'cross_referrals': {
            'description': 'Patient referrals between Hill Valley and UHS networks',
            'incremental_revenue': 75,  # $75M over 3 years
            'ebitda_margin': 0.20,
            'incremental_ebitda': 15,
        },
        'payor_contracts': {
            'description': 'Improved rates from combined negotiating leverage',
            'rate_improvement_pct': 0.01,  # 1% rate increase
            'incremental_revenue': total_revenue * 0.01,
            'ebitda_margin': 0.20,
            'incremental_ebitda': total_revenue * 0.01 * 0.20,
        },
        'de_novo_expansion': {
            'description': 'New behavioral facilities in Hill Valley markets',
            'new_facilities': 10,
            'revenue_per_facility': 20,  # $20M each
            'incremental_revenue': 200,
            'ebitda_margin': 0.22,
            'incremental_ebitda': 44,
        },
    }

    total_revenue_synergy = sum(s['incremental_ebitda'] for s in revenue_synergies.values())

    return revenue_synergies, total_revenue_synergy

# ============================================================================
# STEP 4: PRO-FORMA FINANCIALS WITH SYNERGIES
# ============================================================================

def build_proforma_financials(baseline, cost_synergies, revenue_synergies_total):
    """Build 3-year pro-forma P&L with synergies"""

    years = ['Year 0 (Current)', 'Year 1', 'Year 2', 'Year 3']

    # Revenue (assume 3% organic growth)
    revenue_growth = 0.03
    revenue = [baseline['revenue']]
    for i in range(3):
        revenue.append(revenue[-1] * (1 + revenue_growth))

    # EBITDA (baseline + synergies)
    baseline_ebitda = [baseline['total_ebitda']]
    for i in range(3):
        baseline_ebitda.append(baseline_ebitda[-1] * (1 + revenue_growth))

    # Cost synergies by year
    cost_synergy_impact = [
        0,
        cost_synergies['total']['year_1_savings'],
        cost_synergies['total']['year_2_savings'],
        cost_synergies['total']['year_3_savings'],
    ]

    # Pro-forma EBITDA
    proforma_ebitda = [baseline_ebitda[i] + cost_synergy_impact[i] for i in range(4)]

    # EBITDA margins
    ebitda_margin = [proforma_ebitda[i] / revenue[i] for i in range(4)]

    # Build DataFrame
    proforma = pd.DataFrame({
        'Revenue': revenue,
        'Baseline EBITDA': baseline_ebitda,
        'Cost Synergies': cost_synergy_impact,
        'Pro-Forma EBITDA': proforma_ebitda,
        'EBITDA Margin %': [m * 100 for m in ebitda_margin],
    }, index=years)

    return proforma

# ============================================================================
# STEP 5: SYNERGY VALUE CREATION
# ============================================================================

def calculate_synergy_value(cost_synergies, multiple=10.0):
    """
    Value created from synergies

    Synergy Value = Annual Run-Rate Savings × EBITDA Multiple

    Multiple: 10x (conservative for healthcare services)
    """

    annual_run_rate = cost_synergies['total']['total_annual_savings']

    synergy_value = annual_run_rate * multiple
    synergy_value_per_share = synergy_value / 64.98  # 65M shares

    return {
        'annual_run_rate_savings': annual_run_rate,
        'multiple': multiple,
        'total_synergy_value': synergy_value,
        'synergy_value_per_share': synergy_value_per_share,
    }

# ============================================================================
# STEP 6: GENERATE REPORTS
# ============================================================================

def generate_synergies_report():
    """Generate comprehensive synergies analysis"""

    print("=" * 80)
    print("HILL VALLEY ACQUISITION OF UHS - SYNERGIES ANALYSIS")
    print("=" * 80)
    print()

    # Load baseline
    baseline = load_uhs_data()

    # Calculate synergies
    print("STEP 1: COST SYNERGIES ANALYSIS")
    print("-" * 80)
    cost_synergies = calculate_cost_synergies(baseline)

    # Build summary table
    synergy_data = []
    for key, synergy in cost_synergies.items():
        if key == 'total':
            continue
        synergy_data.append({
            'Category': synergy['description'],
            'Baseline Cost ($M)': f"${synergy['baseline_cost']:.0f}",
            'Synergy %': f"{synergy['synergy_pct']*100:.0f}%",
            'Annual Savings ($M)': f"${synergy['annual_savings']:.0f}",
            'Implementation ($M)': f"${synergy['implementation_cost']:.0f}",
            'Time to Realize': f"{synergy['time_to_realize_months']} months",
        })

    synergy_df = pd.DataFrame(synergy_data)
    print(synergy_df.to_string(index=False))
    print()

    # Total synergies
    total = cost_synergies['total']
    print("TOTAL COST SYNERGIES:")
    print(f"  Annual Run-Rate Savings:  ${total['total_annual_savings']:.0f}M")
    print(f"  Implementation Cost:      ${total['total_implementation_cost']:.0f}M")
    print(f"  Year 1 Savings:           ${total['year_1_savings']:.0f}M")
    print(f"  Year 2 Savings:           ${total['year_2_savings']:.0f}M")
    print(f"  Year 3 Savings (Full):    ${total['year_3_savings']:.0f}M")
    print(f"  Payback Period:           {total['total_implementation_cost'] / total['total_annual_savings']:.1f} years")
    print()

    # Revenue synergies (upside)
    print("STEP 2: REVENUE SYNERGIES (UPSIDE)")
    print("-" * 80)
    revenue_synergies, revenue_total = calculate_revenue_synergies(baseline)

    for key, synergy in revenue_synergies.items():
        print(f"{synergy['description']}:")
        print(f"  Incremental Revenue: ${synergy['incremental_revenue']:.0f}M")
        print(f"  Incremental EBITDA:  ${synergy['incremental_ebitda']:.0f}M")
        print()

    print(f"TOTAL REVENUE SYNERGIES (EBITDA): ${revenue_total:.0f}M")
    print()

    # Pro-forma financials
    print("STEP 3: PRO-FORMA FINANCIALS WITH SYNERGIES")
    print("-" * 80)
    proforma = build_proforma_financials(baseline, cost_synergies, revenue_total)
    print(proforma.to_string())
    print()

    # Synergy value creation
    print("STEP 4: SYNERGY VALUE CREATION")
    print("-" * 80)
    synergy_value = calculate_synergy_value(cost_synergies, multiple=10.0)
    print(f"Annual Run-Rate Savings:       ${synergy_value['annual_run_rate_savings']:.0f}M")
    print(f"Applied Multiple:              {synergy_value['multiple']:.1f}x")
    print(f"Total Synergy Value:           ${synergy_value['total_synergy_value']:,.0f}M")
    print(f"Synergy Value Per Share:       ${synergy_value['synergy_value_per_share']:.2f}")
    print()

    # Combined valuation
    print("STEP 5: COMBINED VALUATION (BASE + SYNERGIES)")
    print("-" * 80)
    base_fair_value = 448.89  # From SOTP model
    synergy_value_ps = synergy_value['synergy_value_per_share']
    combined_value = base_fair_value + synergy_value_ps

    print(f"Base Fair Value (SOTP):        ${base_fair_value:.2f}")
    print(f"+ Synergy Value:               ${synergy_value_ps:.2f}")
    print(f"= Combined Fair Value:         ${combined_value:.2f}")
    print()
    print(f"Current Market Price:          $208.39")
    print(f"Upside to Combined Value:      {((combined_value - 208.39) / 208.39 * 100):.1f}%")
    print()

    # Save outputs
    print("STEP 6: SAVING OUTPUTS...")
    print("-" * 80)

    synergy_df.to_csv('data/graphs/hill_valley_cost_synergies.csv', index=False)
    print("✓ Saved: data/graphs/hill_valley_cost_synergies.csv")

    proforma.to_csv('data/graphs/hill_valley_proforma_financials.csv')
    print("✓ Saved: data/graphs/hill_valley_proforma_financials.csv")

    # Save summary
    summary = {
        'cost_synergies_annual': total['total_annual_savings'],
        'revenue_synergies_annual': revenue_total,
        'total_synergies_annual': total['total_annual_savings'] + revenue_total,
        'implementation_cost': total['total_implementation_cost'],
        'synergy_value_at_10x': synergy_value['total_synergy_value'],
        'synergy_value_per_share': synergy_value['synergy_value_per_share'],
        'base_fair_value': base_fair_value,
        'combined_fair_value': combined_value,
        'upside_pct': ((combined_value - 208.39) / 208.39 * 100),
    }

    summary_df = pd.DataFrame([summary])
    summary_df.to_csv('data/graphs/hill_valley_synergies_summary.csv', index=False)
    print("✓ Saved: data/graphs/hill_valley_synergies_summary.csv")

    print()
    print("=" * 80)
    print("SYNERGIES ANALYSIS COMPLETE!")
    print("=" * 80)

    return {
        'cost_synergies': cost_synergies,
        'revenue_synergies': revenue_synergies,
        'proforma': proforma,
        'synergy_value': synergy_value,
        'combined_value': combined_value,
    }

# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    results = generate_synergies_report()
