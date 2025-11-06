"""
NPI and CMS Facility Data Retrieval Agent
========================================

This script reads a list of healthcare facilities from one or more CSV files,
queries the **CMS NPI Registry API** for each facility to obtain its National
Provider Identifier (NPI) and related metadata (DBA name, taxonomy, address,
phone, etc.), and saves the enriched dataset to a new CSV file.  Optionally,
the script can attempt to cross‑reference each NPI to a Medicare Certification
Number (CCN) by querying CMS Provider Data Catalog endpoints, although the
crosswalk is not enabled by default.

The script was designed for use outside of this sandbox environment. It uses
the public NPI Registry API (version 2.1) described in the official CMS
documentation【975169929016318†L39-L45】. An API query returns up to 200 results,
so a name/city/state combination should yield a manageable list.  Results are
filtered to find the best match for the facility name.  If multiple candidate
entries remain after filtering, the first entry is used; however, you can
enhance the matching logic as needed.

Usage
-----
```
python npi_agent.py --input uhs_acute_facilities.csv \
                    --input uhs_behavioral_facilities_us.csv \
                    --output uhs_facilities_with_npi.csv
```

By default the script only enriches data with the NPI details. To enable
experimental cross‑mapping to CMS Certification Numbers via the Provider Data
Catalog, include the `--include_ccn` flag.  Note that live internet access is
required for both NPI and CCN lookups.

Limitations
-----------
- This script requires internet connectivity to query the CMS APIs. When run
  inside a restricted environment without external access, it will raise
  connection errors.
- Matching facility names across datasets is inherently fuzzy; the script uses
  simple case‑insensitive string containment. You may need to tweak the
  matching logic for ambiguous cases.
- CCN cross‑mapping uses the CMS Provider Data Catalog endpoints, which may
  change over time. If the endpoints or JSON structures change, update the
  `query_ccn_for_npi` function accordingly.

Author: OpenAI ChatGPT
"""

import argparse
import csv
import json
import logging
import sys
import time
from dataclasses import dataclass, field
from typing import Dict, Iterable, List, Optional, Tuple

import pandas as pd
import requests


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)

NPI_API_URL = "https://npiregistry.cms.hhs.gov/api/"
# Endpoint for the CMS Provider Data Catalog API.  We use the
# hospital general information dataset (ID: xubh-q36u).  Note: this endpoint
# may change; consult CMS documentation if queries fail.
CCN_API_URL = (
    "https://data.cms.gov/provider-data/api/1/datastore/query/xubh-q36u/0"
)


@dataclass
class FacilityRecord:
    """Represents a healthcare facility and the associated NPI/CMS details."""

    facility_name: str
    city: Optional[str]
    state: Optional[str]
    country: Optional[str] = "US"
    npi: Optional[str] = None
    dba_name: Optional[str] = None
    taxonomy: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    ccn: Optional[str] = None
    notes: Optional[str] = None
    source_npi_count: int = 0  # number of candidate NPI results returned
    debug_info: Dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Optional[str]]:
        """Convert record to a dictionary for CSV output."""
        return {
            "Facility": self.facility_name,
            "City": self.city,
            "State": self.state,
            "Country": self.country,
            "NPI": self.npi,
            "DBA": self.dba_name,
            "Primary Taxonomy": self.taxonomy,
            "Phone": self.phone,
            "Address": self.address,
            "CCN": self.ccn,
            "Notes": self.notes,
            "Candidate NPI Count": str(self.source_npi_count),
        }


def query_npi_registry(
    name: str,
    city: Optional[str] = None,
    state: Optional[str] = None,
    limit: int = 10,
    timeout: int = 20,
) -> List[Dict[str, any]]:
    """
    Query the CMS NPI registry API for a given organization name and optional
    location.  Returns a list of provider objects (dictionaries) as provided
    by the API.  If the API call fails, an empty list is returned.

    Parameters
    ----------
    name : str
        The organization name to search for. A trailing wildcard is implied by
        the API, so partial names may match multiple providers.
    city : str, optional
        The city portion of the practice location. Helps to narrow results.
    state : str, optional
        The two‑letter state abbreviation. Required when `city` is provided.
    limit : int
        Maximum number of results to return (API allows up to 200).  Default is
        10.
    timeout : int
        HTTP request timeout in seconds.

    Returns
    -------
    list
        A list of provider dictionaries.  Each provider object contains
        `number` (NPI), `basic` info, `addresses`, `taxonomies`, etc.
    """
    params = {"version": "2.1", "organization_name": name, "limit": limit}
    if city:
        params["city"] = city
    if state:
        params["state"] = state
    try:
        response = requests.get(NPI_API_URL, params=params, timeout=timeout)
        response.raise_for_status()
    except Exception as exc:
        logging.warning("NPI API request failed for %s: %s", name, exc)
        return []
    try:
        data = response.json()
    except Exception as exc:
        logging.warning("Failed to parse JSON for %s: %s", name, exc)
        return []
    return data.get("results", [])


