# Healthcare Facility Public Data Collection Guide

## Overview
This guide provides detailed instructions for collecting public data on healthcare facilities, specifically for UHS behavioral health and acute care facilities.

## Primary Data Sources

### 1. American Hospital Directory (AHD)
**Website:** https://www.ahd.com
**Access:** Free basic profiles, paid subscriptions for detailed data

**How to Search:**
1. Go to https://www.ahd.com
2. Use the search box to enter facility name and state
3. Click on the facility to view free profile
4. Note the Medicare Provider Number (6-digit code like 250151)

**Available Data (Free):**
- Medicare Provider Number
- Bed count
- Ownership type
- Basic utilization statistics
- Location and contact info

**URL Pattern:** 
`https://www.ahd.com/free_profile/[MEDICARE_ID]/[FACILITY-NAME]/[CITY]/[STATE]/`

Example: https://www.ahd.com/free_profile/250151/Alliance-Health-Center/Meridian/Mississippi/

### 2. CMS Provider Data Catalog
**Website:** https://data.cms.gov/provider-data/
**Access:** Completely free, downloadable datasets

**Key Datasets:**
- Hospital General Information
- Hospital Compare
- Provider of Services File
- Behavioral Health Treatment Services Locator

**How to Access:**
1. Visit https://data.cms.gov/provider-data/dataset/xubh-q36u (Hospital General Info)
2. Download CSV or use API
3. Match facilities by name and state
4. Provider ID cross-references with AHD

### 3. NPPES NPI Registry
**Website:** https://nppes.cms.hhs.gov
**API:** https://npiregistry.cms.hhs.gov
**Access:** Free, no registration required

**How to Search:**
1. Go to https://nppes.cms.hhs.gov/NPPES/
2. Select "Organization" search
3. Enter facility name and state
4. Get NPI number (10-digit identifier)

**API Example:**
```
GET https://npiregistry.cms.hhs.gov/api/?version=2.1&organization_name=Alliance+Health+Center&state=MS
```

### 4. SAMHSA Treatment Locator
**Website:** https://findtreatment.samhsa.gov
**Access:** Free, specifically for behavioral health facilities

**Available Data:**
- Services offered
- Payment options accepted
- Special programs
- Age groups served
- Languages spoken

### 5. Joint Commission Quality Check
**Website:** https://www.qualitycheck.org
**Access:** Free, registration optional

**How to Search:**
1. Visit https://www.qualitycheck.org/search/
2. Enter facility name or location
3. View accreditation status
4. Download quality reports

### 6. State Licensing Databases

Each state maintains its own healthcare facility licensing database:

**Examples:**
- **Texas:** https://www.dshs.texas.gov/facilities/find-a-facility
- **California:** https://www.cdph.ca.gov/Programs/CHCQ
- **Florida:** https://www.floridahealthfinder.gov
- **Mississippi:** https://msdh.ms.gov/msdhsite/index.cfm/30,0,83,html

### 7. Medicare Hospital Compare
**Website:** https://www.medicare.gov/care-compare/
**Access:** Free

**Available Data:**
- Overall star rating
- Patient survey scores
- Timely & effective care metrics
- Readmission rates
- Safety measures

## Data Collection Workflow

### Step 1: Basic Information
1. Start with your facility list (name, city, state)
2. Standardize naming (remove "Inc.", "LLC", etc.)
3. Create consistent state abbreviations

### Step 2: Identify Medicare Provider Numbers
1. Search each facility on AHD
2. Record the 6-digit Medicare Provider ID
3. If not found, try CMS Provider dataset

### Step 3: Get NPI Numbers
1. Use NPPES registry for each facility
2. Record 10-digit NPI
3. Note the taxonomy code (specialty designation)

### Step 4: Quality & Accreditation Data
1. Check Joint Commission Quality Check
2. Look up Medicare Hospital Compare ratings
3. Record accreditation status and dates

### Step 5: State-Specific Information
1. Visit state health department website
2. Search facility license database
3. Record license number, status, survey dates

### Step 6: Financial & Operational Data
1. For detailed financials, AHD subscription may be needed
2. Check if facility files cost reports (public for nonprofits)
3. IRS Form 990 for nonprofit facilities (ProPublica)

## Automation Tips

### Using Python
```python
import requests
import pandas as pd

# NPPES API Example
def get_npi(org_name, state):
    url = "https://npiregistry.cms.hhs.gov/api"
    params = {
        'version': '2.1',
        'organization_name': org_name,
        'state': state,
        'limit': 1
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data['result_count'] > 0:
            return data['results'][0]['number']
    return None
```

