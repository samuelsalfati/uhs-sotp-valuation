# UHS SOTP Model - Master Data Status Report

**Date**: October 30, 2025
**Purpose**: Clear separation of verified data vs placeholders requiring external sourcing

---

## 🟢 VERIFIED DATA (100% Confidence - Use These Numbers)

### From UHS 10-K Filing (Fiscal Year Ended December 31, 2024)

**Official Filing**: Available at SEC EDGAR - CIK 0000352915
**Local File**: `data/10k_full_text.txt` (9,661 lines extracted from official 10-K)

#### Segment Financials (2024)

| Metric | Acute Care | Behavioral Health | 10-K Line Reference |
|--------|-----------|-------------------|---------------------|
| **Revenue** | $8,922,327,000 | $6,895,051,000 | Lines 6501, 2713, 2825 |
| **Depreciation & Amortization** | $368,096,000 | $206,362,000 | Lines 6509, 2718, 2830 |
| **Interest Expense** | $6,339,000 | $4,027,000 | Lines 6510, 2722, 2834 |
| **Income Before Tax** | $835,347,000 | $1,360,323,000 | Lines 6512, 2724, 2836 |
| **Rent Expense** | **$99,060,000** | **$46,986,000** | **Lines 2719, 2831** |

**EBITDA (Calculated - Verified Math)**:
```
Acute EBITDA = $835.3M + $6.3M + $368.1M - $1.3M = $1,208.5M
Behavioral EBITDA = $1,360.3M + $4.0M + $206.4M - $3.5M = $1,567.2M
```

**EBITDAR (Calculated)**:
```
Acute EBITDAR = $1,208.5M + $99.1M = $1,307.6M
Behavioral EBITDAR = $1,567.2M + $47.0M = $1,614.2M
```

#### Owned vs Leased Mix (from 10-K Facility Listing)

| Segment | Owned Facilities | Leased Facilities | Owned Beds | Leased Beds | % Owned |
|---------|------------------|-------------------|------------|-------------|---------|
| **Acute Care** | 23 | 5 | 5,190 | 1,246 | 80.6% |
| **Behavioral Health** | 306 | 18 | 22,465 | 1,656 | 93.1% |

**Source**: Facility listing in 10-K (lines ~1430-2000), summarized in JSON extract

#### Property, Plant & Equipment (from 10-K Balance Sheet)

| Item | Amount |
|------|--------|
| **Total PP&E (gross)** | $11,802,280,000 |
| **Total PP&E (net)** | $6,572,225,000 |
| **Operating Lease ROU Assets** | $418,719,000 |
| **Operating Lease Liabilities** | $450,888,000 |

**Source**: 10-K Balance Sheet, Note on PP&E

---

## 🟡 CALCULATED FROM VERIFIED DATA (95% Confidence)

### Rent Imputation Methods

| Method | Acute | Behavioral | Total | Logic |
|--------|-------|-----------|-------|-------|
| **Method 1: Rent per Bed** | | | | |
| Rent per Leased Bed | $79,535/bed | $28,382/bed | — | Actual rent ÷ leased beds |
| × Owned Beds | 5,190 | 22,465 | — | From 10-K facility list |
| **= Imputed Rent** | **$413M** | **$638M** | **$1,050M** | Extrapolated to owned |
| | | | | |
| **Method 2: 6% of Revenue** | | | | |
| Revenue (10-K) | $8,922M | $6,895M | $15,817M | Verified |
| × 6% (industry benchmark) | 6% | 6% | 6% | ⚠️ Needs citation |
| **= Imputed Rent** | **$535M** | **$414M** | **$949M** | Market benchmark |
| | | | | |
| **Method 3: PPE Gross-Based** | | | | |
| Total PPE Gross (10-K) | — | — | $11,802M | Verified |
| × 6.5% cap rate | — | — | 6.5% | ⚠️ Needs citation |
| **= Imputed Rent** | **$342M*** | **$425M*** | **$767M** | *Allocated by revenue |

**Status**:
- ✅ Method 1: Math verified, but sample size is small (9.5% of beds leased)
- ⚠️ Method 2: **Needs citation** for 6% benchmark
- ⚠️ Method 3: **Needs citation** for cap rate assumption

---

