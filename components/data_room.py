"""
Data Room Component for UHS SOTP Valuation
Displays comprehensive document library with search, filtering, and categorization
"""

import streamlit as st
import os
from datetime import datetime


# Document categorization and metadata
DOCUMENT_CATEGORIES = {
    "📊 Investment Case": {
        "description": "Executive summaries and investment thesis",
        "documents": [
            {
                "file": "UHS_SOTP_EXECUTIVE_SUMMARY_FINAL.md",
                "title": "UHS SOTP Executive Summary (Final)",
                "description": "Comprehensive executive summary of UHS SOTP valuation with key findings",
                "tags": ["#critical", "#executive", "#summary"]
            },
            {
                "file": "EXECUTIVE_SUMMARY_HILL_VALLEY_UHS_ACQUISITION.md",
                "title": "Hill Valley UHS Acquisition - Executive Summary",
                "description": "Strategic rationale and synergies for Hill Valley's acquisition of UHS",
                "tags": ["#critical", "#acquisition", "#synergies"]
            },
            {
                "file": "FINAL_SUMMARY.md",
                "title": "Final Investment Summary",
                "description": "Consolidated final summary of all valuation work",
                "tags": ["#critical", "#final", "#summary"]
            }
        ]
    },
    "💎 Valuation Models": {
        "description": "Detailed valuation methodologies and calculations",
        "documents": [
            {
                "file": "UHS_SOTP_MODEL_GUIDE.md",
                "title": "UHS SOTP Model Guide",
                "description": "Comprehensive guide to the 4-part SOTP valuation methodology",
                "tags": ["#methodology", "#sotp", "#guide"]
            },
            {
                "file": "SOTP_VALUATION_CONCLUSION.md",
                "title": "SOTP Valuation Conclusion",
                "description": "Final SOTP valuation results and investment recommendation",
                "tags": ["#sotp", "#valuation", "#conclusion"]
            },
            {
                "file": "SOTP_ASSUMPTIONS_AND_SOURCES.md",
                "title": "SOTP Assumptions & Sources",
                "description": "Detailed assumptions and data sources for SOTP model",
                "tags": ["#sotp", "#assumptions", "#sources"]
            },
            {
                "file": "SOTP_RECALCULATION_BEHAVIORAL_PREMIUM.md",
                "title": "SOTP Behavioral Premium Recalculation",
                "description": "Justification for 9.0x behavioral OpCo multiple with 22.7% margins",
                "tags": ["#sotp", "#behavioral", "#critical"]
            },
            {
                "file": "DCF_ASSUMPTIONS_SOURCED.md",
                "title": "DCF Assumptions (Sourced)",
                "description": "10-year DCF model assumptions with sources",
                "tags": ["#dcf", "#assumptions", "#sources"]
            },
            {
                "file": "FOOTBALL_FIELD_UPDATED_SOURCED.md",
                "title": "Football Field Valuation (Updated)",
                "description": "Multi-method valuation summary with weighted average",
                "tags": ["#valuation", "#football-field", "#summary"]
            }
        ]
    },
    "🏦 Capital Structure & Real Estate": {
        "description": "Capital structure analysis and real estate valuation",
        "documents": [
            {
                "file": "CAPITAL_STRUCTURE_COMPLETE.md",
                "title": "Capital Structure - Complete Analysis",
                "description": "Comprehensive debt and equity capital structure breakdown",
                "tags": ["#capital-structure", "#debt", "#equity"]
            },
            {
                "file": "CAPITAL_STRUCTURE_VISUAL_SUMMARY.md",
                "title": "Capital Structure Visual Summary",
                "description": "Visual representation of UHS capital structure",
                "tags": ["#capital-structure", "#visual", "#summary"]
            },
            {
                "file": "UHS_REAL_ESTATE_VALUATION_DETAILED.md",
                "title": "UHS Real Estate Valuation (Detailed)",
                "description": "PropCo/OpCo methodology with cap rate sourcing from 22 sources",
                "tags": ["#real-estate", "#propco", "#methodology"]
            }
        ]
    },
    "📋 Due Diligence & Data Quality": {
        "description": "Due diligence plans, data audits, and quality assurance",
        "documents": [
            {
                "file": "UHS_COMPREHENSIVE_DUE_DILIGENCE_PLAN.md",
                "title": "Comprehensive Due Diligence Plan",
                "description": "Full due diligence checklist and process",
                "tags": ["#due-diligence", "#checklist", "#plan"]
            },
            {
                "file": "DATA_AUDIT_VERIFIED_VS_NEEDS_SOURCING.md",
                "title": "Data Audit - Verified vs Needs Sourcing",
                "description": "Data quality audit identifying verified and missing sources",
                "tags": ["#data-quality", "#audit", "#sources"]
            },
            {
                "file": "MASTER_DATA_STATUS.md",
                "title": "Master Data Status",
                "description": "Centralized data status tracker across all models",
                "tags": ["#data-quality", "#status", "#tracking"]
            },
            {
                "file": "UHS_10K_EXACT_SOURCE_REFERENCES.md",
                "title": "UHS 10-K Exact Source References",
                "description": "Page-by-page references from UHS 10-K filing",
                "tags": ["#sources", "#10-k", "#references"]
            },
            {
                "file": "FINAL_SOURCED_DATA_SUMMARY.md",
                "title": "Final Sourced Data Summary",
                "description": "Comprehensive summary of all sourced data points",
                "tags": ["#sources", "#data-quality", "#final"]
            },
            {
                "file": "PRECEDENT_TRANSACTIONS_SOURCED.md",
                "title": "Precedent Transactions (Sourced)",
                "description": "Comparable M&A transactions with sources",
                "tags": ["#precedent-transactions", "#comps", "#sources"]
            }
        ]
    },
    "📖 Comprehensive Reports": {
        "description": "Full-length valuation reports and documentation",
        "documents": [
            {
                "file": "UHS_COMPREHENSIVE_VALUATION_REPORT_FINAL.md",
                "title": "UHS Comprehensive Valuation Report (Final)",
                "description": "Complete valuation report with all methodologies",
                "tags": ["#comprehensive", "#report", "#final"]
            },
            {
                "file": "HILL_VALLEY_UHS_DETAILED_VALUATION_BOOK.md",
                "title": "Hill Valley UHS Detailed Valuation Book",
                "description": "Full valuation book prepared for Hill Valley",
                "tags": ["#comprehensive", "#valuation-book", "#hill-valley"]
            }
        ]
    },
    "🔍 Methodology & Technical": {
        "description": "Methodology explanations and technical documentation",
        "documents": [
            {
                "file": "METHODOLOGY_EXPLANATIONS.md",
                "title": "Valuation Methodology Explanations",
                "description": "Detailed explanations of SOTP, DCF, LBO, and Comps methodologies",
                "tags": ["#methodology", "#technical", "#guide"]
            },
            {
                "file": "VALUATION_UPDATE_SUMMARY.md",
                "title": "Valuation Update Summary",
                "description": "Summary of key valuation updates and changes",
                "tags": ["#updates", "#summary", "#changes"]
            },
            {
                "file": "DATA_VISUALIZATION_GUIDE.md",
                "title": "Data Visualization Guide",
                "description": "Guide to interpreting charts and visualizations",
                "tags": ["#visualization", "#guide", "#technical"]
            },
            {
                "file": "MARKET_DATA_SUMMARY.md",
                "title": "Market Data Summary",
                "description": "Summary of market comparables and trading data",
                "tags": ["#market-data", "#comps", "#summary"]
            }
        ]
    }
}


