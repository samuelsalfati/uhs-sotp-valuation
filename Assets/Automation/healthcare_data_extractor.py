#!/usr/bin/env python3
"""
Healthcare Facility Data Extractor
This script helps extract public data from various healthcare databases including:
- AHD (American Hospital Directory)
- CMS (Centers for Medicare & Medicaid Services)
- Hospital Compare
- NPPES (National Provider Identifier)
"""

import requests
import pandas as pd
import time
from bs4 import BeautifulSoup
import re
import json
from typing import Dict, List, Optional

class HealthcareFacilityDataExtractor:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
    def search_ahd_profile(self, facility_name: str, city: str, state: str) -> Dict:
        """
        Search for facility profile on AHD
        Note: AHD requires subscription for full data, but basic info is available
        """
        # Format the search URL
        facility_slug = facility_name.replace(" ", "-").replace("'", "")
        city_slug = city.replace(" ", "-")
        
        # Construct potential URLs
        potential_urls = [
            f"https://www.ahd.com/free_profile/[PROVIDER_ID]/{facility_slug}/{city_slug}/{state}/",
            f"https://www.ahd.com/search.php?search_query={facility_name} {city} {state}"
        ]
        
        facility_data = {
            'facility_name': facility_name,
            'city': city,
            'state': state,
            'ahd_url': potential_urls[0],
            'medicare_provider_id': None,
            'ownership_type': None,
            'bed_count': None,
            'patient_volume': None,
            'quality_rating': None
        }
        
        # Note: Actual scraping would require handling AHD's structure
        # This is a template for the extraction logic
        
        return facility_data
    
    def get_cms_data(self, facility_name: str, state: str) -> Dict:
        """
        Get CMS Provider data
        CMS provides public datasets that can be downloaded
        """
        cms_data = {
            'cms_certification_number': None,
            'ownership_type': None,
            'certification_date': None,
            'total_beds': None,
            'quality_measures': {}
        }
        
        # CMS Provider API endpoint (example)
        # https://data.cms.gov/provider-data/api
        
        return cms_data
    
    def get_nppes_data(self, facility_name: str, city: str, state: str) -> Dict:
        """
        Get National Provider Identifier (NPI) data
        NPPES provides free public access to NPI registry
        """
        # NPPES API endpoint
        base_url = "https://npiregistry.cms.hhs.gov/api"
        
        params = {
            'version': '2.1',
            'organization_name': facility_name,
            'city': city,
            'state': state,
            'limit': 5
        }
        
        nppes_data = {
            'npi': None,
            'organization_name': facility_name,
            'authorized_official': None,
            'telephone_number': None,
            'primary_taxonomy': None
        }
        
        try:
            response = self.session.get(base_url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get('result_count', 0) > 0:
                    result = data['results'][0]
                    nppes_data['npi'] = result.get('number')
                    
                    # Extract basic info
                    basic = result.get('basic', {})
                    nppes_data['organization_name'] = basic.get('organization_name')
                    nppes_data['authorized_official'] = f"{basic.get('authorized_official_first_name', '')} {basic.get('authorized_official_last_name', '')}"
                    nppes_data['telephone_number'] = basic.get('authorized_official_telephone_number')
                    
                    # Extract taxonomy
                    taxonomies = result.get('taxonomies', [])
                    if taxonomies:
                        nppes_data['primary_taxonomy'] = taxonomies[0].get('desc')
        except Exception as e:
            print(f"Error fetching NPPES data: {e}")
        
        return nppes_data
    
    def search_hospital_compare(self, facility_name: str, state: str) -> Dict:
        """
        Search CMS Hospital Compare data
        Public quality ratings and patient experience scores
        """
        compare_data = {
            'overall_rating': None,
            'patient_survey_rating': None,
            'readmission_rate': None,
            'mortality_rate': None,
            'safety_score': None,
            'patient_experience_scores': {}
        }
        
        # Hospital Compare API or downloadable datasets
        # https://data.medicare.gov/data/hospital-compare
        
        return compare_data
    
    def extract_all_facility_data(self, facilities_df: pd.DataFrame) -> pd.DataFrame:
        """
        Extract comprehensive data for all facilities in the dataframe
        """
        enhanced_data = []
        
        for index, row in facilities_df.iterrows():
            print(f"Processing {index + 1}/{len(facilities_df)}: {row['Facility Name']}")
            
            facility_data = {
                'Facility Name': row['Facility Name'],
                'City': row.get('City', ''),
                'State': row.get('State', ''),
                'Number of Beds': row.get('Number of Beds', ''),
                'Property Ownership': row.get('Property Ownership', '')
            }
            
            # Get NPPES data
            nppes_data = self.get_nppes_data(
                row['Facility Name'], 
                row.get('City', ''),
                row.get('State', '')
            )
            facility_data.update({
                'NPI': nppes_data['npi'],
                'Authorized Official': nppes_data['authorized_official'],
                'Phone': nppes_data['telephone_number'],
                'Primary Taxonomy': nppes_data['primary_taxonomy']
            })
            
            # Get other data sources
            # ahd_data = self.search_ahd_profile(...)
            # cms_data = self.get_cms_data(...)
            # compare_data = self.search_hospital_compare(...)
            
            enhanced_data.append(facility_data)
            
            # Be respectful of API rate limits
            time.sleep(0.5)
        
        return pd.DataFrame(enhanced_data)

def main():
    """
    Main function to demonstrate usage
    """
    # Example usage
    extractor = HealthcareFacilityDataExtractor()
    
    # Test with a single facility
    print("Testing NPPES lookup for Alliance Health Center...")
    nppes_data = extractor.get_nppes_data("Alliance Health Center", "Meridian", "Mississippi")
    print(json.dumps(nppes_data, indent=2))
    
    # Load your CSV file
    # df = pd.read_csv('us_behavioral_facilities.csv')
    # enhanced_df = extractor.extract_all_facility_data(df)
    # enhanced_df.to_csv('us_behavioral_facilities_enhanced.csv', index=False)

if __name__ == "__main__":
    main()

"""
Additional Public Data Sources:

1. AHD (American Hospital Directory)
   - Basic profile: Free
   - Detailed financials: Subscription required
   - URL pattern: https://www.ahd.com/free_profile/[PROVIDER_ID]/[FACILITY_NAME]/[CITY]/[STATE]/

2. CMS Provider Data
   - Download: https://data.cms.gov/provider-data/
   - API: https://data.cms.gov/provider-data/api
   - Includes quality measures, patient surveys, utilization data

3. NPPES NPI Registry
   - API: https://npiregistry.cms.hhs.gov/api
   - Free access, no authentication required
   - Provides NPI, taxonomy, contact information

4. Hospital Compare
   - Website: https://www.medicare.gov/hospitalcompare/
   - Data: https://data.medicare.gov/data/hospital-compare
   - Quality ratings, patient experience, clinical outcomes

5. SAMHSA Treatment Locator (for behavioral health)
   - API: https://findtreatment.samhsa.gov/locator
   - Provides service types, payment options, special programs

6. State Health Department Databases
   - Each state maintains licensure databases
   - Usually searchable online
   - Provides license status, violations, surveys

7. Joint Commission Quality Check
   - Website: https://www.qualitycheck.org/
   - Accreditation status and quality reports

8. Leapfrog Hospital Safety Grade
   - Website: https://www.hospitalsafetygrade.org/
   - API available for safety scores

9. ProPublica Nonprofit Explorer (for nonprofit hospitals)
   - Website: https://projects.propublica.org/nonprofits/
   - IRS 990 forms with financial data

10. AHRQ HCUP (Healthcare Cost and Utilization Project)
    - Website: https://www.hcup-us.ahrq.gov/
    - Hospital utilization statistics
"""
