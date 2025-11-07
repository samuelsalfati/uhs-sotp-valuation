# UHS Sum-of-the-Parts Valuation: Comprehensive Due Diligence Plan

**⚠️ CONFIDENTIAL & PROPRIETARY - DO NOT DISTRIBUTE ⚠️**

**Date:** October 27, 2025
**Company:** Universal Health Services, Inc. (NYSE: UHS)
**Valuation Methodology:** Four-Part Sum-of-the-Parts Analysis

---

## 📊 EXECUTIVE SUMMARY

### Investment Thesis
Universal Health Services' current market valuation significantly undervalues the company when analyzed through a **four-part sum-of-the-parts framework**:

1. **Behavioral Health Operations** (OpCo)
2. **Behavioral Health Real Estate** (PropCo)
3. **Acute Care Operations** (OpCo)
4. **Acute Care Real Estate** (PropCo)

By separating operating businesses from owned real estate assets and applying appropriate industry multiples to each, we aim to demonstrate **hidden value** that justifies either:
- Higher equity valuation
- Strategic breakup/spin-off scenario
- Activist investor catalyst

### Four-Part Valuation Framework

```
TOTAL ENTERPRISE VALUE
├── BEHAVIORAL HEALTH SEGMENT
│   ├── Operations: EBITDA × Industry Multiple (9-12x)
│   └── Real Estate: Owned Properties at Market Value
│
├── ACUTE CARE SEGMENT
│   ├── Operations: EBITDA × Industry Multiple (6-8x)
│   └── Real Estate: Owned Properties at Market Value
│
├── LESS: Corporate Overhead (Stranded Costs)
└── LESS: Net Debt

= SOTP EQUITY VALUE
```

---

## 🏗️ FOUR-PART VALUATION STRUCTURE

### Part 1: Behavioral Health Operations (OpCo)
**What We're Valuing:** Cash flows from operating 324 behavioral health facilities

**Key Metrics:**
- **US Facilities:** 177 (from UHS_BEHAVIORAL_COMPLETE_WITH_NPI.csv)
- **UK Facilities:** 147 (from uk_behavioral_facilities.csv)
- **Total Beds:** ~35,000-40,000 (estimated, need to calculate)
- **Ownership:** Mix of owned and leased
- **Revenue Data Available:** 59 facilities with detailed AHD data including:
  - Annual Patient Revenue
  - Annual Discharges
  - Annual Patient Days
  - Occupancy % (where available)

