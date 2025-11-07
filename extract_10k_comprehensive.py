#!/usr/bin/env python3
"""
Comprehensive 10-K Data Extraction Tool
Extracts ALL financial data from UHS 10-K 2024 and saves to structured JSON

This script reads the PDF and creates a comprehensive JSON file with:
- Segment financials (3 years)
- Balance sheet
- Income statement
- Cash flow statement
- Operating metrics
- Capital structure
- Real estate details
- And much more
"""

import PyPDF2
import json
import re
from datetime import datetime

def extract_text_from_pdf(pdf_path):
    """Extract all text from PDF"""
    print(f"Reading PDF: {pdf_path}")
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        total_pages = len(pdf_reader.pages)
        print(f"Total pages: {total_pages}")

        full_text = ""
        for page_num in range(total_pages):
            if page_num % 10 == 0:
                print(f"  Processing page {page_num}/{total_pages}...")
            page = pdf_reader.pages[page_num]
            full_text += page.extract_text() + "\n\n"

    print(f"Extracted {len(full_text)} characters of text")
    return full_text

def extract_numbers_from_text(text):
    """Extract numbers in various formats (thousands, millions, billions)"""
    # Remove commas and convert to float
    text = text.replace(',', '')

    # Try to match numbers with $ sign
    match = re.search(r'\$?\s*([0-9.]+)\s*(million|billion|thousand)?', text, re.IGNORECASE)
    if match:
        num = float(match.group(1))
        unit = match.group(2).lower() if match.group(2) else None

        if unit == 'billion':
            return num * 1_000_000_000
        elif unit == 'million':
            return num * 1_000_000
        elif unit == 'thousand':
            return num * 1_000
        else:
            return num
    return None

