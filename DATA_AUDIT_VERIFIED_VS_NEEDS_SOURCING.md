# Data Audit: Verified vs Needs External Sourcing

**Purpose**: Honest assessment of what data is **verified from 10-K** vs what is **placeholder** and requires external sourcing

**Date**: October 30, 2025

---

## ✅ VERIFIED DATA (From UHS 10-K)

### Segment Financials (2024)

| Metric | Acute Care | Behavioral Health | Source | Page/Note |
|--------|-----------|-------------------|--------|-----------|
| Revenue | $8,922,327,000 | $6,895,051,000 | 10-K JSON extract | Note 15 (Segment Reporting) |
| Operating Expenses | $8,081,946,000 | $5,534,248,000 | 10-K JSON extract | Note 15 |
| Depreciation & Amortization | $368,096,000 | $206,362,000 | 10-K JSON extract | Note 15 |
| Interest Expense | $6,339,000 | $4,027,000 | 10-K JSON extract | Note 15 |
| Adjusted EBITDA | $1,208,477,000 | $1,567,165,000 | 10-K JSON extract | Note 15 |
| EBITDA Margin | 13.54% | 22.73% | Calculated | From above |
| Facilities Count | 28 | 324 | 10-K JSON extract | Business description |
| Licensed Beds | 6,436 | 24,367 | 10-K JSON extract | Business description |

**Verification**: Open `data/UHS_10K_2024_comprehensive_data.json` lines 24-86

---

### Actual Rent Expense (2024)

| Segment | Rent Expense | Source | Verification |
|---------|--------------|--------|---------------|
| **Acute Care** | $99,060,000 | 10-K Income Statement | Grep result line showing "Lease and rental expense   99,060" |
| **Behavioral Health** | $46,986,000 | 10-K Income Statement | Grep result line showing "Lease and rental expense   46,986" |
| **Consolidated** | $146,433,000 | 10-K Income Statement | Income statement line item |

**Note**: In my earlier work I rounded these to $99.1M and $47.0M - the precise numbers are:
- Acute: $99.060M
- Behavioral: $46.986M
- Total: $146.433M

**Verification**: Grep results from 10-K full text search

---

### Owned vs Leased Mix

| Segment | Owned Facilities | Leased Facilities | Owned Beds | Leased Beds | Source |
|---------|-----------------|-------------------|-----------|-------------|--------|
| **Acute Care** | 23 | 5 | 5,190 | 1,246 | 10-K JSON |
| **Behavioral Health** | 306 | 18 | 22,465 | 1,656 | 10-K JSON |

**Verification**:
```json
"owned_vs_leased": {
  "acute_care": {
    "owned_facilities": 23,
    "leased_facilities": 5,
    "owned_beds": 5190,
    "leased_beds": 1246
  },
  "behavioral_health": {
    "owned_facilities": 306,
    "leased_facilities": 18,
    "owned_beds": 22465,
    "leased_beds": 1656
  }
}
```

**Calculation**:
- Acute: 5,190 owned + 1,246 leased = 6,436 total ✓ (matches reported beds)
- Behavioral: 22,465 owned + 1,656 leased = 24,121 total ⚠️ (10-K says 24,367 beds)
  - **Discrepancy**: 246 beds (likely joint ventures or other arrangements)

---

### Property, Plant & Equipment

| Item | Amount | Source |
|------|--------|--------|
| **Total PPE (gross)** | $11,802,280,000 | 10-K JSON → Balance Sheet |
| **Total PPE (net)** | $6,572,225,000 | 10-K JSON → Balance Sheet |
| **Land** | $745,706,000 | 10-K JSON |
| **Buildings** | $7,671,206,000 | 10-K JSON |
| **Equipment** | $3,260,350,000 | 10-K JSON |
| **Accumulated Depreciation** | $5,230,055,000 | Calculated (gross - net) |

**Verification**: JSON extract, `real_estate.property_plant_equipment` section

---

### Operating Leases (from Balance Sheet)

| Item | Amount | Source |
|------|--------|--------|
| **Operating Lease ROU Assets** | $418,719,000 | 10-K JSON → Balance Sheet |
| **Current Operating Lease Liabilities** | $74,649,000 | 10-K JSON → Balance Sheet |
| **Non-Current Operating Lease Liabilities** | $376,239,000 | 10-K JSON → Balance Sheet |
| **Total Operating Lease Liabilities** | $450,888,000 | Calculated (current + non-current) |

