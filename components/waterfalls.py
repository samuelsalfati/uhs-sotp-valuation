"""
Waterfall Chart Components using Plotly
For SOTP, DCF, LBO, and Synergies value bridges
"""

import plotly.graph_objects as go
import pandas as pd
import streamlit as st


def create_sotp_waterfall(current_price, behavioral_opco, behavioral_propco, acute_opco, acute_propco, net_debt, shares):
    """
    Create SOTP value bridge waterfall chart
    Shows progression from current price to fair value
    """
    # Calculate incremental values
    total_ev = behavioral_opco + behavioral_propco + acute_opco + acute_propco
    equity_value = total_ev - net_debt
    fair_value_per_share = equity_value / shares

    # Prepare waterfall data
    categories = [
        "Current Price",
        "Behavioral OpCo",
        "Behavioral PropCo",
        "Acute OpCo",
        "Acute PropCo",
        "Less: Net Debt",
        "Fair Value"
    ]

    values = [
        current_price,
        behavioral_opco / shares,
        behavioral_propco / shares,
        acute_opco / shares,
        acute_propco / shares,
        -(net_debt / shares),
        0  # Will be calculated as cumulative
    ]

    # Create Plotly waterfall
    fig = go.Figure(go.Waterfall(
        name="SOTP Value Bridge",
        orientation="v",
        measure=["absolute", "relative", "relative", "relative", "relative", "relative", "total"],
        x=categories,
        textposition="outside",
        text=[f"${v:,.0f}" for v in values[:-1]] + [f"${fair_value_per_share:,.0f}"],
        y=values,
        connector={"line": {"color": "#2d3e50", "width": 2}},
        increasing={"marker": {"color": "#06ffa5"}},
        decreasing={"marker": {"color": "#ff006e"}},
        totals={"marker": {"color": "#4cc9f0"}}
    ))

    fig.update_layout(
        title={
            'text': "SOTP Value Bridge: Current Price → Fair Value",
            'font': {'size': 20, 'color': '#4cc9f0', 'family': 'Arial Black'},
            'x': 0.5,
            'xanchor': 'center'
        },
        yaxis_title="Value per Share ($)",
        paper_bgcolor='#0a1929',
        plot_bgcolor='#1b263b',
        font=dict(color='#e0e1dd', size=12),
        height=500,
        showlegend=False,
        xaxis=dict(
            showgrid=False,
            tickfont=dict(size=11, color='#e0e1dd')
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='#2d3e50',
            tickfont=dict(size=11, color='#e0e1dd'),
            tickformat='$,.0f'
        ),
        margin=dict(t=80, b=80, l=80, r=80)
    ))

    return fig


def create_synergies_waterfall(base_ebitda, synergies_dict):
    """
    Create synergies EBITDA waterfall chart
    Shows progression from base EBITDA to pro-forma EBITDA with synergies

    synergies_dict: {"Category Name": savings_amount}
    """
    categories = ["Base EBITDA"] + list(synergies_dict.keys()) + ["Pro-forma EBITDA"]
    values = [base_ebitda] + list(synergies_dict.values()) + [0]

    proforma_ebitda = base_ebitda + sum(synergies_dict.values())

    measure = ["absolute"] + ["relative"] * len(synergies_dict) + ["total"]

    fig = go.Figure(go.Waterfall(
        name="Synergies Impact",
        orientation="v",
        measure=measure,
        x=categories,
        textposition="outside",
        text=[f"${base_ebitda:,.0f}M"] + [f"+${v:,.0f}M" for v in synergies_dict.values()] + [f"${proforma_ebitda:,.0f}M"],
        y=values,
        connector={"line": {"color": "#2d3e50", "width": 2}},
        increasing={"marker": {"color": "#06ffa5"}},
        decreasing={"marker": {"color": "#ff006e"}},
        totals={"marker": {"color": "#4cc9f0"}}
    ))

    fig.update_layout(
        title={
            'text': "Cost Synergies Impact on EBITDA",
            'font': {'size': 20, 'color': '#4cc9f0', 'family': 'Arial Black'},
            'x': 0.5,
            'xanchor': 'center'
        },
        yaxis_title="EBITDA ($M)",
        paper_bgcolor='#0a1929',
        plot_bgcolor='#1b263b',
        font=dict(color='#e0e1dd', size=12),
        height=500,
        showlegend=False,
        xaxis=dict(
            showgrid=False,
            tickfont=dict(size=10, color='#e0e1dd'),
            tickangle=-30
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='#2d3e50',
            tickfont=dict(size=11, color='#e0e1dd'),
            tickformat='$,.0f'
        ),
        margin=dict(t=80, b=120, l=80, r=80)
    ))

    return fig


