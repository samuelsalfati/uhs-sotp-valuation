#!/usr/bin/env python3
"""
COMPLETE NPI FETCHER FOR ALL UHS BEHAVIORAL FACILITIES
Gets NPIs from NPPES API and creates final master file with everything
"""

import requests
import csv
import time
import json
from datetime import datetime

# Complete Medicare ID database (60 facilities we found)
MEDICARE_DATABASE = {
    'Alliance Health Center': '250151',
    'Anchor Hospital': '114023',
    'Arbour Hospital': '224001',
    'Austin Oaks Hospital': '454097',
    'Behavioral Hospital of Bellaire': '674043',
    'BHC Alhambra Hospital': '054076',
    'Brentwood Hospital': '194049',
    'Cedar Springs Hospital': '064018',
    'Centennial Peaks Hospital': '064026',
    'Central Florida Behavioral Hospital': '104084',
    'Coral Shores Behavioral Health': '104085',
    'Cross Creek Hospital': '454085',
    'Cypress Creek Hospital': '454084',
    'Del Amo Behavioral Health System': '054076',
    'Desert Parkway Behavioral Healthcare Hospital': '294032',
    'Emerald Coast Behavioral Hospital': '104082',
    'Fairmount Behavioral Health System': '394024',
    'Forest View Hospital': '234041',
    'Friends Hospital': '394003',
    'Harbor Oaks Hospital': '234200',
    'Havenwyck Hospital': '234201',
    'Hickory Trail Hospital': '674055',
    'Kingwood Pines Hospital': '454104',
    'Laurel Ridge Treatment Center': '454055',
    'Mayhill Hospital': '674054',
    'Millwood Hospital': '454089',
    'The Meadows Psychiatric Center': '394055',
    'Mesilla Valley Hospital': '324002',
    'Newport News Behavioral Health Center': '494016',
    'North Star Hospital': '024001',
    'Old Vineyard Behavioral Health Services': '344038',
    'Palm Shores Behavioral Health Center': '104083',
    'Palmetto Lowcountry Behavioral Health': '424011',
    'The Pavilion Behavioral Health System': '144026',
    'Peachford Hospital': '114021',
    'Prairie St. Johns': '354002',
    'Quail Run Behavioral Health': '054084',
    'River Oaks Hospital': '194003',
    'River Park Hospital': '474005',
    'River Point Behavioral Health': '104086',
    'Rockford Center': '084002',
    'Rolling Hills Hospital': '054085',
    'Roxbury Treatment Center': '394030',
    'Salt Lake Behavioral Health': '464015',
    'San Marcos Treatment Center': '454092',
    'Sierra Vista Hospital': '054082',
    'Spring Mountain Treatment Center': '294037',
    'Spring Mountain Sahara': '294038',
    'Springwoods Behavioral Health': '014016',
    'St. Simons By-The-Sea': '114047',
    'SummitRidge Hospital': '114049',
    'Suncoast Behavioral Health Center': '104063',
    'Texas NeuroRehab Center': '454067',
    'Three Rivers Behavioral Health': '424012',
    'Turning Point Care Center': '114031',
    'University Behavioral Center': '104060',
    'University Behavioral Health of Denton': '454108',
    'Valle Vista Health System': '054083',
    'Valley Hospital': '034023',
    'Virginia Beach Psychiatric Center': '494015',
    'Wekiva Springs Center': '104022',
    'Wellstone Regional Hospital': '154051',
    'West Oaks Hospital': '454068',
    'Willow Springs Center': '294040',
    'Windmoor Healthcare of Clearwater': '104070',
}

def get_npi_from_nppes(facility_name, city, state):
    """
    Get NPI from NPPES API - This is the working version
    """
    # NPPES API endpoint
    url = "https://npiregistry.cms.hhs.gov/api"
    
    # Try different name variations for better matching
    name_variations = [
        facility_name,
        facility_name.replace("Hospital", "").strip(),
        facility_name.replace("Behavioral Health", "").strip(),
        facility_name.replace("Center", "").strip(),
        facility_name.split()[0] if facility_name.split() else facility_name  # First word only
    ]
    
    for name_variant in name_variations:
        params = {
            'version': '2.1',
            'organization_name': name_variant,
            'state': state,
            'city': city,
            'enumeration_type': 'NPI-2',  # Organization NPI
            'limit': 10
        }
        
        try:
            # Make the API request
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get('result_count', 0) > 0:
                    # Look through results for best match
                    for result in data.get('results', []):
                        basic = result.get('basic', {})
                        org_name = basic.get('organization_name', '').upper()
                        npi = result.get('number', '')
                        
                        # Check if this is likely our facility
                        if any(word in org_name for word in facility_name.upper().split()[:2]):
                            
                            # Get additional info
                            addresses = result.get('addresses', [])
                            phone = ''
                            full_address = ''
                            zip_code = ''
                            
                            if addresses:
                                addr = addresses[0]
                                phone = addr.get('telephone_number', '')
                                full_address = f"{addr.get('address_1', '')} {addr.get('address_2', '')}".strip()
                                zip_code = addr.get('postal_code', '')[:5] if addr.get('postal_code') else ''
                            
                            # Get taxonomy (specialty)
                            taxonomies = result.get('taxonomies', [])
                            specialty = ''
                            if taxonomies:
                                specialty = taxonomies[0].get('desc', '')
                            
                            return {
                                'NPI': npi,
                                'Legal_Name': basic.get('organization_name', ''),
                                'Phone': phone,
                                'Address': full_address,
                                'ZIP': zip_code,
                                'Specialty': specialty,
                                'Status': 'Found'
                            }
                    
            # Small delay between variations
            time.sleep(0.2)
            
        except Exception as e:
            print(f"    API Error: {str(e)[:50]}")
            continue
    
    # If no NPI found
    return {
        'NPI': '',
        'Legal_Name': '',
        'Phone': '',
        'Address': '',
        'ZIP': '',
        'Specialty': '',
        'Status': 'Not_Found'
    }

