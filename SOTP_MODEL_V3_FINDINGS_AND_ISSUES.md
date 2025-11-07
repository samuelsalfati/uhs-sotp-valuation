# UHS SOTP Model v3.0 - Findings & Issues

## Executive Summary

The corrected SOTP model properly flows from **EBITDA → EBITDAR → Normalized OpCo EBITDA**, but the rent imputation methodology may be overstating PropCo value.

## Key Numbers from 10-K (Verified)

### Segment Performance (2024)
| Segment | Revenue | Reported EBITDA | EBITDA Margin | Actual Rent Expense |
|---------|---------|-----------------|---------------|---------------------|
| **Acute Care** | $8,922M | $1,208M | 13.5% | $99.1M |
| **Behavioral Health** | $6,895M | $1,567M | 22.7% | $47.0M |
| **Total** | $15,817M | $2,775M | 17.5% | $146.1M |

**Source**: 10-K Note 15 (Segment Reporting), Income Statement

### Owned vs Leased Mix (2024)
| Segment | Total Beds | Owned Beds | Leased Beds | Owned % |
|---------|-----------|------------|-------------|---------|
| **Acute Care** | 6,436 | 5,190 | 1,246 | 80.6% |
| **Behavioral Health** | 24,121 | 22,465 | 1,656 | 93.1% |
| **Total** | 30,557 | 27,655 | 2,902 | 90.5% |

**Source**: 10-K Note 9 (Related Party Transactions)

### Real Estate (2024)
| Item | Value |
|------|-------|
| **Total PPE (net)** | $6,572M |
| **Operating Lease ROU Assets** | $419M |
| **Operating Lease Liabilities** | $451M |

**Source**: 10-K Balance Sheet

---

## Normalization Methodology (Corrected)

### The Correct Flow

```
1. Reported EBITDA (from 10-K)         $2,775M
   (AFTER actual rent on leased facilities)

2. + Actual Rent Expense                 $146M
   ────────────────────────────────────────────
3. = EBITDAR                            $2,921M
   (Earnings Before Rent)

4. Calculate Imputed Rent on Owned      $1,050M
   (using methodology below)

5. Total Rent (actual + imputed)        $1,196M
   ────────────────────────────────────────────
6. Normalized OpCo EBITDA               $1,725M
   (EBITDAR - Total Rent)

7. PropCo NOI = Total Rent              $1,196M
```

### Why This Matters

**EBITDA is AFTER rent** (rent is an operating expense). Owned facilities have **no rent** in EBITDA, so they look artificially profitable. To normalize:
- Add back actual rent → get EBITDAR
- Impute market rent on owned assets
- Subtract all rent → get OpCo EBITDA (post-rent)
- PropCo NOI = all rent

---

## Issue: Rent Imputation Methods

### Current Method (Rent per Bed)

**Logic**: Use actual rent on leased facilities to calculate $/bed/year, then extrapolate to owned beds.

**Acute Care:**
- Actual rent on 1,246 leased beds: $99.1M
- Rent per leased bed: $99.1M ÷ 1,246 = **$79,535/bed/year**
- Imputed rent on 5,190 owned beds: $79,535 × 5,190 = **$413M**

**Behavioral Health:**
- Actual rent on 1,656 leased beds: $47.0M
- Rent per leased bed: $47.0M ÷ 1,656 = **$28,382/bed/year**
- Imputed rent on 22,465 owned beds: $28,382 × 22,465 = **$638M**

**Total Imputed Rent**: $1,050M
**Total Rent (actual + imputed)**: $1,196M

**PropCo NOI**: $1,196M
**PropCo Value (6.5% cap)**: $1,196M ÷ 0.065 = **$18,407M**

### Problem

Implied PropCo value of $18.4B vs actual PPE (net) of $6.6B = **2.8x book value**.

While real estate can trade above book (especially with depreciation), this seems aggressive and suggests:
1. Leased facilities may not be representative of owned facilities
2. Small sample size (only 2,902 leased beds out of 30,557 total = 9.5%)
3. Leased facilities might be newer/better quality than average owned

---

## Alternative Rent Imputation Methods

### Method 1: Rent per Bed (Current)
- **Pros**: Uses actual market data from UHS's leased facilities
- **Cons**: Small sample, may not be representative
- **Result**: $1,196M NOI → $18,407M PropCo value (2.8x book)

### Method 2: Rent as % of Revenue (Market Benchmark)
- **Logic**: Healthcare facilities typically pay 5-8% of revenue as rent
- **Conservative (5%)**: $15,817M × 5% = **$791M rent** → $12,169M PropCo value (1.9x book)
- **Mid-range (6.5%)**: $15,817M × 6.5% = **$1,028M rent** → $15,815M PropCo value (2.4x book)
- **Aggressive (8%)**: $15,817M × 8% = **$1,265M rent** → $19,462M PropCo value (3.0x book)

### Method 3: Implied from PPE Book Value
- **Logic**: Back into rent using cap rate and book value
- **PPE (net)**: $6,572M
- **At 6.5% cap**: $6,572M × 6.5% = **$427M NOI**
- **Result**: $427M rent → $6,572M PropCo value (1.0x book)
- **Issue**: This ignores that book value is depreciated (original cost - depreciation)

