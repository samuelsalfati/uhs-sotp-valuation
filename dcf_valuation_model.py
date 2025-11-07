"""
UHS DCF VALUATION MODEL
10-Year Discounted Cash Flow Analysis

Purpose: Value UHS using intrinsic cash flow methodology
Author: Ascendra Capital Investment Team
Date: October 29, 2025
"""

import pandas as pd
import numpy as np
import json

# ============================================================================
# STEP 1: LOAD BASE FINANCIAL DATA
# ============================================================================

def load_financial_data():
    """Load UHS financial data from comprehensive JSON"""
    with open('data/UHS_10K_2024_comprehensive_data.json', 'r') as f:
        data = json.load(f)

    # Extract key metrics (in millions)
    financials = {
        # Income Statement (2024 actuals)
        'revenue': 15_827.9,
        'ebitda': 2_775.6,
        'depreciation': 584.8,
        'ebit': 1_681.8,
        'interest_expense': 186.1,
        'tax_expense': 353.7,
        'net_income': 1_142.1,

        # Cash Flow Statement (2024 actuals)
        'operating_cash_flow': 2_067,
        'capex': 640,
        'free_cash_flow': 1_427,

        # Balance Sheet
        'total_debt': 4_504.5,
        'cash': 126.0,
        'net_debt': 4_378.5,
        'total_equity': 6_666.2,

        # Segments
        'behavioral_revenue': 6_895.1,
        'behavioral_ebitda': 1_567.2,
        'behavioral_margin': 0.227,
        'acute_revenue': 8_922.3,
        'acute_ebitda': 1_208.5,
        'acute_margin': 0.135,

        # Share data (UPDATED Oct 31, 2025)
        'shares_outstanding': 63.64,  # StockAnalysis.com (Oct 2025)
        'current_price': 225.30,      # Yahoo Finance (Oct 29, 2025)
    }

    return financials

# ============================================================================
# STEP 2: BUILD 10-YEAR DCF PROJECTION
# ============================================================================

def build_dcf_projections(financials, assumptions):
    """
    Build 10-year DCF projection model

    Key assumptions:
    - Revenue growth rates by segment
    - EBITDA margin expansion
    - Tax rate
    - CapEx as % of revenue
    - Working capital changes
    - Terminal growth rate
    - WACC (discount rate)
    """

    # Historical base year (2024)
    base_year = {
        'year': 0,
        'revenue': financials['revenue'],
        'ebitda': financials['ebitda'],
        'ebitda_margin': financials['ebitda'] / financials['revenue'],
        'depreciation': financials['depreciation'],
        'ebit': financials['ebit'],
        'tax_rate': financials['tax_expense'] / financials['ebit'],
        'nopat': financials['ebit'] * (1 - financials['tax_expense'] / financials['ebit']),
        'capex': financials['capex'],
        'capex_pct': financials['capex'] / financials['revenue'],
        'nwc_change': 0,  # Simplification
        'fcf': financials['free_cash_flow'],
    }

    # Projection assumptions
    revenue_growth = assumptions['revenue_growth']
    ebitda_margin_target = assumptions['ebitda_margin_target']
    tax_rate = assumptions['tax_rate']
    capex_pct = assumptions['capex_pct']
    depreciation_pct = assumptions['depreciation_pct']
    nwc_change_pct = assumptions['nwc_change_pct']

    # Build 10-year projections
    projections = [base_year]

    for year in range(1, 11):
        prev = projections[year - 1]

        # Revenue growth (declining from 5% to 3% terminal)
        if year <= 3:
            growth = revenue_growth['years_1_3']
        elif year <= 5:
            growth = revenue_growth['years_4_5']
        elif year <= 10:
            growth = revenue_growth['years_6_10']

        revenue = prev['revenue'] * (1 + growth)

        # EBITDA margin expansion (gradual improvement to target)
        margin_improvement = (ebitda_margin_target - base_year['ebitda_margin']) / 10
        ebitda_margin = prev['ebitda_margin'] + margin_improvement
        ebitda = revenue * ebitda_margin

        # Depreciation
        depreciation = revenue * depreciation_pct

        # EBIT
        ebit = ebitda - depreciation

        # Taxes (on EBIT)
        taxes = ebit * tax_rate
        nopat = ebit - taxes

        # CapEx
        capex = revenue * capex_pct

        # Working capital change
        nwc_change = (revenue - prev['revenue']) * nwc_change_pct

        # Free Cash Flow
        fcf = nopat + depreciation - capex - nwc_change

        projections.append({
            'year': year,
            'revenue': revenue,
            'ebitda': ebitda,
            'ebitda_margin': ebitda_margin,
            'depreciation': depreciation,
            'ebit': ebit,
            'tax_rate': tax_rate,
            'taxes': taxes,
            'nopat': nopat,
            'capex': capex,
            'capex_pct': capex_pct,
            'nwc_change': nwc_change,
            'fcf': fcf,
        })

    return projections