def create_dcf_waterfall(fcf_years, terminal_value):
    """
    Create DCF present value waterfall chart
    Shows PV of FCF for years 1-10 plus terminal value

    fcf_years: list of 10 PV(FCF) values
    terminal_value: PV of terminal value
    """
    categories = [f"Year {i+1}" for i in range(len(fcf_years))] + ["Terminal Value", "Enterprise Value"]
    values = fcf_years + [terminal_value, 0]

    enterprise_value = sum(fcf_years) + terminal_value

    measure = ["relative"] * (len(fcf_years) + 1) + ["total"]

    text_values = [f"${v:,.0f}M" for v in fcf_years] + [f"${terminal_value:,.0f}M", f"${enterprise_value:,.0f}M"]

    fig = go.Figure(go.Waterfall(
        name="DCF Components",
        orientation="v",
        measure=measure,
        x=categories,
        textposition="outside",
        text=text_values,
        y=values,
        connector={"line": {"color": "#2d3e50", "width": 2}},
        increasing={"marker": {"color": "#06ffa5"}},
        decreasing={"marker": {"color": "#ff006e"}},
        totals={"marker": {"color": "#4cc9f0"}}
    ))

    fig.update_layout(
        title={
            'text': "DCF Value Breakdown: Present Value Components",
            'font': {'size': 20, 'color': '#4cc9f0', 'family': 'Arial Black'},
            'x': 0.5,
            'xanchor': 'center'
        },
        yaxis_title="Present Value ($M)",
        paper_bgcolor='#0a1929',
        plot_bgcolor='#1b263b',
        font=dict(color='#e0e1dd', size=12),
        height=550,
        showlegend=False,
        xaxis=dict(
            showgrid=False,
            tickfont=dict(size=9, color='#e0e1dd'),
            tickangle=-45
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='#2d3e50',
            tickfont=dict(size=11, color='#e0e1dd'),
            tickformat='$,.0f'
        ),
        margin=dict(t=80, b=140, l=80, r=80)
    ))

    return fig


def create_lbo_waterfall(entry_price, ebitda_growth, debt_paydown, multiple_expansion, exit_value):
    """
    Create LBO returns waterfall chart
    Shows how returns are generated from entry to exit

    entry_price: Initial equity investment
    ebitda_growth: Value from EBITDA growth
    debt_paydown: Value from debt reduction
    multiple_expansion: Value from multiple expansion
    exit_value: Total exit equity value (should equal sum)
    """
    categories = [
        "Entry Equity",
        "EBITDA Growth",
        "Debt Paydown",
        "Multiple Expansion",
        "Exit Equity Value"
    ]

    values = [
        entry_price,
        ebitda_growth,
        debt_paydown,
        multiple_expansion,
        0  # Will be calculated as total
    ]

    measure = ["absolute", "relative", "relative", "relative", "total"]

    text_values = [
        f"${entry_price:,.0f}M",
        f"+${ebitda_growth:,.0f}M",
        f"+${debt_paydown:,.0f}M",
        f"+${multiple_expansion:,.0f}M",
        f"${exit_value:,.0f}M"
    ]

    fig = go.Figure(go.Waterfall(
        name="LBO Returns",
        orientation="v",
        measure=measure,
        x=categories,
        textposition="outside",
        text=text_values,
        y=values,
        connector={"line": {"color": "#2d3e50", "width": 2}},
        increasing={"marker": {"color": "#06ffa5"}},
        decreasing={"marker": {"color": "#ff006e"}},
        totals={"marker": {"color": "#4cc9f0"}}
    ))

    moic = exit_value / entry_price if entry_price > 0 else 0

    fig.update_layout(
        title={
            'text': f"LBO Returns Bridge (MOIC: {moic:.2f}x)",
            'font': {'size': 20, 'color': '#4cc9f0', 'family': 'Arial Black'},
            'x': 0.5,
            'xanchor': 'center'
        },
        yaxis_title="Equity Value ($M)",
        paper_bgcolor='#0a1929',
        plot_bgcolor='#1b263b',
        font=dict(color='#e0e1dd', size=12),
        height=500,
        showlegend=False,
        xaxis=dict(
            showgrid=False,
            tickfont=dict(size=11, color='#e0e1dd')
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='#2d3e50',
            tickfont=dict(size=11, color='#e0e1dd'),
            tickformat='$,.0f'
        ),
        margin=dict(t=80, b=80, l=80, r=80)
    ))

    return fig


def render_waterfall(chart_type, **kwargs):
    """
    Render a waterfall chart in Streamlit

    chart_type: "sotp", "synergies", "dcf", or "lbo"
    **kwargs: Arguments specific to each chart type
    """
    if chart_type == "sotp":
        fig = create_sotp_waterfall(**kwargs)
    elif chart_type == "synergies":
        fig = create_synergies_waterfall(**kwargs)
    elif chart_type == "dcf":
        fig = create_dcf_waterfall(**kwargs)
    elif chart_type == "lbo":
        fig = create_lbo_waterfall(**kwargs)
    else:
        st.error(f"Unknown waterfall chart type: {chart_type}")
        return

    st.plotly_chart(fig, use_container_width=True)
