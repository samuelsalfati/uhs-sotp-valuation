"""
Data Integrity Validation Module for UHS SOTP Valuation

This module performs comprehensive data integrity checks across all CSV files
to ensure consistency, accuracy, and completeness of valuation data.
"""

import pandas as pd
import os
from datetime import datetime
import streamlit as st


class DataValidator:
    """Validates data integrity across all valuation files"""

    def __init__(self, data_path="data/graphs"):
        self.data_path = data_path
        self.checks_passed = []
        self.checks_failed = []
        self.warnings = []

    def run_all_checks(self, data_dict):
        """Run all validation checks"""
        self.check_file_completeness()
        self.check_sotp_calculations(data_dict)
        self.check_dcf_calculations(data_dict)
        self.check_lbo_calculations(data_dict)
        self.check_cross_file_consistency(data_dict)
        self.check_data_reasonableness(data_dict)

        return {
            'passed': self.checks_passed,
            'failed': self.checks_failed,
            'warnings': self.warnings,
            'total_checks': len(self.checks_passed) + len(self.checks_failed),
            'pass_rate': len(self.checks_passed) / (len(self.checks_passed) + len(self.checks_failed)) * 100 if (len(self.checks_passed) + len(self.checks_failed)) > 0 else 0
        }

    def check_file_completeness(self):
        """Check that all required CSV files exist and are not empty"""
        required_files = [
            'sotp_valuation_scenarios.csv',
            'sotp_valuation_detailed.csv',
            'dcf_projections_10yr.csv',
            'dcf_valuation_summary.csv',
            'lbo_projections_5yr.csv',
            'lbo_valuation_summary.csv',
            'football_field_summary.csv',
            'segment_financials_3yr.csv',
            'debt_maturity_schedule.csv',
        ]

        for filename in required_files:
            filepath = os.path.join(self.data_path, filename)
            if os.path.exists(filepath):
                if os.path.getsize(filepath) > 0:
                    self.checks_passed.append(f"✓ {filename} exists and is not empty")
                else:
                    self.checks_failed.append(f"✗ {filename} is empty")
            else:
                self.checks_failed.append(f"✗ {filename} not found")

    def check_sotp_calculations(self, data_dict):
        """Validate SOTP sum-of-parts calculations"""
        try:
            sotp_detailed = data_dict.get('sotp_detailed')
            if sotp_detailed is not None and not sotp_detailed.empty:
                for idx, row in sotp_detailed.iterrows():
                    scenario = row.get('Scenario', 'Unknown')

                    # Check EV = sum of 4 parts
                    behavioral_opco = float(str(row.get('Behavioral_OpCo_Value', 0)).replace('$', '').replace(',', '').replace('M', ''))
                    behavioral_propco = float(str(row.get('Behavioral_PropCo_Value', 0)).replace('$', '').replace(',', '').replace('M', ''))
                    acute_opco = float(str(row.get('Acute_OpCo_Value', 0)).replace('$', '').replace(',', '').replace('M', ''))
                    acute_propco = float(str(row.get('Acute_PropCo_Value', 0)).replace('$', '').replace(',', '').replace('M', ''))
                    total_ev_calc = behavioral_opco + behavioral_propco + acute_opco + acute_propco
                    total_ev_stated = float(str(row.get('Total_EV', 0)).replace('$', '').replace(',', '').replace('M', '').replace('B', '')) * (1000 if 'B' in str(row.get('Total_EV', '')) else 1)

                    if abs(total_ev_calc - total_ev_stated) / total_ev_stated < 0.01:  # Within 1%
                        self.checks_passed.append(f"✓ SOTP {scenario}: EV calculation matches (${total_ev_stated:,.0f}M)")
                    else:
                        self.checks_failed.append(f"✗ SOTP {scenario}: EV mismatch - Calculated: ${total_ev_calc:,.0f}M vs Stated: ${total_ev_stated:,.0f}M")

        except Exception as e:
            self.warnings.append(f"⚠ Could not validate SOTP calculations: {str(e)}")

    def check_dcf_calculations(self, data_dict):
        """Validate DCF present value calculations"""
        try:
            dcf_pv = data_dict.get('dcf_pv')
            dcf_summary = data_dict.get('dcf_summary')

            if dcf_pv is not None and not dcf_pv.empty and dcf_summary is not None and not dcf_summary.empty:
                # Check that PV of FCF + Terminal Value = Enterprise Value
                for idx, row in dcf_summary.iterrows():
                    scenario = row.get('scenario', 'Unknown')
                    pv_fcf = float(str(row.get('pv_fcf_10yr', 0)).replace('$', '').replace(',', '').replace('M', ''))
                    pv_terminal = float(str(row.get('pv_terminal_value', 0)).replace('$', '').replace(',', '').replace('M', ''))
                    ev_stated = float(str(row.get('enterprise_value', 0)).replace('$', '').replace(',', '').replace('M', '').replace('B', '')) * (1000 if 'B' in str(row.get('enterprise_value', '')) else 1)

                    ev_calc = pv_fcf + pv_terminal

                    if abs(ev_calc - ev_stated) / ev_stated < 0.01:
                        self.checks_passed.append(f"✓ DCF {scenario}: EV = PV(FCF) + PV(Terminal) matches")
                    else:
                        self.checks_failed.append(f"✗ DCF {scenario}: EV mismatch - Calculated: ${ev_calc:,.0f}M vs Stated: ${ev_stated:,.0f}M")

        except Exception as e:
            self.warnings.append(f"⚠ Could not validate DCF calculations: {str(e)}")

    def check_lbo_calculations(self, data_dict):
        """Validate LBO MOIC and IRR calculations"""
        try:
            lbo_summary = data_dict.get('lbo_summary')
            if lbo_summary is not None and not lbo_summary.empty:
                for idx, row in lbo_summary.iterrows():
                    scenario = row.get('scenario', 'Unknown')

                    # Check MOIC = Exit Equity / Initial Equity
                    exit_equity = float(str(row.get('exit_equity_value', 0)).replace('$', '').replace(',', '').replace('M', '').replace('B', '')) * (1000 if 'B' in str(row.get('exit_equity_value', '')) else 1)
                    initial_equity = float(str(row.get('initial_equity', 0)).replace('$', '').replace(',', '').replace('M', '').replace('B', '')) * (1000 if 'B' in str(row.get('initial_equity', '')) else 1)
                    moic_stated = float(str(row.get('moic', 0)).replace('x', ''))

                    if initial_equity > 0:
                        moic_calc = exit_equity / initial_equity
                        if abs(moic_calc - moic_stated) / moic_stated < 0.05:  # Within 5%
                            self.checks_passed.append(f"✓ LBO {scenario}: MOIC calculation matches ({moic_stated:.2f}x)")
                        else:
                            self.checks_failed.append(f"✗ LBO {scenario}: MOIC mismatch - Calculated: {moic_calc:.2f}x vs Stated: {moic_stated:.2f}x")

        except Exception as e:
            self.warnings.append(f"⚠ Could not validate LBO calculations: {str(e)}")

    def check_cross_file_consistency(self, data_dict):
        """Check consistency across different valuation files"""
        try:
            # Check that base case SOTP matches football field
            sotp_scenarios = data_dict.get('sotp_scenarios')
            football_field = data_dict.get('football_field')

            if sotp_scenarios is not None and football_field is not None:
                sotp_base = sotp_scenarios[sotp_scenarios['Scenario'] == 'BASE']['Value Per Share'].values
                ff_sotp = football_field[football_field['Valuation Method'].str.contains('SOTP', na=False)]['Base ($)'].values

                if len(sotp_base) > 0 and len(ff_sotp) > 0:
                    sotp_value = float(str(sotp_base[0]).replace('$', '').replace(',', ''))
                    ff_value = float(str(ff_sotp[0]).replace('$', '').replace(',', ''))

                    if abs(sotp_value - ff_value) / sotp_value < 0.01:
                        self.checks_passed.append(f"✓ SOTP Base Case consistent across files (${sotp_value:,.0f})")
                    else:
                        self.checks_failed.append(f"✗ SOTP Base Case mismatch - SOTP: ${sotp_value:,.0f} vs Football Field: ${ff_value:,.0f}")

        except Exception as e:
            self.warnings.append(f"⚠ Could not validate cross-file consistency: {str(e)}")

    def check_data_reasonableness(self, data_dict):
        """Check that values are within reasonable ranges"""
        try:
            # Check OpCo multiples
            sotp_detailed = data_dict.get('sotp_detailed')
            if sotp_detailed is not None and not sotp_detailed.empty:
                for idx, row in sotp_detailed.iterrows():
                    scenario = row.get('Scenario', 'Unknown')

                    beh_multiple = float(str(row.get('Behavioral_OpCo_Multiple', 0)).replace('x', ''))
                    acute_multiple = float(str(row.get('Acute_OpCo_Multiple', 0)).replace('x', ''))

                    if 5 <= beh_multiple <= 15:
                        self.checks_passed.append(f"✓ {scenario}: Behavioral multiple ({beh_multiple:.1f}x) within reasonable range")
                    else:
                        self.warnings.append(f"⚠ {scenario}: Behavioral multiple ({beh_multiple:.1f}x) outside typical range (5-15x)")

                    if 5 <= acute_multiple <= 15:
                        self.checks_passed.append(f"✓ {scenario}: Acute multiple ({acute_multiple:.1f}x) within reasonable range")
                    else:
                        self.warnings.append(f"⚠ {scenario}: Acute multiple ({acute_multiple:.1f}x) outside typical range (5-15x)")

            # Check cap rates
            if sotp_detailed is not None and not sotp_detailed.empty:
                for idx, row in sotp_detailed.iterrows():
                    scenario = row.get('Scenario', 'Unknown')

                    beh_cap = float(str(row.get('Behavioral_PropCo_Cap', 0)).replace('%', ''))
                    acute_cap = float(str(row.get('Acute_PropCo_Cap', 0)).replace('%', ''))

                    if 4 <= beh_cap <= 10:
                        self.checks_passed.append(f"✓ {scenario}: Behavioral cap rate ({beh_cap:.1f}%) within reasonable range")
                    else:
                        self.warnings.append(f"⚠ {scenario}: Behavioral cap rate ({beh_cap:.1f}%) outside typical range (4-10%)")

        except Exception as e:
            self.warnings.append(f"⚠ Could not validate data reasonableness: {str(e)}")


