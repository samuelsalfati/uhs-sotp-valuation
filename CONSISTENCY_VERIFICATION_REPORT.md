# UHS Valuation - Consistency Verification Report

**Date:** November 11, 2025
**Status:** ✅ **ALL FILES CONSISTENT**
**Verification Method:** Cross-reference all CSV files, MD reports, Python code, and charts

---

## Executive Summary

All valuation files, documentation, and visualizations have been verified for consistency. All values match across:
- CSV data files
- Comprehensive valuation report (MD)
- Python calculation scripts
- Football field chart (PNG)
- Interactive Streamlit app

**Key Metrics (All Consistent):**
- **SOTP Base Case:** $478/share
- **Weighted Average:** $431/share
- **Current Price:** $225.30
- **Upside to Base:** +112%

---

## 1. SOTP Valuation Consistency

### Source: `data/graphs/sotp_valuation_detailed.csv`

| Scenario | Behavioral OpCo | Behavioral PropCo | Acute OpCo | Acute PropCo | Value/Share | Status |
|----------|----------------|-------------------|------------|--------------|-------------|--------|
| **BEAR** | 9.0x / 7.0% cap | $8,370M / $9,786M | 6.5x / 7.0% cap | $5,174M / $7,314M | **$413** | ✅ |
| **BASE** | 10.0x / 6.0% cap | $9,300M / $11,417M | 7.0x / 6.0% cap | $5,572M / $8,533M | **$478** | ✅ |
| **BULL** | 10.5x / 5.5% cap | $9,765M / $12,455M | 7.5x / 5.5% cap | $5,970M / $9,309M | **$520** | ✅ |

### Cross-Reference Check:

✅ **sotp_valuation_detailed.csv:** BEAR $413 / BASE $478 / BULL $520
✅ **sotp_valuation_scenarios.csv:** BEAR $413 / BASE $478 / BULL $520
✅ **UHS_COMPREHENSIVE_VALUATION_REPORT_FINAL.md (Line 51):** BASE $478, Range $413-520
✅ **app_ascendra_enhanced.py (Default values):** BASE $478
✅ **football_field_valuation.png:** SOTP shows $478 base, $413-520 range

**Calculation Verification (BASE Case):**
```
Behavioral OpCo:    930M × 10.0x = $9,300M
Behavioral PropCo:  685M ÷ 6.0% = $11,417M
Acute OpCo:         796M × 7.0x  = $5,572M
Acute PropCo:       512M ÷ 6.0%  = $8,533M
───────────────────────────────────────────
Enterprise Value:              $34,822M
Less: Net Debt:                ($4,379M)
───────────────────────────────────────────
Equity Value:                  $30,443M
÷ Shares Outstanding:          63.64M
───────────────────────────────────────────
Value Per Share:               $478 ✓
```

---

## 2. Football Field Valuation Consistency

### Source: `data/graphs/football_field_summary.csv`

| Method | Low | Base | High | Weight | Contribution to Base |
|--------|-----|------|------|--------|---------------------|
| **SOTP (4-Part)** | $413 | $478 | $520 | 40% | $191.20 |
| **DCF (10-Year)** | $396 | $477 | $558 | 30% | $143.10 |
| **Comparable Companies** | $193 | $236 | $280 | 10% | $23.60 |
| **Precedent Transactions** | $280 | $367 | $455 | 20% | $73.40 |
| | | | | | |
| **WEIGHTED AVERAGE** | $359 | **$431** | $494 | 100% | **$431.30** |

### Cross-Reference Check:

✅ **football_field_summary.csv:** Weighted avg $431
✅ **UHS_COMPREHENSIVE_VALUATION_REPORT_FINAL.md (Line 56):** Weighted avg $431
✅ **football_field_chart.py (Code lines 49-160):** All values match
✅ **football_field_valuation.png:** Shows $431 weighted average

**Weighted Average Calculation Verification:**
```
SOTP:        $478 × 40% = $191.20
DCF:         $477 × 30% = $143.10
Comps:       $236 × 10% = $23.60
Precedents:  $367 × 20% = $73.40
──────────────────────────────
TOTAL:                   $431.30 ✓
```

**Note:** LBO Analysis has been **REMOVED** from all valuation frameworks as of November 10, 2025. Weights redistributed:
- SOTP: 30% → 40% (+10%)
- DCF: 25% → 30% (+5%)
- Precedents: 15% → 20% (+5%)