def choose_best_provider(
    facility_name: str, candidates: List[Dict[str, any]],
) -> Optional[Dict[str, any]]:
    """
    Given a list of provider results from the NPI API, pick the entry that
    best matches the facility name.  The current implementation uses
    case‑insensitive containment: a candidate is considered a strong match if
    the facility name appears within the provider's registered name or DBA.

    If no strong matches are found, the first result is returned as a fallback.

    Parameters
    ----------
    facility_name : str
        The facility name from the input CSV.
    candidates : list
        A list of provider dictionaries from the NPI API.

    Returns
    -------
    dict or None
        The best matching provider dictionary, or None if there are no
        candidates.
    """
    facility_lower = facility_name.lower()
    strong_matches = []
    for provider in candidates:
        # Basic organization name
        basic = provider.get("basic", {})
        org_name = basic.get("organization_name", "").lower()
        # Other (DBA) names
        other_names = provider.get("other_names", []) or []
        dba_names = [n.get("organization_name", "").lower() for n in other_names]
        # Check if facility name is contained in any available names
        names_to_check = [org_name] + dba_names
        if any(facility_lower in nm for nm in names_to_check if nm):
            strong_matches.append(provider)
    if strong_matches:
        # Choose the first strong match
        return strong_matches[0]
    # Fallback to the first result if no strong match
    return candidates[0] if candidates else None


def extract_provider_details(provider: Dict[str, any]) -> Tuple[str, str, str, str, str]:
    """
    Extract relevant fields from a provider dictionary returned by the NPI API.

    Returns
    -------
    tuple
        (NPI number, DBA name, taxonomy description, practice phone, practice address)
    """
    number = provider.get("number")
    basic = provider.get("basic", {})
    # DBA name may be in other_names with use code 'DBA'.  If none found, fall
    # back to the primary organization name.
    dba_name = None
    for name_entry in provider.get("other_names", []):
        if name_entry.get("type") == "DBA" and name_entry.get("organization_name"):
            dba_name = name_entry["organization_name"]
            break
    if not dba_name:
        dba_name = basic.get("organization_name")
    # Primary taxonomy description (desc) from taxonomies list
    taxonomy = None
    for tax in provider.get("taxonomies", []):
        # Choose a taxonomy marked as primary or the first one in the list
        if tax.get("primary"):
            taxonomy = tax.get("desc")
            break
    if not taxonomy and provider.get("taxonomies"):
        taxonomy = provider["taxonomies"][0].get("desc")
    # Practice location is the first entry in addresses array
    address = None
    phone = None
    for addr in provider.get("addresses", []):
        if addr.get("address_purpose") == "LOCATION":
            address = f"{addr.get('address_1', '')} {addr.get('address_2', '')}, {addr.get('city', '')}, {addr.get('state', '')} {addr.get('postal_code', '')}".strip()
            phone = addr.get("telephone_number")
            break
    return number, dba_name, taxonomy, phone, address


def query_ccn_for_npi(npi: str, timeout: int = 20) -> Optional[str]:
    """
    Attempt to cross‑reference an NPI to a Medicare CMS Certification Number (CCN).
    This function calls the CMS Provider Data Catalog API using the hospital
    dataset.  Because not all provider types appear in this dataset, this
    cross‑mapping is best effort and may return None.  If multiple matches are
    found, the first CCN is returned.

    Parameters
    ----------
    npi : str
        The NPI for which to find a CCN.
    timeout : int
        HTTP request timeout in seconds.

    Returns
    -------
    str or None
        The CCN corresponding to the provider's NPI, or None if not found.
    """
    # The hospital general information dataset does not expose NPI directly,
    # so this function would normally join through other datasets or require
    # prior knowledge.  As a placeholder, we illustrate how to query a CMS
    # dataset via the Socrata API.  Users should replace this with an
    # appropriate crosswalk dataset.
    params = {
        "limit": 5,
        # Additional query parameters could be added here to filter by facility
        # name, city, or state once they are known.  Without a published NPI
        # column in this dataset, CCN lookup must be performed via an
        # alternative source.
    }
    try:
        response = requests.get(CCN_API_URL, params=params, timeout=timeout)
        response.raise_for_status()
        # Parse JSON but ignore data; cross‑mapping not implemented
    except Exception as exc:
        logging.debug("CCN API request failed for NPI %s: %s", npi, exc)
    # Cross‑walk not implemented; return None
    return None


