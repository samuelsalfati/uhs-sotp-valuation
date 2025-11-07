#!/usr/bin/env python3
"""
Prepare UHS data in formats optimized for graphing and visualization
Creates CSV files and structured data for all key metrics
"""

import json
import pandas as pd
import numpy as np

def load_data():
    """Load comprehensive JSON data"""
    with open('data/UHS_10K_2024_comprehensive_data.json', 'r') as f:
        return json.load(f)

def create_segment_financials_table(data):
    """Create 3-year segment financials table"""

    segments_data = []

    # Acute Care
    for year in ['2024', '2023', '2022']:
        if data['segment_financials']['acute_care'].get(year):
            segment_data = data['segment_financials']['acute_care'][year]
            segments_data.append({
                'Year': int(year),
                'Segment': 'Acute Care',
                'Revenue_M': segment_data.get('revenue', 0) / 1e6 if segment_data.get('revenue') else None,
                'EBITDA_M': segment_data.get('adjusted_ebitda', 0) / 1e6 if segment_data.get('adjusted_ebitda') else None,
                'EBITDA_Margin_Pct': segment_data.get('ebitda_margin', 0) * 100 if segment_data.get('ebitda_margin') else None,
                'Facilities': segment_data.get('facilities_count'),
                'Beds': segment_data.get('licensed_beds')
            })

    # Behavioral Health
    for year in ['2024', '2023', '2022']:
        if data['segment_financials']['behavioral_health'].get(year):
            segment_data = data['segment_financials']['behavioral_health'][year]
            segments_data.append({
                'Year': int(year),
                'Segment': 'Behavioral Health',
                'Revenue_M': segment_data.get('revenue', 0) / 1e6 if segment_data.get('revenue') else None,
                'EBITDA_M': segment_data.get('adjusted_ebitda', 0) / 1e6 if segment_data.get('adjusted_ebitda') else None,
                'EBITDA_Margin_Pct': segment_data.get('ebitda_margin', 0) * 100 if segment_data.get('ebitda_margin') else None,
                'Facilities': segment_data.get('facilities_count'),
                'Beds': segment_data.get('licensed_beds')
            })

    df = pd.DataFrame(segments_data)
    df = df.sort_values(['Segment', 'Year'])
    return df

def create_consolidated_financials_table(data):
    """Create 3-year consolidated financials"""

    financials_data = []

    for year in ['2024', '2023', '2022']:
        if data['income_statement'].get(year):
            income_data = data['income_statement'][year]

            revenue = income_data.get('revenue', {}).get('total_revenue', 0)
            operating_income = income_data.get('operating_income', 0)
            net_income = income_data.get('net_income', 0)
            eps_diluted = income_data.get('earnings_per_share', {}).get('diluted', 0)

            financials_data.append({
                'Year': int(year),
                'Revenue_M': revenue / 1e6 if revenue else None,
                'Operating_Income_M': operating_income / 1e6 if operating_income else None,
                'Net_Income_M': net_income / 1e6 if net_income else None,
                'EPS_Diluted': eps_diluted,
                'Operating_Margin_Pct': (operating_income / revenue * 100) if revenue else None
            })

    df = pd.DataFrame(financials_data)
    df = df.sort_values('Year')

    # Calculate YoY growth
    if len(df) > 1:
        df['Revenue_Growth_Pct'] = df['Revenue_M'].pct_change() * 100
        df['Operating_Income_Growth_Pct'] = df['Operating_Income_M'].pct_change() * 100
        df['Net_Income_Growth_Pct'] = df['Net_Income_M'].pct_change() * 100
        df['EPS_Growth_Pct'] = df['EPS_Diluted'].pct_change() * 100

    return df

