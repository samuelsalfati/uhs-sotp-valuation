"""
UHS Sum-of-the-Parts Valuation Analysis
CONFIDENTIAL & PROPRIETARY - Streamlit Dashboard

Inspired by Ora Living financial model design.
"""

import streamlit as st
import pandas as pd
import numpy as np
from model import (
    default_uhs_data, default_valuation_multiples,
    calculate_sotp, run_all_scenarios, sensitivity_analysis,
    CONFIDENTIALITY_NOTICE
)

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="UHS SOTP Valuation",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# CONFIDENTIALITY DISCLAIMER (ALWAYS VISIBLE)
# ==========================================

st.sidebar.markdown(f"""
<div style="background-color: #FFE6E6; padding: 15px; border-radius: 8px; border: 2px solid #FF4444; margin-bottom: 20px;">
    <h3 style="color: #CC0000; margin: 0;">⚠️ CONFIDENTIAL</h3>
    <p style="font-size: 11px; margin: 5px 0 0 0; color: #CC0000;">
        <b>PROPRIETARY ANALYSIS</b><br>
        This valuation model contains confidential financial projections and investment strategies.
        <b>Do not distribute or share.</b>
    </p>
</div>
""", unsafe_allow_html=True)

# ==========================================
# CUSTOM CSS (ORA LIVING BLUE THEME)
# ==========================================