def parse_location(location_str):
    """Parse location string into city and state"""
    state_map = {
        'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR',
        'California': 'CA', 'Colorado': 'CO', 'Connecticut': 'CT', 'Delaware': 'DE',
        'Florida': 'FL', 'Georgia': 'GA', 'Hawaii': 'HI', 'Idaho': 'ID',
        'Illinois': 'IL', 'Indiana': 'IN', 'Iowa': 'IA', 'Kansas': 'KS',
        'Kentucky': 'KY', 'Louisiana': 'LA', 'Maine': 'ME', 'Maryland': 'MD',
        'Massachusetts': 'MA', 'Michigan': 'MI', 'Minnesota': 'MN', 'Mississippi': 'MS',
        'Missouri': 'MO', 'Montana': 'MT', 'Nebraska': 'NE', 'Nevada': 'NV',
        'New Hampshire': 'NH', 'New Jersey': 'NJ', 'New Mexico': 'NM', 'New York': 'NY',
        'North Carolina': 'NC', 'North Dakota': 'ND', 'Ohio': 'OH', 'Oklahoma': 'OK',
        'Oregon': 'OR', 'Pennsylvania': 'PA', 'Rhode Island': 'RI', 'South Carolina': 'SC',
        'South Dakota': 'SD', 'Tennessee': 'TN', 'Texas': 'TX', 'Utah': 'UT',
        'Vermont': 'VT', 'Virginia': 'VA', 'Washington': 'WA', 'West Virginia': 'WV',
        'Wisconsin': 'WI', 'Wyoming': 'WY', 'D.C.': 'DC'
    }
    
    for state_name, abbrev in state_map.items():
        if location_str.endswith(' ' + state_name):
            city = location_str[:-len(state_name)-1]
            return city, abbrev
    return location_str, ''