### Method 4: Implied from PPE Gross Value
- **PPE (gross)**: $11,802M (from 10-K)
- **At 6.5% cap**: $11,802M × 6.5% = **$767M NOI**
- **Result**: $767M rent → $11,803M PropCo value (1.8x book)

---

## Recommended Approach: Multiple Scenarios

Given the uncertainty, recommend presenting **three rent scenarios**:

### Conservative (Method 4: PPE Gross-Based)
- **Total Rent**: $767M ($620M imputed + $146M actual)
- **OpCo EBITDA**: $2,154M
- **PropCo NOI**: $767M
- **PropCo Value (6.5% cap)**: $11,803M

### Base Case (Method 2: 6% of Revenue)
- **Total Rent**: $949M ($803M imputed + $146M actual)
- **OpCo EBITDA**: $1,972M
- **PropCo NOI**: $949M
- **PropCo Value (6.5% cap)**: $14,600M

### Aggressive (Method 1: Rent per Bed)
- **Total Rent**: $1,196M ($1,050M imputed + $146M actual)
- **OpCo EBITDA**: $1,725M
- **PropCo NOI**: $1,196M
- **PropCo Value (6.5% cap)**: $18,407M

---

## Cap Rate vs Dividend Yield: The Bridge

### They Are NOT the Same Thing

**Cap Rate** (6.5%):
- Values the **real estate asset**
- Formula: `Property Value = NOI / Cap Rate`
- Represents **unlevered return** on the property

**Dividend Yield** (8.0% target):
- Return to **REIT equity holders**
- **After debt service** (leverage amplifies returns)
- Formula: `Equity Yield = (Cap Rate - (Debt Constant × LTV)) / (1 - LTV)`

### Can 6.5% Cap Rate Support 8% Dividend?

**Example** (using base case PropCo value of $14,600M):

```
PropCo NOI:              $949M
Cap Rate:                6.5%
PropCo Value:            $14,600M

Leverage Scenario:
  LTV:                   65%
  Debt:                  $9,490M
  Equity:                $5,110M

Debt Terms:
  Interest Rate:         6.0%
  Amortization:          1.0% (25-year am)
  Debt Constant:         7.0%

Debt Service:            $9,490M × 7.0% = $664M

Cash to Equity:          $949M - $664M = $285M
Equity Yield:            $285M / $5,110M = 5.6%

DSCR:                    $949M / $664M = 1.43x ✓
```

**Result**: At 65% LTV and 6% interest, equity yield is **5.6%**, **NOT 8%**.

### What Would Be Required for 8% Dividend?

To achieve 8% equity yield, you would need one or more of:

1. **Higher LTV** (e.g., 75-80%) - but DSCR would drop below 1.20x
2. **Lower debt cost** (e.g., 4-5% interest) - unrealistic in current environment
3. **Higher NOI** (i.e., higher imputed rent or lower cap rate)
4. **Accept lower DSCR** (e.g., 1.10x) - riskier

**Bottom Line**: An 8% dividend is **NOT feasible** with conservative REIT underwriting (DSCR ≥ 1.20x) at current debt costs, UNLESS you use the aggressive rent imputation method.

---

## SOTP Valuation Results (Base Case)

Using **Method 2** (6% of revenue) and **base multiples**:

| Component | EBITDA/NOI | Multiple | Value |
|-----------|-----------|----------|-------|
| **Behavioral OpCo** | $1,340M | 9.5x | $12,730M |
| **Behavioral PropCo** | $582M | 6.5% cap | $8,954M |
| **Acute OpCo** | $632M | 7.0x | $4,424M |
| **Acute PropCo** | $367M | 6.5% cap | $5,646M |
| **Total EV** | | | **$31,754M** |
| **Less: Net Debt** | | | ($4,379M) |
| **Equity Value** | | | **$27,375M** |
| **Value per Share** | | | **$421.28** |
| **Current Price** | | | $208.39 |
| **Upside** | | | **+102.1%** |

---

## Next Steps

1. **Validate rent assumptions** with market comps (REIT lease rates, Triple-Net healthcare)
2. **Refine OpCo multiples** with detailed comp analysis (ACHC, THC, etc.)
3. **Model synergies** if this is for Hill Valley acquisition
4. **Build sources & uses** if PropCo will fund the deal
5. **Sensitivity analysis** on all key assumptions

---

## Data Traceability

All numbers tied to 10-K:

| Data Point | 10-K Source |
|-----------|-------------|
| Segment EBITDA | Note 15 (Segment Reporting) |
| Actual Rent Expense | Income Statement by segment |
| Owned/Leased Mix | Note 9 (Related Party - UHT leases) |
| PPE Values | Balance Sheet (Property, Plant & Equipment) |
| Lease Obligations | Note 7 (Leases) |
| Net Debt | Balance Sheet & Debt Schedule |
| Shares Outstanding | Capital Structure note |

---

**Date**: October 30, 2025
**Model Version**: v3.0
**Status**: Methodology correct; rent imputation requires validation
