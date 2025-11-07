"""
UHS VALUATION FOOTBALL FIELD CHART
Comprehensive valuation summary across all methodologies

Purpose: Visual summary showing valuation range from all methods
Author: Ascendra Capital Investment Team
Date: October 29, 2025
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd
import numpy as np

# ============================================================================
# STEP 1: GATHER VALUATION RESULTS FROM ALL MODELS
# ============================================================================

def load_all_valuations():
    """
    Load valuation results from all models:
    1. SOTP (4-part sum-of-the-parts)
    2. DCF (10-year discounted cash flow)
    3. LBO (leveraged buyout analysis)
    4. Comparable Companies (trading multiples)
    5. Precedent Transactions (M&A multiples)
    """

    valuations = []

    # 1. SOTP Valuation (from sotp_valuation_scenarios.csv)
    try:
        sotp = pd.read_csv('data/graphs/sotp_valuation_scenarios.csv')

        # Clean currency formatting (remove $ and ,)
        def clean_currency(val):
            if isinstance(val, str):
                return float(val.replace('$', '').replace(',', '').replace('+', '').replace('%', ''))
            return float(val)

        bear = clean_currency(sotp[sotp['Scenario'] == 'BEAR']['Value Per Share'].values[0])
        base = clean_currency(sotp[sotp['Scenario'] == 'BASE']['Value Per Share'].values[0])
        bull = clean_currency(sotp[sotp['Scenario'] == 'BULL']['Value Per Share'].values[0])

        valuations.append({
            'method': 'SOTP (4-Part)',
            'low': float(bear),
            'base': float(base),
            'high': float(bull),
            'weight': 0.30,  # 30% weight (primary method)
        })
    except Exception as e:
        print(f"Warning: Could not load SOTP data: {e}")
        # Using updated SOTP values (Oct 31, 2025, BEHAVIORAL PREMIUM APPLIED)
        valuations.append({
            'method': 'SOTP (4-Part)',
            'low': 489,   # Conservative: 8.5x Beh (below historical), 6.0x Acute, 7.0% cap
            'base': 530,  # Base: 9.0x Beh (historical avg, justified by 22.7% margins), 6.5x Acute, 6.5% cap
            'high': 578,  # Optimistic: 9.5x Beh (M&A range), 7.0x Acute, 6.0% cap
            'weight': 0.30,
        })

    # 2. DCF Valuation (from dcf_valuation_summary.csv) - UPDATED Oct 31, 2025
    try:
        dcf = pd.read_csv('data/graphs/dcf_valuation_summary.csv')
        dcf_value = dcf['value_per_share'].values[0]

        # Use sensitivity for range based on WACC 8.5-9.5%
        valuations.append({
            'method': 'DCF (10-Year)',
            'low': 396,  # WACC 9.5% (conservative)
            'base': 434,  # WACC 9.0% (historical ERP 5.0%)
            'high': 477,  # WACC 8.5% (current ERP 4.65%)
            'weight': 0.25,  # 25% weight
        })
    except:
        # Updated DCF values based on sourced WACC (Oct 31, 2025)
        valuations.append({
            'method': 'DCF (10-Year)',
            'low': 396,   # WACC 9.5%, terminal 2.5%
            'base': 434,  # WACC 9.0%, terminal 2.5%
            'high': 477,  # WACC 8.5%, terminal 2.5%
            'weight': 0.25,
        })

    # 3. LBO Analysis (from reverse LBO)
    # LBO tells us what a financial buyer would pay
    # Use reverse LBO results: 20-30% IRR targets
    try:
        # From LBO output, we know:
        # 20% IRR → Max $300
        # 25% IRR → Max $265
        # 30% IRR → Max $225
        # For strategic buyer (lower return requirement): 15-20% IRR
        valuations.append({
            'method': 'LBO Analysis',
            'low': 265,  # 25% IRR (aggressive PE)
            'base': 320,  # ~17% IRR (strategic buyer)
            'high': 385,  # ~12% IRR (low return threshold)
            'weight': 0.20,  # 20% weight
        })
    except:
        valuations.append({
            'method': 'LBO Analysis',
            'low': 265,
            'base': 320,
            'high': 385,
            'weight': 0.20,
        })

    # 4. Comparable Companies (trading multiples) - UPDATED Oct 31, 2025
    # Use current EV/EBITDA market multiples (SOURCED)
    current_ebitda = 2775.6  # $M (UHS 10-K FY2024)
    shares = 63.64  # M (StockAnalysis.com, Oct 2025)
    net_debt = 4379  # $M (UHS 10-K FY2024)

    # Industry comps (SOURCED): THC 6.0x, ACHC 6.6-7.3x, CYH 9.65x, HCA 9.1x, Median 7.84x
    comp_multiples = {
        'low': 6.0,   # THC level (conservative)
        'base': 7.0,  # Below industry median (reflects undervaluation)
        'high': 8.0,  # Closer to industry median
    }

    comp_values = {}
    for case, multiple in comp_multiples.items():
        ev = current_ebitda * multiple
        equity_value = ev - net_debt
        value_per_share = equity_value / shares
        comp_values[case] = value_per_share

    valuations.append({
        'method': 'Comparable Companies',
        'low': comp_values['low'],
        'base': comp_values['base'],
        'high': comp_values['high'],
        'weight': 0.10,  # 10% weight (less relevant, single multiple)
    })

    # 5. Precedent Transactions (M&A multiples) - UPDATED Oct 31, 2025
    # SOURCED: First Page Sage (7-9x), Healthcare Capital (10x median), RL Hulett (8.0x strategic)
    precedent_multiples = {
        'low': 8.0,   # Hospital-focused deal (7-9x range low end)
        'base': 10.0, # Industry median (Healthcare Capital 2023)
        'high': 12.0, # Premium deal / competitive auction (75th percentile 13.9x)
    }

    precedent_values = {}
    for case, multiple in precedent_multiples.items():
        ev = current_ebitda * multiple
        equity_value = ev - net_debt
        value_per_share = equity_value / shares
        precedent_values[case] = value_per_share

    valuations.append({
        'method': 'Precedent Transactions',
        'low': precedent_values['low'],
        'base': precedent_values['base'],
        'high': precedent_values['high'],
        'weight': 0.15,  # 15% weight
    })

    return pd.DataFrame(valuations)

# ============================================================================
# STEP 2: CALCULATE WEIGHTED AVERAGE VALUATION
# ============================================================================

def calculate_weighted_average(valuations_df):
    """
    Calculate weighted average valuation across all methods
    """

    weighted_low = (valuations_df['low'] * valuations_df['weight']).sum()
    weighted_base = (valuations_df['base'] * valuations_df['weight']).sum()
    weighted_high = (valuations_df['high'] * valuations_df['weight']).sum()

    return {
        'method': 'WEIGHTED AVERAGE',
        'low': weighted_low,
        'base': weighted_base,
        'high': weighted_high,
        'weight': 1.0,
    }

# ============================================================================
# STEP 3: CREATE FOOTBALL FIELD CHART
# ============================================================================

def create_football_field_chart(valuations_df, weighted_avg, current_price=225.30):
    """
    Create professional football field valuation chart

    Chart shows:
    - Horizontal bars for each valuation method
    - Range (low to high)
    - Base case marker
    - Current price line
    - Weighted average highlighted
    """

    # Set up figure with Ascendra color scheme (increased width for labels)
    fig, ax = plt.subplots(figsize=(16, 10))
    fig.patch.set_facecolor('#0a1929')
    ax.set_facecolor('#0d1b2a')

    # Color scheme
    colors = {
        'SOTP (4-Part)': '#4cc9f0',
        'DCF (10-Year)': '#3a86ff',
        'LBO Analysis': '#7209b7',
        'Comparable Companies': '#f72585',
        'Precedent Transactions': '#06ffa5',
        'WEIGHTED AVERAGE': '#ffba08',
    }

    # Add weighted average to dataframe
    weighted_row = pd.DataFrame([weighted_avg])
    full_df = pd.concat([valuations_df, weighted_row], ignore_index=True)

    # Reverse order for plotting (top to bottom)
    full_df = full_df.iloc[::-1].reset_index(drop=True)

    y_positions = np.arange(len(full_df))

    # Plot horizontal bars
    for idx, row in full_df.iterrows():
        method = row['method']
        low = row['low']
        base = row['base']
        high = row['high']

        # Bar width
        bar_width = 0.6 if method != 'WEIGHTED AVERAGE' else 0.8

        # Color
        color = colors.get(method, '#778da9')

        # Bar from low to high
        bar_length = high - low

        # Draw bar
        if method == 'WEIGHTED AVERAGE':
            # Highlight weighted average
            ax.barh(y_positions[idx], bar_length, left=low, height=bar_width,
                   color=color, alpha=0.9, edgecolor='white', linewidth=3, zorder=10)
        else:
            ax.barh(y_positions[idx], bar_length, left=low, height=bar_width,
                   color=color, alpha=0.7, edgecolor='white', linewidth=1.5)

        # Mark base case
        ax.plot(base, y_positions[idx], marker='D', markersize=12, color='white',
               markeredgecolor=color, markeredgewidth=2, zorder=15)

        # Add value labels
        # Low
        ax.text(low - 10, y_positions[idx], f'${low:.0f}',
               ha='right', va='center', fontsize=9, color='#e0e1dd', fontweight='bold')
        # High
        ax.text(high + 10, y_positions[idx], f'${high:.0f}',
               ha='left', va='center', fontsize=9, color='#e0e1dd', fontweight='bold')
        # Base (above bar)
        ax.text(base, y_positions[idx] + 0.45, f'${base:.0f}',
               ha='center', va='bottom', fontsize=10, color='white', fontweight='bold',
               bbox=dict(boxstyle='round,pad=0.3', facecolor=color, edgecolor='white', linewidth=1))

    # Current price line
    ax.axvline(current_price, color='#d62828', linewidth=3, linestyle='--',
              label=f'Current Price: ${current_price:.2f}', zorder=5)

    # Offer range (recommended $425-475) - UPDATED Oct 31, 2025 with Behavioral Premium
    offer_low = 425
    offer_high = 475
    ax.axvspan(offer_low, offer_high, alpha=0.15, color='#06ffa5', zorder=1)
    ax.text((offer_low + offer_high) / 2, len(full_df) - 0.5,
           'Recommended\nOffer Range\n$425-475',
           ha='center', va='top', fontsize=11, color='#06ffa5',
           fontweight='bold',
           bbox=dict(boxstyle='round,pad=0.5', facecolor='#0d1b2a', edgecolor='#06ffa5', linewidth=2))

    # Labels and styling
    ax.set_yticks(y_positions)
    ax.set_yticklabels(full_df['method'], fontsize=12, color='#e0e1dd', fontweight='bold')

    ax.set_xlabel('Equity Value per Share ($)', fontsize=14, color='#e0e1dd', fontweight='bold')
    ax.set_title('UHS VALUATION FOOTBALL FIELD\nComprehensive Valuation Across All Methodologies',
                fontsize=18, color='#4cc9f0', fontweight='bold', pad=20)

    # Grid
    ax.grid(axis='x', alpha=0.3, linestyle='--', color='#778da9')
    ax.set_axisbelow(True)

    # X-axis range (extend left to prevent overlap with y-axis labels)
    ax.set_xlim(150, 600)

    # Spine colors
    for spine in ax.spines.values():
        spine.set_edgecolor('#2d3e50')
        spine.set_linewidth(2)

    # Tick colors with more padding
    ax.tick_params(axis='x', colors='#e0e1dd', labelsize=11)
    ax.tick_params(axis='y', colors='#e0e1dd', pad=10)  # Added padding for y-axis labels

    # Legend
    legend_elements = [
        mpatches.Patch(color='#d62828', label=f'Current Price: ${current_price:.2f}'),
        mpatches.Patch(color='#06ffa5', alpha=0.3, label='Recommended Offer Range: $425-475'),
        mpatches.Patch(color='#ffba08', label=f'Weighted Average: ${weighted_avg["base"]:.0f}'),
    ]
    ax.legend(handles=legend_elements, loc='lower right', fontsize=11,
             facecolor='#1b263b', edgecolor='#2d3e50', labelcolor='#e0e1dd', framealpha=0.95)

    # Add footer
    fig.text(0.5, 0.02, '🔒 CONFIDENTIAL & PROPRIETARY | ASCENDRA CAPITAL | October 2025',
            ha='center', fontsize=10, color='#778da9', style='italic')

    # Adjust layout to prevent y-axis label overlap
    plt.tight_layout(rect=[0.05, 0.03, 1, 0.97])  # Add left margin for y-axis labels

    # Save
    plt.savefig('data/graphs/football_field_valuation.png', dpi=300, facecolor='#0a1929', edgecolor='none', bbox_inches='tight')
    print("✓ Saved: data/graphs/football_field_valuation.png")

    plt.savefig('football_field_valuation.png', dpi=300, facecolor='#0a1929', edgecolor='none', bbox_inches='tight')
    print("✓ Saved: football_field_valuation.png (root folder)")

    plt.show()

# ============================================================================
# STEP 4: GENERATE SUMMARY TABLE
# ============================================================================

def create_summary_table(valuations_df, weighted_avg):
    """Create summary table with all valuations"""

    # Add weighted average
    full_df = pd.concat([valuations_df, pd.DataFrame([weighted_avg])], ignore_index=True)

    # Format for display
    summary = full_df.copy()
    summary['Range'] = summary.apply(lambda x: f"${x['low']:.0f} - ${x['high']:.0f}", axis=1)
    summary['Base Case'] = summary['base'].apply(lambda x: f"${x:.0f}")
    summary['Weight'] = summary['weight'].apply(lambda x: f"{x:.0%}")

    summary_display = summary[['method', 'Range', 'Base Case', 'Weight']]
    summary_display.columns = ['Valuation Method', 'Range', 'Base Case', 'Weight']

    return summary_display

# ============================================================================
# STEP 5: GENERATE REPORT
# ============================================================================

def generate_football_field_report():
    """Generate complete football field analysis"""

    print("=" * 80)
    print("UHS VALUATION FOOTBALL FIELD")
    print("Comprehensive Summary Across All Methodologies")
    print("=" * 80)
    print()

    # Load valuations
    print("STEP 1: GATHERING VALUATION RESULTS FROM ALL MODELS")
    print("-" * 80)

    valuations_df = load_all_valuations()

    print("Valuation methods loaded:")
    for idx, row in valuations_df.iterrows():
        print(f"  ✓ {row['method']}: ${row['low']:.0f} - ${row['high']:.0f} (Base: ${row['base']:.0f})")
    print()

    # Calculate weighted average
    print("STEP 2: CALCULATING WEIGHTED AVERAGE")
    print("-" * 80)

    weighted_avg = calculate_weighted_average(valuations_df)

    print(f"Weighted Average Valuation:")
    print(f"  Low:  ${weighted_avg['low']:.2f}")
    print(f"  Base: ${weighted_avg['base']:.2f}")
    print(f"  High: ${weighted_avg['high']:.2f}")
    print()

    # Summary table
    print("STEP 3: VALUATION SUMMARY TABLE")
    print("-" * 80)

    summary_table = create_summary_table(valuations_df, weighted_avg)
    print("\n" + summary_table.to_string(index=False))
    print()

    # Key insights
    print("STEP 4: KEY INSIGHTS")
    print("-" * 80)

    current_price = 225.30  # Updated Oct 29, 2025
    median_base = valuations_df['base'].median()

    print(f"Current Market Price:        ${current_price:.2f}")
    print(f"Median Base Case:            ${median_base:.2f}")
    print(f"Weighted Average Base:       ${weighted_avg['base']:.2f}")
    print(f"Implied Upside (Median):     {((median_base - current_price) / current_price * 100):.1f}%")
    print(f"Implied Upside (Weighted):   {((weighted_avg['base'] - current_price) / current_price * 100):.1f}%")
    print()

    print("Valuation Range Summary:")
    print(f"  Minimum (Comps Low):       ${valuations_df['low'].min():.0f}")
    print(f"  Maximum (DCF High):        ${valuations_df['high'].max():.0f}")
    print(f"  Range:                     ${valuations_df['low'].min():.0f} - ${valuations_df['high'].max():.0f}")
    print()

    print("Recommended Offer Range: $425 - $475/share")
    print(f"  Premium to Current:        89% - 111%")
    print(f"  vs. Weighted Average Base: {((425 - weighted_avg['base']) / weighted_avg['base'] * 100):.1f}% to {((475 - weighted_avg['base']) / weighted_avg['base'] * 100):.1f}%")
    print()

    # Create chart
    print("STEP 5: GENERATING FOOTBALL FIELD CHART")
    print("-" * 80)

    create_football_field_chart(valuations_df, weighted_avg)

    # Save data
    print()
    print("STEP 6: SAVING OUTPUTS")
    print("-" * 80)

    summary_table.to_csv('data/graphs/football_field_summary.csv', index=False)
    print("✓ Saved: data/graphs/football_field_summary.csv")

    # Master valuation summary
    master_summary = {
        'current_price': current_price,
        'weighted_average_low': weighted_avg['low'],
        'weighted_average_base': weighted_avg['base'],
        'weighted_average_high': weighted_avg['high'],
        'median_base': median_base,
        'min_valuation': valuations_df['low'].min(),
        'max_valuation': valuations_df['high'].max(),
        'recommended_offer_low': 425,
        'recommended_offer_high': 475,
        'upside_to_weighted_avg': ((weighted_avg['base'] - current_price) / current_price * 100),
    }

    master_df = pd.DataFrame([master_summary])
    master_df.to_csv('data/graphs/valuation_master_summary.csv', index=False)
    print("✓ Saved: data/graphs/valuation_master_summary.csv")

    print()
    print("=" * 80)
    print("FOOTBALL FIELD ANALYSIS COMPLETE!")
    print("=" * 80)
    print()
    print(f"📊 CONCLUSION:")
    print(f"   Weighted Average Fair Value: ${weighted_avg['base']:.0f}/share")
    print(f"   Current Price: ${current_price:.2f}/share")
    print(f"   Implied Upside: {((weighted_avg['base'] - current_price) / current_price * 100):.0f}%")
    print()
    print(f"   Recommended Offer: $425-475/share (89-111% premium)")
    print(f"   → At {((450 - weighted_avg['base']) / weighted_avg['base'] * 100):.0f}% to weighted average fair value")
    print()

    return {
        'valuations': valuations_df,
        'weighted_avg': weighted_avg,
        'summary_table': summary_table,
    }

# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    results = generate_football_field_report()
