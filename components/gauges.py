"""
Gauge Chart Components using Plotly
For deal scores, valuation metrics, and credit health
"""

import plotly.graph_objects as go
import streamlit as st


def create_deal_score_gauge(score, max_score=100):
    """
    Create deal attractiveness score gauge
    Score based on: (Upside % + IRR + Synergy Value/Share) weighted

    Zones:
    - 0-30: Poor (red)
    - 30-50: Fair (yellow)
    - 50-70: Good (light green)
    - 70-100: Excellent (bright green)
    """

    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Deal Attractiveness Score", 'font': {'size': 24, 'color': '#4cc9f0'}},
        delta={'reference': 70, 'increasing': {'color': "#06ffa5"}, 'decreasing': {'color': "#ff006e"}},
        gauge={
            'axis': {'range': [None, max_score], 'tickwidth': 2, 'tickcolor': "#e0e1dd"},
            'bar': {'color': "#4cc9f0", 'thickness': 0.75},
            'bgcolor': "#1b263b",
            'borderwidth': 2,
            'bordercolor': "#2d3e50",
            'steps': [
                {'range': [0, 30], 'color': '#ff006e'},
                {'range': [30, 50], 'color': '#ffd60a'},
                {'range': [50, 70], 'color': '#90ee90'},
                {'range': [70, 100], 'color': '#06ffa5'}
            ],
            'threshold': {
                'line': {'color': "#e0e1dd", 'width': 4},
                'thickness': 0.75,
                'value': 70
            }
        }
    ))

    fig.update_layout(
        paper_bgcolor='#0a1929',
        font={'color': "#e0e1dd", 'family': "Arial"},
        height=350,
        margin=dict(t=80, b=50, l=50, r=50)
    )

    return fig


def create_valuation_gauge(current_price, fair_value, method_name="SOTP"):
    """
    Create valuation speedometer showing current price vs fair value

    Shows upside/downside potential
    """

    upside_pct = ((fair_value - current_price) / current_price) * 100

    # Set range based on current price
    min_val = min(current_price * 0.5, fair_value * 0.5)
    max_val = max(current_price * 1.5, fair_value * 1.5)

    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=current_price,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': f"{method_name} Valuation", 'font': {'size': 20, 'color': '#4cc9f0'}},
        number={'prefix': "$", 'font': {'size': 36, 'color': '#e0e1dd'}},
        delta={
            'reference': fair_value,
            'relative': True,
            'position': "bottom",
            'valueformat': ".1%",
            'increasing': {'color': "#ff006e"},  # Current > Fair Value = overvalued
            'decreasing': {'color': "#06ffa5"}   # Current < Fair Value = undervalued
        },
        gauge={
            'axis': {'range': [min_val, max_val], 'tickwidth': 2, 'tickcolor': "#e0e1dd", 'tickformat': '$,.0f'},
            'bar': {'color': "#4cc9f0", 'thickness': 0.6},
            'bgcolor': "#1b263b",
            'borderwidth': 2,
            'bordercolor': "#2d3e50",
            'steps': [
                {'range': [min_val, current_price], 'color': '#90ee90'},  # Below current = good
                {'range': [current_price, fair_value], 'color': '#ffd60a'},  # Current to fair = opportunity
                {'range': [fair_value, max_val], 'color': '#ff006e'}  # Above fair = overvalued
            ],
            'threshold': {
                'line': {'color': "#06ffa5", 'width': 4},
                'thickness': 0.8,
                'value': fair_value
            }
        }
    ))

    fig.update_layout(
        paper_bgcolor='#0a1929',
        font={'color': "#e0e1dd", 'family': "Arial"},
        height=350,
        margin=dict(t=70, b=20, l=50, r=50),
        annotations=[
            dict(
                text=f"Target: ${fair_value:,.0f} ({upside_pct:+.1f}% upside)",
                xref="paper",
                yref="paper",
                x=0.5,
                y=-0.05,
                showarrow=False,
                font=dict(size=14, color='#06ffa5')
            )
        ]
    )

    return fig