## 🔴 PLACEHOLDER DATA (Requires External Sourcing - DO NOT USE)

### Comparable Company Multiples

**WARNING**: All comp multiples below are ESTIMATES based on general market knowledge.

| Company | Ticker | Sector | EV/EBITDA | Status |
|---------|--------|--------|-----------|--------|
| Acadia Healthcare | ACHC | Behavioral | **~9.0x** | ❌ PLACEHOLDER - Need Capital IQ/Bloomberg |
| American Addiction Centers | AAC | Behavioral | **~8.2x** | ❌ PLACEHOLDER |
| Tenet Healthcare | THC | Acute | **~6.6x** | ❌ PLACEHOLDER - Need Capital IQ/Bloomberg |
| Community Health Systems | CYH | Acute | **~6.1x** | ❌ PLACEHOLDER |
| LifePoint Health | LPNT | Acute | **~6.5x** | ❌ PLACEHOLDER |
| HCA Healthcare | HCA | Acute | **~6.2x** | ❌ PLACEHOLDER |

**Action Required**: Pull real multiples from:
- Capital IQ / Bloomberg (institutional)
- OR manually calculate from public 10-Ks + Yahoo Finance

### Transaction Comps

**WARNING**: All transaction multiples are ESTIMATES.

| Transaction | Year | Multiple | Status |
|-------------|------|----------|--------|
| Springstone / KKR | 2021 | **~10.0x** | ❌ PLACEHOLDER - Need PitchBook |
| Newport Healthcare / GTCR | 2023 | **~10.7x** | ❌ PLACEHOLDER |
| Regional Care / LifePoint | 2022 | **~7.2x** | ❌ PLACEHOLDER |

**Action Required**: Pull real deal data from PitchBook or press releases

### REIT Cap Rates

**WARNING**: All cap rates are ESTIMATES based on typical REIT trading ranges.

| REIT | Ticker | Asset Type | Cap Rate Range | Status |
|------|--------|-----------|----------------|--------|
| Ventas | VTR | Hospitals | **6.0-6.5%** | ❌ PLACEHOLDER - Need investor presentation |
| Healthpeak | PEAK | MOBs | **5.5-6.0%** | ❌ PLACEHOLDER |
| Healthcare Realty | HR | MOBs | **6.0-6.5%** | ❌ PLACEHOLDER |
| Medical Properties Trust | MPW | Hospitals | **7.0-8.5%** | ❌ PLACEHOLDER |

**Action Required**: Download REIT investor presentations / supplementals:
- VTR: ventasreit.com/investors
- PEAK: healthpeak.com/investors
- HR: healthcarerealty.com/investors
- MPW: medicalpropertiestrust.com/investors

### Rent Benchmarks

**WARNING**: "5-8% of revenue" benchmark has no specific citation.

| Source | Metric | Status |
|--------|--------|--------|
| Becker's Hospital Review | Rent as % of revenue | ❌ Need specific article/report |
| HREI Survey | Behavioral facilities: 6-7% | ❌ Need subscription |
| CBRE Healthcare Tenant Survey | Acute hospitals: 5-6% | ❌ Need report |

**Action Required**: Find published healthcare rent surveys or REIT lease disclosure analysis

### REIT Leverage Assumptions

| Parameter | Assumed Value | Status |
|-----------|---------------|--------|
| LTV Range | 60-70% | ❌ ESTIMATE - Need to verify from VTR, HR balance sheets |
| Healthcare RE Loan Rate | 6.0% | ❌ ESTIMATE - Need Walker & Dunlop or CBRE lending reports |
| Debt Constant | 7.0% | ❌ ESTIMATE (6% int + 1% am) |
| Minimum DSCR | 1.20x | ❌ ESTIMATE - Need to verify lender standards |

**Action Required**: Pull actual data from REIT financials and healthcare lending reports

### Current Market Data

| Item | Value Used | Status |
|------|-----------|--------|
| UHS Stock Price | **$208.39** | ❌ PLACEHOLDER - Pull from Yahoo Finance/Bloomberg |
| Shares Outstanding | **64.98M** | ⚠️ VERIFY from latest 10-K or 10-Q |
| Net Debt | **$4,378.5M** | ⚠️ VERIFY - Need to extract debt schedule from 10-K |

