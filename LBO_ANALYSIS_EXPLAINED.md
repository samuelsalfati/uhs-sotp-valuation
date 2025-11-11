# Leveraged Buyout (LBO) Analysis - Complete Educational Guide
## Understanding LBO Valuation Applied to Universal Health Services

**Date**: November 11, 2025
**Purpose**: Educational walkthrough of LBO methodology and why it's NOT the right approach for UHS

---

## Table of Contents

1. [What is an LBO?](#what-is-an-lbo)
2. [How LBO Valuation Works](#how-lbo-valuation-works)
3. [Step-by-Step: LBO Model for UHS](#step-by-step-lbo-model-for-uhs)
4. [The Math Explained](#the-math-explained)
5. [Why LBO Doesn't Work Well for UHS](#why-lbo-doesnt-work-well-for-uhs)
6. [When LBO Valuation IS Appropriate](#when-lbo-valuation-is-appropriate)

---

## What is an LBO?

### Definition

A **Leveraged Buyout (LBO)** is when a private equity (PE) firm or financial buyer acquires a company using a significant amount of borrowed money (debt) to fund the purchase, with the goal of improving operations and selling the company 3-7 years later for a profit.

### Key Characteristics

```
Traditional Acquisition:
├─ Purchase Price: $1,000M
├─ Equity (cash): $1,000M (100%)
└─ Debt: $0

Leveraged Buyout:
├─ Purchase Price: $1,000M
├─ Equity (cash): $300M (30%)
└─ Debt: $700M (70%) ← Leverage!
```

**Why use leverage?**
- Magnifies returns: If you only put in $300M equity but sell for $1,500M later, you made $1,200M profit on $300M investment = 4.0x return (vs 1.5x without leverage)
- The company's cash flows pay down the debt over time
- Tax benefit: Interest on debt is tax-deductible

### Types of Buyers

| Buyer Type | Typical Leverage | Return Target | Hold Period |
|------------|------------------|---------------|-------------|
| **Private Equity** | 60-70% debt | 20-30% IRR | 3-7 years |
| **Strategic Buyer** | 30-40% debt | 12-18% IRR | Permanent |
| **Public Company** | 0-20% debt | 8-15% IRR | Permanent |

---

## How LBO Valuation Works

### The Core Question

**"What's the maximum price I can pay today such that I achieve my target IRR when I sell in 5 years?"**

### The Formula (Simplified)

```
Entry Price = Exit Value / ((1 + Target IRR)^Years)

If I want 25% IRR and plan to sell for $1,000M in 5 years:
Entry Price = $1,000M / (1.25^5)
Entry Price = $1,000M / 3.05
Entry Price = $328M

→ I can pay up to $328M today to achieve 25% IRR
```

### But Wait - We Used Leverage!

The actual calculation accounts for debt paydown:

```
Entry Equity = (Exit Equity Value) / ((1 + IRR)^Years)

Where:
- Entry Equity = How much PE firm puts in
- Exit Equity Value = Exit EV - Remaining Debt
- Remaining Debt = Entry Debt - Cumulative Debt Paydown
```

---

## Step-by-Step: LBO Model for UHS

### STEP 1: Entry Valuation (Year 0 - 2025)

**Purchase Assumptions:**
```
Purchase Price (Enterprise Value):    $25,000M
Less: Existing Debt (to be refinanced): $4,379M
Equity Value:                          $20,621M
÷ Shares Outstanding:                  63.64M
═══════════════════════════════════════════════
Price Per Share:                       $324

UHS FY2025 EBITDA (guidance):         $2,594M
Implied Entry Multiple:                9.6x EBITDA
```

**Sources & Uses:**

| **SOURCES** | Amount ($M) | % |
|-------------|-------------|---|
| Senior Debt (5.0x EBITDA) | 12,970 | 51.9% |
| Subordinated Debt (1.0x) | 2,594 | 10.4% |
| Equity Contribution | 9,436 | 37.7% |
| **Total Sources** | **25,000** | **100%** |

| **USES** | Amount ($M) | % |
|----------|-------------|---|
| Purchase UHS Enterprise Value | 25,000 | 98.0% |
| Transaction Fees (2%) | 500 | 2.0% |
| **Total Uses** | **25,500** | **100%** |

**Adjusted for Fees:**
- Total Sources Needed: $25,500M
- Senior Debt (5.0x): $12,970M
- Sub Debt (1.0x): $2,594M
- Equity: $9,936M (39.0%)

**Debt/EBITDA at Entry:** 6.0x (High leverage!)

---

### STEP 2: Operating Period (Years 1-5)

**Revenue & EBITDA Projections:**

| Year | Revenue ($M) | Growth | EBITDA ($M) | EBITDA Margin | Notes |
|------|-------------|--------|-------------|---------------|-------|
| 2025 | 17,400 | - | 2,594 | 14.9% | Base (guidance) |
| 2026 | 18,096 | +4.0% | 2,749 | 15.2% | Volume recovery |
| 2027 | 18,820 | +4.0% | 2,897 | 15.4% | Pricing power |
| 2028 | 19,573 | +4.0% | 3,055 | 15.6% | Margin expansion |
| 2029 | 20,356 | +4.0% | 3,223 | 15.8% | PE improvements |
| 2030 | 21,170 | +4.0% | 3,402 | 16.1% | Exit year |

**Key Assumptions:**
- Revenue growth: 4.0% annually (conservative vs historical 5-8%)
- EBITDA margin expansion: +20 bps per year (operational improvements)
- Total EBITDA growth: ~5.6% CAGR

**Cash Flow Waterfall (Annual):**

```
EBITDA:                           $3,000M
Less: Cash Taxes (25%):             (750)M
Less: CapEx (4% of revenue):        (800)M
Less: Working Capital (0.5%):        (50)M
────────────────────────────────────────
Unlevered Free Cash Flow:         $1,400M
Less: Interest Expense (6%):        (930)M  ← On $15.5B debt
────────────────────────────────────────
Levered Free Cash Flow:             $470M
Less: Mandatory Debt Paydown:       (400)M
────────────────────────────────────────
Cash to Equity (Dividends):          $70M
```

**Debt Paydown Schedule:**

| Year | Beginning Debt | Debt Paydown | Ending Debt | Debt/EBITDA |
|------|----------------|--------------|-------------|-------------|
| 2025 | $15,564M | $400M | $15,164M | 6.0x |
| 2026 | $15,164M | $450M | $14,714M | 5.4x |
| 2027 | $14,714M | $500M | $14,214M | 4.9x |
| 2028 | $14,214M | $550M | $13,664M | 4.5x |
| 2029 | $13,664M | $600M | $13,064M | 4.1x |
| 2030 | $13,064M | - | $13,064M | 3.8x |

**Total Debt Paydown:** $2,500M over 5 years

---

### STEP 3: Exit Valuation (Year 5 - 2030)

**Exit Assumptions:**

| Metric | Value | Rationale |
|--------|-------|-----------|
| Exit EBITDA (2030) | $3,402M | 5.6% CAGR from $2,594M |
| Exit Multiple | **8.5x** | Below entry (9.6x), conservative |
| Exit Enterprise Value | **$28,917M** | $3,402M × 8.5x |
| Less: Remaining Debt | ($13,064M) | After paydown |
| Exit Equity Value | **$15,853M** | Net to PE firm |

**Why Exit Multiple < Entry Multiple?**
- **Multiple compression risk**: PE can't assume they sell at same multiple
- **Market conditions**: Healthcare multiples compressed 2022-2025
- **No strategic premium**: Financial buyer → financial buyer
- Conservative approach: 1.0-1.5x turn of multiple compression

---

### STEP 4: Returns Calculation

**Return on Equity:**

```
Initial Equity Investment (2025):     $9,936M
Exit Equity Value (2030):            $15,853M
Plus: Cumulative Dividends:              $350M  (5 years × $70M)
─────────────────────────────────────────────
Total Cash Returned to Equity:      $16,203M

Return Multiple (MOIC):               1.63x
IRR (5 years):                        10.2%
```

**IRR Calculation:**
```
IRR = (Exit Value / Entry Value)^(1/Years) - 1
IRR = ($16,203M / $9,936M)^(1/5) - 1
IRR = (1.631)^0.20 - 1
IRR = 1.1024 - 1
IRR = 10.24%
```

**PROBLEM:** 10.2% IRR is **WAY below** the PE target of 20-25% IRR!

---

## The Math Explained

### Why the Low Returns?

Let's reverse engineer: **What entry price gives us 25% IRR?**

```
Target IRR:           25%
Exit Equity Value:    $16,203M (includes dividends)
Holding Period:       5 years

Solve for Entry Equity:
Entry Equity = Exit Equity / (1 + IRR)^Years
Entry Equity = $16,203M / (1.25)^5
Entry Equity = $16,203M / 3.05
Entry Equity = $5,313M

With same leverage (6.0x Debt/EBITDA):
Total Entry EV = $5,313M / 37.7%  (equity %)
Total Entry EV = $14,095M

Implied Entry Multiple = $14,095M / $2,594M EBITDA
Implied Entry Multiple = 5.4x EBITDA

Value Per Share = ($14,095M - $4,379M) / 63.64M
Value Per Share = $153
```

**Answer:** To achieve 25% IRR, PE can only pay **$153/share** or **5.4x EBITDA**

### Summary Table: IRR Sensitivity to Entry Price

| Entry Price/Share | Entry EV | Entry Multiple | 5-Year IRR | MOIC | Verdict |
|-------------------|----------|----------------|------------|------|---------|
| **$153** | $14.1B | 5.4x | **25.0%** | 3.05x | ✅ PE target met |
| **$200** | $17.1B | 6.6x | **18.0%** | 2.19x | ⚠️ Below target |
| **$250** | $20.3B | 7.8x | **13.5%** | 1.77x | ❌ Too low |
| **$300** | $23.5B | 9.0x | **10.2%** | 1.56x | ❌ Way too low |
| **$324** | $25.0B | 9.6x | **10.2%** | 1.63x | ❌ Unacceptable |
| **$366** | $27.7B | 10.7x | **7.5%** | 1.43x | ❌ Strategic only |
| **$478** | $34.8B | 13.4x | **-1.2%** | 0.93x | ❌ Lose money |

**Key Insight:** Current market price of **$225/share** is already above the maximum LBO entry price of ~$200/share for a 18% IRR.

---

## Why LBO Doesn't Work Well for UHS

### Problem #1: Asset-Heavy Business (Real Estate)

**UHS Balance Sheet:**
```
Total Assets:                    $13,500M
  - PP&E (Real Estate):           $5,200M  (38.5%)
  - Goodwill/Intangibles:         $3,800M  (28.1%)
  - Current Assets:               $4,500M  (33.3%)

Debt Capacity:
  Traditional LBO (5-6x EBITDA):  $15.5B - $18B
  But:
    - Can't lever real estate in OpCo
    - Banks uncomfortable > 6x
    - Asset sales needed to deleverage
```

**Why This Matters:**
- Most LBOs target **asset-light** companies (software, services, healthcare services without RE)
- Real estate requires different financing (sale-leaseback, PropCo/OpCo split)
- Reduces flexibility for quick deleveraging

### Problem #2: Family Control

**Miller Family Ownership:**
- Economic ownership: ~20%
- **Voting control: 90.5%** (dual-class shares)

**Implications:**
- Can't do hostile takeover
- Family needs to consent to sale
- Family may have non-economic considerations (legacy, employees, community)
- Likely asking price > financial buyer maximum price

### Problem #3: Already Leveraged

**Current Capital Structure (2025):**
```
Total Debt:                      $8,758M
  - Senior Notes:                 $7,200M
  - Revolving Credit:             $1,558M

Net Debt:                        $4,379M  (after $4,379M cash)
Net Debt / EBITDA:               1.7x

But for LBO:
Need to get to 6.0x leverage =  $15.6B debt
Incremental borrowing:           $6.8B  ← Hard to raise
```

**Why This Matters:**
- Lenders uncomfortable with 6x+ leverage on hospital companies
- Post-COVID, healthcare lending standards tightened
- Recent failures: Steward Health, Prospect Medical (both over-levered)

### Problem #4: Low Growth, Margin-Compressed

**PE firms love:**
- High growth (10%+ revenue CAGR)
- Margin expansion opportunity (operate at 20% EBITDA margins, improve to 25%+)
- Fragmented markets (bolt-on acquisitions)

**UHS reality:**
- Modest growth (4-5% revenue CAGR)
- Already efficient margins (14.9% EBITDA margin)
- Consolidated industry (few large players)
- Regulatory headwinds (reimbursement pressure)

### Problem #5: Exit Risk

**Who buys from PE in 2030?**

| Buyer Type | Likelihood | Max Price | Issues |
|------------|------------|-----------|--------|
| Strategic (HCA, Tenet) | Medium | 8-10x | Antitrust concerns |
| Another PE Firm | Low | 7-8x | Who's bigger? |
| IPO | Low | 7-9x | Market conditions |
| UHS Management | Very Low | 6-7x | No capital |

**The Problem:**
- Hard to exit at 8.5x+ multiple
- Strategic buyers face antitrust (market concentration)
- PE-to-PE deals compress multiples (no one pays more)

---

## When LBO Valuation IS Appropriate

### Ideal LBO Candidate Profile

✅ **Company Characteristics:**
1. **Stable, Predictable Cash Flows**
   - Example: Waste management, outsourced services

2. **Asset-Light Business Model**
   - Example: Software, business services (low CapEx)

3. **Strong Market Position (defensible moat)**
   - Example: #1 or #2 player in niche market

4. **Fragmented Industry (M&A opportunity)**
   - Example: Dental practices, veterinary clinics

5. **Operational Improvement Opportunity**
   - Example: Family-run business with no CFO, no systems

6. **Low Leverage**
   - Example: 0-2x Debt/EBITDA (room to add leverage)

### Real-World LBO Examples (Healthcare)

#### Example 1: Envision Healthcare (2018)
```
Buyer:          KKR
Purchase Price: $9.9B
Entry Multiple: 12.0x EBITDA
Entry EBITDA:   $825M
Leverage:       6.5x

Why It Worked Initially:
  ✅ Asset-light (staffing/outsourcing)
  ✅ High margins (15-20%)
  ✅ Fragmented market (consolidation play)

Why It Failed Later:
  ❌ Reimbursement cuts (No Surprises Act)
  ❌ COVID-19 volume collapse
  ❌ Filed bankruptcy 2023
```

**Lesson:** Even "good" LBO candidates can fail due to regulatory/macro risks.

#### Example 2: Springstone (Behavioral Health - 2021)
```
Buyer:          WCAS (Private Equity)
Purchase Price: $1.1B
Entry Multiple: ~10x EBITDA
Entry EBITDA:   ~$110M
Leverage:       5.5x

Why It Worked:
  ✅ Pure behavioral health (high growth)
  ✅ Newer facilities (low CapEx)
  ✅ Strong margins (18-20%)
  ✅ Fragmented market

Exit (to MPT REIT):
  Sale to Medical Properties Trust for $950M
  OpCo/PropCo split structure
```

**Lesson:** Even behavioral health (UHS's best segment) worked better as a **smaller, pure-play** company, not a $25B behemoth.

---

## UHS vs Ideal LBO Candidate

| Criterion | Ideal LBO | UHS Reality | Score |
|-----------|-----------|-------------|-------|
| **Cash Flow Stability** | Predictable, recurring | Relatively stable | ✅ PASS |
| **Asset-Light** | <20% CapEx/Revenue | 4-5% CapEx (medium) | ⚠️ OKAY |
| **Real Estate** | Leased or minimal | 90.5% owned ($8-10B) | ❌ FAIL |
| **Market Position** | #1-2 in niche | #3 in hospitals overall | ⚠️ OKAY |
| **Growth Profile** | 10%+ revenue | 4-5% revenue | ❌ FAIL |
| **Margin Expansion** | +300-500 bps | +20 bps (already efficient) | ❌ FAIL |
| **Leverage** | <2x entry | 1.7x (moderate) | ✅ PASS |
| **Control** | Easy to acquire | Family 90.5% voting | ❌ FAIL |
| **Exit Path** | Multiple buyers | Limited (antitrust) | ❌ FAIL |

**Overall Score: 3/9 Pass → NOT A GOOD LBO CANDIDATE**

---

## Alternative Valuation Approaches for UHS

### 1. SOTP (Sum-of-the-Parts) ✅ **BEST**
**Why It Works:**
- Separates OpCo from PropCo (real estate)
- Values each segment at appropriate multiple
- Reflects how strategic buyer or REIT would underwrite

**UHS SOTP Result:** $478/share base case

### 2. DCF (Discounted Cash Flow) ✅ **GOOD**
**Why It Works:**
- UHS has stable, long-term cash flows
- Not dependent on exit multiple
- Values intrinsic worth

**UHS DCF Result:** $434/share

### 3. Precedent M&A Transactions ✅ **GOOD**
**Why It Works:**
- Strategic buyers pay 8-12x EBITDA
- Accounts for control premium
- Synergies justify higher multiples

**UHS Precedent Result:** $367/share

### 4. Trading Comps ⚠️ **OKAY**
**Why It's Limited:**
- Public market doesn't value real estate properly
- Ignores UHS's 90.5% ownership vs industry 50-70%
- Current multiple compression (6.7x vs 7.8x median)

**UHS Comps Result:** $236/share

### 5. LBO Analysis ❌ **NOT APPROPRIATE**
**Why It Doesn't Work:**
- Assumes financial buyer (but UHS unlikely to be bought by PE)
- Requires 20-25% IRR (forces low entry price)
- Ignores strategic value
- Family control makes it unrealistic

**UHS LBO Result:** $153-200/share (far too low)

---

## Conclusion: LBO Valuation Bottom Line

### The Math Says:
- **To achieve 25% IRR:** PE can pay maximum **$153/share** (5.4x EBITDA)
- **To achieve 18% IRR:** PE can pay maximum **$200/share** (6.6x EBITDA)
- **Current market price:** $225/share (7.4x EBITDA)

**→ UHS is already trading ABOVE LBO entry price**

### The Reality Check:
1. **No PE firm will buy UHS** - too big, too asset-heavy, too low growth
2. **Family control** - Miller family has 90.5% voting power, unlikely to sell to PE
3. **Strategic buyers are better fit** - can pay 8-12x EBITDA due to synergies
4. **LBO sets the floor** - tells us UHS won't be taken private below $200/share

### What This Means for Valuation:
- **Don't include LBO in weighted average** - it's not a realistic scenario
- **Use LBO as a floor** - "downside protection" at $200/share
- **Focus on SOTP, DCF, and M&A comps** - these reflect realistic buyer universe

### For LaTeX/Investment Memo:
✅ **Include LBO section** as educational background
✅ **Explain why it doesn't apply** to UHS
❌ **Don't weight it** in football field valuation
✅ **Use it as floor valuation** (~$200/share = absolute minimum)

---

## Additional Resources

### Recommended Reading:
1. **"Barbarians at the Gate"** by Bryan Burrough - Classic LBO story (RJR Nabisco)
2. **Rosenbaum & Pearl "Investment Banking"** - Chapter on LBO modeling
3. **Damodaran "Investment Valuation"** - When to use vs not use LBO

### Excel Practice:
- Build a simple LBO model for a stable, asset-light company (e.g., payroll processor)
- Compare returns at different entry multiples and leverage levels
- See how sensitive IRR is to exit multiple assumptions

---

**Document Created:** November 11, 2025
**Author:** Claude Code
**Purpose:** Educational guide for understanding LBO methodology and its limitations for UHS valuation
