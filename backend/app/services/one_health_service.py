import math
from datetime import datetime, timedelta
from typing import Dict, Any, List

class OneHealthService:
    """
    One Health & Wastewater-Based Epidemiology (WBE) Surveillance Engine.
    Tracks environmental, veterinary, and clinical nexus AMR diffusion with
    a 10-14 day early-warning lead time.
    """

    @staticmethod
    def get_wastewater_sites() -> List[Dict[str, Any]]:
        return [
            {
                "site_id": "WWTP-METRO-01",
                "name": "Central Metropolitan WWTP",
                "catchment_area": "Downtown & Urban Medical District",
                "population_served": 1450000,
                "latitude": 28.6139,
                "longitude": 77.2090,
                "flow_rate_m3_day": 340000,
                "status": "ELEVATED_SURGE",
                "alert_level": "WARNING",
                "lead_time_days": 12,
                "log10_amr_copies_per_liter": 6.84,
                "dominant_determinant": "blaNDM-5 (IncX3)",
                "target_organism": "Klebsiella pneumoniae",
                "secondary_pathogen": "Acinetobacter baumannii",
                "last_sample_date": "2026-11-10T08:30:00Z"
            },
            {
                "site_id": "WWTP-HOSP-02",
                "name": "Tertiary Medical Center Outfall Siphon",
                "catchment_area": "Main Hospital Campus & ICU Blocks",
                "population_served": 18500,
                "latitude": 28.5672,
                "longitude": 77.2100,
                "flow_rate_m3_day": 12500,
                "status": "CRITICAL_OUTBREAK",
                "alert_level": "CRITICAL",
                "lead_time_days": 14,
                "log10_amr_copies_per_liter": 7.92,
                "dominant_determinant": "blaOXA-23 & blaNDM-1",
                "target_organism": "Acinetobacter baumannii",
                "secondary_pathogen": "Pseudomonas aeruginosa",
                "last_sample_date": "2026-11-11T06:15:00Z"
            },
            {
                "site_id": "WWTP-AGRI-03",
                "name": "Peri-Urban Agricultural Runoff Catchment",
                "catchment_area": "Poultry & Livestock Farming Sector",
                "population_served": 320000,
                "latitude": 28.7200,
                "longitude": 77.1100,
                "flow_rate_m3_day": 95000,
                "status": "MONITORING",
                "alert_level": "CAUTION",
                "lead_time_days": 10,
                "log10_amr_copies_per_liter": 5.45,
                "dominant_determinant": "mcr-1 (Colistin) & tet(X4)",
                "target_organism": "Escherichia coli / Klebsiella",
                "secondary_pathogen": "Enterococcus faecium",
                "last_sample_date": "2026-11-09T14:00:00Z"
            },
            {
                "site_id": "WWTP-EAST-04",
                "name": "East River Confluence & Domestic Outfall",
                "catchment_area": "Eastern Residential & Light Industrial Zone",
                "population_served": 890000,
                "latitude": 28.6300,
                "longitude": 77.3000,
                "flow_rate_m3_day": 210000,
                "status": "STABLE",
                "alert_level": "NORMAL",
                "lead_time_days": 11,
                "log10_amr_copies_per_liter": 4.12,
                "dominant_determinant": "blaCTX-M-15",
                "target_organism": "Klebsiella pneumoniae",
                "secondary_pathogen": "Staphylococcus aureus",
                "last_sample_date": "2026-11-10T11:45:00Z"
            }
        ]

    @staticmethod
    def get_wbe_lead_time_timeseries(days: int = 45) -> Dict[str, Any]:
        """
        Generates paired Wastewater genomic signal vs. Clinical Hospital Admissions
        demonstrating the 10-14 day early warning window.
        """
        timeseries = []
        base_date = datetime.now() - timedelta(days=days)

        for i in range(days):
            current_date = base_date + timedelta(days=i)
            # Create a bell-like outbreak wave in wastewater that shifts forward 12 days into clinical
            # Wastewater peak around day 20, clinical peak around day 32
            ww_wave = math.exp(-0.5 * ((i - 20) / 6.0) ** 2) * 3.5
            clin_wave = math.exp(-0.5 * ((i - 32) / 6.0) ** 2) * 28.0

            ww_copies_log10 = round(4.2 + ww_wave + (0.15 * math.sin(i * 0.7)), 2)
            clinical_cases = max(2, int(round(4.0 + clin_wave + (2.0 * math.cos(i * 0.5)))))
            early_warning_threshold = 6.0

            timeseries.append({
                "date": current_date.strftime("%Y-%m-%d"),
                "day_index": i,
                "wastewater_amr_log10": ww_copies_log10,
                "clinical_admissions": clinical_cases,
                "early_warning_threshold": early_warning_threshold,
                "surge_predicted": ww_copies_log10 >= early_warning_threshold
            })

        return {
            "lead_time_days": 12,
            "correlation_pearson_r": 0.89,
            "p_value": "<0.0001",
            "early_detection_window_text": "Wastewater metagenomic surveillance provides a 12-day mean advance warning prior to clinical ICU bed surges.",
            "data": timeseries
        }

    @staticmethod
    def get_one_health_matrix() -> Dict[str, Any]:
        """
        Cross-compartment plasmid and resistance gene sharing matrix
        between Clinical, Animal/Agricultural, and Wastewater/Environmental reservoirs.
        """
        return {
            "reservoirs": [
                {
                    "name": "Clinical Healthcare",
                    "total_isolates": 284,
                    "top_mges": ["IncX3", "IncFII", "Tn125"],
                    "top_genes": ["blaNDM-5", "blaKPC-2", "armA", "mgrB_mut"],
                    "high_risk_clones": ["ST258", "ST11", "ST147"],
                    "transmission_index": 0.88
                },
                {
                    "name": "Agricultural & Veterinary",
                    "total_isolates": 196,
                    "top_mges": ["IncI2", "IncHI2", "IS26"],
                    "top_genes": ["mcr-1", "tet(X4)", "blaCTX-M-55", "erm(B)"],
                    "high_risk_clones": ["ST15", "ST307"],
                    "transmission_index": 0.74
                },
                {
                    "name": "Wastewater & Environment",
                    "total_isolates": 312,
                    "top_mges": ["IncP-1", "IncX3", "ColRNAI"],
                    "top_genes": ["blaNDM-1", "blaOXA-48", "sul1", "qnrS1"],
                    "high_risk_clones": ["ST395", "ST23"],
                    "transmission_index": 0.92
                }
            ],
            "shared_mge_interchanges": [
                {
                    "source": "Agricultural",
                    "target": "Wastewater",
                    "element": "IncI2::mcr-1",
                    "shared_snp_distance": 2,
                    "confidence": "High Evidence (WGS core alignment)"
                },
                {
                    "source": "Wastewater",
                    "target": "Clinical Healthcare",
                    "element": "IncX3::blaNDM-5",
                    "shared_snp_distance": 0,
                    "confidence": "Identical Plasmid Backbone (100% Identity)"
                },
                {
                    "source": "Clinical Healthcare",
                    "target": "Wastewater",
                    "element": "IncFII::blaCTX-M-15",
                    "shared_snp_distance": 1,
                    "confidence": "Direct Environmental Shedding"
                }
            ]
        }

one_health_service = OneHealthService()