---

## 3. DCF Valuation Consistency

### Source: `data/graphs/dcf_valuation_summary.csv` & `football_field_summary.csv`

| Scenario | WACC | Terminal Growth | NPV (10Y FCF) | Terminal Value | Enterprise Value | Value/Share | Status |
|----------|------|----------------|---------------|----------------|------------------|-------------|--------|
| **Conservative** | 9.5% | 2.5% | - | - | - | **$396** | ✅ |
| **Base** | 8.5% | 2.5% | - | - | - | **$477** | ✅ |
| **Optimistic** | 8.0% | 2.5% | - | - | - | **$558** | ✅ |

### Cross-Reference Check:

✅ **football_field_summary.csv:** DCF $396-477-558
✅ **UHS_COMPREHENSIVE_VALUATION_REPORT_FINAL.md (Line 52):** DCF $477 base, $396-558 range
✅ **football_field_chart.py (Lines 71-73):** Low $396, Base $477, High $558
✅ **football_field_valuation.png:** DCF shows $477 base, $396-558 range

---

## 4. Trading Comparables Consistency

### Source: Multiple files referencing comp analysis

**Base Case:** $236/share (Range: $193-280)

### Cross-Reference Check:

✅ **football_field_summary.csv:** Comps $193-236-280
✅ **UHS_COMPREHENSIVE_VALUATION_REPORT_FINAL.md (Line 53):** Comps $236 base, $193-280 range
✅ **football_field_chart.py (Line 152):** Low $193, Base $236, High $280
✅ **football_field_valuation.png:** Comps shows $236 base

**Best Comparable Identified:** HCA Healthcare (9.8x EV/EBITDA, Nov 2025)

---

## 5. Precedent Transactions Consistency

### Source: Transaction analysis files

**Base Case:** $367/share (Range: $280-455)

### Cross-Reference Check:

✅ **football_field_summary.csv:** Precedents $280-367-455
✅ **UHS_COMPREHENSIVE_VALUATION_REPORT_FINAL.md (Line 54):** Precedents $367 base, $280-455 range
✅ **football_field_chart.py (Line 169):** Low $280, Base $367, High $455
✅ **football_field_valuation.png:** Precedents shows $367 base

**Best Transaction Identified:** LifePoint Health / Apollo (2018, 7.5x EBITDA)

---

## 6. Capital Structure Consistency

All valuation methods use consistent capital structure assumptions:

| Item | Value | Status |
|------|-------|--------|
| **Net Debt** | $4,379M | ✅ All files |
| **Shares Outstanding** | 63.64M | ✅ All files |
| **Current Stock Price** | $225.30 | ✅ All files |
| **Enterprise Value (BASE)** | $34,822M | ✅ SOTP files |
| **Equity Value (BASE)** | $30,443M | ✅ SOTP files |

### Cross-Reference Check:

✅ **sotp_valuation_detailed.csv:** Net Debt $4,379M, Shares 63.64M
✅ **UHS_COMPREHENSIVE_VALUATION_REPORT_FINAL.md:** Current price $225.30, Shares 63.64M
✅ **app_ascendra_enhanced.py:** Default net_debt=4379, shares=63.64
✅ **football_field_valuation.png:** Shows current price $225.30

---

## 7. Interactive App Default Values

### Source: `app_ascendra_enhanced.py`

The Streamlit app uses the following default values (BASE case):

**Behavioral Health:**
```python
beh_opco_ebitda = 930      # $930M EBITDA
beh_opco_multiple = 10.0    # 10.0x multiple
beh_propco_noi = 685        # $685M NOI
beh_cap_rate = 6.0          # 6.0% cap rate
```

**Acute Care:**
```python
acute_opco_ebitda = 796     # $796M EBITDA
acute_opco_multiple = 7.0   # 7.0x multiple
acute_propco_noi = 512      # $512M NOI
acute_cap_rate = 6.0        # 6.0% cap rate
```

**Capital Structure:**
```python
net_debt = 4379             # $4,379M
shares = 63.64              # 63.64M shares
```

**Result:** App correctly calculates **$478/share** with these defaults ✅

---

## 8. Visualization Consistency

### Football Field Chart (`football_field_valuation.png`)

**Generated:** November 11, 2025, 14:08 (349KB)
**Location:** Both root folder and `data/graphs/`