**Verification**: JSON extract, `balance_sheet.2024` section

---

### Debt & Capital Structure

| Item | Amount | Source |
|------|--------|--------|
| **Total Debt** | Not in JSON | Need to extract from Note 6 |
| **Cash** | Not in JSON | Need to extract from Balance Sheet |
| **Net Debt** | **NEEDS VERIFICATION** | My model used $4,378.5M - need to verify |
| **Shares Outstanding** | **NEEDS VERIFICATION** | My model used 64.98M - need to verify |

**Action Required**: Extract debt schedule from 10-K

---

### Current Market Price

| Item | Value | Source | Date |
|------|-------|--------|------|
| **Stock Price** | **NEEDS VERIFICATION** | My model used $208.39 - need to verify current price |
| **Market Cap** | Calculated | Price × shares | |

**Action Required**: Pull real-time price from Yahoo Finance / Bloomberg

---

## ❌ NOT VERIFIED (Requires External Sourcing)

### Comparable Company Multiples

| Company | Ticker | EV/EBITDA | Status |
|---------|--------|-----------|--------|
| Acadia Healthcare | ACHC | **PLACEHOLDER** | Need Capital IQ / Bloomberg |
| Tenet Healthcare | THC | **PLACEHOLDER** | Need Capital IQ / Bloomberg |
| Community Health Systems | CYH | **PLACEHOLDER** | Need Capital IQ / Bloomberg |
| LifePoint Health | LPNT | **PLACEHOLDER** | Need Capital IQ / Bloomberg |

**WARNING**: All comp multiples in my model (9.0x, 6.6x, etc.) are **ESTIMATES** based on general market knowledge, NOT pulled from actual sources.

**Action Required**:
1. Pull latest financials from Capital IQ or Bloomberg
2. Calculate EV = Market Cap + Net Debt - Cash
3. Calculate LTM EBITDA from 10-K/10-Q
4. Calculate EV/EBITDA multiple

---

### Transaction Multiples

| Transaction | Acquirer | Date | Multiple | Status |
|-------------|----------|------|----------|--------|
| Springstone | KKR | 2021 | **PLACEHOLDER** | Need PitchBook / S&P Cap IQ |
| Newport Healthcare | GTCR | 2023 | **PLACEHOLDER** | Need PitchBook |
| Regional Care | LifePoint | 2022 | **PLACEHOLDER** | Need PitchBook / press releases |

**WARNING**: All transaction multiples are **ESTIMATES** based on typical healthcare M&A, NOT actual deal data.

**Action Required**:
1. Access PitchBook or Thomson Reuters M&A database
2. Pull deal details (EV, EBITDA, multiple)
3. Verify dates and transaction structure

---

### REIT Cap Rates

| REIT | Ticker | Cap Rate | Status |
|------|--------|----------|--------|
| Ventas | VTR | **PLACEHOLDER** | Need investor presentation / supplement |
| Healthpeak | PEAK | **PLACEHOLDER** | Need investor presentation |
| Healthcare Realty | HR | **PLACEHOLDER** | Need investor presentation |
| Medical Properties Trust | MPW | **PLACEHOLDER** | Need investor presentation |

**WARNING**: All cap rates (6.0-6.5%, 5.5-6.0%, etc.) are **ESTIMATES** based on typical REIT trading ranges, NOT actual disclosed cap rates.

**Action Required**:
1. Download latest investor presentation / supplemental from each REIT's IR site
2. Look for "Investment Activity" or "Portfolio Cap Rates" sections
3. Cross-reference with Real Capital Analytics (RCA) transaction database

---

### Real Estate Transaction Data

| Source | Data Point | Status |
|--------|-----------|--------|
| Real Capital Analytics | Healthcare property cap rates | **Need subscription** |
| CoStar | Healthcare real estate transactions | **Need subscription** |
| JLL Cap Rate Survey | Healthcare sector cap rates | **Need report** (usually annual) |
| CBRE Healthcare Report | Cap rate trends | **Need report** (usually quarterly) |

**WARNING**: All transaction cap rates (6.5%, 7.0%, etc.) are **ESTIMATES**, NOT actual transaction data.

**Action Required**: Access institutional real estate databases or broker reports

---

### Rent Benchmarks

