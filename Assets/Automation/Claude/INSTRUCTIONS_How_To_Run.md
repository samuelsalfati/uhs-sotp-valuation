# STEP-BY-STEP INSTRUCTIONS: How to Extract Healthcare Facility Data

## What This Does
The Python script automatically looks up public information for each healthcare facility in your CSV file and adds:
- NPI (National Provider Identifier) number
- Medicare Provider ID  
- Phone, fax, address
- Authorized official name
- Quality ratings
- Direct links to AHD profiles

## STEP 1: Set Up Your Computer

### Option A: If you have Python installed
1. Open Terminal (Mac) or Command Prompt (Windows)
2. Install required packages:
```bash
pip install requests pandas beautifulsoup4
```

### Option B: If you don't have Python
1. Go to https://www.python.org/downloads/
2. Download and install Python 3.8 or newer
3. During installation, check "Add Python to PATH"
4. Then follow Option A above

## STEP 2: Prepare Your Files

1. **Download the script**
   - Save `demo_facility_lookup.py` to your Desktop
   
2. **Prepare your CSV file**
   - Make sure it has these column headers:
     - Facility Name
     - City  
     - State
     - Beds
     - Ownership
   - Save it as `facilities.csv` on your Desktop

## STEP 3: Run the Script

### On Windows:
1. Open Command Prompt
2. Type these commands:
```cmd
cd Desktop
python demo_facility_lookup.py
```

### On Mac:
1. Open Terminal
2. Type these commands:
```bash
cd ~/Desktop
python3 demo_facility_lookup.py
```

## STEP 4: Check Your Results

The script creates a new file called `enhanced_output.csv` with all the additional data added.

## What the Output Looks Like

Your original CSV:
```
Facility Name,City,State,Beds,Ownership
Alliance Health Center,Meridian,MS,214,Owned
```

Becomes this enhanced CSV:
```
Facility Name,City,State,Beds,Ownership,NPI,Medicare_ID,Phone,Address,ZIP,Quality_Rating,AHD_URL
Alliance Health Center,Meridian,MS,214,Owned,1164425633,250151,(601) 483-6211,5900 Highway 39 North,39301,4/5,https://www.ahd.com/free_profile/250151/...
```

## For Real API Access (Not Demo)

To get REAL data instead of demo data, you need to modify the script to use actual APIs:

### 1. NPPES API (FREE - Works immediately)
```python
import requests

def get_real_npi(facility_name, city, state):
    url = "https://npiregistry.cms.hhs.gov/api"
    params = {
        'version': '2.1',
        'organization_name': facility_name,
        'city': city,
        'state': state
    }
    response = requests.get(url, params=params)
    data = response.json()
    
    if data['result_count'] > 0:
        return data['results'][0]['number']
    return None
```

### 2. Run on Your Full CSV
```bash
python3 facility_lookup.py your_facilities.csv enhanced_facilities.csv
```

## Troubleshooting

### "Python not found" error
- Make sure Python is installed
- On Windows, try `py` instead of `python`
- On Mac, try `python3` instead of `python`

### "Module not found" error
- Install the missing module: `pip install [module_name]`

### API returns no results
- Check facility name spelling
- Try variations (e.g., "Center" vs "Centre")
- Some facilities may not be registered

### Rate limiting errors
- Add delays between requests: `time.sleep(1)`
- Process in smaller batches

## Processing Large Files

For files with hundreds of facilities:

1. **Process in batches**
```python
# Process 50 at a time
batch_size = 50
for i in range(0, len(facilities), batch_size):
    batch = facilities[i:i+batch_size]
    # Process batch
    time.sleep(5)  # Pause between batches
```

2. **Save progress periodically**
```python
# Save every 10 facilities
if i % 10 == 0:
    save_progress(enhanced_data)
```

## Example: Processing Your UHS Facilities

1. Take your CSV with 181 behavioral facilities
2. Run: `python3 facility_lookup.py behavioral_facilities.csv behavioral_enhanced.csv`
3. Wait about 15-20 minutes (with delays for rate limits)
4. Get enhanced CSV with all public data added

## Manual Alternative

If the script doesn't work, you can manually look up each facility:

1. **NPPES**: https://nppes.cms.hhs.gov
   - Search by organization name
   - Copy NPI number

2. **AHD**: https://www.ahd.com
   - Search facility name + state
   - Copy Medicare Provider ID

3. **Quality Ratings**: https://www.medicare.gov/care-compare/
   - Search facility
   - Note star rating

## Next Steps

Once you have the enhanced data, you can:
1. Import to Excel for analysis
2. Create pivot tables by state/ownership
3. Map facilities with quality ratings
4. Identify facilities missing key data
5. Cross-reference with state licensing databases

## Support

- NPPES Help: 1-800-465-3203
- CMS Support: https://www.cms.gov/contact
- Python Help: https://www.python.org/about/help/

Remember: This uses PUBLIC data only. No private or patient information is accessed.