def create_segment_comparison_2024(data):
    """Create side-by-side segment comparison for 2024"""

    acute = data['segment_financials']['acute_care']['2024']
    behavioral = data['segment_financials']['behavioral_health']['2024']

    comparison_data = {
        'Metric': [
            'Revenue ($M)',
            'EBITDA ($M)',
            'EBITDA Margin (%)',
            'Facilities (#)',
            'Licensed Beds (#)',
            'Revenue per Facility ($M)',
            'Revenue per Bed ($k)',
            'EBITDA per Facility ($M)',
            'EBITDA per Bed ($k)'
        ],
        'Acute_Care': [
            acute['revenue'] / 1e6,
            acute['adjusted_ebitda'] / 1e6,
            acute['ebitda_margin'] * 100,
            acute['facilities_count'],
            acute['licensed_beds'],
            (acute['revenue'] / acute['facilities_count']) / 1e6,
            (acute['revenue'] / acute['licensed_beds']) / 1e3,
            (acute['adjusted_ebitda'] / acute['facilities_count']) / 1e6,
            (acute['adjusted_ebitda'] / acute['licensed_beds']) / 1e3
        ],
        'Behavioral_Health': [
            behavioral['revenue'] / 1e6,
            behavioral['adjusted_ebitda'] / 1e6,
            behavioral['ebitda_margin'] * 100,
            behavioral['facilities_count'],
            behavioral['licensed_beds'],
            (behavioral['revenue'] / behavioral['facilities_count']) / 1e6,
            (behavioral['revenue'] / behavioral['licensed_beds']) / 1e3,
            (behavioral['adjusted_ebitda'] / behavioral['facilities_count']) / 1e6,
            (behavioral['adjusted_ebitda'] / behavioral['licensed_beds']) / 1e3
        ]
    }

    df = pd.DataFrame(comparison_data)

    # Add total column
    total_revenue = acute['revenue'] + behavioral['revenue']
    total_ebitda = acute['adjusted_ebitda'] + behavioral['adjusted_ebitda']
    total_facilities = acute['facilities_count'] + behavioral['facilities_count']
    total_beds = acute['licensed_beds'] + behavioral['licensed_beds']

    df['Total'] = [
        total_revenue / 1e6,
        total_ebitda / 1e6,
        (total_ebitda / total_revenue) * 100,
        total_facilities,
        total_beds,
        (total_revenue / total_facilities) / 1e6,
        (total_revenue / total_beds) / 1e3,
        (total_ebitda / total_facilities) / 1e6,
        (total_ebitda / total_beds) / 1e3
    ]

    # Add percentage columns
    df['Acute_Pct_of_Total'] = (df['Acute_Care'] / df['Total'] * 100).round(1)
    df['Behavioral_Pct_of_Total'] = (df['Behavioral_Health'] / df['Total'] * 100).round(1)

    return df

def create_facilities_portfolio_summary():
    """Create facilities portfolio summary from CSV data"""

    # Load facilities data
    acute_df = pd.read_csv('Assets/Automation/Claude/us_acute_care_facilities.csv')
    behavioral_us_df = pd.read_csv('Assets/Automation/Claude/UHS_BEHAVIORAL_COMPLETE_WITH_NPI.csv')
    behavioral_uk_df = pd.read_csv('Assets/Automation/Claude/uk_behavioral_facilities.csv')

    portfolio_data = []

    # Acute Care
    portfolio_data.append({
        'Segment': 'Acute Care',
        'Region': 'US',
        'Total_Facilities': len(acute_df),
        'Owned_Facilities': len(acute_df[acute_df['Property Ownership'] == 'Owned']),
        'Leased_Facilities': len(acute_df[acute_df['Property Ownership'] == 'Leased']),
        'Total_Beds': acute_df['Number of Beds'].sum(),
        'Owned_Beds': acute_df[acute_df['Property Ownership'] == 'Owned']['Number of Beds'].sum(),
        'Leased_Beds': acute_df[acute_df['Property Ownership'] == 'Leased']['Number of Beds'].sum(),
        'Avg_Beds_per_Facility': acute_df['Number of Beds'].mean()
    })

    # Behavioral US
    portfolio_data.append({
        'Segment': 'Behavioral Health',
        'Region': 'US',
        'Total_Facilities': len(behavioral_us_df),
        'Owned_Facilities': len(behavioral_us_df[behavioral_us_df['Ownership'] == 'OWNED']),
        'Leased_Facilities': len(behavioral_us_df[behavioral_us_df['Ownership'] == 'LEASED']),
        'Total_Beds': behavioral_us_df['Beds'].sum(),
        'Owned_Beds': behavioral_us_df[behavioral_us_df['Ownership'] == 'OWNED']['Beds'].sum(),
        'Leased_Beds': behavioral_us_df[behavioral_us_df['Ownership'] == 'LEASED']['Beds'].sum(),
        'Avg_Beds_per_Facility': behavioral_us_df['Beds'].mean()
    })

    # Behavioral UK
    portfolio_data.append({
        'Segment': 'Behavioral Health',
        'Region': 'UK',
        'Total_Facilities': len(behavioral_uk_df),
        'Owned_Facilities': len(behavioral_uk_df[behavioral_uk_df['Property Ownership'] == 'Owned']),
        'Leased_Facilities': len(behavioral_uk_df[behavioral_uk_df['Property Ownership'] == 'Leased']),
        'Total_Beds': behavioral_uk_df['Number of Beds'].sum(),
        'Owned_Beds': behavioral_uk_df[behavioral_uk_df['Property Ownership'] == 'Owned']['Number of Beds'].sum(),
        'Leased_Beds': behavioral_uk_df[behavioral_uk_df['Property Ownership'] == 'Leased']['Number of Beds'].sum(),
        'Avg_Beds_per_Facility': behavioral_uk_df['Number of Beds'].mean()
    })

    df = pd.DataFrame(portfolio_data)

    # Calculate percentages
    df['Owned_Pct'] = (df['Owned_Facilities'] / df['Total_Facilities'] * 100).round(1)
    df['Leased_Pct'] = (df['Leased_Facilities'] / df['Total_Facilities'] * 100).round(1)
    df['Owned_Beds_Pct'] = (df['Owned_Beds'] / df['Total_Beds'] * 100).round(1)

    return df

