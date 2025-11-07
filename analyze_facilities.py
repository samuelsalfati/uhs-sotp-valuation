#!/usr/bin/env python3
"""
UHS Facilities Portfolio Analysis
Analyzes all behavioral and acute care facilities to calculate key metrics
"""

import pandas as pd
import numpy as np

print("="*80)
print("UHS FACILITIES PORTFOLIO ANALYSIS")
print("="*80)
print()

# ==============================================================================
# 1. ACUTE CARE FACILITIES ANALYSIS
# ==============================================================================

print("1. ACUTE CARE HOSPITALS ANALYSIS")
print("-" * 80)

# Load acute care data
acute_df = pd.read_csv('Assets/Automation/Claude/us_acute_care_facilities.csv')

# Clean up location field to extract state
acute_df['State'] = acute_df['Location'].str.extract(r'([A-Z][a-z]+\s?[A-Z]?[a-z]*|D\.C\.)$')

# Calculate metrics
total_acute_facilities = len(acute_df)
total_acute_beds = acute_df['Number of Beds'].sum()
owned_acute = acute_df[acute_df['Property Ownership'] == 'Owned']
leased_acute = acute_df[acute_df['Property Ownership'] == 'Leased']

owned_acute_facilities = len(owned_acute)
leased_acute_facilities = len(leased_acute)
owned_acute_beds = owned_acute['Number of Beds'].sum()
leased_acute_beds = leased_acute['Number of Beds'].sum()

avg_beds_per_facility = total_acute_beds / total_acute_facilities

print(f"Total Acute Care Facilities: {total_acute_facilities}")
print(f"  - Owned: {owned_acute_facilities} ({owned_acute_facilities/total_acute_facilities*100:.1f}%)")
print(f"  - Leased: {leased_acute_facilities} ({leased_acute_facilities/total_acute_facilities*100:.1f}%)")
print()
print(f"Total Licensed Beds: {total_acute_beds:,}")
print(f"  - Owned: {owned_acute_beds:,} ({owned_acute_beds/total_acute_beds*100:.1f}%)")
print(f"  - Leased: {leased_acute_beds:,} ({leased_acute_beds/total_acute_beds*100:.1f}%)")
print()
print(f"Average Facility Size: {avg_beds_per_facility:.0f} beds")
print()

# Size distribution
print("Facility Size Distribution:")
large = len(acute_df[acute_df['Number of Beds'] >= 300])
medium = len(acute_df[(acute_df['Number of Beds'] >= 150) & (acute_df['Number of Beds'] < 300)])
small = len(acute_df[acute_df['Number of Beds'] < 150])

print(f"  - Large (300+ beds): {large} facilities")
print(f"  - Medium (150-299 beds): {medium} facilities")
print(f"  - Small (<150 beds): {small} facilities")
print()

# Geographic distribution
print("Geographic Distribution (Top 10 States by Bed Count):")
state_beds = acute_df.groupby('State')['Number of Beds'].agg(['count', 'sum'])
state_beds.columns = ['Facilities', 'Total Beds']
state_beds = state_beds.sort_values('Total Beds', ascending=False)
print(state_beds.head(10).to_string())
print()

# Top 5 largest facilities
print("Top 5 Largest Acute Care Facilities:")
top5 = acute_df.nlargest(5, 'Number of Beds')[['Facility Name', 'Location', 'Number of Beds', 'Property Ownership']]
print(top5.to_string(index=False))
print()

# ==============================================================================
# 2. BEHAVIORAL HEALTH FACILITIES ANALYSIS
# ==============================================================================

print("\n" + "="*80)
print("2. BEHAVIORAL HEALTH FACILITIES ANALYSIS")
print("-" * 80)

# Load behavioral health data
behavioral_us_df = pd.read_csv('Assets/Automation/Claude/UHS_BEHAVIORAL_COMPLETE_WITH_NPI.csv')
behavioral_ahd_df = pd.read_csv('Assets/Automation/Claude/FINAL_AHD_EXTRACTION_TEMPLATE.csv')
behavioral_uk_df = pd.read_csv('Assets/Automation/Claude/uk_behavioral_facilities.csv')

# US Behavioral Analysis
print("\nUS BEHAVIORAL FACILITIES:")
total_us_behavioral = len(behavioral_us_df)
owned_us_behavioral = len(behavioral_us_df[behavioral_us_df['Ownership'] == 'OWNED'])
leased_us_behavioral = len(behavioral_us_df[behavioral_us_df['Ownership'] == 'LEASED'])

