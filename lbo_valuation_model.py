"""
UHS LBO VALUATION MODEL
Leveraged Buyout Analysis for Ascendra Capital

Purpose: Model returns from acquiring UHS at various entry prices
Author: Ascendra Capital Investment Team
Date: October 29, 2025
"""

import pandas as pd
import numpy as np
from numpy_financial import irr

# ============================================================================
# STEP 1: DEFINE LBO TRANSACTION STRUCTURE
# ============================================================================

def build_lbo_transaction(entry_price_per_share, entry_multiple):
    """
    Build sources & uses for LBO transaction

    Entry Assumptions:
    - Purchase price per share
    - Entry EBITDA multiple (for cross-check)
    - Debt/Equity mix
    - Transaction fees
    """

    # Basic metrics
    shares_outstanding = 64.98  # Million
    current_ebitda = 2_775.6  # $M (2024)
    existing_net_debt = 4_378.5  # $M

    # Purchase price
    equity_purchase_price = entry_price_per_share * shares_outstanding

    # Implied entry multiple
    implied_entry_ev = equity_purchase_price + existing_net_debt
    implied_entry_multiple = implied_entry_ev / current_ebitda

    # Transaction structure
    transaction = {
        'entry_price_per_share': entry_price_per_share,
        'shares_outstanding': shares_outstanding,
        'equity_purchase_price': equity_purchase_price,
        'existing_net_debt': existing_net_debt,
        'enterprise_value': implied_entry_ev,
        'current_ebitda': current_ebitda,
        'implied_entry_multiple': implied_entry_multiple,
    }

    return transaction

def sources_and_uses(transaction):
    """
    Sources & Uses of Funds

    Uses:
    - Equity purchase price
    - Refinance existing debt
    - Transaction fees (2%)

    Sources:
    - New debt (60-65% of EV)
    - Ascendra equity (35-40% of EV)
    """

    # Uses
    equity_purchase = transaction['equity_purchase_price']
    existing_debt_refi = transaction['existing_net_debt']
    transaction_fees = (equity_purchase + existing_debt_refi) * 0.02  # 2% fees

    total_uses = equity_purchase + existing_debt_refi + transaction_fees

    # Sources
    # Target: 60% debt, 40% equity
    # But constrain to reasonable leverage (e.g., 5.0x Net Debt/EBITDA max)
    max_debt = transaction['current_ebitda'] * 5.0  # 5.0x leverage cap

    # New debt: Lesser of 60% of uses or 5.0x EBITDA
    new_debt = min(total_uses * 0.60, max_debt)

    # Ascendra equity: Remainder
    ascendra_equity = total_uses - new_debt

    # Debt % and equity %
    debt_pct = new_debt / total_uses
    equity_pct = ascendra_equity / total_uses

    sources_uses = {
        'uses': {
            'equity_purchase': equity_purchase,
            'refinance_debt': existing_debt_refi,
            'transaction_fees': transaction_fees,
            'total_uses': total_uses,
        },
        'sources': {
            'new_debt': new_debt,
            'ascendra_equity': ascendra_equity,
            'total_sources': total_uses,
            'debt_pct': debt_pct,
            'equity_pct': equity_pct,
        },
        'entry_leverage': new_debt / transaction['current_ebitda'],
    }

    return sources_uses

# ============================================================================
# STEP 2: 5-YEAR CASH FLOW PROJECTIONS
# ============================================================================