def create_balance_sheet_summary(data):
    """Create balance sheet summary"""

    bs_2024 = data['balance_sheet']['2024']
    bs_2023 = data['balance_sheet']['2023']

    balance_sheet_data = [
        {
            'Year': 2024,
            'Item': 'Total Assets',
            'Amount_M': bs_2024['assets']['total_assets'] / 1e6
        },
        {
            'Year': 2024,
            'Item': 'PP&E (net)',
            'Amount_M': bs_2024['assets']['non_current_assets']['property_plant_equipment']['net_ppe'] / 1e6
        },
        {
            'Year': 2024,
            'Item': 'Total Debt',
            'Amount_M': data['capital_structure']['debt']['total_debt_outstanding'] / 1e6
        },
        {
            'Year': 2024,
            'Item': 'Cash',
            'Amount_M': bs_2024['assets']['current_assets']['cash_and_equivalents'] / 1e6
        },
        {
            'Year': 2024,
            'Item': 'Net Debt',
            'Amount_M': data['capital_structure']['debt']['net_debt'] / 1e6
        },
        {
            'Year': 2024,
            'Item': 'Stockholders Equity',
            'Amount_M': bs_2024['liabilities_and_equity']['stockholders_equity']['total_stockholders_equity'] / 1e6
        },
        {
            'Year': 2023,
            'Item': 'Total Assets',
            'Amount_M': bs_2023['assets']['total_assets'] / 1e6
        },
        {
            'Year': 2023,
            'Item': 'PP&E (net)',
            'Amount_M': bs_2023['assets']['net_ppe'] / 1e6
        },
        {
            'Year': 2023,
            'Item': 'Total Debt',
            'Amount_M': (126_686_000 + bs_2023['liabilities_and_equity']['long_term_debt']) / 1e6
        },
        {
            'Year': 2023,
            'Item': 'Stockholders Equity',
            'Amount_M': bs_2023['liabilities_and_equity']['total_stockholders_equity'] / 1e6
        }
    ]

    df = pd.DataFrame(balance_sheet_data)
    df_pivot = df.pivot(index='Item', columns='Year', values='Amount_M')

    # Calculate YoY change
    if 2023 in df_pivot.columns and 2024 in df_pivot.columns:
        df_pivot['Change_M'] = df_pivot[2024] - df_pivot[2023]
        df_pivot['Change_Pct'] = ((df_pivot[2024] / df_pivot[2023]) - 1) * 100

    return df_pivot.reset_index()

def create_real_estate_breakdown(data):
    """Create real estate asset breakdown"""

    ppe = data['real_estate']['property_plant_equipment']

    re_data = [
        {'Category': 'Land', 'Gross_Value_M': ppe['land_value'] / 1e6, 'Accum_Depreciation_M': 0, 'Net_Value_M': ppe['land_value'] / 1e6},
        {'Category': 'Buildings', 'Gross_Value_M': ppe['buildings_value'] / 1e6, 'Accum_Depreciation_M': None, 'Net_Value_M': None},
        {'Category': 'Equipment', 'Gross_Value_M': ppe['equipment_value'] / 1e6, 'Accum_Depreciation_M': None, 'Net_Value_M': None},
        {'Category': 'Total PP&E', 'Gross_Value_M': ppe['total_ppe_gross'] / 1e6, 'Accum_Depreciation_M': -6071.058, 'Net_Value_M': ppe['total_ppe_net'] / 1e6}
    ]

    df = pd.DataFrame(re_data)

    # Calculate percentages
    df['Pct_of_Total_Gross'] = (df['Gross_Value_M'] / ppe['total_ppe_gross'] * 1e6 * 100).round(1)
    df['Pct_of_Total_Net'] = (df['Net_Value_M'] / ppe['total_ppe_net'] * 1e6 * 100).round(1)

    return df