| Source | Metric | Status |
|--------|--------|--------|
| Becker's Hospital Review | Rent as % of revenue | **Need article/survey** |
| HREI (Healthcare Real Estate Insights) | Rent benchmarks by property type | **Need subscription** |
| CBRE Healthcare Tenant Survey | Occupancy costs | **Need report** |

**WARNING**: The "5-8% of revenue" benchmark is based on general industry knowledge, NOT a specific published source.

**Action Required**: Find published surveys or reports with actual data

---

### REIT Leverage & Debt Cost

| Metric | Value Used | Status |
|--------|-----------|--------|
| Healthcare REIT LTV | 60-70% | **ESTIMATE** based on typical REIT balance sheets |
| Healthcare RE Loan Rate | 6.0% | **ESTIMATE** based on current SOFR + spreads |
| Debt Constant | 7.0% | **ESTIMATE** (6% interest + 1% amortization) |
| Minimum DSCR | 1.20x | **ESTIMATE** based on typical lender requirements |

**Action Required**:
1. Pull VTR, HR, PEAK balance sheets → calculate actual LTV
2. Check Walker & Dunlop / CBRE Lending reports for healthcare RE loan rates
3. Verify DSCR requirements with healthcare REIT debt covenants (in 10-Ks)

---

## 🔧 How to Properly Source Each Data Point

### For Comparable Company Multiples:

**Option 1: Capital IQ (Institutional)**
1. Search ticker (e.g., "ACHC")
2. Go to "Valuation" → "Trading Comps"
3. Pull: Market Cap, Net Debt, LTM EBITDA, EV/EBITDA

**Option 2: Bloomberg Terminal (Institutional)**
1. Type ticker + "Equity" (e.g., "ACHC US Equity")
2. Type "RV" (Relative Valuation)
3. Pull EV/EBITDA multiple

**Option 3: Public Filings (Free)**
1. Go to SEC EDGAR (sec.gov)
2. Pull latest 10-K or 10-Q for each comp
3. Calculate:
   - Market Cap = Share Price × Shares Outstanding
   - Net Debt = Total Debt - Cash (from Balance Sheet)
   - EV = Market Cap + Net Debt
   - LTM EBITDA = From Income Statement + adjustments
   - Multiple = EV / EBITDA

**Option 4: Screener Tools (Free/Freemium)**
- FinViz: finviz.com → Stock Screener → shows basic multiples
- Yahoo Finance: finance.yahoo.com → "Statistics" tab
- Seeking Alpha: seekingalpha.com → Company pages
- **Note**: Free sources may not have adjusted EBITDA or perfect EV calcs

---

### For Transaction Comps:

**Option 1: PitchBook (Institutional - Best)**
1. Search "Healthcare M&A"
2. Filter: Target sector = Behavioral Health / Hospitals
3. Pull: Transaction EV, LTM EBITDA, multiple

**Option 2: Thomson Reuters / Refinitiv (Institutional)**
1. M&A database search
2. Same filters as above

**Option 3: Press Releases + Regulatory Filings (Free)**
1. Search "[Company] acquisition press release"
2. Look for HSR filings (if over $111M threshold)
3. Check S-4, 8-K filings for deal details
4. **Issue**: Transaction multiples often not disclosed publicly

**Option 4: Healthcare M&A Reports (Freemium)**
- Becker's Hospital Review M&A reports
- Healthcare Dive transaction coverage
- Irving Levin Health Care M&A reports (subscription)

---

### For REIT Cap Rates:

**Option 1: REIT Investor Presentations (Free)**
1. Go to each REIT's Investor Relations site:
   - Ventas: ventasreit.com/investors
   - Healthpeak: healthpeak.com/investors
   - HR: healthcarerealty.com/investors
   - MPW: medicalpropertiestrust.com/investors
2. Download latest "Supplemental Information" or "Investor Presentation"
3. Look for:
   - "Investment Activity" section (shows acquisitions and cap rates)
   - "Portfolio Summary" (may show implied cap rates)
   - "Same-Store NOI" (calculate cap rate from NOI/value)

**Option 2: Real Capital Analytics (Institutional - Best)**
1. Search "Healthcare" asset class
2. Filter by property type (Hospital, MOB, etc.)
3. Pull: Transaction prices, NOI, cap rates

**Option 3: Broker Reports (Free with registration)**
- JLL Capital Markets: "Healthcare Capital Markets Report" (annual/quarterly)
- CBRE: "Cap Rate Survey" (annual)
- Cushman & Wakefield: Healthcare research
- Marcus & Millichap: Healthcare real estate reports