total_us_behavioral_beds = behavioral_us_df['Beds'].sum()
owned_us_behavioral_beds = behavioral_us_df[behavioral_us_df['Ownership'] == 'OWNED']['Beds'].sum()
leased_us_behavioral_beds = behavioral_us_df[behavioral_us_df['Ownership'] == 'LEASED']['Beds'].sum()

print(f"Total US Facilities: {total_us_behavioral}")
print(f"  - Owned: {owned_us_behavioral} ({owned_us_behavioral/total_us_behavioral*100:.1f}%)")
print(f"  - Leased: {leased_us_behavioral} ({leased_us_behavioral/total_us_behavioral*100:.1f}%)")
print()
print(f"Total US Beds: {total_us_behavioral_beds:,}")
print(f"  - Owned: {owned_us_behavioral_beds:,} ({owned_us_behavioral_beds/total_us_behavioral_beds*100:.1f}%)")
print(f"  - Leased: {leased_us_behavioral_beds:,} ({leased_us_behavioral_beds/total_us_behavioral_beds*100:.1f}%)")
print()
print(f"Average US Facility Size: {total_us_behavioral_beds/total_us_behavioral:.0f} beds")
print()

# UK Behavioral Analysis
print("UK BEHAVIORAL FACILITIES:")
total_uk_behavioral = len(behavioral_uk_df)
owned_uk_behavioral = len(behavioral_uk_df[behavioral_uk_df['Property Ownership'] == 'Owned'])
leased_uk_behavioral = len(behavioral_uk_df[behavioral_uk_df['Property Ownership'] == 'Leased'])

total_uk_behavioral_beds = behavioral_uk_df['Number of Beds'].sum()
owned_uk_behavioral_beds = behavioral_uk_df[behavioral_uk_df['Property Ownership'] == 'Owned']['Number of Beds'].sum()
leased_uk_behavioral_beds = behavioral_uk_df[behavioral_uk_df['Property Ownership'] == 'Leased']['Number of Beds'].sum()

print(f"Total UK Facilities: {total_uk_behavioral}")
print(f"  - Owned: {owned_uk_behavioral} ({owned_uk_behavioral/total_uk_behavioral*100:.1f}%)")
print(f"  - Leased: {leased_uk_behavioral} ({leased_uk_behavioral/total_uk_behavioral*100:.1f}%)")
print()
print(f"Total UK Beds: {total_uk_behavioral_beds:,}")
print(f"  - Owned: {owned_uk_behavioral_beds:,} ({owned_uk_behavioral_beds/total_uk_behavioral_beds*100:.1f}%)")
print(f"  - Leased: {leased_uk_behavioral_beds:,} ({leased_uk_behavioral_beds/total_uk_behavioral_beds*100:.1f}%)")
print()
print(f"Average UK Facility Size: {total_uk_behavioral_beds/total_uk_behavioral:.0f} beds")
print()

# Total Behavioral Summary
total_behavioral_facilities = total_us_behavioral + total_uk_behavioral
total_behavioral_beds = total_us_behavioral_beds + total_uk_behavioral_beds
total_owned_behavioral = owned_us_behavioral + owned_uk_behavioral
total_leased_behavioral = leased_us_behavioral + leased_uk_behavioral
total_owned_behavioral_beds = owned_us_behavioral_beds + owned_uk_behavioral_beds
total_leased_behavioral_beds = leased_us_behavioral_beds + leased_uk_behavioral_beds

print("TOTAL BEHAVIORAL HEALTH PORTFOLIO:")
print(f"Total Facilities: {total_behavioral_facilities}")
print(f"  - Owned: {total_owned_behavioral} ({total_owned_behavioral/total_behavioral_facilities*100:.1f}%)")
print(f"  - Leased: {total_leased_behavioral} ({total_leased_behavioral/total_behavioral_facilities*100:.1f}%)")
print()
print(f"Total Beds: {total_behavioral_beds:,}")
print(f"  - Owned: {total_owned_behavioral_beds:,} ({total_owned_behavioral_beds/total_behavioral_beds*100:.1f}%)")
print(f"  - Leased: {total_leased_behavioral_beds:,} ({total_leased_behavioral_beds/total_leased_behavioral_beds*100:.1f}%)")
print()

# ==============================================================================
# 3. BEHAVIORAL HEALTH REVENUE ANALYSIS (59 facilities with data)
# ==============================================================================

print("\n" + "="*80)
print("3. BEHAVIORAL HEALTH REVENUE ANALYSIS (Sample Data)")
print("-" * 80)

# Clean revenue data
behavioral_ahd_df['Patient_Revenue_Clean'] = (
    behavioral_ahd_df['Patient Reve']
    .str.replace('$', '')
    .str.replace(',', '')
    .str.strip()
)