def display_validation_results(validation_results):
    """Display validation results in Streamlit UI"""
    st.subheader("🔍 Data Integrity Dashboard")

    # Summary metrics
    col1, col2, col3 = st.columns(3)

    with col1:
        pass_rate = validation_results['pass_rate']
        st.metric(
            "Pass Rate",
            f"{pass_rate:.1f}%",
            delta="Healthy" if pass_rate >= 90 else "Needs Attention"
        )

    with col2:
        st.metric(
            "Checks Passed",
            len(validation_results['passed']),
            delta=f"{len(validation_results['passed'])} / {validation_results['total_checks']}"
        )

    with col3:
        st.metric(
            "Warnings",
            len(validation_results['warnings']),
            delta="Review" if len(validation_results['warnings']) > 0 else "None"
        )

    # Detailed results
    st.markdown("---")

    # Passed checks
    with st.expander(f"✅ Passed Checks ({len(validation_results['passed'])})", expanded=False):
        for check in validation_results['passed']:
            st.success(check)

    # Failed checks
    if validation_results['failed']:
        with st.expander(f"❌ Failed Checks ({len(validation_results['failed'])})", expanded=True):
            for check in validation_results['failed']:
                st.error(check)

    # Warnings
    if validation_results['warnings']:
        with st.expander(f"⚠️ Warnings ({len(validation_results['warnings'])})", expanded=True):
            for warning in validation_results['warnings']:
                st.warning(warning)