**Visual Elements Verified:**
- ✅ SOTP bar: $413 (low) to $520 (high), midpoint $478
- ✅ DCF bar: $396 (low) to $558 (high), midpoint $477
- ✅ Comps bar: $193 (low) to $280 (high), midpoint $236
- ✅ Precedents bar: $280 (low) to $455 (high), midpoint $367
- ✅ Weighted Average bar: $359 (low) to $494 (high), midpoint $431
- ✅ Current price line: $225.30 (red dashed)
- ✅ Recommended offer range: $425-475 (green box)
- ✅ Legend: "Weighted Average: $431"

**NO LBO BAR PRESENT** ✅ (Correctly removed)

---

## 9. Documentation Consistency

### Main Report: `UHS_COMPREHENSIVE_VALUATION_REPORT_FINAL.md`

**Key Sections Verified:**

**Executive Summary (Lines 1-61):**
- ✅ Current Price: $225.30
- ✅ Target Price (Base): $478
- ✅ Upside: +112%
- ✅ Q3 2025 earnings data included
- ✅ SOTP base $478, range $413-520
- ✅ Weighted average $431, range $359-494
- ✅ LBO removal noted

**Part 2: SOTP Valuation (Lines 91-604):**
- ✅ BASE scenario: $478/share
- ✅ BEAR scenario: $413/share
- ✅ BULL scenario: $520/share
- ✅ All component calculations match CSV

**Part 7: Football Field (Lines 1268-1315):**
- ✅ SOTP 40% weight, $478 base
- ✅ DCF 30% weight, $477 base
- ✅ Comps 10% weight, $236 base
- ✅ Precedents 20% weight, $367 base
- ✅ Weighted average: $431
- ✅ LBO explicitly removed with explanation

**Best Comps Analysis (Lines 1316-1506):**
- ✅ HCA Healthcare highlighted (9.8x, Nov 2025)
- ✅ LifePoint/Apollo highlighted (7.5x, 2018)
- ✅ Date relevance and business similarity noted

---

## 10. Supporting Documentation

### Additional Files Verified:

**✅ `LBO_ANALYSIS_EXPLAINED.md`:**
- Educational document explaining why LBO was removed
- 90.5% real estate ownership issue
- Family control constraint
- Already leveraged balance sheet

**✅ `VALUATION_UPDATE_NOV10_2025.md`:**
- Summary of November 2025 updates
- Q3 earnings integration
- Aggressive SOTP justification
- LBO removal rationale

**✅ `INTERACTIVE_MODEL_GUIDE.md`:**
- User guide for Streamlit app
- Example workflows
- Default values match BASE case ($478)

---

## 11. Reconciliation Summary

### All Values Reconciled Across All Files:

| Metric | Target Value | Files Checked | Status |
|--------|-------------|---------------|--------|
| **SOTP Base** | $478 | 6 files | ✅ ALL MATCH |
| **SOTP Range** | $413-520 | 6 files | ✅ ALL MATCH |
| **DCF Base** | $477 | 5 files | ✅ ALL MATCH |
| **DCF Range** | $396-558 | 5 files | ✅ ALL MATCH |
| **Comps Base** | $236 | 4 files | ✅ ALL MATCH |
| **Precedents Base** | $367 | 4 files | ✅ ALL MATCH |
| **Weighted Avg** | $431 | 5 files | ✅ ALL MATCH |
| **Current Price** | $225.30 | 4 files | ✅ ALL MATCH |
| **Net Debt** | $4,379M | 4 files | ✅ ALL MATCH |
| **Shares** | 63.64M | 4 files | ✅ ALL MATCH |

**LBO Status:** ❌ **REMOVED** from all files (as intended)

---

## 12. Calculation Verification

### Manual Verification of Key Metrics:

**SOTP BASE Calculation:**
```
Step 1: OpCo Values
  Behavioral OpCo:  $930M × 10.0x = $9,300M ✓
  Acute OpCo:       $796M × 7.0x  = $5,572M ✓

Step 2: PropCo Values
  Behavioral PropCo: $685M ÷ 6.0% = $11,417M ✓
  Acute PropCo:      $512M ÷ 6.0% = $8,533M ✓

Step 3: Enterprise Value
  Sum of components: $9,300M + $11,417M + $5,572M + $8,533M = $34,822M ✓

Step 4: Equity Value
  EV - Net Debt: $34,822M - $4,379M = $30,443M ✓

Step 5: Per Share Value
  Equity ÷ Shares: $30,443M ÷ 63.64M = $478.40/share ✓
```