st.markdown("""
<style>
    /* Light blue background */
    .stApp {
        background-color: #F8FCFD !important;
    }

    .main {
        background-color: #F8FCFD !important;
    }

    section[data-testid="stSidebar"] {
        background-color: #EBF7FA !important;
    }

    .block-container {
        background-color: #F8FCFD !important;
        padding-top: 2rem;
    }

    /* FIX: Make all text dark and visible */
    h1, h2, h3, h4, h5, h6 {
        color: #1E3A8A !important;
    }

    p, span, div, label, li {
        color: #1F2937 !important;
    }

    .stMarkdown {
        color: #1F2937 !important;
    }

    /* Metric containers with subtle white background */
    div[data-testid="metric-container"] {
        background-color: rgba(255, 255, 255, 0.8);
        padding: 15px;
        border-radius: 10px;
        border: 1px solid rgba(0, 183, 216, 0.2);
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }

    /* Metric text - make dark */
    div[data-testid="metric-container"] label {
        color: #374151 !important;
    }

    div[data-testid="metric-container"] [data-testid="stMetricValue"] {
        color: #1E3A8A !important;
    }

    div[data-testid="metric-container"] [data-testid="stMetricDelta"] {
        color: #059669 !important;
    }

    /* DataFrames clean white background */
    .stDataFrame {
        background-color: white;
        padding: 10px;
        border-radius: 8px;
    }

    /* Make table text visible */
    table {
        color: #1F2937 !important;
    }

    thead tr th {
        color: #1E3A8A !important;
        background-color: #F3F4F6 !important;
    }

    tbody tr td {
        color: #1F2937 !important;
    }

    /* Sidebar text - make dark */
    section[data-testid="stSidebar"] * {
        color: #1F2937 !important;
    }

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #1E3A8A !important;
    }

    /* Slider labels */
    .stSlider label {
        color: #374151 !important;
    }

    /* Radio button labels */
    .stRadio label {
        color: #374151 !important;
    }

    /* Blue sliders */
    div[data-baseweb="slider"] > div > div > div > div:nth-child(1) > div {
        background-color: rgb(0, 183, 216) !important;
    }

    div[data-baseweb="slider"] > div > div > div > div:nth-child(2) {
        background-color: rgb(0, 183, 216) !important;
    }

    div[role="slider"] {
        background-color: rgb(0, 183, 216) !important;
    }

    /* Tab styling - more prominent */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: rgba(255, 255, 255, 0.5);
        padding: 10px;
        border-radius: 10px;
    }

    .stTabs [data-baseweb="tab"] {
        background-color: white;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: 600;
        border: 1px solid rgba(0, 183, 216, 0.2);
    }

    .stTabs [aria-selected="true"] {
        background-color: rgb(0, 183, 216) !important;
        color: white !important;
    }

    /* Confidentiality banner at top */
    .confidential-banner {
        background: linear-gradient(135deg, #FF4444 0%, #CC0000 100%);
        color: white;
        padding: 10px 20px;
        text-align: center;
        font-weight: bold;
        margin-bottom: 20px;
        border-radius: 8px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# CONFIDENTIALITY BANNER (TOP OF PAGE)
# ==========================================

st.markdown("""
<div class="confidential-banner">
    ⚠️ CONFIDENTIAL & PROPRIETARY ANALYSIS - DO NOT DISTRIBUTE ⚠️
</div>
""", unsafe_allow_html=True)

# ==========================================
# HEADER
# ==========================================

st.title("🏥 Universal Health Services (UHS)")
st.subheader("Sum-of-the-Parts Valuation Analysis")
st.markdown("---")

# ==========================================
# LOAD DATA
# ==========================================

data = default_uhs_data()
multiples = default_valuation_multiples()

# ==========================================
# SIDEBAR CONTROLS
# ==========================================

st.sidebar.header("⚙️ Valuation Assumptions")

st.sidebar.markdown("### Operating Segment Multiples")

multiples["acute_care"]["base"] = st.sidebar.slider(
    "Acute Care EBITDA Multiple",
    min_value=5.0,
    max_value=10.0,
    value=7.0,
    step=0.5,
    help="Typical range: 6-8x for acute care hospitals"
)

multiples["behavioral"]["base"] = st.sidebar.slider(
    "Behavioral Health EBITDA Multiple",
    min_value=8.0,
    max_value=14.0,
    value=10.5,
    step=0.5,
    help="Typical range: 9-12x for behavioral health (higher quality)"
)

st.sidebar.markdown("### Real Estate Valuation")

re_method = st.sidebar.radio(
    "Primary RE Valuation Method",
    ["Cap Rate Method", "Per SqFt Market Value", "Higher of Both"],
    index=2
)

multiples["real_estate_cap_rate"]["base"] = st.sidebar.slider(
    "Capitalization Rate (%)",
    min_value=5.0,
    max_value=8.0,
    value=6.5,
    step=0.25,
) / 100

multiples["real_estate_sqft"]["base"] = st.sidebar.slider(
    "Market Value per SqFt ($)",
    min_value=200,
    max_value=600,
    value=400,
    step=25,
)

st.sidebar.markdown("### Corporate Overhead")

overhead_reduction_pct = st.sidebar.slider(
    "Overhead Reduction (%)",
    min_value=0,
    max_value=50,
    value=33,
    step=5,
    help="% reduction in corporate overhead post-separation"
) / 100

data["corporate_overhead"]["optimized_annual"] = (
    data["corporate_overhead"]["current_annual"] * (1 - overhead_reduction_pct)
)

# ==========================================
# CALCULATE SOTP
# ==========================================

base_result = calculate_sotp(data, multiples, "base")
scenarios_df = run_all_scenarios(data, multiples)

# ==========================================
# MAIN CONTENT TABS
# ==========================================

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📊 SOTP Summary",
    "🏥 Operating Segments",
    "🏢 Real Estate",
    "💰 Capital Structure",
    "📈 Scenarios & Sensitivity",
    "📋 Detailed Tables"
])

# ----- TAB 1: SOTP SUMMARY -----
with tab1:
    st.header("Sum-of-the-Parts Valuation Summary")

    # Key Metrics (Top Row)
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "SOTP Value per Share",
            f"${base_result['metrics']['SOTP Value per Share']:.2f}",
            delta=f"+${base_result['metrics']['Implied Upside ($)']:.2f}",
            delta_color="normal"
        )

    with col2:
        st.metric(
            "Current Share Price",
            f"${base_result['metrics']['Current Share Price']:.2f}"
        )

    with col3:
        upside_pct = base_result['metrics']['Implied Upside (%)'] * 100
        st.metric(
            "Implied Upside",
            f"{upside_pct:.1f}%",
            delta=f"${base_result['metrics']['Implied Upside ($)']:.2f}"
        )

    with col4:
        st.metric(
            "Total Equity Value",
            f"${base_result['metrics']['SOTP Equity Value']/1e9:.2f}B"
        )

    st.markdown("---")

    # SOTP Waterfall Chart
    st.subheader("Valuation Waterfall")

    components_df = pd.DataFrame({
        "Component": list(base_result["components"].keys()),
        "Value ($B)": [v/1e9 for v in base_result["components"].values()]
    })

    st.bar_chart(components_df.set_index("Component"))

    # Components Table
    st.subheader("Valuation Components Breakdown")

    components_display = []
    for comp, value in base_result["components"].items():
        components_display.append({
            "Component": comp,
            "Value ($M)": f"${value/1e6:,.0f}",
            "Value ($B)": f"${value/1e9:.2f}"
        })

    st.dataframe(pd.DataFrame(components_display), use_container_width=True)

    # Investment Thesis Summary
    st.markdown("---")
    st.subheader("💡 Investment Thesis")

    if upside_pct > 20:
        thesis_color = "#00CC00"
        thesis_text = "STRONG BUY"
    elif upside_pct > 10:
        thesis_color = "#66CC00"
        thesis_text = "BUY"
    else:
        thesis_color = "#FF8800"
        thesis_text = "HOLD"

    st.markdown(f"""
    <div style="background-color: rgba(255,255,255,0.8); padding: 20px; border-radius: 10px; border-left: 5px solid {thesis_color};">
        <h3 style="color: {thesis_color}; margin-top: 0;">Recommendation: {thesis_text}</h3>
        <p><b>Implied Upside:</b> {upside_pct:.1f}% (${base_result['metrics']['Implied Upside ($)']:.2f} per share)</p>
        <p><b>Key Drivers:</b></p>
        <ul>
            <li>Behavioral Health segment trading at premium multiples (10-12x EBITDA)</li>
            <li>Significant real estate value (~${base_result['components']['Real Estate Value']/1e9:.2f}B) hidden in balance sheet</li>
            <li>Corporate overhead reduction opportunity creates additional value</li>
            <li>Sum-of-parts significantly exceeds current market valuation</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# ----- TAB 2: OPERATING SEGMENTS -----
with tab2:
    st.header("Operating Segment Analysis")

    col1, col2 = st.columns(2)

    # Acute Care
    with col1:
        st.subheader("🏥 Acute Care Hospitals")
        acute = data["segments"]["acute_care"]

        st.metric("LTM Revenue", f"${acute.revenue/1e9:.2f}B")
        st.metric("LTM EBITDA", f"${acute.ebitda/1e9:.2f}B")
        st.metric("EBITDA Margin", f"{acute.ebitda_margin:.1%}")
        st.metric("Number of Facilities", f"{acute.facilities}")

        st.markdown(f"**Valuation Multiple:** {multiples['acute_care']['base']:.1f}x")
        st.metric(
            "Implied Enterprise Value",
            f"${base_result['components']['Acute Care EV']/1e9:.2f}B"
        )

    # Behavioral Health
    with col2:
        st.subheader("🧠 Behavioral Health")
        behavioral = data["segments"]["behavioral"]

        st.metric("LTM Revenue", f"${behavioral.revenue/1e9:.2f}B")
        st.metric("LTM EBITDA", f"${behavioral.ebitda/1e9:.2f}B")
        st.metric("EBITDA Margin", f"{behavioral.ebitda_margin:.1%}")
        st.metric("Number of Facilities", f"{behavioral.facilities}")

        st.markdown(f"**Valuation Multiple:** {multiples['behavioral']['base']:.1f}x")
        st.metric(
            "Implied Enterprise Value",
            f"${base_result['components']['Behavioral Health EV']/1e9:.2f}B"
        )

    st.markdown("---")

    # Segment Comparison
    st.subheader("Segment Comparison")

    segment_compare = pd.DataFrame({
        "Metric": ["Revenue ($B)", "EBITDA ($B)", "EBITDA Margin", "Facilities", "Multiple", "Enterprise Value ($B)"],
        "Acute Care": [
            f"${acute.revenue/1e9:.2f}",
            f"${acute.ebitda/1e9:.2f}",
            f"{acute.ebitda_margin:.1%}",
            acute.facilities,
            f"{multiples['acute_care']['base']:.1f}x",
            f"${base_result['components']['Acute Care EV']/1e9:.2f}"
        ],
        "Behavioral Health": [
            f"${behavioral.revenue/1e9:.2f}",
            f"${behavioral.ebitda/1e9:.2f}",
            f"{behavioral.ebitda_margin:.1%}",
            behavioral.facilities,
            f"{multiples['behavioral']['base']:.1f}x",
            f"${base_result['components']['Behavioral Health EV']/1e9:.2f}"
        ]
    })

    st.dataframe(segment_compare, use_container_width=True)

# ----- TAB 3: REAL ESTATE -----
with tab3:
    st.header("Real Estate Valuation")

    re = data["real_estate"]

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Book Value", f"${re.book_value/1e9:.2f}B")
        st.metric("Owned Sq Ft", f"{re.owned_sqft/1e6:.1f}M")

    with col2:
        st.metric("Market Value (SOTP)", f"${base_result['components']['Real Estate Value']/1e9:.2f}B")
        st.metric("Leased Sq Ft", f"{re.leased_sqft/1e6:.1f}M")

    with col3:
        implied_markup = (base_result['components']['Real Estate Value'] / re.book_value - 1) * 100
        st.metric("Value vs Book", f"+{implied_markup:.0f}%")
        st.metric("Total Sq Ft", f"{(re.owned_sqft + re.leased_sqft)/1e6:.1f}M")

    st.markdown("---")

    # Valuation Methods Comparison
    st.subheader("Valuation Methods")

    re_methods = pd.DataFrame({
        "Method": ["Cap Rate Method", "Per Sq Ft Market Value", "Book Value (for reference)"],
        "Calculation": [
            f"${re.annual_rent_potential/1e6:.0f}M rent / {multiples['real_estate_cap_rate']['base']:.2%} cap rate",
            f"{re.owned_sqft/1e6:.1f}M sqft × ${multiples['real_estate_sqft']['base']}/sqft",
            "Historical cost basis"
        ],
        "Value ($B)": [
            f"${base_result['real_estate_methods']['Cap Rate Method']/1e9:.2f}",
            f"${base_result['real_estate_methods']['Per SqFt Method']/1e9:.2f}",
            f"${re.book_value/1e9:.2f}"
        ]
    })

    st.dataframe(re_methods, use_container_width=True)

    st.info(f"**Method Used:** {re_method} = **${base_result['components']['Real Estate Value']/1e9:.2f}B**")

    # REIT Spin Analysis
    st.markdown("---")
    st.subheader("Potential REIT Spin-Off Analysis")

    st.markdown(f"""
    If UHS were to spin off its real estate into a separate REIT:

    - **Asset Value:** ${base_result['components']['Real Estate Value']/1e9:.2f}B
    - **Annual Rent (pro forma):** ${re.annual_rent_potential/1e6:.0f}M
    - **Implied Cap Rate:** {multiples['real_estate_cap_rate']['base']:.2%}
    - **REIT Yield to Investors:** ~5-6% (typical healthcare REIT)

    **Benefits:**
    - Unlock hidden real estate value
    - Create tax-efficient structure
    - Reduce OpCo leverage
    - Create two publicly-traded entities
    """)

# ----- TAB 4: CAPITAL STRUCTURE -----
with tab4:
    st.header("Capital Structure Analysis")

    capital = data["capital_structure"]

    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("Debt & Cash")
        st.metric("Total Debt", f"${capital.total_debt/1e9:.2f}B")
        st.metric("Cash", f"${capital.cash/1e9:.2f}B")
        st.metric("Net Debt", f"${capital.net_debt/1e9:.2f}B")

    with col2:
        st.subheader("Equity")
        st.metric("Shares Outstanding", f"{capital.shares_outstanding/1e6:.1f}M")
        st.metric("Current Share Price", f"${capital.share_price:.2f}")
        st.metric("Market Cap", f"${capital.market_cap/1e9:.2f}B")

    with col3:
        st.subheader("Enterprise Value")
        st.metric("Current EV", f"${capital.enterprise_value/1e9:.2f}B")
        st.metric("SOTP Equity Value", f"${base_result['metrics']['SOTP Equity Value']/1e9:.2f}B")
        sotp_ev = base_result['metrics']['SOTP Equity Value'] + capital.net_debt
        st.metric("SOTP Implied EV", f"${sotp_ev/1e9:.2f}B")

    st.markdown("---")

    # Debt to EBITDA
    st.subheader("Leverage Analysis")

    total_ebitda = data["segments"]["acute_care"].ebitda + data["segments"]["behavioral"].ebitda
    debt_to_ebitda = capital.net_debt / total_ebitda

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Total LTM EBITDA", f"${total_ebitda/1e9:.2f}B")
        st.metric("Net Debt / EBITDA", f"{debt_to_ebitda:.2f}x")

    with col2:
        st.metric("EV / EBITDA (Current)", f"{capital.enterprise_value / total_ebitda:.1f}x")
        st.metric("EV / EBITDA (SOTP)", f"{sotp_ev / total_ebitda:.1f}x")

    # Share Structure
    st.markdown("---")
    st.subheader("Share Structure")

    share_structure = pd.DataFrame({
        "Share Class": ["Class A (Common)", "Class B (if applicable)", "Diluted Shares"],
        "Shares Outstanding (M)": [
            f"{capital.class_a_shares/1e6:.2f}",
            f"{capital.class_b_shares/1e6:.2f}",
            f"{capital.diluted_shares/1e6:.2f}"
        ],
        "% of Total": [
            f"{capital.class_a_shares/capital.diluted_shares*100:.1f}%",
            f"{capital.class_b_shares/capital.diluted_shares*100:.1f}%",
            "100.0%"
        ]
    })

    st.dataframe(share_structure, use_container_width=True)

# ----- TAB 5: SCENARIOS & SENSITIVITY -----
with tab5:
    st.header("Scenario Analysis")

    # Scenario Comparison
    st.subheader("Bear / Base / Bull Scenarios")

    st.dataframe(
        scenarios_df.style.format({
            "SOTP Value per Share": "${:.2f}",
            "Implied Upside (%)": "{:.1f}%",
            "Acute Care EV": "${:.2f}B",
            "Behavioral EV": "${:.2f}B",
            "Real Estate Value": "${:.2f}B",
            "Total Equity Value": "${:.2f}B",
            "Current Price": "${:.2f}",
        }),
        use_container_width=True
    )

    # Scenario Chart
    st.subheader("Value per Share by Scenario")
    scenario_chart = scenarios_df[["SOTP Value per Share", "Current Price"]]
    st.bar_chart(scenario_chart)

    st.markdown("---")

    # Sensitivity Analysis
    st.subheader("Sensitivity Analysis")

    st.markdown("**Key Drivers:** Behavioral Health and Acute Care multiples have the largest impact on valuation.")

    # Simple sensitivity table
    sensitivity_data = []
    behavioral_mults = [9.0, 10.0, 10.5, 11.0, 12.0]

    for mult in behavioral_mults:
        temp_multiples = multiples.copy()
        temp_multiples["behavioral"]["base"] = mult
        result = calculate_sotp(data, temp_multiples, "base")

        sensitivity_data.append({
            "Behavioral Multiple": f"{mult:.1f}x",
            "Value per Share": f"${result['metrics']['SOTP Value per Share']:.2f}",
            "Upside": f"{result['metrics']['Implied Upside (%)']:.1%}"
        })

    st.dataframe(pd.DataFrame(sensitivity_data), use_container_width=True)

# ----- TAB 6: DETAILED TABLES -----
with tab6:
    st.header("Detailed Data Tables")

    # Export full results
    st.subheader("Complete SOTP Calculation")

    full_results = {
        "Component": list(base_result["components"].keys()),
        "Value ($M)": [v/1e6 for v in base_result["components"].values()],
        "Value ($B)": [v/1e9 for v in base_result["components"].values()],
    }

    full_df = pd.DataFrame(full_results)

    st.dataframe(full_df, use_container_width=True)

    # Download button
    csv = full_df.to_csv(index=False)
    st.download_button(
        "Download SOTP Calculation (CSV)",
        csv,
        "uhs_sotp_valuation.csv",
        "text/csv",
        key="download-sotp"
    )

    st.markdown("---")

    # Input Assumptions Summary
    st.subheader("Input Assumptions Summary")

    assumptions = {
        "Category": [
            "Acute Care Multiple",
            "Behavioral Health Multiple",
            "Real Estate Cap Rate",
            "Real Estate $/SqFt",
            "Overhead Reduction",
            "Shares Outstanding (M)",
            "Current Share Price",
            "Net Debt ($B)"
        ],
        "Value": [
            f"{multiples['acute_care']['base']:.1f}x",
            f"{multiples['behavioral']['base']:.1f}x",
            f"{multiples['real_estate_cap_rate']['base']:.2%}",
            f"${multiples['real_estate_sqft']['base']:.0f}",
            f"{overhead_reduction_pct:.0%}",
            f"{capital.shares_outstanding/1e6:.1f}",
            f"${capital.share_price:.2f}",
            f"${capital.net_debt/1e9:.2f}"
        ]
    }

    st.dataframe(pd.DataFrame(assumptions), use_container_width=True)

# ==========================================
# FOOTER
# ==========================================

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #CC0000; font-size: 12px; padding: 20px; background-color: rgba(255, 230, 230, 0.5); border-radius: 8px;">
    <b>⚠️ CONFIDENTIAL & PROPRIETARY ANALYSIS ⚠️</b><br>
    This valuation model is confidential and intended solely for authorized use.<br>
    Unauthorized distribution or disclosure is strictly prohibited.<br>
    © 2025 - All Rights Reserved
</div>
""", unsafe_allow_html=True)