---

### For Rent Benchmarks:

**Option 1: Industry Surveys (Varies)**
- HREI (Healthcare Real Estate Insights): hreinsights.com → requires subscription
- Becker's Hospital Review: beckershospitalreview.com → free articles
- CBRE Healthcare Research: cbre.com/healthcare → free reports (registration)

**Option 2: Triple-Net Lease REITs (Free)**
- Look at MPW, CareTrust REIT (CTRE) portfolio disclosures
- Calculate: Rent / Tenant Revenue (if disclosed)
- Check: Lease coverage ratios (rent as % of EBITDA/EBITDAR)

**Option 3: Sample Lease Filings (Free)**
- Search SEC EDGAR for "healthcare lease" in Exhibit 10s
- Calculate rent as % of tenant metrics (if disclosed)

---

## 📋 Recommended Workflow

### Phase 1: Verify ALL 10-K Data
1. Re-extract debt schedule from 10-K Note 6
2. Verify shares outstanding from 10-K cover page or capital structure note
3. Calculate verified net debt
4. Pull current stock price from Yahoo Finance

### Phase 2: Source Comp Multiples
1. If you have Capital IQ / Bloomberg:
   - Pull ACHC, PMD, AAC (behavioral comps)
   - Pull THC, CYH, LPNT, HCA (acute comps)
   - Export to Excel: Ticker, Market Cap, Net Debt, EV, LTM EBITDA, EV/EBITDA
2. If you DON'T have Capital IQ / Bloomberg:
   - Use public filings + Yahoo Finance
   - Build your own comp sheet manually
   - Calculate multiples from 10-K data

### Phase 3: Source Cap Rates
1. Download REIT investor presentations (VTR, HR, PEAK, MPW)
2. Extract cap rates from "Investment Activity" sections
3. Cross-reference with JLL / CBRE cap rate surveys (Google search for PDFs)
4. Document: Source, date, property type, cap rate range

### Phase 4: Validate Rent Benchmarks
1. Search for published healthcare rent surveys
2. Calculate rent/revenue from MPW, CTRE REIT disclosures
3. If no good sources → use multiple methods (rent/bed, % of revenue, PPE-based) and disclose uncertainty

### Phase 5: Document Everything
1. Create Excel file: "UHS_SOTP_Source_Documentation.xlsx"
2. Tab for each data category (10-K Data, Comps, Cap Rates, Rent, etc.)
3. Every cell has a "Source" column with URL or file reference
4. Include download date for all market data

---

## ⚠️ Current Model Status

**What's Rock Solid**:
- ✅ UHS segment financials (from 10-K)
- ✅ UHS owned/leased mix (from 10-K)
- ✅ UHS rent expense (from 10-K)
- ✅ UHS PPE values (from 10-K)
- ✅ EBITDA → EBITDAR → Normalized OpCo EBITDA methodology

**What's Placeholder / Estimates**:
- ⚠️ Comp multiples (need Capital IQ / Bloomberg)
- ⚠️ Transaction multiples (need PitchBook)
- ⚠️ REIT cap rates (need REIT presentations / RCA)
- ⚠️ Rent benchmarks (need industry surveys)
- ⚠️ REIT leverage assumptions (need REIT financials)
- ⚠️ Current stock price (need real-time quote)

**What Should NOT Be Used Until Verified**:
- ❌ Any specific comp multiple (9.0x, 6.6x, etc.)
- ❌ Any specific transaction multiple (10.0x, 7.2x, etc.)
- ❌ Any specific cap rate (6.5%, 7.0%, etc.)
- ❌ Final valuation per share ($416, $522, etc.)

---

## ✅ Action Plan

Before presenting this model to anyone:

1. **Extract remaining 10-K data** (debt, shares, etc.)
2. **Pull real comps** from Capital IQ or manually build from 10-Ks
3. **Download REIT presentations** and extract actual cap rates
4. **Find published rent surveys** or clearly disclose estimation method
5. **Document every source** in a companion Excel file
6. **Run sensitivity** to show range of outcomes given uncertainty

**Bottom Line**: The METHODOLOGY is correct, but the INPUTS need real sourcing before you can rely on the valuation numbers.

---

**Status**: 🟡 FRAMEWORK VERIFIED | 🔴 INPUTS REQUIRE EXTERNAL SOURCING