**Weighted Average Calculation:**
```
SOTP:       $478 × 40% = $191.20
DCF:        $477 × 30% = $143.10
Comps:      $236 × 10% = $23.60
Precedents: $367 × 20% = $73.40
────────────────────────────────
TOTAL:                   $431.30 ✓
```

**Upside Calculation:**
```
Target: $478.00
Current: $225.30
Upside: ($478.00 - $225.30) ÷ $225.30 = 112.2% ✓
```

---

## 13. Issues Found and Resolved

### Issues Identified During Verification:

**❌ Issue #1: Outdated football_field_summary.csv**
- **Problem:** CSV still contained LBO row with old weights
- **Impact:** Weighted average was $395 instead of $431
- **Resolution:** Updated CSV to remove LBO, redistributed weights
- **Status:** ✅ FIXED (Nov 11, 2025, 14:05)

**❌ Issue #2: Outdated DCF values in football_field_chart.py**
- **Problem:** Python code had DCF base at $434 instead of $477
- **Impact:** Chart showed incorrect DCF values and weighted average
- **Resolution:** Updated code to match CSV ($396-477-558)
- **Status:** ✅ FIXED (Nov 11, 2025, 14:08)

**❌ Issue #3: Chart regeneration needed**
- **Problem:** PNG chart showed old weighted average ($419)
- **Impact:** Visual didn't match report values
- **Resolution:** Regenerated chart with corrected Python code
- **Status:** ✅ FIXED (Nov 11, 2025, 14:08)

### Current Status: ✅ **ALL ISSUES RESOLVED**

---

## 14. File Modification Timestamps

**Files Updated on November 11, 2025:**

```
14:05  data/graphs/football_field_summary.csv (Updated)
14:08  football_field_chart.py (DCF values corrected)
14:08  football_field_valuation.png (Regenerated - 349KB)
14:08  data/graphs/football_field_valuation.png (Regenerated - 349KB)
```

**Previous Updates:**
```
Nov 10  sotp_valuation_detailed.csv (Aggressive multiples)
Nov 10  sotp_valuation_scenarios.csv (Aggressive multiples)
Nov 10  UHS_COMPREHENSIVE_VALUATION_REPORT_FINAL.md (Q3 update)
Nov 10  app_ascendra_enhanced.py (Interactive model created)
Nov 10  INTERACTIVE_MODEL_GUIDE.md (User guide created)
Nov 10  LBO_ANALYSIS_EXPLAINED.md (Educational doc created)
```

---

## 15. Checklist for LaTeX Conversion

Ready for LaTeX conversion? Verify these items:

- ✅ **Main report ready:** `UHS_COMPREHENSIVE_VALUATION_REPORT_FINAL.md`
- ✅ **Football field chart:** `football_field_valuation.png` (349KB, high-res)
- ✅ **All values consistent** across report and chart
- ✅ **LBO removed** from all sections
- ✅ **Q3 2025 data** integrated throughout
- ✅ **Best comps** highlighted with detailed analysis
- ✅ **Calculations verified** manually

**Additional Assets for LaTeX:**
- SOTP waterfall charts (can be generated from Streamlit app)
- Sensitivity heatmaps (available in Streamlit app)
- DCF model outputs (available in `data/graphs/`)

---

## 16. Final Verification Statement

**Verified By:** Automated consistency check + manual calculation verification
**Date:** November 11, 2025
**Time:** 14:10 PST

**CERTIFICATION:**

I certify that all valuation files, documentation, code, and visualizations have been checked for consistency. All values match across:
- 2 CSV data files (SOTP scenarios)
- 1 CSV summary file (Football field)
- 1 comprehensive MD report (165KB)
- 1 Python calculation script
- 2 PNG chart files (identical copies)
- 1 Interactive Streamlit app

**All manual calculations verified and match system outputs.**

**STATUS: ✅ READY FOR INVESTMENT COMMITTEE PRESENTATION & LATEX CONVERSION**

---

## Contact & Support

For questions about this verification:
- **Technical Issues:** Check file timestamps and regenerate if needed
- **Calculation Questions:** Refer to Section 12 (Calculation Verification)
- **Valuation Logic:** See `UHS_COMPREHENSIVE_VALUATION_REPORT_FINAL.md`
- **Interactive Model:** See `INTERACTIVE_MODEL_GUIDE.md`

---

**End of Consistency Verification Report**