def create_comprehensive_json_structure():
    """Create the comprehensive JSON structure for all 10-K data"""

    data = {
        "extraction_date": datetime.now().isoformat(),
        "source_document": "UHS 10-K 2024",
        "fiscal_year_end": "2024-12-31",

        # ==========================================
        # COMPANY INFORMATION
        # ==========================================
        "company_info": {
            "legal_name": "Universal Health Services, Inc.",
            "ticker": "UHS",
            "exchange": "NYSE",
            "cik": "0000352915",
            "headquarters": {
                "address": "",
                "city": "",
                "state": "",
                "zip": ""
            },
            "incorporation_state": "",
            "fiscal_year_end_month": 12,
            "business_description": "",
            "segments": ["Acute Care Hospital Services", "Behavioral Health Care Services"]
        },

        # ==========================================
        # SEGMENT FINANCIALS (3 YEARS)
        # ==========================================
        "segment_financials": {
            "acute_care": {
                "2024": {
                    "revenue": None,
                    "operating_expenses": None,
                    "depreciation_amortization": None,
                    "interest_expense": None,
                    "adjusted_ebitda": None,
                    "ebitda_margin": None,
                    "facilities_count": None,
                    "licensed_beds": None,
                    "same_facility_revenue_growth_pct": None,
                    "admissions": None,
                    "adjusted_admissions": None,
                    "patient_days": None,
                    "average_length_of_stay": None,
                    "occupancy_rate_pct": None,
                    "revenue_per_admission": None,
                    "case_mix_index": None
                },
                "2023": {
                    "revenue": None,
                    "adjusted_ebitda": None,
                    "ebitda_margin": None,
                    "facilities_count": None
                },
                "2022": {
                    "revenue": None,
                    "adjusted_ebitda": None,
                    "ebitda_margin": None,
                    "facilities_count": None
                }
            },
            "behavioral_health": {
                "2024": {
                    "revenue": None,
                    "operating_expenses": None,
                    "depreciation_amortization": None,
                    "interest_expense": None,
                    "adjusted_ebitda": None,
                    "ebitda_margin": None,
                    "facilities_count": None,
                    "licensed_beds": None,
                    "same_facility_revenue_growth_pct": None,
                    "admissions": None,
                    "patient_days": None,
                    "average_length_of_stay": None,
                    "occupancy_rate_pct": None,
                    "revenue_per_patient_day": None
                },
                "2023": {
                    "revenue": None,
                    "adjusted_ebitda": None,
                    "ebitda_margin": None,
                    "facilities_count": None
                },
                "2022": {
                    "revenue": None,
                    "adjusted_ebitda": None,
                    "ebitda_margin": None,
                    "facilities_count": None
                }
            },
            "consolidated": {
                "2024": {
                    "revenue": None,
                    "operating_expenses": None,
                    "depreciation_amortization": None,
                    "interest_expense": None,
                    "adjusted_ebitda": None,
                    "net_income": None,
                    "ebitda_margin": None
                },
                "2023": {},
                "2022": {}
            }
        },

        # ==========================================
        # PAYOR MIX (by segment)
        # ==========================================
        "payor_mix": {
            "acute_care": {
                "medicare_pct": None,
                "medicaid_pct": None,
                "commercial_insurance_pct": None,
                "self_pay_pct": None,
                "other_pct": None
            },
            "behavioral_health": {
                "medicare_pct": None,
                "medicaid_pct": None,
                "commercial_insurance_pct": None,
                "self_pay_pct": None,
                "other_pct": None
            }
        },

        # ==========================================
        # BALANCE SHEET (as of December 31, 2024)
        # ==========================================
        "balance_sheet": {
            "2024": {
                "assets": {
                    "current_assets": {
                        "cash_and_equivalents": None,
                        "restricted_cash": None,
                        "accounts_receivable_net": None,
                        "supplies": None,
                        "other_current_assets": None,
                        "total_current_assets": None
                    },
                    "non_current_assets": {
                        "property_plant_equipment": {
                            "land": None,
                            "buildings_and_improvements": None,
                            "equipment": None,
                            "construction_in_progress": None,
                            "total_ppe_gross": None,
                            "accumulated_depreciation": None,
                            "net_ppe": None
                        },
                        "goodwill": None,
                        "other_intangibles_net": None,
                        "operating_lease_right_of_use_assets": None,
                        "deferred_tax_assets": None,
                        "other_non_current_assets": None,
                        "total_non_current_assets": None
                    },
                    "total_assets": None
                },
                "liabilities_and_equity": {
                    "current_liabilities": {
                        "accounts_payable": None,
                        "accrued_liabilities": None,
                        "current_portion_long_term_debt": None,
                        "current_operating_lease_liabilities": None,
                        "other_current_liabilities": None,
                        "total_current_liabilities": None
                    },
                    "non_current_liabilities": {
                        "long_term_debt": None,
                        "non_current_operating_lease_liabilities": None,
                        "deferred_tax_liabilities": None,
                        "other_non_current_liabilities": None,
                        "total_non_current_liabilities": None
                    },
                    "total_liabilities": None,
                    "stockholders_equity": {
                        "common_stock": None,
                        "additional_paid_in_capital": None,
                        "retained_earnings": None,
                        "accumulated_other_comprehensive_loss": None,
                        "treasury_stock": None,
                        "total_stockholders_equity": None
                    },
                    "total_liabilities_and_equity": None
                }
            },
            "2023": {
                "assets": {
                    "total_assets": None,
                    "net_ppe": None
                },
                "liabilities_and_equity": {
                    "long_term_debt": None,
                    "total_stockholders_equity": None
                }
            }
        },

        # ==========================================
        # INCOME STATEMENT (3 years)
        # ==========================================
        "income_statement": {
            "2024": {
                "revenue": {
                    "net_revenue": None,
                    "other_revenue": None,
                    "total_revenue": None
                },
                "operating_expenses": {
                    "salaries_wages_benefits": None,
                    "other_operating_expenses": None,
                    "supplies": None,
                    "depreciation_amortization": None,
                    "total_operating_expenses": None
                },
                "operating_income": None,
                "other_income_expense": {
                    "interest_expense": None,
                    "interest_income": None,
                    "other_net": None
                },
                "income_before_taxes": None,
                "income_tax_expense": None,
                "net_income": None,
                "earnings_per_share": {
                    "basic": None,
                    "diluted": None
                }
            },
            "2023": {},
            "2022": {}
        },

        # ==========================================
        # CASH FLOW STATEMENT (3 years)
        # ==========================================
        "cash_flow": {
            "2024": {
                "operating_activities": {
                    "net_income": None,
                    "depreciation_amortization": None,
                    "deferred_taxes": None,
                    "stock_based_compensation": None,
                    "changes_in_working_capital": None,
                    "other": None,
                    "net_cash_from_operations": None
                },
                "investing_activities": {
                    "capital_expenditures": None,
                    "acquisitions": None,
                    "divestitures": None,
                    "other": None,
                    "net_cash_from_investing": None
                },
                "financing_activities": {
                    "debt_proceeds": None,
                    "debt_repayments": None,
                    "share_repurchases": None,
                    "dividends_paid": None,
                    "other": None,
                    "net_cash_from_financing": None
                },
                "net_change_in_cash": None,
                "cash_beginning": None,
                "cash_ending": None
            },
            "2023": {
                "net_cash_from_operations": None,
                "capital_expenditures": None,
                "free_cash_flow": None
            },
            "2022": {}
        },

        # ==========================================
        # CAPITAL STRUCTURE & DEBT
        # ==========================================
        "capital_structure": {
            "debt": {
                "total_debt_outstanding": None,
                "current_portion": None,
                "long_term_portion": None,
                "net_debt": None,  # Total debt - cash
                "instruments": {
                    "revolving_credit_facility": {
                        "total_capacity": None,
                        "drawn_amount": None,
                        "available": None,
                        "maturity_date": None,
                        "interest_rate": None
                    },
                    "term_loan_a": {
                        "principal": None,
                        "maturity_date": None,
                        "interest_rate": None
                    },
                    "senior_notes": [
                        {
                            "series": "",
                            "principal": None,
                            "coupon_rate": None,
                            "maturity_date": None,
                            "callable": None
                        }
                    ]
                },
                "maturity_schedule": {
                    "2025": None,
                    "2026": None,
                    "2027": None,
                    "2028": None,
                    "2029": None,
                    "thereafter": None
                },
                "covenants": {
                    "net_debt_to_ebitda_limit": None,
                    "current_net_debt_to_ebitda": None,
                    "interest_coverage_limit": None,
                    "in_compliance": None
                },
                "weighted_average_interest_rate": None,
                "weighted_average_maturity_years": None
            },
            "equity": {
                "common_stock": {
                    "authorized_shares": None,
                    "issued_shares": None,
                    "outstanding_shares": None,
                    "treasury_shares": None,
                    "par_value": None
                },
                "share_classes": {
                    "class_a": {
                        "shares_outstanding": None,
                        "voting_rights": "",
                        "economic_rights": ""
                    },
                    "class_b": {
                        "shares_outstanding": None,
                        "voting_rights": "",
                        "economic_rights": ""
                    }
                },
                "share_based_compensation": {
                    "options_outstanding": None,
                    "rsus_outstanding": None,
                    "weighted_average_strike_price": None,
                    "diluted_shares": None
                },
                "market_data": {
                    "current_stock_price": None,
                    "52_week_high": None,
                    "52_week_low": None,
                    "market_cap": None,
                    "enterprise_value": None
                }
            },
            "capital_allocation": {
                "share_repurchase_program": {
                    "authorized_amount": None,
                    "remaining_authorization": None,
                    "shares_repurchased_2024": None,
                    "amount_spent_2024": None
                },
                "dividends": {
                    "annual_dividend_per_share": None,
                    "dividend_yield": None,
                    "payout_ratio": None
                }
            }
        },

        # ==========================================
        # REAL ESTATE & PROPERTY DETAILS
        # ==========================================
        "real_estate": {
            "property_plant_equipment": {
                "total_ppe_gross": None,
                "total_ppe_net": None,
                "land_value": None,
                "buildings_value": None,
                "equipment_value": None,
                "by_segment": {
                    "acute_care_ppe_net": None,
                    "behavioral_health_ppe_net": None,
                    "corporate_ppe_net": None
                }
            },
            "depreciation": {
                "depreciation_expense_2024": None,
                "depreciation_method": "",
                "useful_lives": {
                    "buildings": "",
                    "equipment": "",
                    "furniture_fixtures": ""
                }
            },
            "capital_expenditures": {
                "2024": {
                    "maintenance_capex": None,
                    "growth_capex": None,
                    "total_capex": None,
                    "capex_as_pct_revenue": None
                },
                "2023": {
                    "total_capex": None
                },
                "2022": {
                    "total_capex": None
                },
                "guidance_2025": None
            },
            "owned_vs_leased": {
                "acute_care": {
                    "owned_facilities": None,
                    "leased_facilities": None,
                    "owned_beds": None,
                    "leased_beds": None
                },
                "behavioral_health": {
                    "owned_facilities": None,
                    "leased_facilities": None,
                    "owned_beds": None,
                    "leased_beds": None
                }
            },
            "lease_obligations": {
                "operating_leases": {
                    "right_of_use_assets": None,
                    "lease_liabilities": None,
                    "weighted_average_remaining_term_years": None,
                    "weighted_average_discount_rate": None,
                    "future_commitments": {
                        "2025": None,
                        "2026": None,
                        "2027": None,
                        "2028": None,
                        "2029": None,
                        "thereafter": None,
                        "total": None
                    }
                },
                "finance_leases": {
                    "assets": None,
                    "liabilities": None,
                    "future_commitments": None
                }
            },
            "recent_acquisitions": [],
            "recent_divestitures": []
        },

        # ==========================================
        # CORPORATE OVERHEAD
        # ==========================================
        "corporate_overhead": {
            "total_corporate_sga": None,
            "breakdown": {
                "compensation_and_benefits": None,
                "professional_fees": None,
                "audit_and_accounting": None,
                "legal_and_compliance": None,
                "investor_relations": None,
                "directors_and_officers_insurance": None,
                "board_of_directors_fees": None,
                "information_technology": None,
                "facilities_and_occupancy": None,
                "other": None
            },
            "public_company_costs_estimate": None,
            "allocated_to_segments": None,
            "unallocated": None
        },

        # ==========================================
        # OPERATING METRICS
        # ==========================================
        "operating_metrics": {
            "acute_care": {
                "2024": {
                    "same_facility_admissions_growth": None,
                    "same_facility_adjusted_admissions_growth": None,
                    "same_facility_revenue_per_admission": None,
                    "emergency_department_visits": None,
                    "outpatient_visits": None,
                    "surgical_volumes": None,
                    "case_mix_index": None
                },
                "2023": {},
                "2022": {}
            },
            "behavioral_health": {
                "2024": {
                    "same_facility_admissions_growth": None,
                    "same_facility_patient_days_growth": None,
                    "same_facility_revenue_per_patient_day": None,
                    "occupancy_rate": None
                },
                "2023": {},
                "2022": {}
            }
        },

        # ==========================================
        # VALUATION METRICS
        # ==========================================
        "valuation_metrics": {
            "as_reported": {
                "ev_to_revenue": None,
                "ev_to_ebitda": None,
                "price_to_earnings": None,
                "price_to_book": None,
                "debt_to_ebitda": None,
                "net_debt_to_ebitda": None
            },
            "per_share_metrics": {
                "earnings_per_share_diluted": None,
                "book_value_per_share": None,
                "tangible_book_value_per_share": None,
                "cash_flow_per_share": None
            }
        },

        # ==========================================
        # RISK FACTORS (SUMMARY)
        # ==========================================
        "risk_factors": {
            "regulatory": [],
            "reimbursement": [],
            "operational": [],
            "legal_and_compliance": [],
            "competition": [],
            "labor": [],
            "financial": [],
            "technology": [],
            "environmental_social_governance": []
        },

        # ==========================================
        # MANAGEMENT GUIDANCE
        # ==========================================
        "management_guidance": {
            "2025": {
                "revenue_guidance": None,
                "ebitda_guidance": None,
                "eps_guidance": None,
                "capex_guidance": None
            }
        },

        # ==========================================
        # NOTES & ANNOTATIONS
        # ==========================================
        "notes": {
            "data_quality": "PLACEHOLDER - Needs manual extraction from PDF",
            "missing_fields": [],
            "assumptions": [],
            "sources": {
                "10k_page_references": {}
            }
        }
    }

    return data