**Action Required**:
1. Get real-time stock price
2. Verify shares outstanding from 10-K cover page or Note
3. Build debt schedule from 10-K Note 6 (Long-Term Debt)

---

## 📋 SOURCING INSTRUCTIONS

### For Each Placeholder Data Point:

#### 1. Comp Multiples

**If you have Capital IQ / Bloomberg**:
```
1. Search ticker (e.g., "ACHC")
2. Navigate to Valuation → Trading Comps
3. Pull: Market Cap, Net Debt, LTM EBITDA, EV/EBITDA
4. Export to Excel with download date
```

**If you DON'T have institutional tools**:
```
1. Go to SEC EDGAR (sec.gov)
2. Find latest 10-K or 10-Q for each comp
3. Extract: Revenue, EBITDA (or calculate from income statement), Debt, Cash
4. Go to Yahoo Finance for market cap
5. Calculate: EV = Market Cap + Net Debt
6. Calculate: EV/EBITDA multiple
7. Document source and date
```

#### 2. REIT Cap Rates

```
1. Go to REIT investor relations site
2. Download latest "Supplemental Information" or "Investor Presentation"
3. Find "Investment Activity" or "Acquisitions" section
4. Extract cap rates by property type
5. Save PDF to project folder with download date
6. Create Excel table with source links
```

#### 3. Rent Benchmarks

**Option A**: Industry surveys
```
1. Search Google Scholar or industry sites for:
   - "healthcare facility rent as percentage of revenue"
   - "triple net lease rates behavioral health"
   - "hospital occupancy cost benchmarks"
2. Download any published reports (HREI, Becker's, CBRE, JLL)
3. Extract relevant statistics
4. Cite source, date, page number
```

**Option B**: REIT lease disclosure analysis
```
1. Review MPW, CareTrust REIT (CTRE) lease disclosures
2. Find properties where both rent and tenant revenue are disclosed
3. Calculate: Rent / Revenue ratio
4. Compile sample of 10+ properties for average
5. Document source: REIT 10-K, Note on leases, page X
```

#### 4. Current Market Data

```
Stock Price:
  - Yahoo Finance: finance.yahoo.com/quote/UHS
  - Document: Date, time, source

Shares Outstanding:
  - UHS 10-K: Cover page or capital structure note
  - Or latest 10-Q

Net Debt:
  - UHS 10-K: Note 6 (Long-Term Debt)
  - Build schedule: Total debt - Cash
  - Verify against balance sheet
```

---

## 🎯 MODEL USAGE GUIDELINES

### ✅ OK to Use Now (With Disclaimers):

1. **Methodology Discussion**: The EBITDA → EBITDAR → OpCo EBITDA flow is correct
2. **Framework Presentation**: Explaining why SOTP is required and how OpCo/PropCo split works
3. **Sensitivity Analysis**: Showing range of outcomes given multiple scenarios
4. **Internal Discussion**: Using for preliminary analysis and identifying data needs

### ❌ DO NOT Use Yet:

1. **Final Valuation**: Do not present $416/share or any specific valuation to external parties
2. **Investment Recommendation**: Cannot make buy/sell decision without verified comps
3. **Board Presentation**: Need verified data for fiduciary responsibility
4. **Acquisition Offer**: Cannot base bid on placeholder assumptions

### ⚠️ Required Before External Use:

1. ✅ All comp multiples sourced and documented
2. ✅ All cap rates sourced from REITs or broker reports
3. ✅ Rent benchmarks cited to published sources
4. ✅ Current stock price and market data verified
5. ✅ Debt schedule built from 10-K
6. ✅ Create "Sources" tab in Excel model with all links/citations
7. ✅ Have someone else independently verify 3-5 key numbers

---

## 📊 MODEL CONFIDENCE LEVELS

| Component | Confidence | Status | Blocker |
|-----------|-----------|--------|---------|
| **UHS 10-K Data** | 100% | ✅ Verified | None |
| **EBITDA Calculations** | 100% | ✅ Verified | None |
| **Rent Normalization Math** | 95% | ✅ Logic verified | Method selection needs validation |
| **OpCo Multiples** | 0% | ❌ Placeholder | Need Capital IQ or manual comp build |
| **PropCo Cap Rates** | 0% | ❌ Placeholder | Need REIT presentations |
| **Final Valuation** | 0% | ❌ Not Ready | Missing all external data |