def build_lbo_projections(transaction, sources_uses):
    """
    Build 5-year LBO projection model

    Key assumptions:
    - Revenue growth
    - EBITDA margin expansion (from synergies)
    - CapEx
    - Interest expense
    - Debt paydown from FCF
    """

    # Starting point (Year 0)
    base_year = {
        'year': 0,
        'revenue': 15_827.9,  # $M
        'ebitda': 2_775.6,  # $M
        'ebitda_margin': 2_775.6 / 15_827.9,
        'ebit': 1_681.8,  # $M
        'depreciation': 584.8,  # $M
        'capex': 640.0,  # $M
        'fcf_before_debt': 1_427.0,  # $M
        'debt_balance': sources_uses['sources']['new_debt'],
        'interest_rate': 0.075,  # 7.5% (blended rate on new debt)
    }

    # Assumptions
    revenue_growth = 0.04  # 4% annually (organic + inflation)
    ebitda_margin_target = 0.19  # 19% (from 17.5%, synergy improvement)
    margin_improvement_annual = (ebitda_margin_target - base_year['ebitda_margin']) / 3  # 3-year improvement
    capex_pct = 0.04  # 4% of revenue
    depreciation_pct = 0.037  # 3.7% of revenue
    tax_rate = 0.21  # 21%
    mandatory_debt_paydown_pct = 0.05  # 5% of starting debt per year (amortization)

    # Build projections
    projections = [base_year]

    for year in range(1, 6):
        prev = projections[year - 1]

        # Revenue growth
        revenue = prev['revenue'] * (1 + revenue_growth)

        # EBITDA margin expansion (gradual)
        if year <= 3:
            ebitda_margin = prev['ebitda_margin'] + margin_improvement_annual
        else:
            ebitda_margin = ebitda_margin_target

        ebitda = revenue * ebitda_margin

        # Depreciation & CapEx
        depreciation = revenue * depreciation_pct
        capex = revenue * capex_pct

        # EBIT
        ebit = ebitda - depreciation

        # Interest expense (on beginning debt balance)
        interest_expense = prev['debt_balance'] * base_year['interest_rate']

        # EBT & Taxes
        ebt = ebit - interest_expense
        taxes = ebt * tax_rate if ebt > 0 else 0
        net_income = ebt - taxes

        # Cash flow
        operating_cash_flow = net_income + depreciation
        fcf_after_capex = operating_cash_flow - capex

        # Debt paydown
        mandatory_amortization = sources_uses['sources']['new_debt'] * mandatory_debt_paydown_pct
        optional_paydown = max(fcf_after_capex - mandatory_amortization, 0)  # Pay down more if FCF available
        total_debt_paydown = mandatory_amortization + optional_paydown

        # Ending debt balance
        debt_balance = max(prev['debt_balance'] - total_debt_paydown, 0)

        # FCF to equity (after debt paydown)
        fcf_to_equity = fcf_after_capex - total_debt_paydown

        projections.append({
            'year': year,
            'revenue': revenue,
            'ebitda': ebitda,
            'ebitda_margin': ebitda_margin,
            'depreciation': depreciation,
            'ebit': ebit,
            'interest_expense': interest_expense,
            'ebt': ebt,
            'taxes': taxes,
            'net_income': net_income,
            'capex': capex,
            'fcf_after_capex': fcf_after_capex,
            'debt_paydown': total_debt_paydown,
            'debt_balance': debt_balance,
            'fcf_to_equity': fcf_to_equity,
        })

    return projections

# ============================================================================
# STEP 3: EXIT VALUATION & RETURNS
# ============================================================================