### Using Excel/Google Sheets
1. Use IMPORTDATA or IMPORTXML functions for web scraping
2. Create lookup tables for Medicare IDs
3. Use VLOOKUP to match data across sources

## Data Fields to Collect

### Essential Fields
- [ ] Facility Name (official)
- [ ] Street Address
- [ ] City, State, ZIP
- [ ] County
- [ ] Phone Number
- [ ] Website
- [ ] Medicare Provider ID
- [ ] NPI Number
- [ ] Bed Count (licensed vs operational)
- [ ] Ownership Type (for-profit, nonprofit, government)
- [ ] Parent Company

### Quality Indicators
- [ ] Joint Commission Accreditation (Y/N, date)
- [ ] Medicare Star Rating (1-5)
- [ ] Patient Experience Scores
- [ ] Safety Grade (Leapfrog)
- [ ] Recent Survey Deficiencies
- [ ] Readmission Rates

### Operational Data
- [ ] Services Offered
- [ ] Patient Population (age groups)
- [ ] Specialties/Programs
- [ ] Average Length of Stay
- [ ] Occupancy Rate
- [ ] Annual Admissions
- [ ] Payer Mix (% Medicare, Medicaid, Commercial)

### Staffing Information
- [ ] Total Employees
- [ ] Clinical Staff Count
- [ ] Medical Director Name
- [ ] CEO/Administrator Name
- [ ] Nurse-to-Patient Ratio

## Bulk Data Download Options

### CMS Datasets
1. **Provider of Services File**
   - Download: https://data.cms.gov/provider-characteristics/hospitals-and-other-facilities/provider-of-services-file-hospital-non-hospital-facilities
   - Contains all Medicare-certified facilities
   - Updated quarterly

2. **Hospital Compare Database**
   - Download: https://data.medicare.gov/data/hospital-compare
   - Comprehensive quality metrics
   - Updated monthly

3. **NPPES Data Dissemination**
   - Download: https://download.cms.gov/nppes/NPI_Files.html
   - Full NPI database (large file)
   - Updated weekly

## Important Notes

1. **Data Currency:** Healthcare facility data changes frequently. Note collection dates.

2. **Name Variations:** Facilities may be listed under different names:
   - Legal name vs. DBA (Doing Business As)
   - Parent company name vs. facility name
   - Historical names

3. **Multiple Identifiers:** Same facility may have:
   - Multiple NPIs (organization and individual providers)
   - Different IDs for different programs
   - State-specific license numbers

4. **Privacy Considerations:**
   - Patient data is protected by HIPAA
   - Only use publicly available information
   - Respect website terms of service

5. **Data Quality:**
   - Cross-reference multiple sources
   - Verify current operational status
   - Note discrepancies between sources

## Sample API Calls

### NPPES NPI Lookup
```bash
curl "https://npiregistry.cms.hhs.gov/api/?version=2.1&organization_name=Alliance%20Health%20Center&state=MS"
```

### CMS Provider API
```bash
curl "https://data.cms.gov/provider-data/api/1/datastore/sql?query=SELECT%20*%20FROM%20hospital_general_info%20WHERE%20state='MS'"
```

## Excel Formulas for Data Processing

### Clean Facility Names
```excel
=TRIM(SUBSTITUTE(SUBSTITUTE(A2,"Inc.",""),"LLC",""))
```

### Create AHD URL
```excel
=CONCATENATE("https://www.ahd.com/free_profile/",B2,"/",SUBSTITUTE(A2," ","-"),"/",C2,"/",D2,"/")
```

### Lookup Medicare ID
```excel
=VLOOKUP(A2,MedicareProviders!A:B,2,FALSE)
```

## Contact Information for Data Issues

- **CMS Help Desk:** 1-410-786-2580
- **NPPES Customer Service:** 1-800-465-3203
- **Joint Commission:** 630-792-5000
- **SAMHSA:** 1-877-726-4727

## Update Schedule

- **Weekly:** NPPES
- **Monthly:** Hospital Compare, CMS quality measures
- **Quarterly:** Provider of Services file, Cost reports
- **Annual:** Joint Commission accreditation, State licenses

This guide should enable systematic collection of public healthcare facility data. Start with automated sources (APIs, bulk downloads) before manual searches.