**Overall Model Status**:
- **Framework**: ✅ Ready
- **Inputs**: 🔴 Not Ready (need external sourcing)
- **Outputs**: 🔴 Placeholder Only

---

## ✅ IMMEDIATE ACTION PLAN

### Phase 1: Complete 10-K Extraction (1 hour)
- [ ] Extract debt schedule from 10-K Note 6
- [ ] Calculate net debt (Total debt - Cash)
- [ ] Verify shares outstanding from 10-K cover
- [ ] Download official 10-K PDF from SEC EDGAR
- [ ] Map line numbers to PDF pages for citations

### Phase 2: Source Market Data (2-3 hours with tools, 1 day without)
- [ ] Pull comp multiples (ACHC, THC, CYH, LPNT, HCA)
  - If have Capital IQ/Bloomberg: 30 min
  - If manual from 10-Ks: 4-6 hours
- [ ] Download 4-5 REIT presentations (VTR, HR, PEAK, MPW)
- [ ] Extract cap rates from REIT investment activity sections
- [ ] Get current UHS stock price

### Phase 3: Validate Rent Assumptions (2-4 hours)
- [ ] Search for published rent surveys (Google Scholar, HREI, Becker's)
- [ ] Analyze MPW/CTRE lease disclosures for rent/revenue ratios
- [ ] Document: "Best available estimate is X%, based on [source]"
- [ ] OR: Present all three methods with pros/cons

### Phase 4: Document Everything (1 hour)
- [ ] Create Excel file "UHS_SOTP_Sources.xlsx"
- [ ] Tab for each category (Comps, Cap Rates, Rent, etc.)
- [ ] Every cell has source, date, link
- [ ] Add to model documentation

### Phase 5: Verify & QC (1 hour)
- [ ] Have someone independently verify 5 key numbers
- [ ] Check all calculations
- [ ] Confirm all sources are cited
- [ ] Final confidence check before presenting

**Total Time**:
- With institutional tools (Capital IQ, Bloomberg, PitchBook): **6-8 hours**
- Without institutional tools (all manual): **2-3 days**

---

## 🎓 LESSONS LEARNED

### What We Got Right:
1. ✅ Methodology is sound (EBITDA → EBITDAR → Normalized OpCo)
2. ✅ All 10-K data extraction is accurate
3. ✅ Framework correctly separates cap rate from dividend yield
4. ✅ Honest about what's estimated vs verified

### What Needs Improvement:
1. ⚠️ Should not have provided specific comp multiples without sourcing
2. ⚠️ Should have flagged rent imputation uncertainty upfront
3. ⚠️ Should have built data sourcing plan before building model
4. ⚠️ Need systematic process for tracking data confidence levels

### Best Practices Going Forward:
1. ✅ Always separate "verified" from "estimated" in documentation
2. ✅ Build data sourcing checklist before starting model
3. ✅ Use ranges/scenarios when inputs are uncertain
4. ✅ Create "Sources" tab in Excel alongside model
5. ✅ Have independent verification step before presenting

---

## 📞 GETTING HELP

### If You Get Stuck on Sourcing:

**Comp Multiples**:
- Can use FinViz screener (finviz.com) for basic multiples
- Yahoo Finance "Statistics" tab has some valuation metrics
- Manually building from 10-Ks is time-consuming but doable

**Cap Rates**:
- REIT investor presentations are PUBLIC and FREE
- Google: "[REIT name] investor presentation Q3 2024 PDF"
- If you can't find acquisition cap rates, use broker reports (also searchable)

**Rent Benchmarks**:
- Hardest to source - may need to accept "best estimate"
- Suggestion: Present all 3 methods (rent/bed, % revenue, PPE-based)
- Show sensitivity to rent assumption (biggest driver of OpCo/PropCo split)

**General**:
- Many broker research reports are available free with email registration
- University library access often includes business databases
- Can request sample reports from brokers (CBRE, JLL, C&W)

---

**Status**: 🟢 FRAMEWORK VERIFIED | 🔴 INPUTS PENDING | 📋 READY FOR SOURCING

**Recommendation**: Complete Phase 1 immediately (finish 10-K extraction), then tackle Phase 2 before using model externally.