def calculate_lbo_returns(projections, sources_uses, exit_multiple):
    """
    Calculate exit value and returns to equity

    Exit Assumptions:
    - Exit in Year 5
    - Exit EBITDA multiple (typically same as entry or slightly lower)
    - Exit enterprise value = Year 5 EBITDA × Exit Multiple
    - Exit equity value = Exit EV - Exit Debt
    - Returns: IRR, MOIC (Multiple of Invested Capital)
    """

    year_5 = projections[5]

    # Exit enterprise value
    exit_ebitda = year_5['ebitda']
    exit_enterprise_value = exit_ebitda * exit_multiple

    # Exit debt balance
    exit_debt = year_5['debt_balance']

    # Exit equity value
    exit_equity_value = exit_enterprise_value - exit_debt

    # Initial equity invested
    initial_equity = sources_uses['sources']['ascendra_equity']

    # Returns
    moic = exit_equity_value / initial_equity

    # IRR calculation
    cash_flows = [-initial_equity]  # Year 0: invest equity
    for year in range(1, 6):
        cash_flows.append(projections[year]['fcf_to_equity'])
    cash_flows[5] += exit_equity_value  # Year 5: exit + FCF

    irr_value = irr(cash_flows)

    returns = {
        'exit_year': 5,
        'exit_ebitda': exit_ebitda,
        'exit_multiple': exit_multiple,
        'exit_enterprise_value': exit_enterprise_value,
        'exit_debt': exit_debt,
        'exit_equity_value': exit_equity_value,
        'initial_equity_invested': initial_equity,
        'moic': moic,
        'irr': irr_value,
        'annualized_return_pct': (moic ** (1/5) - 1) * 100,
    }

    return returns

# ============================================================================
# STEP 4: RUN MULTIPLE SCENARIOS
# ============================================================================

def lbo_scenario_analysis(entry_prices, exit_multiples):
    """
    Run LBO analysis across multiple entry prices and exit multiples

    Returns: DataFrame showing IRR and MOIC for each combination
    """

    scenarios = []

    for entry_price in entry_prices:
        for exit_multiple in exit_multiples:
            # Build transaction
            transaction = build_lbo_transaction(entry_price, None)
            sources_uses_result = sources_and_uses(transaction)

            # Build projections
            projections = build_lbo_projections(transaction, sources_uses_result)

            # Calculate returns
            returns = calculate_lbo_returns(projections, sources_uses_result, exit_multiple)

            scenarios.append({
                'entry_price': entry_price,
                'entry_multiple': transaction['implied_entry_multiple'],
                'exit_multiple': exit_multiple,
                'initial_equity': sources_uses_result['sources']['ascendra_equity'],
                'exit_equity_value': returns['exit_equity_value'],
                'moic': returns['moic'],
                'irr': returns['irr'],
            })

    return pd.DataFrame(scenarios)

# ============================================================================
# STEP 5: REVERSE LBO (Target IRR)
# ============================================================================

def reverse_lbo(target_irr, exit_multiple):
    """
    Reverse LBO: What price can we pay to achieve target IRR?

    Logic:
    - Start with various entry prices
    - Calculate IRR for each
    - Find price that delivers target IRR
    """

    # Try entry prices from $200 to $450
    entry_prices = np.arange(200, 451, 5)

    results = []

    for entry_price in entry_prices:
        transaction = build_lbo_transaction(entry_price, None)
        sources_uses_result = sources_and_uses(transaction)
        projections = build_lbo_projections(transaction, sources_uses_result)
        returns = calculate_lbo_returns(projections, sources_uses_result, exit_multiple)

        results.append({
            'entry_price': entry_price,
            'irr': returns['irr'],
            'moic': returns['moic'],
        })

    results_df = pd.DataFrame(results)

    # Find closest to target IRR
    results_df['irr_diff'] = abs(results_df['irr'] - target_irr)
    closest = results_df.loc[results_df['irr_diff'].idxmin()]

    return closest

# ============================================================================
# STEP 6: GENERATE LBO REPORT
# ============================================================================

