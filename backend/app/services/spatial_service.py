import re
import math
import time
from typing import List, Dict, Any, Optional, Tuple
from sqlalchemy.orm import Session
from app.models.isolate import Isolate
from app.models.amr import AMRDeterminant

# Known Geographic Reference Coordinates for Regional Calibration
CITY_COORDINATES_REGISTRY = {
    "vadodara": (22.3072, 73.1812),
    "ahmedabad": (23.0225, 72.5714),
    "mumbai": (19.0760, 72.8777),
    "delhi": (28.6139, 77.2090),
    "new delhi": (28.6139, 77.2090),
    "boston": (42.3601, -71.0589),
    "shanghai": (31.2304, 121.4737),
    "rome": (41.9028, 12.4964),
    "athens": (37.9838, 23.7275),
    "sao paulo": (-23.5505, -46.6333),
    "são paulo": (-23.5505, -46.6333),
    "london": (51.5074, -0.1278),
    "atlanta": (33.7490, -84.3880)
}

def haversine_distance_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculates great-circle distance between two decimal degree points on Earth."""
    R = 6371.0  # Earth radius in kilometers
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = (math.sin(delta_phi / 2.0) ** 2 +
         math.cos(phi1) * math.cos(phi2) * (math.sin(delta_lambda / 2.0) ** 2))
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
    return R * c

class GeospatialSurveillanceService:
    """Manages PostGIS queries, spatial clustering, and safe parameterized natural language translation."""

    @staticmethod
    def get_spatial_clusters(
        db: Session,
        organism: Optional[str] = None,
        country: Optional[str] = None,
        year: Optional[int] = None,
        gene: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Queries isolates with coordinates and attached surveillance attributes."""
        query = db.query(Isolate).filter(Isolate.latitude.isnot(None), Isolate.longitude.isnot(None))

        if organism:
            query = query.filter(Isolate.organism.ilike(f"%{organism}%"))
        if country:
            query = query.filter(Isolate.country.ilike(f"%{country}%"))
        if year:
            query = query.filter(Isolate.collection_year == year)

        isolates = query.all()
        results = []

        for iso in isolates:
            carbs = [d.gene_symbol for d in iso.amr_determinants if d.subclass == "Carbapenem"]
            colistin = [d.gene_symbol for d in iso.amr_determinants if d.subclass == "Colistin"]
            
            # If gene filter requested
            if gene:
                all_genes = [d.gene_symbol.lower() for d in iso.amr_determinants]
                if not any(gene.lower() in g for g in all_genes):
                    continue

            st = iso.molecular_types[0].sequence_type if iso.molecular_types else None

            results.append({
                "id": iso.id,
                "latitude": iso.latitude,
                "longitude": iso.longitude,
                "accession": iso.accession,
                "organism": iso.organism,
                "sequence_type": st,
                "carbapenemases": carbs,
                "colistin_genes": colistin,
                "country": iso.country,
                "city": iso.city,
                "collection_year": iso.collection_year,
                "qc_status": iso.qc_status
            })

        return results

    @staticmethod
    def parse_and_execute_nl_query(db: Session, query_text: str) -> Dict[str, Any]:
        """
        Translates natural language questions like:
        'Show all K. pneumoniae isolates with blaNDM within 50 km of Vadodara'
        into safe parameterized ORM query filters with distance thresholding.
        ZERO raw SQL is generated or executed.
        """
        start_time = time.time()
        lower_q = query_text.lower()

        # 1. Extract Target Organism
        organism = "Klebsiella pneumoniae"
        if "e. coli" in lower_q or "escherichia coli" in lower_q:
            organism = "Escherichia coli"
        elif "acinetobacter" in lower_q:
            organism = "Acinetobacter baumannii"
        elif "salmonella" in lower_q:
            organism = "Salmonella enterica"

        # 2. Extract AMR Gene determinant
        gene_match = re.search(r'\b(blandm[\w\-]*|blakpc[\w\-]*|blaoxa[\w\-]*|blavim[\w\-]*|blaimp[\w\-]*|mcr[\w\-]*|arm[\w\-]*|gyra[\w\-]*)\b', lower_q)
        target_gene = gene_match.group(1) if gene_match else None
        # Handle cases like "with blaNDM"
        if not target_gene and "ndm" in lower_q:
            target_gene = "blandm"
        elif not target_gene and "kpc" in lower_q:
            target_gene = "blakpc"
        elif not target_gene and "oxa" in lower_q:
            target_gene = "blaoxa"
        elif not target_gene and "colistin" in lower_q:
            target_gene = "mcr"

        # 3. Extract Proximity Radius (km)
        dist_match = re.search(r'(\d+)\s*(?:km|kilometers|kilometer)', lower_q)
        radius_km = float(dist_match.group(1)) if dist_match else 100.0

        # 4. Extract Target City/Location
        target_city = None
        target_coords: Optional[Tuple[float, float]] = None

        for city_name, coords in CITY_COORDINATES_REGISTRY.items():
            if city_name in lower_q:
                target_city = city_name.title()
                target_coords = coords
                break

        # Execute safe parameterized filtering
        base_clusters = GeospatialSurveillanceService.get_spatial_clusters(
            db,
            organism=organism,
            gene=target_gene
        )

        matched_isolates = []
        if target_coords:
            c_lat, c_lon = target_coords
            for item in base_clusters:
                d = haversine_distance_km(c_lat, c_lon, item["latitude"], item["longitude"])
                if d <= radius_km:
                    item_copy = dict(item)
                    item_copy["distance_km"] = round(d, 2)
                    matched_isolates.append(item_copy)
        else:
            matched_isolates = base_clusters

        elapsed = (time.time() - start_time) * 1000.0

        return {
            "interpreted_query": {
                "organism": organism,
                "target_gene": target_gene,
                "radius_km": radius_km if target_coords else None,
                "target_location": target_city,
                "center_coordinates": target_coords
            },
            "total_matched": len(matched_isolates),
            "matched_isolates": matched_isolates,
            "execution_time_ms": round(elapsed, 2)
        }

spatial_service = GeospatialSurveillanceService()

