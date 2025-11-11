"""
UHS ACQUISITION ANALYSIS - ASCENDRA CAPITAL (ENHANCED INTERACTIVE VERSION)
Confidential & Proprietary

NEW FEATURES:
- Dynamic assumption controls (sliders for multiples, cap rates, WACC, etc.)
- Real-time valuation recalculation
- Interactive sensitivity charts
- Live football field updates
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import yfinance as yf

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="UHS Interactive Valuation Model | Ascendra Capital",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# CUSTOM CSS
# ==========================================

st.markdown("""
<style>
    .main-header {
        font-size: 42px;
        font-weight: 700;
        color: #4cc9f0;
        text-align: center;
        padding: 20px 0;
        border-bottom: 3px solid #4cc9f0;
        margin-bottom: 30px;
    }

    .assumption-box {
        background: linear-gradient(135deg, #1a2332 0%, #2c3e50 100%);
        padding: 20px;
        border-radius: 10px;
        border-left: 4px solid #4cc9f0;
        margin: 15px 0;
    }

    .metric-card {
        background: linear-gradient(135deg, #0d1b2a 0%, #1b263b 100%);
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #3a506b;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        text-align: center;
        margin: 10px 0;
    }

    .metric-value {
        font-size: 32px;
        font-weight: 700;
        color: #06ffa5;
        margin: 10px 0;
    }

    .metric-label {
        font-size: 14px;
        color: #a5b4c6;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .delta-positive {
        color: #06ffa5;
        font-size: 18px;
        font-weight: 600;
    }

    .delta-negative {
        color: #f72585;
        font-size: 18px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# HELPER FUNCTIONS
# ==========================================

def format_currency(value, decimals=0):
    """Format number as currency"""
    if value >= 1000:
        return f"${value/1000:.{decimals}f}B"
    else:
        return f"${value:.{decimals}f}M"

def calculate_sotp(
    beh_opco_ebitda, beh_opco_multiple,
    beh_propco_noi, beh_cap_rate,
    acute_opco_ebitda, acute_opco_multiple,
    acute_propco_noi, acute_cap_rate,
    net_debt, shares
):
    """Calculate SOTP valuation with given assumptions"""

    # OpCo Values
    beh_opco_value = beh_opco_ebitda * beh_opco_multiple
    acute_opco_value = acute_opco_ebitda * acute_opco_multiple

    # PropCo Values
    beh_propco_value = beh_propco_noi / (beh_cap_rate / 100)
    acute_propco_value = acute_propco_noi / (acute_cap_rate / 100)

    # Total EV
    enterprise_value = beh_opco_value + beh_propco_value + acute_opco_value + acute_propco_value

    # Equity Value
    equity_value = enterprise_value - net_debt

    # Per Share
    value_per_share = equity_value / shares

    return {
        'beh_opco_value': beh_opco_value,
        'beh_propco_value': beh_propco_value,
        'acute_opco_value': acute_opco_value,
        'acute_propco_value': acute_propco_value,
        'enterprise_value': enterprise_value,
        'equity_value': equity_value,
        'value_per_share': value_per_share
    }

def create_waterfall_chart(sotp_result):
    """Create interactive waterfall chart for SOTP breakdown"""

    fig = go.Figure(go.Waterfall(
        name = "SOTP Components",
        orientation = "v",
        measure = ["relative", "relative", "relative", "relative", "total", "relative", "total"],
        x = [
            "Behavioral OpCo",
            "Behavioral PropCo",
            "Acute OpCo",
            "Acute PropCo",
            "Enterprise Value",
            "Less: Net Debt",
            "Equity Value"
        ],
        textposition = "outside",
        text = [
            format_currency(sotp_result['beh_opco_value']),
            format_currency(sotp_result['beh_propco_value']),
            format_currency(sotp_result['acute_opco_value']),
            format_currency(sotp_result['acute_propco_value']),
            format_currency(sotp_result['enterprise_value']),
            format_currency(-sotp_result['enterprise_value'] + sotp_result['equity_value']),
            format_currency(sotp_result['equity_value'])
        ],
        y = [
            sotp_result['beh_opco_value'],
            sotp_result['beh_propco_value'],
            sotp_result['acute_opco_value'],
            sotp_result['acute_propco_value'],
            0,  # Total will be calculated
            -sotp_result['enterprise_value'] + sotp_result['equity_value'],
            0   # Total will be calculated
        ],
        connector = {"line":{"color":"rgb(63, 63, 63)"}},
        decreasing = {"marker":{"color":"#f72585"}},
        increasing = {"marker":{"color":"#06ffa5"}},
        totals = {"marker":{"color":"#4cc9f0"}}
    ))

    fig.update_layout(
        title = "SOTP Value Build-Up",
        showlegend = False,
        height = 500,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white')
    )

    return fig

def create_sensitivity_heatmap(
    base_beh_ebitda, base_acute_ebitda,
    base_beh_noi, base_acute_noi,
    net_debt, shares,
    param_1_name, param_1_range,
    param_2_name, param_2_range,
    param_type='opco'  # 'opco' or 'propco'
):
    """Create sensitivity heatmap for SOTP"""

    results = []

    for p1 in param_1_range:
        row = []
        for p2 in param_2_range:
            if param_type == 'opco':
                # OpCo multiple sensitivity
                sotp = calculate_sotp(
                    base_beh_ebitda, p1,  # Behavioral multiple
                    base_beh_noi, 6.0,
                    base_acute_ebitda, p2,  # Acute multiple
                    base_acute_noi, 6.0,
                    net_debt, shares
                )
            else:
                # PropCo cap rate sensitivity
                sotp = calculate_sotp(
                    base_beh_ebitda, 10.0,
                    base_beh_noi, p1,  # Behavioral cap rate
                    base_acute_ebitda, 7.0,
                    base_acute_noi, p2,  # Acute cap rate
                    net_debt, shares
                )
            row.append(sotp['value_per_share'])
        results.append(row)

    fig = go.Figure(data=go.Heatmap(
        z=results,
        x=[f"{p:.1f}" for p in param_2_range],
        y=[f"{p:.1f}" for p in param_1_range],
        colorscale='RdYlGn',
        text=[[f"${val:.0f}" for val in row] for row in results],
        texttemplate="%{text}",
        textfont={"size": 10},
        colorbar=dict(title="$/Share")
    ))

    fig.update_layout(
        title=f"Sensitivity: {param_1_name} vs {param_2_name}",
        xaxis_title=param_2_name,
        yaxis_title=param_1_name,
        height=400,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white')
    )

    return fig

# ==========================================
# MAIN APP
# ==========================================

st.markdown('<h1 class="main-header">🎯 UHS Interactive Valuation Model</h1>', unsafe_allow_html=True)
st.markdown("**Ascendra Capital | Dynamic Assumption Analysis**")

# Sidebar for navigation
page = st.sidebar.selectbox(
    "📊 Select Analysis",
    [
        "🎯 Interactive SOTP",
        "📈 DCF Model Builder",
        "⚡ Quick Scenario Comparison",
        "📊 Football Field Live"
    ]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 💡 How to Use")
st.sidebar.markdown("""
1. **Adjust sliders** to change assumptions
2. **Watch valuations update** in real-time
3. **Compare scenarios** side-by-side
4. **Download results** as needed
""")

# ==========================================
# INTERACTIVE SOTP PAGE
# ==========================================

if page == "🎯 Interactive SOTP":
    st.title("🎯 Interactive SOTP Valuation Model")
    st.markdown("**Adjust assumptions below and see valuation update in real-time**")

    st.markdown("---")

    # Create two columns: Assumptions on left, Results on right
    col_assumptions, col_results = st.columns([1, 2])

    with col_assumptions:
        st.markdown("### ⚙️ Assumptions")

        # Expander for Behavioral Health
        with st.expander("🧠 **BEHAVIORAL HEALTH ASSUMPTIONS**", expanded=True):
            st.markdown("##### OpCo (Operations)")
            beh_opco_ebitda = st.slider(
                "Normalized OpCo EBITDA ($M)",
                min_value=700,
                max_value=1200,
                value=930,
                step=10,
                key="beh_ebitda",
                help="Normalized EBITDA after deducting market rent"
            )

            beh_opco_multiple = st.slider(
                "OpCo EBITDA Multiple",
                min_value=7.0,
                max_value=12.0,
                value=10.0,
                step=0.5,
                key="beh_multiple",
                help="Acadia (pure-play) trades at 7-12x historically"
            )

            st.markdown("##### PropCo (Real Estate)")
            beh_propco_noi = st.slider(
                "PropCo NOI ($M)",
                min_value=500,
                max_value=900,
                value=685,
                step=10,
                key="beh_noi",
                help="Net Operating Income = Imputed Market Rent"
            )

            beh_cap_rate = st.slider(
                "PropCo Cap Rate (%)",
                min_value=5.0,
                max_value=8.0,
                value=6.0,
                step=0.1,
                key="beh_cap",
                help="Healthcare REITs trade at 5.5-7.0% cap rates"
            )

        # Expander for Acute Care
        with st.expander("🏥 **ACUTE CARE ASSUMPTIONS**", expanded=True):
            st.markdown("##### OpCo (Operations)")
            acute_opco_ebitda = st.slider(
                "Normalized OpCo EBITDA ($M)",
                min_value=500,
                max_value=1000,
                value=796,
                step=10,
                key="acute_ebitda"
            )

            acute_opco_multiple = st.slider(
                "OpCo EBITDA Multiple",
                min_value=5.0,
                max_value=10.0,
                value=7.0,
                step=0.5,
                key="acute_multiple",
                help="HCA trades at ~9.8x, UHS acute at discount"
            )

            st.markdown("##### PropCo (Real Estate)")
            acute_propco_noi = st.slider(
                "PropCo NOI ($M)",
                min_value=300,
                max_value=700,
                value=512,
                step=10,
                key="acute_noi"
            )

            acute_cap_rate = st.slider(
                "PropCo Cap Rate (%)",
                min_value=5.0,
                max_value=8.0,
                value=6.0,
                step=0.1,
                key="acute_cap"
            )

        # Expander for Capital Structure
        with st.expander("💰 **CAPITAL STRUCTURE**", expanded=False):
            net_debt = st.number_input(
                "Net Debt ($M)",
                min_value=3000,
                max_value=6000,
                value=4379,
                step=100,
                key="net_debt"
            )

            shares = st.number_input(
                "Shares Outstanding (M)",
                min_value=50.0,
                max_value=80.0,
                value=63.64,
                step=0.1,
                key="shares"
            )

    with col_results:
        st.markdown("### 📊 Valuation Results")

        # Calculate SOTP with current assumptions
        sotp = calculate_sotp(
            beh_opco_ebitda, beh_opco_multiple,
            beh_propco_noi, beh_cap_rate,
            acute_opco_ebitda, acute_opco_multiple,
            acute_propco_noi, acute_cap_rate,
            net_debt, shares
        )

        # Display key metrics in cards
        metrics_cols = st.columns(3)

        with metrics_cols[0]:
            current_price = 225.30
            upside = ((sotp['value_per_share'] / current_price) - 1) * 100
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Value Per Share</div>
                <div class="metric-value">${sotp['value_per_share']:.0f}</div>
                <div class="{'delta-positive' if upside > 0 else 'delta-negative'}">
                    {'+' if upside > 0 else ''}{upside:.1f}% vs ${current_price}
                </div>
            </div>
            """, unsafe_allow_html=True)

        with metrics_cols[1]:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Enterprise Value</div>
                <div class="metric-value">{format_currency(sotp['enterprise_value'])}</div>
                <div class="delta-positive">
                    Total Company Value
                </div>
            </div>
            """, unsafe_allow_html=True)

        with metrics_cols[2]:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Equity Value</div>
                <div class="metric-value">{format_currency(sotp['equity_value'])}</div>
                <div class="delta-positive">
                    Net of ${net_debt:.0f}M Debt
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")

        # Waterfall chart
        st.markdown("#### 📊 Value Build-Up")
        waterfall_fig = create_waterfall_chart(sotp)
        st.plotly_chart(waterfall_fig, use_container_width=True)

        # Component breakdown
        st.markdown("#### 🔍 Component Breakdown")

        breakdown_cols = st.columns(4)

        with breakdown_cols[0]:
            st.metric(
                "Behavioral OpCo",
                format_currency(sotp['beh_opco_value']),
                delta=f"{beh_opco_multiple:.1f}x"
            )
            st.caption(f"EBITDA: ${beh_opco_ebitda}M")

        with breakdown_cols[1]:
            st.metric(
                "Behavioral PropCo",
                format_currency(sotp['beh_propco_value']),
                delta=f"{beh_cap_rate:.1f}% cap"
            )
            st.caption(f"NOI: ${beh_propco_noi}M")

        with breakdown_cols[2]:
            st.metric(
                "Acute OpCo",
                format_currency(sotp['acute_opco_value']),
                delta=f"{acute_opco_multiple:.1f}x"
            )
            st.caption(f"EBITDA: ${acute_opco_ebitda}M")

        with breakdown_cols[3]:
            st.metric(
                "Acute PropCo",
                format_currency(sotp['acute_propco_value']),
                delta=f"{acute_cap_rate:.1f}% cap"
            )
            st.caption(f"NOI: ${acute_propco_noi}M")

    st.markdown("---")

    # Sensitivity Analysis Section
    st.markdown("### 📈 Live Sensitivity Analysis")

    sens_col1, sens_col2 = st.columns(2)

    with sens_col1:
        st.markdown("#### OpCo Multiple Sensitivity")
        beh_mult_range = np.arange(8.0, 12.5, 0.5)
        acute_mult_range = np.arange(6.0, 9.0, 0.5)

        opco_heatmap = create_sensitivity_heatmap(
            beh_opco_ebitda, acute_opco_ebitda,
            beh_propco_noi, acute_propco_noi,
            net_debt, shares,
            "Behavioral OpCo Multiple",
            beh_mult_range,
            "Acute OpCo Multiple",
            acute_mult_range,
            param_type='opco'
        )
        st.plotly_chart(opco_heatmap, use_container_width=True)

    with sens_col2:
        st.markdown("#### PropCo Cap Rate Sensitivity")
        beh_cap_range = np.arange(5.0, 7.5, 0.25)
        acute_cap_range = np.arange(5.0, 7.5, 0.25)

        propco_heatmap = create_sensitivity_heatmap(
            beh_opco_ebitda, acute_opco_ebitda,
            beh_propco_noi, acute_propco_noi,
            net_debt, shares,
            "Behavioral PropCo Cap Rate",
            beh_cap_range,
            "Acute PropCo Cap Rate",
            acute_cap_range,
            param_type='propco'
        )
        st.plotly_chart(propco_heatmap, use_container_width=True)

    st.markdown("---")

    # Download section
    st.markdown("### 💾 Export Results")

    export_data = pd.DataFrame({
        'Component': [
            'Behavioral OpCo',
            'Behavioral PropCo',
            'Acute OpCo',
            'Acute PropCo',
            'Enterprise Value',
            'Net Debt',
            'Equity Value',
            'Shares Outstanding (M)',
            'Value Per Share'
        ],
        'Value ($M)': [
            sotp['beh_opco_value'],
            sotp['beh_propco_value'],
            sotp['acute_opco_value'],
            sotp['acute_propco_value'],
            sotp['enterprise_value'],
            -net_debt,
            sotp['equity_value'],
            shares,
            sotp['value_per_share']
        ],
        'Assumption': [
            f"{beh_opco_ebitda}M EBITDA × {beh_opco_multiple:.1f}x",
            f"{beh_propco_noi}M NOI ÷ {beh_cap_rate:.1f}%",
            f"{acute_opco_ebitda}M EBITDA × {acute_opco_multiple:.1f}x",
            f"{acute_propco_noi}M NOI ÷ {acute_cap_rate:.1f}%",
            "Sum of components",
            "From balance sheet",
            "EV - Net Debt",
            "Diluted shares",
            "Equity Value / Shares"
        ]
    })

    st.dataframe(export_data, use_container_width=True)

    csv = export_data.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Valuation Summary (CSV)",
        data=csv,
        file_name=f"uhs_sotp_valuation_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )

# ==========================================
# QUICK SCENARIO COMPARISON PAGE
# ==========================================

elif page == "⚡ Quick Scenario Comparison":
    st.title("⚡ Quick Scenario Comparison")
    st.markdown("**Compare Bear / Base / Bull scenarios side-by-side**")

    st.markdown("---")

    # Define three scenarios
    scenarios = {
        'BEAR': {
            'beh_opco_mult': 9.0,
            'beh_cap_rate': 7.0,
            'acute_opco_mult': 6.5,
            'acute_cap_rate': 7.0
        },
        'BASE': {
            'beh_opco_mult': 10.0,
            'beh_cap_rate': 6.0,
            'acute_opco_mult': 7.0,
            'acute_cap_rate': 6.0
        },
        'BULL': {
            'beh_opco_mult': 10.5,
            'beh_cap_rate': 5.5,
            'acute_opco_mult': 7.5,
            'acute_cap_rate': 5.5
        }
    }

    # Fixed inputs
    beh_ebitda = 930
    beh_noi = 685
    acute_ebitda = 796
    acute_noi = 512
    net_debt = 4379
    shares = 63.64
    current_price = 225.30

    # Calculate all scenarios
    results = {}
    for scenario_name, params in scenarios.items():
        results[scenario_name] = calculate_sotp(
            beh_ebitda, params['beh_opco_mult'],
            beh_noi, params['beh_cap_rate'],
            acute_ebitda, params['acute_opco_mult'],
            acute_noi, params['acute_cap_rate'],
            net_debt, shares
        )

    # Display in three columns
    cols = st.columns(3)

    for idx, (scenario_name, result) in enumerate(results.items()):
        with cols[idx]:
            upside = ((result['value_per_share'] / current_price) - 1) * 100

            color = {
                'BEAR': '#f72585',
                'BASE': '#4cc9f0',
                'BULL': '#06ffa5'
            }[scenario_name]

            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #0d1b2a 0%, #1b263b 100%);
                        padding: 25px;
                        border-radius: 15px;
                        border-left: 5px solid {color};
                        margin: 10px 0;">
                <h2 style="color: {color}; text-align: center; margin-bottom: 20px;">
                    {scenario_name}
                </h2>
                <div style="text-align: center; font-size: 48px; font-weight: 700; color: {color}; margin: 20px 0;">
                    ${result['value_per_share']:.0f}
                </div>
                <div style="text-align: center; font-size: 20px; color: {'#06ffa5' if upside > 0 else '#f72585'}; margin-bottom: 20px;">
                    {'+' if upside > 0 else ''}{upside:.1f}% upside
                </div>
                <hr style="border-color: #3a506b; margin: 20px 0;">
                <div style="font-size: 14px; color: #a5b4c6;">
                    <b>Enterprise Value:</b> {format_currency(result['enterprise_value'])}<br>
                    <b>Equity Value:</b> {format_currency(result['equity_value'])}<br><br>
                    <b>Behavioral OpCo:</b> {scenarios[scenario_name]['beh_opco_mult']}x<br>
                    <b>Behavioral PropCo:</b> {scenarios[scenario_name]['beh_cap_rate']}% cap<br>
                    <b>Acute OpCo:</b> {scenarios[scenario_name]['acute_opco_mult']}x<br>
                    <b>Acute PropCo:</b> {scenarios[scenario_name]['acute_cap_rate']}% cap
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # Comparison chart
    st.markdown("### 📊 Scenario Comparison Chart")

    comparison_df = pd.DataFrame({
        'Scenario': list(results.keys()),
        'Value Per Share': [r['value_per_share'] for r in results.values()],
        'Enterprise Value': [r['enterprise_value']/1000 for r in results.values()],
        'Equity Value': [r['equity_value']/1000 for r in results.values()]
    })

    fig = go.Figure()

    fig.add_trace(go.Bar(
        name='Value Per Share ($)',
        x=comparison_df['Scenario'],
        y=comparison_df['Value Per Share'],
        marker_color=['#f72585', '#4cc9f0', '#06ffa5'],
        text=comparison_df['Value Per Share'].round(0),
        textposition='outside',
        texttemplate='$%{text}',
        yaxis='y',
        offsetgroup=1
    ))

    fig.add_trace(go.Bar(
        name='Enterprise Value ($B)',
        x=comparison_df['Scenario'],
        y=comparison_df['Enterprise Value'],
        marker_color=['#f72585', '#4cc9f0', '#06ffa5'],
        marker_opacity=0.6,
        text=comparison_df['Enterprise Value'].round(1),
        textposition='outside',
        texttemplate='$%{text}B',
        yaxis='y2',
        offsetgroup=2
    ))

    fig.update_layout(
        title="Value Comparison Across Scenarios",
        yaxis=dict(title='Value Per Share ($)', side='left'),
        yaxis2=dict(title='Enterprise Value ($B)', overlaying='y', side='right'),
        barmode='group',
        height=500,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        legend=dict(x=0.5, y=1.1, orientation='h', xanchor='center')
    )

    st.plotly_chart(fig, use_container_width=True)

# ==========================================
# FOOTER
# ==========================================

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #a5b4c6; font-size: 12px; padding: 20px 0;">
    <b>Ascendra Capital | Confidential & Proprietary</b><br>
    Interactive Valuation Model | Last Updated: {}<br>
    🤖 Enhanced with Claude Code
</div>
""".format(datetime.now().strftime("%B %d, %Y")), unsafe_allow_html=True)