def create_ownership_summary():
    """Create ownership summary by segment and type"""

    data_dict = {
        'Segment': ['Acute Care', 'Acute Care', 'Behavioral Health', 'Behavioral Health', 'Total', 'Total'],
        'Ownership': ['Owned', 'Leased', 'Owned', 'Leased', 'Owned', 'Leased'],
        'Facilities': [23, 5, 306, 18, 329, 23],
        'Beds': [5190, 1246, 22465, 1656, 27655, 2902]
    }

    df = pd.DataFrame(data_dict)

    # Calculate percentages
    total_facilities = df.groupby('Segment')['Facilities'].sum()
    total_beds = df.groupby('Segment')['Beds'].sum()

    df['Facilities_Pct_of_Segment'] = df.apply(
        lambda row: (row['Facilities'] / total_facilities[row['Segment']] * 100) if row['Segment'] != 'Total' else (row['Facilities'] / (329 + 23) * 100),
        axis=1
    ).round(1)

    df['Beds_Pct_of_Segment'] = df.apply(
        lambda row: (row['Beds'] / total_beds[row['Segment']] * 100) if row['Segment'] != 'Total' else (row['Beds'] / (27655 + 2902) * 100),
        axis=1
    ).round(1)

    return df

def main():
    print("="*80)
    print("PREPARING UHS DATA FOR GRAPHING & VISUALIZATION")
    print("="*80)
    print()

    data = load_data()

    # Create output directory
    import os
    os.makedirs('data/graphs', exist_ok=True)

    # 1. Segment Financials (3 years)
    print("1. Creating segment financials table (3 years)...")
    segment_financials = create_segment_financials_table(data)
    segment_financials.to_csv('data/graphs/segment_financials_3yr.csv', index=False)
    print(f"   ✓ Saved: data/graphs/segment_financials_3yr.csv ({len(segment_financials)} rows)")
    print(segment_financials.to_string(index=False))
    print()

    # 2. Consolidated Financials (3 years)
    print("2. Creating consolidated financials table (3 years)...")
    consolidated_financials = create_consolidated_financials_table(data)
    consolidated_financials.to_csv('data/graphs/consolidated_financials_3yr.csv', index=False)
    print(f"   ✓ Saved: data/graphs/consolidated_financials_3yr.csv ({len(consolidated_financials)} rows)")
    print(consolidated_financials.to_string(index=False))
    print()

    # 3. Segment Comparison 2024
    print("3. Creating segment comparison table (2024)...")
    segment_comparison = create_segment_comparison_2024(data)
    segment_comparison.to_csv('data/graphs/segment_comparison_2024.csv', index=False)
    print(f"   ✓ Saved: data/graphs/segment_comparison_2024.csv ({len(segment_comparison)} rows)")
    print(segment_comparison.to_string(index=False))
    print()

    # 4. Facilities Portfolio Summary
    print("4. Creating facilities portfolio summary...")
    portfolio_summary = create_facilities_portfolio_summary()
    portfolio_summary.to_csv('data/graphs/facilities_portfolio_summary.csv', index=False)
    print(f"   ✓ Saved: data/graphs/facilities_portfolio_summary.csv ({len(portfolio_summary)} rows)")
    print(portfolio_summary.to_string(index=False))
    print()

    # 5. Balance Sheet Summary
    print("5. Creating balance sheet summary...")
    balance_sheet = create_balance_sheet_summary(data)
    balance_sheet.to_csv('data/graphs/balance_sheet_summary.csv', index=False)
    print(f"   ✓ Saved: data/graphs/balance_sheet_summary.csv ({len(balance_sheet)} rows)")
    print(balance_sheet.to_string(index=False))
    print()

    # 6. Real Estate Breakdown
    print("6. Creating real estate breakdown...")
    real_estate = create_real_estate_breakdown(data)
    real_estate.to_csv('data/graphs/real_estate_breakdown.csv', index=False)
    print(f"   ✓ Saved: data/graphs/real_estate_breakdown.csv ({len(real_estate)} rows)")
    print(real_estate.to_string(index=False))
    print()

    # 7. Ownership Summary
    print("7. Creating ownership summary...")
    ownership = create_ownership_summary()
    ownership.to_csv('data/graphs/ownership_summary.csv', index=False)
    print(f"   ✓ Saved: data/graphs/ownership_summary.csv ({len(ownership)} rows)")
    print(ownership.to_string(index=False))
    print()

    print("="*80)
    print("DATA PREPARATION COMPLETE!")
    print("="*80)
    print()
    print("All data files ready for graphing in: data/graphs/")
    print()
    print("Files created:")
    print("  1. segment_financials_3yr.csv - Historical segment performance")
    print("  2. consolidated_financials_3yr.csv - Company-wide financials")
    print("  3. segment_comparison_2024.csv - Side-by-side segment metrics")
    print("  4. facilities_portfolio_summary.csv - Facility counts and ownership")
    print("  5. balance_sheet_summary.csv - Balance sheet items over time")
    print("  6. real_estate_breakdown.csv - PP&E composition")
    print("  7. ownership_summary.csv - Owned vs leased analysis")
    print()

if __name__ == "__main__":
    main()