# Filter out rows with 'x' or empty revenue
revenue_df = behavioral_ahd_df[
    behavioral_ahd_df['Patient_Revenue_Clean'].notna() &
    (behavioral_ahd_df['Patient_Revenue_Clean'] != 'x') &
    (behavioral_ahd_df['Patient_Revenue_Clean'] != '')
].copy()

revenue_df['Patient_Revenue_Clean'] = pd.to_numeric(revenue_df['Patient_Revenue_Clean'], errors='coerce')
revenue_df = revenue_df.dropna(subset=['Patient_Revenue_Clean'])

facilities_with_revenue = len(revenue_df)
total_revenue_sample = revenue_df['Patient_Revenue_Clean'].sum()
beds_with_revenue = revenue_df['Beds'].sum()

print(f"Facilities with Revenue Data: {facilities_with_revenue}")
print(f"Total Beds (sample): {beds_with_revenue:,}")
print(f"Total Patient Revenue (sample): ${total_revenue_sample:,.0f}")
print()

# Calculate key metrics
avg_revenue_per_facility = total_revenue_sample / facilities_with_revenue
avg_revenue_per_bed = total_revenue_sample / beds_with_revenue
avg_beds_per_facility_sample = beds_with_revenue / facilities_with_revenue

print(f"Average Revenue per Facility: ${avg_revenue_per_facility:,.0f}")
print(f"Average Revenue per Bed: ${avg_revenue_per_bed:,.0f}")
print(f"Average Beds per Facility (sample): {avg_beds_per_facility_sample:.0f}")
print()

# Clean patient days and discharges
revenue_df['Annual_Patient_Days_Clean'] = (
    revenue_df[' Annual_Patient_Days ']
    .astype(str)
    .str.replace(',', '')
    .str.strip()
)
revenue_df['Annual_Discharges_Clean'] = (
    revenue_df[' Annual_Discharges ']
    .astype(str)
    .str.replace(',', '')
    .str.strip()
)

revenue_df['Annual_Patient_Days_Clean'] = pd.to_numeric(revenue_df['Annual_Patient_Days_Clean'], errors='coerce')
revenue_df['Annual_Discharges_Clean'] = pd.to_numeric(revenue_df['Annual_Discharges_Clean'], errors='coerce')

# Calculate metrics for facilities with complete data
complete_df = revenue_df.dropna(subset=['Annual_Patient_Days_Clean', 'Annual_Discharges_Clean'])

if len(complete_df) > 0:
    complete_df['Revenue_per_Patient_Day'] = complete_df['Patient_Revenue_Clean'] / complete_df['Annual_Patient_Days_Clean']
    complete_df['Revenue_per_Discharge'] = complete_df['Patient_Revenue_Clean'] / complete_df['Annual_Discharges_Clean']
    complete_df['ALOS'] = complete_df['Annual_Patient_Days_Clean'] / complete_df['Annual_Discharges_Clean']
    complete_df['Occupancy_Est'] = complete_df['Annual_Patient_Days_Clean'] / (complete_df['Beds'] * 365)

    print(f"Facilities with Complete Data (Revenue + Patient Days + Discharges): {len(complete_df)}")
    print()
    print("KEY OPERATIONAL METRICS (Averages):")
    print(f"  Revenue per Patient Day: ${complete_df['Revenue_per_Patient_Day'].median():.0f}")
    print(f"  Revenue per Discharge: ${complete_df['Revenue_per_Discharge'].median():.0f}")
    print(f"  Average Length of Stay (ALOS): {complete_df['ALOS'].median():.1f} days")
    print(f"  Estimated Occupancy Rate: {complete_df['Occupancy_Est'].median()*100:.1f}%")
    print()

# ==============================================================================
# 4. EXTRAPOLATION TO FULL PORTFOLIO
# ==============================================================================

print("\n" + "="*80)
print("4. EXTRAPOLATION TO FULL BEHAVIORAL PORTFOLIO")
print("-" * 80)

# Use average revenue per bed from sample to estimate total behavioral revenue
estimated_total_behavioral_revenue = avg_revenue_per_bed * total_behavioral_beds

print(f"Sample Data:")
print(f"  - {facilities_with_revenue} facilities with revenue data")
print(f"  - {beds_with_revenue:,} beds")
print(f"  - ${total_revenue_sample:,.0f} total revenue")
print(f"  - ${avg_revenue_per_bed:,.0f} average revenue per bed")
print()
print(f"Extrapolation to Full Portfolio:")
print(f"  - Total Behavioral Beds: {total_behavioral_beds:,}")
print(f"  - Estimated Total Behavioral Revenue: ${estimated_total_behavioral_revenue:,.0f}")
print(f"  - OR ${estimated_total_behavioral_revenue/1e9:.2f} Billion")
print()
print("NOTE: This should be compared to 10-K segment revenue for validation")
print()