def enrich_facility_record(
    record: FacilityRecord,
    include_ccn: bool = False,
    api_limit: int = 10,
    sleep_seconds: float = 0.1,
) -> FacilityRecord:
    """
    Given a FacilityRecord with facility_name, city, and state populated,
    query the NPI registry and optionally the CCN API to fill in additional
    details.  The updated record is returned.

    Parameters
    ----------
    record : FacilityRecord
        The facility record to enrich.  Only facility_name, city, state and
        country need to be set initially.
    include_ccn : bool
        Whether to attempt CCN lookup via the CMS Provider Data Catalog.  Defaults
        to False.
    api_limit : int
        Maximum number of NPI results to retrieve per facility.  A smaller value
        reduces the likelihood of ambiguous matches.  The API allows up to 200.
    sleep_seconds : float
        Time (in seconds) to wait between successive API requests.  Helps to
        avoid rate limits.

    Returns
    -------
    FacilityRecord
        The enriched facility record with NPI details populated.
    """
    # Query NPI registry for the facility
    candidates = query_npi_registry(
        name=record.facility_name,
        city=record.city,
        state=record.state,
        limit=api_limit,
    )
    record.source_npi_count = len(candidates)
    if not candidates:
        record.notes = "NPI not found"
        return record
    # Choose the best provider match
    provider = choose_best_provider(record.facility_name, candidates)
    if not provider:
        record.notes = "No suitable NPI match"
        return record
    # Extract provider details
    record.npi, record.dba_name, record.taxonomy, record.phone, record.address = (
        extract_provider_details(provider)
    )
    # Optionally query for CCN
    if include_ccn and record.npi:
        record.ccn = query_ccn_for_npi(record.npi)
    # Sleep briefly to respect API rate limits
    time.sleep(sleep_seconds)
    return record


def read_facility_list(path: str) -> Iterable[FacilityRecord]:
    """
    Read a CSV file containing facilities and yield FacilityRecord objects.

    The input CSV should have at least the columns 'Facility Name', 'City', and
    'State / Region'.  Additional columns are ignored.

    Parameters
    ----------
    path : str
        The path to the CSV file.

    Yields
    ------
    FacilityRecord
        A FacilityRecord with facility_name, city, state, and country.
    """
    df = pd.read_csv(path)
    # Normalize column names
    df.columns = [c.strip().lower() for c in df.columns]
    name_col = None
    city_col = None
    state_col = None
    for col in df.columns:
        if "facility" in col and "name" in col:
            name_col = col
        elif "city" in col:
            city_col = col
        elif "state" in col:
            state_col = col
    if not name_col:
        raise ValueError(f"Facility name column not found in {path}")
    for _, row in df.iterrows():
        facility = FacilityRecord(
            facility_name=str(row.get(name_col, "")).strip(),
            city=str(row.get(city_col, "")).strip() if city_col else None,
            state=str(row.get(state_col, "")).strip() if state_col else None,
            country="US",
        )
        # Skip blank facility names
        if facility.facility_name:
            yield facility


def write_records_to_csv(records: List[FacilityRecord], output_path: str) -> None:
    """
    Write a list of FacilityRecord objects to a CSV file.

    Parameters
    ----------
    records : list of FacilityRecord
        The enriched facility records to output.
    output_path : str
        Path to the output CSV file.
    """
    fieldnames = [
        "Facility",
        "City",
        "State",
        "Country",
        "NPI",
        "DBA",
        "Primary Taxonomy",
        "Phone",
        "Address",
        "CCN",
        "Notes",
        "Candidate NPI Count",
    ]
    with open(output_path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for rec in records:
            writer.writerow(rec.to_dict())


def parse_arguments(argv: Optional[List[str]] = None) -> argparse.Namespace:
    """
    Parse command‑line arguments.

    Parameters
    ----------
    argv : list of str, optional
        List of command‑line arguments.  If None, defaults to sys.argv[1:].

    Returns
    -------
    argparse.Namespace
        Parsed arguments.
    """
    parser = argparse.ArgumentParser(
        description="Enrich facility lists with NPI and optional CCN details"
    )
    parser.add_argument(
        "--input",
        action="append",
        required=True,
        help="Path to an input CSV file containing facilities.",
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Path to the output CSV file with enriched data.",
    )
    parser.add_argument(
        "--include_ccn",
        action="store_true",
        help="Attempt to cross‑map NPI values to CMS Certification Numbers (CCNs)",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=10,
        help="Maximum number of NPI results to query per facility (1–200)",
    )
    parser.add_argument(
        "--rate_limit",
        type=float,
        default=0.1,
        help="Seconds to wait between API requests (to avoid rate limiting)",
    )
    return parser.parse_args(argv)


def main(argv: Optional[List[str]] = None) -> None:
    args = parse_arguments(argv)
    all_records: List[FacilityRecord] = []
    # Read and enrich each input file
    for input_path in args.input:
        logging.info("Processing %s", input_path)
        for record in read_facility_list(input_path):
            try:
                enriched = enrich_facility_record(
                    record,
                    include_ccn=args.include_ccn,
                    api_limit=args.limit,
                    sleep_seconds=args.rate_limit,
                )
                all_records.append(enriched)
            except Exception as exc:
                logging.error(
                    "Error processing facility %s: %s", record.facility_name, exc
                )
    # Write output file
    write_records_to_csv(all_records, args.output)
    logging.info(
        "Completed processing %d facilities. Output written to %s",
        len(all_records),
        args.output,
    )


if __name__ == "__main__":
    main()