# ============================================================================
# STEP 3: CALCULATE TERMINAL VALUE
# ============================================================================

def calculate_terminal_value(projections, assumptions):
    """
    Calculate terminal value using perpetuity growth method

    Terminal Value = FCF(Year 10) × (1 + g) / (WACC - g)
    where g = terminal growth rate (typically 2-3%)
    """

    year_10 = projections[-1]
    terminal_fcf = year_10['fcf'] * (1 + assumptions['terminal_growth_rate'])

    terminal_value = terminal_fcf / (assumptions['wacc'] - assumptions['terminal_growth_rate'])

    return terminal_value

# ============================================================================
# STEP 4: DISCOUNT CASH FLOWS TO PRESENT VALUE
# ============================================================================

def discount_cash_flows(projections, terminal_value, wacc):
    """
    Discount all future cash flows to present value

    PV = FCF / (1 + WACC)^year
    """

    pv_fcf_list = []

    for proj in projections[1:]:  # Skip year 0
        year = proj['year']
        fcf = proj['fcf']
        discount_factor = (1 + wacc) ** year
        pv_fcf = fcf / discount_factor

        pv_fcf_list.append({
            'year': year,
            'fcf': fcf,
            'discount_factor': discount_factor,
            'pv_fcf': pv_fcf,
        })

    # Discount terminal value
    terminal_discount_factor = (1 + wacc) ** 10
    pv_terminal_value = terminal_value / terminal_discount_factor

    # Sum of PV of FCFs
    total_pv_fcf = sum(item['pv_fcf'] for item in pv_fcf_list)

    return pv_fcf_list, pv_terminal_value, total_pv_fcf

# ============================================================================
# STEP 5: CALCULATE EQUITY VALUE
# ============================================================================

def calculate_equity_value(total_pv_fcf, pv_terminal_value, net_debt, shares_outstanding):
    """
    Enterprise Value = PV(FCFs) + PV(Terminal Value)
    Equity Value = Enterprise Value - Net Debt
    Value per Share = Equity Value / Shares Outstanding
    """

    enterprise_value = total_pv_fcf + pv_terminal_value
    equity_value = enterprise_value - net_debt
    value_per_share = equity_value / shares_outstanding

    return {
        'enterprise_value': enterprise_value,
        'equity_value': equity_value,
        'value_per_share': value_per_share,
    }

# ============================================================================
# STEP 6: SENSITIVITY ANALYSIS
# ============================================================================

def dcf_sensitivity_analysis(financials, base_assumptions):
    """
    Run DCF sensitivity on two key variables:
    1. WACC (discount rate)
    2. Terminal growth rate
    """

    wacc_range = np.arange(0.07, 0.12, 0.005)  # 7% to 12% in 0.5% steps
    terminal_growth_range = np.arange(0.015, 0.035, 0.0025)  # 1.5% to 3.5%

    sensitivity_results = pd.DataFrame(
        index=[f"{w:.1%}" for w in wacc_range],
        columns=[f"{g:.1%}" for g in terminal_growth_range]
    )

    for wacc in wacc_range:
        for term_growth in terminal_growth_range:
            # Update assumptions
            assumptions = base_assumptions.copy()
            assumptions['wacc'] = wacc
            assumptions['terminal_growth_rate'] = term_growth

            # Run DCF
            projections = build_dcf_projections(financials, assumptions)
            terminal_value = calculate_terminal_value(projections, assumptions)
            pv_fcf_list, pv_terminal, total_pv = discount_cash_flows(projections, terminal_value, wacc)
            valuation = calculate_equity_value(total_pv, pv_terminal, financials['net_debt'], financials['shares_outstanding'])

            # Store result
            sensitivity_results.loc[f"{wacc:.1%}", f"{term_growth:.1%}"] = valuation['value_per_share']

    return sensitivity_results.astype(float)