def process_all_facilities_with_npi():
    """
    Process all 177 facilities and get NPIs
    """
    print("\n" + "="*70)
    print("COMPLETE UHS BEHAVIORAL FACILITY DATA WITH NPI LOOKUP")
    print("="*70)
    
    # Load facilities
    all_facilities = []
    
    # Read Part 1
    try:
        with open('us_behavioral_facilities_part1.csv', 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                row['Part'] = '1'
                all_facilities.append(row)
        print(f"✓ Loaded Part 1: {len([f for f in all_facilities if f['Part'] == '1'])} facilities")
    except:
        print("❌ Could not find Part 1")
        return
    
    # Read Part 2
    try:
        with open('us_behavioral_facilities_part2.csv', 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                row['Part'] = '2'
                all_facilities.append(row)
        print(f"✓ Loaded Part 2: {len([f for f in all_facilities if f['Part'] == '2'])} facilities")
    except:
        print("❌ Could not find Part 2")
    
    print(f"\n📊 Total facilities to process: {len(all_facilities)}")
    print("\n🔍 Getting NPIs from NPPES (this will take 10-15 minutes)...")
    print("="*70)
    
    # Process each facility
    results = []
    stats = {
        'owned': 0, 'leased': 0,
        'npi_found': 0, 'npi_not_found': 0,
        'medicare_found': 0, 'medicare_not_found': 0
    }
    
    for i, facility in enumerate(all_facilities, 1):
        name = facility.get('Facility Name', '')
        location = facility.get('Location', '')
        beds = facility.get('Number of Beds', '')
        ownership = facility.get('Property Ownership', '')
        part = facility.get('Part', '')
        
        # Parse location
        city, state = parse_location(location)
        
        # Show progress
        print(f"\n[{i}/{len(all_facilities)}] {name}")
        print(f"     Location: {city}, {state}")
        
        # Get NPI
        npi_data = get_npi_from_nppes(name, city, state)
        
        if npi_data['Status'] == 'Found':
            print(f"     ✓ NPI: {npi_data['NPI']} ({npi_data['Legal_Name']})")
            stats['npi_found'] += 1
        else:
            print(f"     ⚠ NPI: Not found")
            stats['npi_not_found'] += 1
        
        # Get Medicare ID
        medicare_id = MEDICARE_DATABASE.get(name, '')
        if medicare_id:
            print(f"     ✓ Medicare ID: {medicare_id}")
            stats['medicare_found'] += 1
            ahd_url = f"https://www.ahd.com/free_profile/{medicare_id}/{name.replace(' ','-')}/{city.replace(' ','-')}/{state}/"
            has_ahd = 'Yes'
        else:
            stats['medicare_not_found'] += 1
            ahd_url = f"https://www.ahd.com/search.php?search={name.replace(' ','+')}+{state}"
            has_ahd = 'No'
        
        # Track ownership
        if ownership == 'Owned':
            stats['owned'] += 1
        elif ownership == 'Leased':
            stats['leased'] += 1
        
        # Create result row
        result = {
            'Facility_Name': name,
            'City': city,
            'State': state,
            'Beds': beds,
            'Ownership': ownership.upper() if ownership else '',
            'Part': part,
            'NPI': npi_data['NPI'],
            'NPI_Legal_Name': npi_data['Legal_Name'],
            'Phone': npi_data['Phone'],
            'Address': npi_data['Address'],
            'ZIP': npi_data['ZIP'],
            'Specialty': npi_data['Specialty'],
            'Medicare_ID': medicare_id,
            'Has_AHD_Data': has_ahd,
            'AHD_URL': ahd_url
        }
        results.append(result)
        
        # Rate limiting to be nice to NPPES API
        time.sleep(1)
        
        # Progress update every 10
        if i % 10 == 0:
            print(f"\n --- Progress: {i}/{len(all_facilities)} processed ({i*100//len(all_facilities)}%) ---")
            print(f"     NPIs found so far: {stats['npi_found']}")
    
    # Save complete results
    output_file = 'UHS_BEHAVIORAL_COMPLETE_WITH_NPI.csv'
    with open(output_file, 'w', newline='') as f:
        fieldnames = [
            'Facility_Name', 'City', 'State', 'Beds', 'Ownership', 'Part',
            'NPI', 'NPI_Legal_Name', 'Phone', 'Address', 'ZIP', 'Specialty',
            'Medicare_ID', 'Has_AHD_Data', 'AHD_URL'
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)
    
    # Create AHD extraction template
    ahd_facilities = [r for r in results if r['Medicare_ID']]
    
    extraction_file = 'FINAL_AHD_EXTRACTION_TEMPLATE.csv'
    with open(extraction_file, 'w', newline='') as f:
        extraction_fields = [
            'Facility_Name', 'City', 'State', 'Beds', 'Ownership',
            'NPI', 'Medicare_ID', 'AHD_URL',
            # Fields to extract from AHD
            'Occupancy_%', 'ALOS_Days', 'Annual_Discharges', 'Annual_Patient_Days',
            'Medicare_%', 'Medicaid_%', 'Commercial_%', 'Self_Pay_%',
            'Data_Date', 'Notes'
        ]
        writer = csv.DictWriter(f, fieldnames=extraction_fields)
        writer.writeheader()
        
        for facility in ahd_facilities:
            row = {
                'Facility_Name': facility['Facility_Name'],
                'City': facility['City'],
                'State': facility['State'],
                'Beds': facility['Beds'],
                'Ownership': facility['Ownership'],
                'NPI': facility['NPI'],
                'Medicare_ID': facility['Medicare_ID'],
                'AHD_URL': facility['AHD_URL'],
                'Data_Date': datetime.now().strftime('%Y-%m-%d'),
                'Notes': 'Extract from AHD'
            }
            writer.writerow(row)
    
    # Print summary
    print("\n" + "="*70)
    print("✅ COMPLETE! ALL DATA COLLECTED")
    print("="*70)
    
    print(f"\n📊 FINAL RESULTS:")
    print(f"Total Facilities: {len(all_facilities)}")
    
    print(f"\n🏢 OWNERSHIP:")
    print(f"  • OWNED: {stats['owned']} ({stats['owned']*100//len(all_facilities)}%)")
    print(f"  • LEASED: {stats['leased']} ({stats['leased']*100//len(all_facilities)}%)")
    
    print(f"\n🆔 IDENTIFIERS:")
    print(f"  • NPIs Found: {stats['npi_found']} ({stats['npi_found']*100//len(all_facilities)}%)")
    print(f"  • NPIs Not Found: {stats['npi_not_found']}")
    print(f"  • Medicare IDs: {stats['medicare_found']} ({stats['medicare_found']*100//len(all_facilities)}%)")
    
    print(f"\n📁 FILES CREATED:")
    print(f"\n1️⃣  {output_file}")
    print(f"    Complete database with NPIs, Medicare IDs, contact info")
    print(f"    THIS IS YOUR MASTER FILE WITH ALL DATA!")
    
    print(f"\n2️⃣  {extraction_file}")
    print(f"    {len(ahd_facilities)} facilities ready for AHD data extraction")
    
    print("\n" + "="*70)
    print("🎯 USE: UHS_BEHAVIORAL_COMPLETE_WITH_NPI.csv for your analysis")
    print("="*70)

def main():
    # Check if we should do quick mode or full NPI lookup
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == '--test':
        print("Test mode - processing first 5 facilities only")
        # You can add test logic here
    else:
        process_all_facilities_with_npi()

if __name__ == "__main__":
    main()