**Valuation Approach:**
- Apply behavioral health industry EBITDA multiple (9-12x)
- Adjust EBITDA to exclude rent on owned properties (since we're valuing RE separately)
- Calculate "Pure OpCo" EBITDA as if all properties were leased at market rates
- Reference comps: Acadia Healthcare (ACHC) trades at 10-12x EBITDA

**Data Sources:**
- 10-K 2024: Segment revenue and adjusted EBITDA
- FINAL_AHD_EXTRACTION_TEMPLATE.csv: 59 facilities with revenue/discharge data
- Industry reports: Behavioral health facility economics

---

### Part 2: Behavioral Health Real Estate (PropCo)
**What We're Valuing:** Owned real estate underlying behavioral health facilities

**Key Metrics:**
- **Owned vs Leased Breakdown:** Need to calculate from CSVs
- **Estimated Value Methods:**
  1. **Replacement Cost Approach:** Book value × 2-3x multiplier
  2. **Cap Rate Approach:** Pro-forma NOI ÷ Cap Rate (6.0-7.0%)
  3. **Market Value per Bed:** Comparable transactions ($150k-$250k per bed)
  4. **Market Value per Sq Ft:** Regional market rates

**Comparable REITs & Cap Rates:**
- Healthcare REIT Cap Rates: 6.0-7.5%
- Behavioral Health Premium: Potentially lower cap rate (5.5-6.5%) due to scarcity
- Recent Transactions: Private equity paying premium for behavioral RE

**Calculation Methodology:**
```
Behavioral Real Estate Value =

Option 1: (Owned Facilities × Avg Beds per Facility × $200k per bed)
Option 2: (Estimated Annual Market Rent × 1 / Cap Rate)
Option 3: Book Value × Real Estate Appreciation Multiplier (2.0-3.0x)

Use the HIGHER of the three methods (conservative)
```

**Data Sources:**
- 10-K: Property, Plant & Equipment note (split behavioral vs acute)
- CSV data: Owned vs leased designation
- Market research: Healthcare real estate transactions

---

### Part 3: Acute Care Operations (OpCo)
**What We're Valuing:** Cash flows from operating 28 acute care hospitals

**Key Metrics:**
- **Total Facilities:** 28 hospitals
- **Total Licensed Beds:** ~6,700 beds (from us_acute_care_facilities.csv)
- **Owned:** 23 facilities (82%)
- **Leased:** 5 facilities (18%)
- **Geographic Concentration:**
  - Nevada: 6 hospitals (Las Vegas/Reno markets)
  - California: 5 hospitals
  - Texas: 5 hospitals
  - Florida: 3 hospitals
  - Other: 9 hospitals

**Facility Size Distribution:**
- Large (300+ beds): 6 facilities (Valley Hospital 420 beds, McAllen 420, etc.)
- Medium (150-299 beds): 15 facilities
- Small (<150 beds): 7 facilities

**Valuation Approach:**
- Apply acute care industry EBITDA multiple (6-8x)
- Adjust EBITDA to exclude rent on owned properties
- Calculate "Pure OpCo" EBITDA assuming market-rate leases
- Reference comps: Tenet Healthcare (THC), HCA Healthcare (HCA)

**Key Operating Metrics to Extract:**
- Revenue per adjusted admission
- Case mix index (acuity)
- Payor mix (Medicare/Medicaid/Commercial)
- EBITDA margin by facility size
- CapEx intensity

**Data Sources:**
- 10-K 2024: Segment financials
- us_acute_care_facilities.csv: 28 facilities with bed counts
- CMS Hospital Compare: Quality metrics, case mix
- State licensing data: Detailed facility financials

---

### Part 4: Acute Care Real Estate (PropCo)
**What We're Valuing:** Owned real estate underlying 23 acute care hospitals

**Key Metrics:**
- **Owned Hospitals:** 23 of 28 (82%)
- **Estimated Total Beds (Owned):** ~5,500 beds
- **Property Types:**
  - Full-service acute care hospitals (expensive build cost)
  - Emergency departments
  - Outpatient facilities
  - Medical office buildings (MOBs)

**Valuation Approach (Most Conservative):**
```
Acute Care Real Estate Value =

Method 1: Book Value × Appreciation Multiplier (2.5-3.5x)
  - Hospitals built 20-40 years ago
  - Replacement cost much higher than book value
  - Land appreciation (especially CA, NV, FL)

Method 2: Market Rent Capitalization
  - Estimate fair market rent per bed ($50k-$75k per bed annually)
  - Divide by cap rate (6.5-7.5%)

Method 3: Comparable Transactions
  - Recent hospital RE sales: $500k-$1M+ per bed in urban markets
  - MOB values: $250-$400 per sq ft

Use MEDIAN of three methods
```

**Geographic Value Add:**
- **Nevada (6 hospitals):** Las Vegas/Reno = high-growth markets, limited CON restrictions
- **California (5 hospitals):** Extremely high RE values, CON restrictions create scarcity
- **Florida (3 hospitals):** High-growth, favorable demographics
- **Texas (5 hospitals):** No CON, but strong healthcare demand

**Data Sources:**
- 10-K: PP&E note (Land, Buildings, Equipment split)
- Real Capital Analytics: Hospital transaction comps
- Healthcare REIT investor presentations: Cap rates and valuations
- CoStar / local brokers: Market rent data by MSA

---

## 📋 COMPREHENSIVE DATA EXTRACTION CHECKLIST

### From 10-K 2024 Annual Report

#### SEGMENT FINANCIALS (Item 1 & Item 8 - Note on Segments)

**Acute Care Segment:**
- [ ] Total Revenue (FY 2024)
- [ ] Total Revenue (FY 2023, FY 2022) - for trend analysis
- [ ] Adjusted EBITDA (FY 2024)
- [ ] Adjusted EBITDA (FY 2023, FY 2022)
- [ ] EBITDA Margin %
- [ ] Number of facilities (verify vs CSV = 28)
- [ ] Number of licensed beds
- [ ] Same-facility revenue growth %
- [ ] Acquisitions/dispositions during year

**Behavioral Health Segment:**
- [ ] Total Revenue (FY 2024)
- [ ] Total Revenue (FY 2023, FY 2022)
- [ ] Adjusted EBITDA (FY 2024)
- [ ] Adjusted EBITDA (FY 2023, FY 2022)
- [ ] EBITDA Margin %
- [ ] Number of facilities (verify vs CSV = 324)
- [ ] Number of licensed beds
- [ ] Same-facility revenue growth %
- [ ] Acquisitions/dispositions during year

**Reconciliation to Consolidated:**
- [ ] Corporate overhead allocation
- [ ] Unallocated expenses
- [ ] Interest expense allocation
- [ ] Depreciation & Amortization by segment

#### REAL ESTATE (Property, Plant & Equipment Note)

**Total PP&E:**
- [ ] Land (by segment if disclosed)
- [ ] Buildings and improvements
- [ ] Equipment (medical & other)
- [ ] Construction in progress
- [ ] Accumulated depreciation
- [ ] Net PP&E book value
- [ ] Depreciation method & useful lives

**Lease Information (Lease Note):**
- [ ] Operating lease commitments (5-year schedule)
- [ ] Operating lease ROU assets
- [ ] Finance lease obligations
- [ ] Weighted average remaining lease term
- [ ] Weighted average discount rate
- [ ] Number of facilities leased vs owned (by segment)

**Capital Expenditures:**
- [ ] Maintenance CapEx (FY 2024, 2023, 2022)
- [ ] Growth CapEx (new facilities, expansions)
- [ ] CapEx as % of revenue
- [ ] Projected CapEx guidance (if disclosed)

#### CAPITAL STRUCTURE (Balance Sheet & Notes)

**Debt:**
- [ ] Current portion of long-term debt
- [ ] Long-term debt (by instrument)
- [ ] Revolving credit facility (drawn/available)
- [ ] Term loans (maturity, interest rate)
- [ ] Senior notes (maturity, coupon, principal)
- [ ] Total debt outstanding
- [ ] Weighted average interest rate
- [ ] Debt covenants (Net Debt/EBITDA limits)
- [ ] Debt maturity schedule (next 5 years)

**Cash & Liquidity:**
- [ ] Cash and cash equivalents
- [ ] Restricted cash
- [ ] Marketable securities
- [ ] Total liquidity
- [ ] Cash flow from operations (3-year trend)
- [ ] Free cash flow (CFO - CapEx)

**Equity:**
- [ ] Common stock outstanding (basic shares)
- [ ] Treasury stock
- [ ] Diluted shares outstanding
- [ ] Share classes (Class A, Class B if applicable)
- [ ] Share-based compensation outstanding (options, RSUs)
- [ ] Weighted average shares for EPS calculation

#### CORPORATE OVERHEAD (Income Statement & SG&A Note)

- [ ] Total Corporate SG&A expenses
- [ ] Public company costs breakdown:
  - [ ] Audit & accounting fees
  - [ ] D&O insurance
  - [ ] Investor relations
  - [ ] Board of directors fees
  - [ ] Legal & compliance (SEC, Sarbanes-Oxley)
  - [ ] Corporate headquarters rent/occupancy
- [ ] Allocated vs unallocated overhead
- [ ] Estimated "stranded costs" in spin-off scenario

#### OPERATING METRICS (MD&A Section)

**Acute Care Metrics:**
- [ ] Same-facility admissions growth %
- [ ] Same-facility revenue per admission
- [ ] Average length of stay (ALOS)
- [ ] Case mix index
- [ ] Emergency department visits
- [ ] Outpatient visits
- [ ] Surgical volumes (inpatient/outpatient)

**Behavioral Health Metrics:**
- [ ] Same-facility admissions growth %
- [ ] Same-facility revenue per patient day
- [ ] Average length of stay (ALOS)
- [ ] Occupancy rate % (if disclosed)
- [ ] Patient days (total and same-facility)

**Payor Mix (Both Segments):**
- [ ] Medicare %
- [ ] Medicaid %
- [ ] Commercial insurance %
- [ ] Self-pay/uninsured %
- [ ] Other (Workers' Comp, etc.)

#### RISK FACTORS (Item 1A)

- [ ] Reimbursement risk (Medicare/Medicaid cuts)
- [ ] Regulatory risk (licensing, CON, DOJ investigations)
- [ ] Competition
- [ ] Labor costs & staffing challenges
- [ ] Malpractice/litigation exposure
- [ ] Cyber security
- [ ] Climate/ESG risks

---

### From Facilities Data (CSV Files)

#### Acute Care Facilities Analysis

**us_acute_care_facilities.csv (28 facilities):**
- [x] Total licensed beds: **6,700** (calculated)
- [ ] Owned vs Leased count: 23 owned, 5 leased
- [ ] Total owned beds: ___
- [ ] Total leased beds: ___
- [ ] Average facility size: ___
- [ ] Geographic distribution by state
- [ ] Top 5 largest facilities (by beds)
- [ ] Smallest 5 facilities (potential divestiture candidates?)

**Metrics to Calculate:**
- [ ] Revenue per bed (Segment Revenue ÷ Total Beds)
- [ ] EBITDA per bed
- [ ] Estimated occupancy rate (industry avg 60-65% for acute care)
- [ ] Estimated annual admissions (beds × occupancy × 365 ÷ ALOS)
- [ ] Market value per bed (for owned facilities)

#### Behavioral Health Facilities Analysis

**UHS_BEHAVIORAL_COMPLETE_WITH_NPI.csv (177 US facilities):**
- [ ] Total licensed beds across all facilities
- [ ] Owned vs Leased count and bed breakdown
- [ ] Facilities WITH revenue data (59 from FINAL_AHD template)
- [ ] Facilities WITHOUT revenue data (118 facilities)
- [ ] NPI coverage (% with NPI numbers)
- [ ] Medicare ID coverage
- [ ] Geographic distribution (top 10 states)

**FINAL_AHD_EXTRACTION_TEMPLATE.csv (59 facilities with financials):**

Key data fields to analyze:
- [x] Annual Patient Revenue (59 facilities have this!)
- [x] Annual Discharges
- [x] Annual Patient Days
- [ ] Occupancy % (where available)
- [ ] Average Length of Stay (calculate if missing)
- [ ] Revenue per patient day (Revenue ÷ Patient Days)
- [ ] Revenue per discharge (Revenue ÷ Discharges)
- [ ] Revenue per bed (Revenue ÷ Beds)

**Extrapolation for Missing Facilities:**
- [ ] Average revenue per bed from 59 facilities with data
- [ ] Apply to 118 facilities without revenue data
- [ ] Calculate estimated total behavioral revenue (bottom-up)
- [ ] Compare to 10-K segment revenue (top-down validation)
- [ ] Reconcile any gaps

**uk_behavioral_facilities.csv (147 UK facilities):**
- [ ] Total beds
- [ ] Owned vs Leased
- [ ] Revenue estimation (if no data, use UK market rates)
- [ ] Regulatory environment (CQC ratings)
- [ ] Brexit impact considerations

#### Total Behavioral Portfolio Summary

```
Total Behavioral Health Facilities: 324
  ├── US: 177 facilities
  │     ├── With Revenue Data: 59 facilities
  │     └── Without Revenue Data: 118 facilities
  │
  └── UK: 147 facilities

Total Behavioral Beds: _______ (TO CALCULATE)
  ├── US Owned: _______ beds
  ├── US Leased: _______ beds
  ├── UK Owned: _______ beds
  └── UK Leased: _______ beds
```

---

## 💰 VALUATION METHODOLOGY: FOUR-PART SOTP

### Step 1: Behavioral Health Operations Valuation

**Inputs Required:**
- Behavioral segment Adjusted EBITDA from 10-K: $_______ million
- Owned facilities rent adjustment: $_______ million (add back)
- Pro-forma OpCo EBITDA (as if all leased): $_______ million

**Industry Multiple Research:**
- Acadia Healthcare (ACHC): Current EV/EBITDA = ___x
- Select Medical (SEM) behavioral segment: ___x
- Recent M&A transactions: ___x (median)
- Range: 9.0x (bear) to 12.0x (bull), 10.5x (base)

**Valuation Calculation:**
```
Behavioral OpCo Value = Pro-forma EBITDA × Multiple

Bear Case (9.0x):  $________ million
Base Case (10.5x): $________ million
Bull Case (12.0x): $________ million
```

---

### Step 2: Behavioral Health Real Estate Valuation

**Method A: Replacement Cost Approach**
```
Book Value of Behavioral PP&E: $________ million (from 10-K)
Appreciation Multiplier: 2.0x - 3.0x (based on age of assets)
Estimated Market Value: $________ million
```

**Method B: Cap Rate Approach**
```
Owned Behavioral Facilities: _____ facilities
Estimated Market Rent per Bed: $30,000 - $40,000 annually
Total Owned Beds: _____ beds
Annual Market Rent: $________ million

Cap Rate: 6.0% (bull) to 7.0% (bear), 6.5% (base)

Real Estate Value = Annual Rent ÷ Cap Rate
Bear (7.0%): $________ million
Base (6.5%): $________ million
Bull (6.0%):  $________ million
```

**Method C: Market Value per Bed**
```
Comparable Transactions: $150k - $250k per bed
Owned Beds: _____ beds

Bear ($150k/bed): $________ million
Base ($200k/bed): $________ million
Bull ($250k/bed):  $________ million
```

**Selected Value: HIGHER of Method B and Method C (conservative)**

---

### Step 3: Acute Care Operations Valuation

**Inputs Required:**
- Acute Care segment Adjusted EBITDA from 10-K: $_______ million
- Owned facilities rent adjustment: $_______ million (add back)
- Pro-forma OpCo EBITDA (as if all leased): $_______ million

**Industry Multiple Research:**
- Tenet Healthcare (THC): Current EV/EBITDA = ___x
- HCA Healthcare (HCA): Current EV/EBITDA = ___x (premium)
- Community Health Systems (CYH): ___x
- Recent M&A transactions: ___x (median)
- Range: 6.0x (bear) to 8.5x (bull), 7.0x (base)

**Valuation Calculation:**
```
Acute Care OpCo Value = Pro-forma EBITDA × Multiple

Bear Case (6.0x):  $________ million
Base Case (7.0x):  $________ million
Bull Case (8.5x):  $________ million
```

---

### Step 4: Acute Care Real Estate Valuation

**Method A: Book Value Appreciation**
```
Book Value of Acute Care PP&E: $________ million (from 10-K)
Appreciation Multiplier: 2.5x - 3.5x (hospitals are expensive assets)
Estimated Market Value: $________ million
```

**Method B: Cap Rate Approach**
```
Owned Acute Care Facilities: 23 hospitals
Owned Beds: ~5,500 beds
Market Rent per Bed: $50,000 - $75,000 annually
Annual Market Rent: $________ million

Cap Rate: 6.5% (bull) to 7.5% (bear), 7.0% (base)

Real Estate Value = Annual Rent ÷ Cap Rate
Bear (7.5%): $________ million
Base (7.0%): $________ million
Bull (6.5%):  $________ million
```

**Method C: Replacement Cost**
```
Cost to Build New Hospital: $1M - $1.5M per bed (industry standard)
Owned Beds: ~5,500 beds
Replacement Cost: $5.5B - $8.25B

Discount for Age/Location: 60-80% of replacement cost
Value: $________ million
```

**Selected Value: MEDIAN of three methods**

---

### Step 5: Adjustments & Final SOTP Calculation

**Corporate Overhead Adjustment:**
```
Current Annual Corporate Overhead: $_______ million (from 10-K)
Public Company Costs (eliminable): $_______ million
  - Audit fees
  - D&O insurance
  - Investor relations
  - SOX compliance
  - Board fees

Stranded Costs (unavoidable): $_______ million
  - Core management
  - IT infrastructure
  - Shared services

Net Overhead Reduction (Annual): $_______ million
NPV of Savings (10x multiple): $_______ million VALUE CREATION
```

**Capital Structure:**
```
Total Debt: $_______ million
Cash: $_______ million
Net Debt: $_______ million

Shares Outstanding (basic): _______ million
Diluted Shares: _______ million
Current Share Price: $______
Current Market Cap: $_______ million
Current Enterprise Value: $_______ million
```

**FINAL SOTP CALCULATION:**

```
═══════════════════════════════════════════════════════════
                    UHS SOTP VALUATION SUMMARY
═══════════════════════════════════════════════════════════

OPERATING BUSINESSES (Enterprise Value):
  1. Behavioral Health Operations      $________ M
  2. Acute Care Operations              $________ M
                                       ──────────
     Total Operating Value              $________ M

REAL ESTATE ASSETS:
  3. Behavioral Health Real Estate      $________ M
  4. Acute Care Real Estate             $________ M
                                       ──────────
     Total Real Estate Value            $________ M

                                       ──────────
TOTAL ENTERPRISE VALUE                  $________ M

ADJUSTMENTS:
  Less: Net Debt                       ($________ M)
  Add: Corporate Overhead Savings      $ ________ M
                                       ──────────
TOTAL EQUITY VALUE                      $________ M

Divided by Shares Outstanding           _______ M
                                       ══════════
SOTP VALUE PER SHARE                    $ ______

CURRENT MARKET PRICE                    $ ______
IMPLIED UPSIDE/DOWNSIDE                 $ ______ (___%)

═══════════════════════════════════════════════════════════
```

---

## 📊 COMPARABLE COMPANY ANALYSIS

### Behavioral Health Comps

| Company | Ticker | Market Cap | EV | LTM EBITDA | EV/EBITDA | Notes |
|---------|--------|------------|-----|------------|-----------|-------|
| Acadia Healthcare | ACHC | | | | | Pure-play behavioral |
| UHS (behavioral only) | UHS | | | | | Our segment |
| Select Medical (behavioral) | SEM | | | | | Partial comp |

**Private Transactions:**
- [List recent behavioral health M&A with multiples]

### Acute Care Comps

| Company | Ticker | Market Cap | EV | LTM EBITDA | EV/EBITDA | Notes |
|---------|--------|------------|-----|------------|-----------|-------|
| HCA Healthcare | HCA | | | | | Premium operator |
| Tenet Healthcare | THC | | | | | Direct comp |
| Community Health Systems | CYH | | | | | Smaller regional |
| UHS (acute only) | UHS | | | | | Our segment |

### Healthcare REIT Comps (for Real Estate Valuation)

| REIT | Ticker | Cap Rate | Dividend Yield | Focus |
|------|--------|----------|----------------|-------|
| Welltower | WELL | | | Senior housing, MOB |
| Healthpeak | PEAK | | | Hospitals, MOB |
| Sabra Health | SBRA | | | SNF, behavioral |
| Medical Properties Trust | MPW | | | Hospitals |
| Physicians Realty | DOC | | | MOB |

**Median Healthcare REIT Cap Rate:** _____%

---

## 🎯 SCENARIO ANALYSIS FRAMEWORK

### Bear Case Assumptions
- **Economic Recession:** Reduced elective procedures, lower behavioral admissions
- **Reimbursement Cuts:** Medicare/Medicaid rates down 3-5%
- **Labor Cost Inflation:** Nurse wages up 8-10%
- **Regulatory Headwinds:** Increased scrutiny on behavioral health
- **Valuation Multiples:** Low end of range
  - Behavioral OpCo: 9.0x EBITDA
  - Acute Care OpCo: 6.0x EBITDA
  - Real Estate: 7.0-7.5% cap rates

**Bear Case SOTP:** $______ per share (____% upside/downside)

---

### Base Case Assumptions
- **Stable Environment:** Current trends continue
- **Modest Growth:** 3-5% annual revenue growth
- **Reimbursement:** Flat to +1% annually
- **Labor Costs:** Normal inflation (4-5%)
- **Valuation Multiples:** Mid-range
  - Behavioral OpCo: 10.5x EBITDA
  - Acute Care OpCo: 7.0x EBITDA
  - Real Estate: 6.5-7.0% cap rates

**Base Case SOTP:** $______ per share (____% upside/downside)

---

### Bull Case Assumptions
- **Strong Economic Growth:** Increased healthcare utilization
- **Behavioral Health Boom:** Mental health awareness drives demand
- **Favorable Policy:** Mental health parity enforcement, surprise billing protection
- **Strategic Buyer Interest:** Private equity or strategic acquirer emerges
- **Valuation Multiples:** High end of range
  - Behavioral OpCo: 12.0x EBITDA
  - Acute Care OpCo: 8.5x EBITDA
  - Real Estate: 6.0-6.5% cap rates

**Bull Case SOTP:** $______ per share (____% upside/downside)

---

## 🔍 SENSITIVITY ANALYSIS

### Key Driver #1: Behavioral Health Multiple

| Behavioral EBITDA Multiple | 9.0x | 9.5x | 10.0x | 10.5x | 11.0x | 11.5x | 12.0x |
|----------------------------|------|------|-------|-------|-------|-------|-------|
| **SOTP Value per Share** | | | | | | | |
| **Implied Upside (%)** | | | | | | | |

### Key Driver #2: Acute Care Multiple

| Acute Care EBITDA Multiple | 6.0x | 6.5x | 7.0x | 7.5x | 8.0x | 8.5x |
|----------------------------|------|------|------|------|------|------|
| **SOTP Value per Share** | | | | | | |
| **Implied Upside (%)** | | | | | | |

### Key Driver #3: Real Estate Cap Rate

| Real Estate Cap Rate | 7.5% | 7.0% | 6.5% | 6.0% | 5.5% |
|---------------------|------|------|------|------|------|
| **Total RE Value ($M)** | | | | | |
| **SOTP Value per Share** | | | | | |
| **Implied Upside (%)** | | | | | |

### Two-Way Sensitivity: Behavioral Multiple vs Real Estate Cap Rate

|  | **Cap Rate: 7.0%** | **Cap Rate: 6.5%** | **Cap Rate: 6.0%** |
|--|---------------------|---------------------|---------------------|
| **Behavioral 12.0x** | | | |
| **Behavioral 11.0x** | | | |
| **Behavioral 10.5x** | | | |
| **Behavioral 10.0x** | | | |
| **Behavioral 9.0x** | | | |

---

## 🚨 RISK FACTORS & MITIGANTS

### Regulatory & Reimbursement Risks

**Risk:** Medicare/Medicaid rate cuts reduce profitability
- **Impact:** Each 1% reimbursement cut = ~$___M EBITDA impact
- **Probability:** Medium (ongoing CMS pressure)
- **Mitigant:** Diversified payor mix, shift to higher commercial %

**Risk:** Increased regulatory scrutiny on behavioral health (DOJ investigations)
- **Impact:** Fines, consent decrees, operational restrictions
- **Probability:** Medium-High (industry-wide issue)
- **Mitigant:** Compliance investments, transparency in billing practices

**Risk:** Certificate of Need (CON) restrictions limit expansion
- **Impact:** Limits growth opportunities in some states
- **Probability:** High (political environment)
- **Mitigant:** Focus growth in non-CON states (TX, AZ)

---

### Operating & Labor Risks

**Risk:** Healthcare labor shortage drives wage inflation
- **Impact:** Nursing wages up 8-10%, margin compression
- **Probability:** High (structural shortage)
- **Mitigant:** Technology investments, productivity improvements

**Risk:** Behavioral health staffing challenges (psychiatrist shortage)
- **Impact:** Limited capacity, difficulty filling beds
- **Probability:** High (nationwide shortage)
- **Mitigant:** Telemedicine, mid-level providers (NPs, PAs)

---

### Market & Competitive Risks

**Risk:** Recession reduces elective procedures (acute care)
- **Impact:** Volume down 5-10% in acute care segment
- **Probability:** Medium (cyclical)
- **Mitigant:** Behavioral health is counter-cyclical, diversification

**Risk:** New behavioral health entrants (telehealth, value-based care)
- **Impact:** Market share erosion, pricing pressure
- **Probability:** Medium (evolving landscape)
- **Mitigant:** Inpatient behavioral has high barriers to entry

---

### Financial & Execution Risks

**Risk:** High debt load limits financial flexibility
- **Impact:** Covenant violations, refinancing risk
- **Probability:** Low (currently investment grade)
- **Mitigant:** Strong cash flow generation, deleveraging

**Risk:** Spin-off execution complexity (stranded costs, dis-synergies)
- **Impact:** Overhead costs don't scale down proportionally
- **Probability:** High (any corporate separation is complex)
- **Mitigant:** Careful planning, TSAs (transition service agreements)

---

## 💡 VALUE CREATION OPPORTUNITIES

### Opportunity #1: REIT Spin-Off
**Concept:** Spin owned real estate into separate publicly-traded REIT

**Value Creation:**
- Unlock hidden real estate value (~$____B at 6.5% cap rate)
- Reduce OpCo leverage (asset sale or drop-down transaction)
- Create two separately-traded securities (sum-of-parts re-rating)
- Tax-efficient structure for investors

**Precedents:**
- Tenet Healthcare → separate REIT consideration
- HCA Healthcare → explored REIT structure
- Select Medical → separate property entities

**Challenges:**
- IRS REIT qualification (healthcare REIT rules)
- Need 100+ unrelated tenants or REIT structure
- Dis-synergies from separation
- Market receptivity to new healthcare REIT

---

### Opportunity #2: Behavioral Health Spin-Off
**Concept:** Spin behavioral segment into separate public company

**Value Creation:**
- Pure-play behavioral would trade at premium multiple (10-12x vs 7-8x blended)
- Dedicated management focus
- M&A currency for behavioral roll-up strategy
- ESG/impact investing appeal (mental health focus)

**Comparable Spin-Offs:**
- [Research recent healthcare spin-offs and valuations]

**Challenges:**
- Stranded corporate costs
- Loss of scale benefits
- Debt allocation
- Two smaller companies may have less liquidity

---

### Opportunity #3: Strategic Sale (Whole Company or Parts)
**Concept:** Sell to private equity or strategic buyer

**Potential Buyers:**
- **Private Equity:** KKR, Blackstone, Apollo (healthcare PE funds)
- **Strategic:** HCA, Tenet, international healthcare companies
- **Behavioral-focused:** Acadia Healthcare (if regulatory approval possible)

**Valuation:**
- PE firms paying 10-12x EBITDA for quality healthcare assets
- Control premium: 25-35% typical
- Recent healthcare take-privates: [list examples with multiples]

---

### Opportunity #4: Asset Sales (Non-Core Divestitures)
**Concept:** Sell underperforming or non-strategic facilities

**Candidates:**
- Small acute care hospitals in competitive markets
- Underperforming behavioral facilities (occupancy <60%)
- Assets in states with unfavorable regulatory environment

**Use of Proceeds:**
- Debt paydown (reduce leverage to <3.0x Net Debt/EBITDA)
- Share buybacks (if trading below intrinsic value)
- Reinvest in high-growth behavioral markets

---

## 📅 WORK PLAN & TIMELINE

### Week 1: Data Collection & Extraction (Days 1-5)
- [ ] **Day 1-2:** Extract all financial data from 10-K 2024
  - Segment financials (revenue, EBITDA, margins)
  - PP&E and real estate data
  - Capital structure (debt, equity, shares)
  - Operating metrics

- [ ] **Day 3:** Analyze behavioral facilities CSV data
  - Calculate total beds by segment
  - Owned vs leased breakdown
  - Revenue analysis from 59 facilities with data
  - Extrapolate to full portfolio

- [ ] **Day 4:** Analyze acute care facilities data
  - Verify 28 facilities, 6,700 beds
  - Geographic analysis
  - Calculate segment metrics

- [ ] **Day 5:** Research industry multiples & comps
  - Pull public company data (ACHC, THC, HCA, CYH, SEM)
  - Research recent M&A transactions
  - Healthcare REIT cap rates

**Deliverable:** Data extraction workbook with all inputs

---

### Week 2: Valuation Build (Days 6-10)

- [ ] **Day 6:** Build Behavioral Health OpCo valuation
  - Adjust EBITDA for owned property rent
  - Apply industry multiples (3 scenarios)

- [ ] **Day 7:** Build Behavioral Health Real Estate valuation
  - 3 methods: replacement cost, cap rate, market value per bed
  - Select conservative approach

- [ ] **Day 8:** Build Acute Care OpCo valuation
  - Adjust EBITDA for owned property rent
  - Apply industry multiples (3 scenarios)

- [ ] **Day 9:** Build Acute Care Real Estate valuation
  - 3 methods: book value appreciation, cap rate, replacement cost
  - Select median approach

- [ ] **Day 10:** Integrate all four components into master SOTP model
  - Add corporate overhead adjustments
  - Calculate final equity value
  - Build three scenarios (Bear/Base/Bull)

**Deliverable:** Excel model with four-part SOTP calculation

---

### Week 3: Analysis & Reporting (Days 11-15)

- [ ] **Day 11:** Sensitivity analysis
  - Key driver tables (behavioral multiple, acute multiple, cap rate)
  - Two-way sensitivity matrices
  - Tornado chart (value impact of each variable)

- [ ] **Day 12:** Comparable company analysis
  - Trading multiples table
  - Transaction multiples table
  - Precedent spin-offs/break-ups

- [ ] **Day 13:** Risk assessment & value creation opportunities
  - Detailed risk analysis with probability/impact
  - Spin-off scenario modeling
  - Strategic alternatives analysis

- [ ] **Day 14:** Investment thesis synthesis
  - Executive summary
  - Key findings & recommendations
  - Price target and rating (BUY/HOLD/SELL)

- [ ] **Day 15:** Final report and presentation prep
  - Update Streamlit dashboard with real data
  - Create PowerPoint summary (10-15 slides)
  - Prepare investment memo (5-10 pages)

**Deliverable:** Full investment report with SOTP valuation

---

## 📈 SUCCESS METRICS

### Valuation Accuracy
- [ ] SOTP model reconciles to 10-K data (within 1%)
- [ ] Bottom-up facility revenue ties to segment revenue
- [ ] Real estate valuation validated by 3 independent methods
- [ ] Industry multiples sourced from credible data (CapIQ, Bloomberg)

### Analysis Depth
- [ ] All 4 segments valued separately (Behavioral Ops/RE, Acute Ops/RE)
- [ ] 3 scenarios modeled (Bear/Base/Bull)
- [ ] Sensitivity analysis on 5+ key variables
- [ ] Risk assessment with probability-weighted outcomes

### Actionable Insights
- [ ] Clear investment thesis (long/short/neutral)
- [ ] Specific catalysts identified (activist, M&A, spin-off)
- [ ] Price target with timeframe
- [ ] Risk/reward ratio quantified

---

## 📚 DATA SOURCES & REFERENCES

### Primary Sources (Company)
- [ ] 10-K Annual Report (FY 2024)
- [ ] 10-Q Quarterly Reports (Q1-Q3 2024)
- [ ] Proxy Statement (DEF 14A)
- [ ] Investor presentations & earnings call transcripts
- [ ] Company website (facility listings, press releases)

### Secondary Sources (Industry)
- [ ] Becker's Hospital Review (industry news & trends)
- [ ] Modern Healthcare (rankings, financial data)
- [ ] American Hospital Association (AHA) data
- [ ] National Association of Psychiatric Health Systems (NAPHS)
- [ ] CMS Hospital Compare (quality metrics, volume data)
- [ ] State health department licensing databases

### Financial Data Sources
- [ ] S&P Capital IQ (comps, multiples, transaction data)
- [ ] Bloomberg Terminal
- [ ] PitchBook (private transaction multiples)
- [ ] FactSet
- [ ] Company filings (for comps)

### Real Estate Data Sources
- [ ] Real Capital Analytics (healthcare RE transactions)
- [ ] CoStar (commercial RE data)
- [ ] Healthcare REIT investor presentations (WELL, PEAK, SBRA)
- [ ] CBRE Healthcare reports
- [ ] JLL Healthcare reports

---

## ⚠️ ASSUMPTIONS & LIMITATIONS

### Key Assumptions
1. **Market Multiples:** Based on current trading levels; subject to market volatility
2. **Real Estate Values:** Estimated using multiple methods; actual values subject to appraisal
3. **Corporate Overhead:** Savings estimates assume efficient separation; may vary
4. **No Change in Operations:** Assumes current business model continues
5. **No Material Acquisitions/Divestitures:** Based on existing portfolio

### Limitations
1. **Public Data Only:** Limited access to non-public facility-level financials
2. **Extrapolation Required:** Not all facilities have detailed revenue data
3. **Market Conditions:** Valuation sensitive to interest rates, multiples compression
4. **Regulatory Uncertainty:** Healthcare policy changes could materially impact
5. **Execution Risk:** Spin-off scenarios assume successful execution

### Disclaimer
This analysis is for informational and educational purposes only. It does not constitute investment advice, a recommendation to buy or sell securities, or an offer or solicitation. All information is derived from public sources believed to be reliable but not guaranteed. Consult a licensed financial advisor before making investment decisions.

---

## 🎯 FINAL DELIVERABLES

### 1. Excel Valuation Model
- Four-part SOTP calculation
- Three scenarios (Bear/Base/Bull)
- Sensitivity tables
- Assumptions page with sources
- Executive summary dashboard

### 2. Streamlit Interactive Dashboard
- Updated app.py with real data
- Four-segment visualization
- Scenario toggle
- Real-time sensitivity analysis
- Downloadable reports

### 3. Investment Memo (5-10 pages)
- Executive summary
- Company overview
- Four-part SOTP valuation
- Comparable company analysis
- Risk factors
- Investment recommendation

### 4. PowerPoint Presentation (10-15 slides)
- Investment thesis (1 slide)
- Company overview (1-2 slides)
- SOTP valuation summary (2-3 slides)
- Segment deep-dives (4 slides: Behavioral Ops/RE, Acute Ops/RE)
- Scenarios & sensitivity (2-3 slides)
- Risks & opportunities (1-2 slides)
- Recommendation (1 slide)

### 5. Supporting Data Files
- Facilities analysis workbook
- Comparable companies data
- Industry research notes
- Real estate valuation backup

---

## 📞 NEXT STEPS

**Immediate Actions (Today):**
1. ✅ Create this comprehensive plan document
2. Start 10-K data extraction
3. Analyze behavioral facilities CSV (calculate total beds, revenue)
4. Begin industry comps research

**This Week:**
- Complete all data extraction
- Build preliminary four-part SOTP model
- Calculate base case valuation

**Questions to Resolve:**
- Do we have access to S&P Capital IQ or Bloomberg for comps data?
- Any specific investment thesis to test (e.g., activist position, short thesis)?
- Target completion date for final report?
- Any specific formatting preferences for deliverables?

---

**Document Version:** 1.0
**Last Updated:** October 27, 2025
**Status:** READY TO EXECUTE

⚠️ **CONFIDENTIAL & PROPRIETARY - DO NOT DISTRIBUTE** ⚠️