def create_credit_health_gauge(net_debt_to_ebitda):
    """
    Create credit health gauge based on leverage ratio

    Zones:
    - 0-2x: Conservative (green)
    - 2-4x: Moderate (light green)
    - 4-6x: Aggressive (yellow)
    - 6-8x: Stressed (orange)
    - 8x+: Distressed (red)
    """

    # Determine status
    if net_debt_to_ebitda < 2:
        status = "Conservative"
        status_color = "#06ffa5"
    elif net_debt_to_ebitda < 4:
        status = "Moderate"
        status_color = "#90ee90"
    elif net_debt_to_ebitda < 6:
        status = "Aggressive"
        status_color = "#ffd60a"
    elif net_debt_to_ebitda < 8:
        status = "Stressed"
        status_color = "#ff9500"
    else:
        status = "Distressed"
        status_color = "#ff006e"

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=net_debt_to_ebitda,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Credit Health: Net Debt / EBITDA", 'font': {'size': 20, 'color': '#4cc9f0'}},
        number={'suffix': "x", 'font': {'size': 40, 'color': status_color}},
        gauge={
            'axis': {'range': [0, 10], 'tickwidth': 2, 'tickcolor': "#e0e1dd", 'ticksuffix': "x"},
            'bar': {'color': status_color, 'thickness': 0.7},
            'bgcolor': "#1b263b",
            'borderwidth': 2,
            'bordercolor': "#2d3e50",
            'steps': [
                {'range': [0, 2], 'color': '#06ffa5'},
                {'range': [2, 4], 'color': '#90ee90'},
                {'range': [4, 6], 'color': '#ffd60a'},
                {'range': [6, 8], 'color': '#ff9500'},
                {'range': [8, 10], 'color': '#ff006e'}
            ],
            'threshold': {
                'line': {'color': "#e0e1dd", 'width': 3},
                'thickness': 0.75,
                'value': 4  # Industry standard threshold
            }
        }
    ))

    fig.update_layout(
        paper_bgcolor='#0a1929',
        font={'color': "#e0e1dd", 'family': "Arial"},
        height=350,
        margin=dict(t=70, b=50, l=50, r=50),
        annotations=[
            dict(
                text=f"Status: {status}",
                xref="paper",
                yref="paper",
                x=0.5,
                y=0.15,
                showarrow=False,
                font=dict(size=18, color=status_color, family="Arial Black")
            )
        ]
    )

    return fig


def create_synergy_confidence_gauge(implementation_pct):
    """
    Create synergy implementation confidence gauge

    Shows % confidence in achieving stated synergies
    """

    if implementation_pct < 40:
        status = "Low Confidence"
        status_color = "#ff006e"
    elif implementation_pct < 60:
        status = "Moderate"
        status_color = "#ffd60a"
    elif implementation_pct < 80:
        status = "High Confidence"
        status_color = "#90ee90"
    else:
        status = "Very High"
        status_color = "#06ffa5"

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=implementation_pct,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Synergy Implementation Confidence", 'font': {'size': 20, 'color': '#4cc9f0'}},
        number={'suffix': "%", 'font': {'size': 40, 'color': status_color}},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 2, 'tickcolor': "#e0e1dd", 'ticksuffix': "%"},
            'bar': {'color': status_color, 'thickness': 0.7},
            'bgcolor': "#1b263b",
            'borderwidth': 2,
            'bordercolor': "#2d3e50",
            'steps': [
                {'range': [0, 40], 'color': '#ff006e'},
                {'range': [40, 60], 'color': '#ffd60a'},
                {'range': [60, 80], 'color': '#90ee90'},
                {'range': [80, 100], 'color': '#06ffa5'}
            ],
            'threshold': {
                'line': {'color': "#e0e1dd", 'width': 3},
                'thickness': 0.75,
                'value': 70
            }
        }
    ))

    fig.update_layout(
        paper_bgcolor='#0a1929',
        font={'color': "#e0e1dd", 'family': "Arial"},
        height=350,
        margin=dict(t=70, b=50, l=50, r=50),
        annotations=[
            dict(
                text=f"{status}",
                xref="paper",
                yref="paper",
                x=0.5,
                y=0.15,
                showarrow=False,
                font=dict(size=18, color=status_color, family="Arial Black")
            )
        ]
    )

    return fig


def render_gauge(gauge_type, **kwargs):
    """
    Render a gauge chart in Streamlit

    gauge_type: "deal_score", "valuation", "credit_health", or "synergy_confidence"
    **kwargs: Arguments specific to each gauge type
    """
    if gauge_type == "deal_score":
        fig = create_deal_score_gauge(**kwargs)
    elif gauge_type == "valuation":
        fig = create_valuation_gauge(**kwargs)
    elif gauge_type == "credit_health":
        fig = create_credit_health_gauge(**kwargs)
    elif gauge_type == "synergy_confidence":
        fig = create_synergy_confidence_gauge(**kwargs)
    else:
        st.error(f"Unknown gauge type: {gauge_type}")
        return

    st.plotly_chart(fig, use_container_width=True)