def render_document_card(doc_info, base_path, search_term="", selected_tags=None):
    """Render a single document card"""
    if selected_tags is None:
        selected_tags = []

    # Filter by search term
    if search_term and search_term.lower() not in doc_info['title'].lower() and search_term.lower() not in doc_info['description'].lower():
        return False

    # Filter by tags
    if selected_tags and not any(tag in doc_info['tags'] for tag in selected_tags):
        return False

    # Read first few lines for preview
    filepath = os.path.join(base_path, doc_info['file'])
    preview_text = ""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()[:5]  # First 5 lines
            preview_text = ''.join(lines).strip()
            if len(preview_text) > 200:
                preview_text = preview_text[:200] + "..."
    except:
        preview_text = "Preview not available"

    # Get file stats
    try:
        file_stats = os.stat(filepath)
        file_size = file_stats.st_size / 1024  # KB
        modified_time = datetime.fromtimestamp(file_stats.st_mtime).strftime("%Y-%m-%d")
    except:
        file_size = 0
        modified_time = "Unknown"

    # Render card
    with st.container():
        st.markdown(f"""
        <div style="
            border: 1px solid #2d3e50;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
            background: linear-gradient(135deg, #0a1929 0%, #1b263b 100%);
            transition: all 0.3s ease;
        ">
            <h4 style="color: #4cc9f0; margin-top: 0;">{doc_info['title']}</h4>
            <p style="color: #778da9; font-size: 14px;">{doc_info['description']}</p>
            <p style="color: #415a77; font-size: 12px; font-style: italic;">
                📄 {file_size:.1f} KB • 📅 Modified: {modified_time}
            </p>
            <div style="margin-top: 10px;">
                {''.join([f'<span style="background: #1b263b; color: #06ffa5; padding: 3px 8px; border-radius: 5px; font-size: 11px; margin-right: 5px;">{tag}</span>' for tag in doc_info['tags']])}
            </div>
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns([3, 1])
        with col1:
            if st.button(f"📖 View Document", key=f"view_{doc_info['file']}"):
                st.session_state[f"show_{doc_info['file']}"] = True

        with col2:
            with open(filepath, 'r', encoding='utf-8') as f:
                st.download_button(
                    label="⬇ Download",
                    data=f.read(),
                    file_name=doc_info['file'],
                    mime="text/markdown",
                    key=f"download_{doc_info['file']}"
                )

        # Show full document if requested
        if st.session_state.get(f"show_{doc_info['file']}", False):
            with st.expander("📄 Full Document", expanded=True):
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                        st.markdown(content)
                except Exception as e:
                    st.error(f"Error loading document: {e}")

                if st.button("✖ Close", key=f"close_{doc_info['file']}"):
                    st.session_state[f"show_{doc_info['file']}"] = False
                    st.rerun()

    return True


def render_data_room_page(base_path=None):
    """Render the complete Data Room page"""

    # Use relative path if not specified (works on Streamlit Cloud)
    if base_path is None:
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    st.title("📚 Data Room")
    st.markdown("### Comprehensive Documentation Library")
    st.markdown("*All valuation documentation, research, and analysis in one organized location*")

    st.markdown("---")

    # Sidebar controls
    st.sidebar.markdown("## 🗂️ Data Room Filters")

    # Category selector
    selected_category = st.sidebar.selectbox(
        "Select Category",
        list(DOCUMENT_CATEGORIES.keys()),
        index=0
    )

    # Search bar
    search_term = st.sidebar.text_input("🔍 Search documents", placeholder="Type to search...")

    # Tag filters
    all_tags = set()
    for category in DOCUMENT_CATEGORIES.values():
        for doc in category['documents']:
            all_tags.update(doc['tags'])
    all_tags = sorted(list(all_tags))

    selected_tags = st.sidebar.multiselect("🏷️ Filter by tags", all_tags)

    # Quick stats
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📊 Library Stats")
    total_docs = sum(len(cat['documents']) for cat in DOCUMENT_CATEGORIES.values())
    st.sidebar.metric("Total Documents", total_docs)
    st.sidebar.metric("Categories", len(DOCUMENT_CATEGORIES))

    # Main content area
    category_info = DOCUMENT_CATEGORIES[selected_category]

    # Category header
    st.markdown(f"## {selected_category}")
    st.markdown(f"*{category_info['description']}*")
    st.markdown("---")

    # Document count
    doc_count = len(category_info['documents'])
    st.markdown(f"**{doc_count} documents** in this category")
    st.markdown("")

    # Render document cards
    docs_displayed = 0
    for doc in category_info['documents']:
        if render_document_card(doc, base_path, search_term, selected_tags):
            docs_displayed += 1

    if docs_displayed == 0:
        st.info("No documents match your search criteria. Try adjusting your filters.")

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #778da9; font-size: 12px; padding: 20px 0;">
        <p>💡 <b>Tip:</b> Use the search bar and tag filters to quickly find relevant documents</p>
        <p>📥 All documents can be downloaded individually using the Download button</p>
    </div>
    """, unsafe_allow_html=True)