def generate_lbo_report():
    """Generate comprehensive LBO analysis report"""

    print("=" * 80)
    print("UHS LBO VALUATION MODEL")
    print("Leveraged Buyout Analysis for Ascendra Capital")
    print("=" * 80)
    print()

    # Base case entry price: $355/share (midpoint of recommended range)
    entry_price = 355
    exit_multiple = 9.0  # Conservative exit (slightly below entry)

    print(f"BASE CASE ASSUMPTIONS")
    print("-" * 80)
    print(f"Entry Price:           ${entry_price:.2f}/share")
    print(f"Exit Multiple:         {exit_multiple:.1f}x EBITDA")
    print(f"Hold Period:           5 years")
    print(f"Revenue Growth:        4% annually")
    print(f"EBITDA Margin Target:  19% (from synergies)")
    print(f"Exit Year:             2030")
    print()

    # Build transaction
    print("STEP 1: TRANSACTION STRUCTURE")
    print("-" * 80)

    transaction = build_lbo_transaction(entry_price, None)

    print(f"Equity Purchase Price:     ${transaction['equity_purchase_price']:,.0f}M")
    print(f"Plus: Existing Net Debt:   ${transaction['existing_net_debt']:,.0f}M")
    print(f"Enterprise Value:          ${transaction['enterprise_value']:,.0f}M")
    print()
    print(f"Current EBITDA (2024):     ${transaction['current_ebitda']:,.0f}M")
    print(f"Implied Entry Multiple:    {transaction['implied_entry_multiple']:.1f}x")
    print()

    # Sources & Uses
    print("STEP 2: SOURCES & USES OF FUNDS")
    print("-" * 80)

    sources_uses_result = sources_and_uses(transaction)

    print("USES:")
    print(f"  Equity Purchase:        ${sources_uses_result['uses']['equity_purchase']:,.0f}M")
    print(f"  Refinance Existing Debt: ${sources_uses_result['uses']['refinance_debt']:,.0f}M")
    print(f"  Transaction Fees (2%):   ${sources_uses_result['uses']['transaction_fees']:,.0f}M")
    print(f"  ───────────────────────────────────────")
    print(f"  Total Uses:              ${sources_uses_result['uses']['total_uses']:,.0f}M")
    print()
    print("SOURCES:")
    print(f"  New Debt:               ${sources_uses_result['sources']['new_debt']:,.0f}M  ({sources_uses_result['sources']['debt_pct']:.1%})")
    print(f"  Ascendra Equity:        ${sources_uses_result['sources']['ascendra_equity']:,.0f}M  ({sources_uses_result['sources']['equity_pct']:.1%})")
    print(f"  ───────────────────────────────────────")
    print(f"  Total Sources:          ${sources_uses_result['sources']['total_sources']:,.0f}M")
    print()
    print(f"Entry Leverage:           {sources_uses_result['entry_leverage']:.2f}x Net Debt/EBITDA")
    print()

    # Projections
    print("STEP 3: 5-YEAR FINANCIAL PROJECTIONS")
    print("-" * 80)

    projections = build_lbo_projections(transaction, sources_uses_result)

    proj_df = pd.DataFrame(projections)
    proj_display = proj_df[['year', 'revenue', 'ebitda', 'ebitda_margin', 'ebit', 'net_income',
                             'fcf_after_capex', 'debt_paydown', 'debt_balance']].copy()

    print("\nProjected Financials ($ in millions):\n")
    print(proj_display.to_string(index=False))
    print()

    # Returns
    print("STEP 4: EXIT VALUATION & RETURNS")
    print("-" * 80)

    returns = calculate_lbo_returns(projections, sources_uses_result, exit_multiple)

    print(f"Exit Year 5 EBITDA:        ${returns['exit_ebitda']:,.0f}M")
    print(f"Exit Multiple:             {returns['exit_multiple']:.1f}x")
    print(f"Exit Enterprise Value:     ${returns['exit_enterprise_value']:,.0f}M")
    print(f"Less: Exit Debt:           ${returns['exit_debt']:,.0f}M")
    print(f"Exit Equity Value:         ${returns['exit_equity_value']:,.0f}M")
    print()
    print(f"Initial Equity Invested:   ${returns['initial_equity_invested']:,.0f}M")
    print(f"Exit Equity Value:         ${returns['exit_equity_value']:,.0f}M")
    print(f"───────────────────────────────────────────────")
    print(f"MOIC (Multiple):           {returns['moic']:.2f}x")
    print(f"IRR:                       {returns['irr']:.1%}")
    print(f"Annualized Return:         {returns['annualized_return_pct']:.1f}%")
    print()

    # Scenario analysis
    print("STEP 5: SCENARIO ANALYSIS (Entry Price vs Exit Multiple)")
    print("-" * 80)

    entry_prices = [300, 325, 350, 355, 375, 400, 425]
    exit_multiples = [8.0, 8.5, 9.0, 9.5, 10.0]

    scenarios = lbo_scenario_analysis(entry_prices, exit_multiples)

    print("\nIRR by Entry Price and Exit Multiple:\n")

    # Pivot table for display
    irr_pivot = scenarios.pivot_table(values='irr', index='entry_price', columns='exit_multiple')
    print((irr_pivot * 100).round(1).to_string())
    print()

    # Reverse LBO
    print("STEP 6: REVERSE LBO (Target Returns)")
    print("-" * 80)

    target_irrs = [0.20, 0.25, 0.30]  # 20%, 25%, 30%

    print(f"What price can we pay to achieve target IRR? (Exit at {exit_multiple:.1f}x)\n")

    reverse_results = []
    for target_irr in target_irrs:
        result = reverse_lbo(target_irr, exit_multiple)
        reverse_results.append({
            'Target IRR': f"{target_irr:.0%}",
            'Max Entry Price': f"${result['entry_price']:.2f}",
            'Actual IRR': f"{result['irr']:.1%}",
            'MOIC': f"{result['moic']:.2f}x"
        })

    reverse_df = pd.DataFrame(reverse_results)
    print(reverse_df.to_string(index=False))
    print()

    # Save outputs
    print("STEP 7: SAVING OUTPUTS...")
    print("-" * 80)

    # Save projections
    proj_df.to_csv('data/graphs/lbo_projections_5yr.csv', index=False)
    print("✓ Saved: data/graphs/lbo_projections_5yr.csv")

    # Save scenarios
    scenarios.to_csv('data/graphs/lbo_scenario_analysis.csv', index=False)
    print("✓ Saved: data/graphs/lbo_scenario_analysis.csv")

    # Save IRR sensitivity
    irr_pivot.to_csv('data/graphs/lbo_sensitivity_irr.csv')
    print("✓ Saved: data/graphs/lbo_sensitivity_irr.csv")

    # MOIC sensitivity
    moic_pivot = scenarios.pivot_table(values='moic', index='entry_price', columns='exit_multiple')
    moic_pivot.to_csv('data/graphs/lbo_sensitivity_moic.csv')
    print("✓ Saved: data/graphs/lbo_sensitivity_moic.csv")

    # Save base case summary
    base_case_summary = {
        'methodology': 'LBO',
        'entry_price': entry_price,
        'entry_multiple': transaction['implied_entry_multiple'],
        'exit_multiple': exit_multiple,
        'initial_equity': returns['initial_equity_invested'],
        'exit_equity_value': returns['exit_equity_value'],
        'moic': returns['moic'],
        'irr': returns['irr'],
        'hold_period_years': 5,
    }

    summary_df = pd.DataFrame([base_case_summary])
    summary_df.to_csv('data/graphs/lbo_valuation_summary.csv', index=False)
    print("✓ Saved: data/graphs/lbo_valuation_summary.csv")

    print()
    print("=" * 80)
    print("LBO VALUATION COMPLETE!")
    print("=" * 80)
    print()
    print(f"KEY TAKEAWAY: At ${entry_price}/share entry, Ascendra earns {returns['irr']:.1%} IRR (5-year hold)")
    print(f"              This is {'ATTRACTIVE' if returns['irr'] >= 0.25 else 'ACCEPTABLE' if returns['irr'] >= 0.20 else 'BELOW TARGET'} for a healthcare LBO")
    print()

    return {
        'transaction': transaction,
        'sources_uses': sources_uses_result,
        'projections': projections,
        'returns': returns,
        'scenarios': scenarios,
    }

# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    results = generate_lbo_report()