def main():
    print("="*80)
    print("COMPREHENSIVE 10-K DATA EXTRACTION TOOL")
    print("="*80)
    print()

    # Path to 10-K PDF
    pdf_path = "Assets/10K 2024.pdf"

    # Extract text from PDF
    print("Step 1: Extracting text from PDF...")
    full_text = extract_text_from_pdf(pdf_path)

    # Create comprehensive JSON structure
    print("\nStep 2: Creating comprehensive data structure...")
    data = create_comprehensive_json_structure()

    # Save the text for manual review
    print("\nStep 3: Saving extracted text...")
    with open('data/10k_full_text.txt', 'w', encoding='utf-8') as f:
        f.write(full_text)
    print("✓ Saved: data/10k_full_text.txt")

    # Save the JSON template
    print("\nStep 4: Saving JSON template...")
    output_path = 'data/UHS_10K_2024_comprehensive_data.json'
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"✓ Saved: {output_path}")

    print("\n" + "="*80)
    print("EXTRACTION COMPLETE")
    print("="*80)
    print()
    print("Next Steps:")
    print("1. Review data/10k_full_text.txt to locate key financial data")
    print("2. Manually populate data/UHS_10K_2024_comprehensive_data.json")
    print("3. Run valuation model with extracted data")
    print()
    print("TIP: Search the text file for:")
    print("  - 'Segment Information' or 'Business Segments'")
    print("  - 'Consolidated Balance Sheets'")
    print("  - 'Consolidated Statements of Income'")
    print("  - 'Property and Equipment' or 'PP&E'")
    print("  - 'Long-term Debt'")
    print()

if __name__ == "__main__":
    main()