# ==============================================================================
# 5. CONSOLIDATED SUMMARY
# ==============================================================================

print("\n" + "="*80)
print("5. CONSOLIDATED UHS PORTFOLIO SUMMARY")
print("="*80)
print()

total_facilities = total_acute_facilities + total_behavioral_facilities
total_beds = total_acute_beds + total_behavioral_beds
total_owned_facilities = owned_acute_facilities + total_owned_behavioral
total_leased_facilities = leased_acute_facilities + total_leased_behavioral
total_owned_beds = owned_acute_beds + total_owned_behavioral_beds
total_leased_beds = leased_acute_beds + total_leased_behavioral_beds

print(f"TOTAL UHS PORTFOLIO:")
print(f"  Total Facilities: {total_facilities}")
print(f"    - Acute Care: {total_acute_facilities} ({total_acute_facilities/total_facilities*100:.1f}%)")
print(f"    - Behavioral Health: {total_behavioral_facilities} ({total_behavioral_facilities/total_facilities*100:.1f}%)")
print()
print(f"  Total Licensed Beds: {total_beds:,}")
print(f"    - Acute Care: {total_acute_beds:,} ({total_acute_beds/total_beds*100:.1f}%)")
print(f"    - Behavioral Health: {total_behavioral_beds:,} ({total_behavioral_beds/total_beds*100:.1f}%)")
print()
print(f"  Ownership Structure:")
print(f"    - Owned: {total_owned_facilities} facilities ({total_owned_facilities/total_facilities*100:.1f}%), {total_owned_beds:,} beds ({total_owned_beds/total_beds*100:.1f}%)")
print(f"    - Leased: {total_leased_facilities} facilities ({total_leased_facilities/total_facilities*100:.1f}%), {total_leased_beds:,} beds ({total_leased_beds/total_beds*100:.1f}%)")
print()

print(f"REAL ESTATE BREAKDOWN:")
print(f"  Acute Care Owned: {owned_acute_facilities} facilities, {owned_acute_beds:,} beds")
print(f"  Acute Care Leased: {leased_acute_facilities} facilities, {leased_acute_beds:,} beds")
print(f"  Behavioral Owned: {total_owned_behavioral} facilities, {total_owned_behavioral_beds:,} beds")
print(f"  Behavioral Leased: {total_leased_behavioral} facilities, {total_leased_behavioral_beds:,} beds")
print()

# ==============================================================================
# 6. SAVE RESULTS TO CSV
# ==============================================================================

print("="*80)
print("Saving analysis results to CSV...")

# Create summary dataframe
summary_data = {
    'Metric': [
        'Total Facilities',
        'Acute Care Facilities',
        'Behavioral Health Facilities',
        'Total Licensed Beds',
        'Acute Care Beds',
        'Behavioral Health Beds',
        'Owned Facilities',
        'Leased Facilities',
        'Owned Beds',
        'Leased Beds',
        'Acute Care Owned Facilities',
        'Acute Care Leased Facilities',
        'Acute Care Owned Beds',
        'Acute Care Leased Beds',
        'Behavioral Owned Facilities',
        'Behavioral Leased Facilities',
        'Behavioral Owned Beds',
        'Behavioral Leased Beds',
        'Est. Behavioral Revenue (from sample)',
        'Avg Revenue per Bed (Behavioral)',
    ],
    'Value': [
        total_facilities,
        total_acute_facilities,
        total_behavioral_facilities,
        total_beds,
        total_acute_beds,
        total_behavioral_beds,
        total_owned_facilities,
        total_leased_facilities,
        total_owned_beds,
        total_leased_beds,
        owned_acute_facilities,
        leased_acute_facilities,
        owned_acute_beds,
        leased_acute_beds,
        total_owned_behavioral,
        total_leased_behavioral,
        total_owned_behavioral_beds,
        total_leased_behavioral_beds,
        f"${estimated_total_behavioral_revenue:,.0f}",
        f"${avg_revenue_per_bed:,.0f}",
    ]
}

summary_df = pd.DataFrame(summary_data)
summary_df.to_csv('data/UHS_Portfolio_Summary.csv', index=False)
print("✓ Saved: data/UHS_Portfolio_Summary.csv")

print()
print("="*80)
print("ANALYSIS COMPLETE")
print("="*80)