# ============================================================================
# STEP 7: GENERATE DCF REPORT
# ============================================================================

def generate_dcf_report():
    """Generate complete DCF valuation report"""

    print("=" * 80)
    print("UHS DCF VALUATION MODEL")
    print("10-Year Discounted Cash Flow Analysis")
    print("=" * 80)
    print()

    # Load data
    financials = load_financial_data()

    # Define assumptions
    print("STEP 1: KEY ASSUMPTIONS")
    print("-" * 80)

    assumptions = {
        'revenue_growth': {
            'years_1_3': 0.05,   # 5% growth (near-term)
            'years_4_5': 0.04,   # 4% growth (mid-term)
            'years_6_10': 0.03,  # 3% growth (long-term, GDP+)
        },
        'ebitda_margin_target': 0.19,  # Target 19% (from 17.5% today, modest expansion)
        'tax_rate': 0.21,  # 21% federal corporate tax
        'capex_pct': 0.04,  # 4% of revenue (maintenance CapEx)
        'depreciation_pct': 0.037,  # 3.7% of revenue (historical)
        'nwc_change_pct': 0.01,  # 1% of revenue growth (working capital increase)
        'terminal_growth_rate': 0.025,  # 2.5% perpetual growth (GDP)
        'wacc': 0.085,  # 8.5% WACC (base case, see DCF_ASSUMPTIONS_SOURCED.md)
        # WACC Calculation: Rf 4.10% + Beta 1.30 × ERP 4.65% = 10.15% Cost of Equity
        # Market weights: 76.6% equity, 23.4% debt (at $225.30/share)
        # WACC = 76.6% × 10.15% + 23.4% × 3.26% = 8.53% ≈ 8.5%
    }

    print(f"Revenue Growth:")
    print(f"  Years 1-3:  {assumptions['revenue_growth']['years_1_3']:.1%}")
    print(f"  Years 4-5:  {assumptions['revenue_growth']['years_4_5']:.1%}")
    print(f"  Years 6-10: {assumptions['revenue_growth']['years_6_10']:.1%}")
    print(f"\nTarget EBITDA Margin: {assumptions['ebitda_margin_target']:.1%}")
    print(f"Tax Rate: {assumptions['tax_rate']:.1%}")
    print(f"CapEx % of Revenue: {assumptions['capex_pct']:.1%}")
    print(f"Terminal Growth Rate: {assumptions['terminal_growth_rate']:.1%}")
    print(f"WACC (Discount Rate): {assumptions['wacc']:.1%}")
    print()

    # Build projections
    print("STEP 2: 10-YEAR CASH FLOW PROJECTIONS")
    print("-" * 80)

    projections = build_dcf_projections(financials, assumptions)

    # Create projection DataFrame
    proj_df = pd.DataFrame(projections)
    proj_df_display = proj_df[['year', 'revenue', 'ebitda', 'ebitda_margin', 'ebit', 'nopat', 'capex', 'fcf']].copy()

    # Format for display
    print("\nProjected Financials ($ in millions):\n")
    print(proj_df_display.to_string(index=False))
    print()

    # Calculate terminal value
    print("STEP 3: TERMINAL VALUE")
    print("-" * 80)

    terminal_value = calculate_terminal_value(projections, assumptions)

    year_10_fcf = projections[-1]['fcf']
    terminal_fcf = year_10_fcf * (1 + assumptions['terminal_growth_rate'])

    print(f"Year 10 FCF:           ${year_10_fcf:,.0f}M")
    print(f"Terminal FCF (Year 11): ${terminal_fcf:,.0f}M")
    print(f"Terminal Growth Rate:   {assumptions['terminal_growth_rate']:.1%}")
    print(f"WACC:                   {assumptions['wacc']:.1%}")
    print(f"Terminal Value:         ${terminal_value:,.0f}M")
    print()

    # Discount cash flows
    print("STEP 4: PRESENT VALUE OF CASH FLOWS")
    print("-" * 80)

    pv_fcf_list, pv_terminal_value, total_pv_fcf = discount_cash_flows(
        projections, terminal_value, assumptions['wacc']
    )

    pv_df = pd.DataFrame(pv_fcf_list)
    print("\nDiscounted Cash Flows:\n")
    print(pv_df.to_string(index=False))
    print()

    print(f"Sum of PV(FCF Years 1-10):  ${total_pv_fcf:,.0f}M")
    print(f"PV(Terminal Value):         ${pv_terminal_value:,.0f}M")
    print(f"Enterprise Value:           ${total_pv_fcf + pv_terminal_value:,.0f}M")
    print()

    # Calculate equity value
    print("STEP 5: EQUITY VALUATION")
    print("-" * 80)

    valuation = calculate_equity_value(
        total_pv_fcf, pv_terminal_value,
        financials['net_debt'], financials['shares_outstanding']
    )

    print(f"Enterprise Value:      ${valuation['enterprise_value']:,.0f}M")
    print(f"Less: Net Debt:        ${financials['net_debt']:,.0f}M")
    print(f"Equity Value:          ${valuation['equity_value']:,.0f}M")
    print()
    print(f"Shares Outstanding:    {financials['shares_outstanding']:.2f}M")
    print(f"DCF Value per Share:   ${valuation['value_per_share']:.2f}")
    print()
    print(f"Current Price:         ${financials['current_price']:.2f}")
    print(f"Implied Upside:        {((valuation['value_per_share'] - financials['current_price']) / financials['current_price'] * 100):.1f}%")
    print()

    # Sensitivity analysis
    print("STEP 6: SENSITIVITY ANALYSIS (WACC vs Terminal Growth)")
    print("-" * 80)

    sensitivity = dcf_sensitivity_analysis(financials, assumptions)

    print("\nValue per Share ($) at different WACC and Terminal Growth rates:\n")
    print(sensitivity.round(2).to_string())
    print()

    # Save outputs
    print("STEP 7: SAVING OUTPUTS...")
    print("-" * 80)

    # Save projections
    proj_df.to_csv('data/graphs/dcf_projections_10yr.csv', index=False)
    print("✓ Saved: data/graphs/dcf_projections_10yr.csv")

    # Save PV analysis
    pv_df.to_csv('data/graphs/dcf_pv_analysis.csv', index=False)
    print("✓ Saved: data/graphs/dcf_pv_analysis.csv")

    # Save sensitivity
    sensitivity.to_csv('data/graphs/dcf_sensitivity_wacc_terminal.csv')
    print("✓ Saved: data/graphs/dcf_sensitivity_wacc_terminal.csv")

    # Save summary
    summary = {
        'methodology': 'DCF',
        'enterprise_value': valuation['enterprise_value'],
        'equity_value': valuation['equity_value'],
        'value_per_share': valuation['value_per_share'],
        'current_price': financials['current_price'],
        'upside_pct': ((valuation['value_per_share'] - financials['current_price']) / financials['current_price'] * 100),
        'wacc': assumptions['wacc'],
        'terminal_growth': assumptions['terminal_growth_rate'],
        'pv_fcf_10yr': total_pv_fcf,
        'pv_terminal_value': pv_terminal_value,
        'terminal_value_pct': (pv_terminal_value / valuation['enterprise_value'] * 100),
    }

    summary_df = pd.DataFrame([summary])
    summary_df.to_csv('data/graphs/dcf_valuation_summary.csv', index=False)
    print("✓ Saved: data/graphs/dcf_valuation_summary.csv")

    print()
    print("=" * 80)
    print("DCF VALUATION COMPLETE!")
    print("=" * 80)

    return {
        'projections': projections,
        'terminal_value': terminal_value,
        'pv_analysis': pv_fcf_list,
        'valuation': valuation,
        'sensitivity': sensitivity,
    }

# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    results = generate_dcf_report()
