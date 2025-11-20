from typing import List, Dict
import time
from ebay_api import EbayAPI
from junkyard_prices import JunkyardPrices

class PartsAnalyzer:
    """Analyzes car parts for ROI potential"""

    # HIGH-PRIORITY PARTS: Most profitable, frequently sold parts
    # Based on market research - these typically have best ROI
    HIGH_PRIORITY_PARTS = [
        # Electronics (HIGH ROI)
        "RADIO",
        "RADIO WITH DISPLAY",
        "RADIO WITHOUT DISPLAY",
        "INSTRUMENT CLUSTER",
        "SPEEDOMETER HEAD ONLY",
        "NAVIGATION GPS SCREEN",
        "DISPLAY SCREEN",
        "ECM (ELECTRONIC CONTROL MODULE)",
        "TCM (TRANSMISSION CONTROL MOD.)",

        # Lighting (GOOD ROI, HIGH DEMAND)
        "HEADLIGHT",
        "TAILLIGHT",
        "FOG LIGHT",

        # Interior Electronics & Components (MEDIUM-HIGH ROI)
        "STEERING WHEEL",
        "CLIMATE CONTROL",
        "SWITCH PANEL",
        "CENTER CONSOLE",
        "MIRROR (SIDE VIEW)",
        "INTERIOR MIRROR",

        # Seats & Airbags (GOOD ROI)
        "SEAT WITH AIR BAG FRONT",
        "SEAT NO AIR BAG FRONT",
        "AIR BAG (FRONT, DRIVER)",
        "AIR BAG (FRONT, PASSENGER)",

        # Body Parts (CONSISTENT DEMAND)
        "GRILLE",
        "BUMPER COVER, FRONT",
        "DOOR, FRONT",
        "HOOD",
        "FENDER",
        "WHEEL (ALUMINUM)"
    ]

    # Interior/easy-to-carry parts (lightweight, good for delivery)
    INTERIOR_KEYWORDS = [
        "CONSOLE", "DASHBOARD", "DASH", "GLOVE", "STEERING", "SEAT",
        "DOOR PANEL", "ARMREST", "CARPET", "HEADLINER", "VISOR",
        "MIRROR", "RADIO", "INSTRUMENT", "CLUSTER", "TRIM", "HANDLE",
        "SWITCH", "VENT", "SHIFTER", "BEZEL", "CUBBY", "ASHTRAY",
        "CUP HOLDER", "KNOB", "BUTTON", "CLOCK"
    ]

    # Light exterior parts (easy to remove/carry)
    LIGHT_EXTERIOR_KEYWORDS = [
        "HEADLIGHT", "TAILLIGHT", "BUMPER COVER", "GRILLE", "EMBLEM",
        "DOOR", "HOOD", "WHEEL", "HUBCAP", "BADGE"
    ]

    def __init__(self, ebay_api: EbayAPI, junkyard_prices: JunkyardPrices):
        self.ebay = ebay_api
        self.junkyard = junkyard_prices

    def get_parts_list(self, vehicle_type: str = "car", filter_type: str = "all") -> List[str]:
        """
        Get parts from junkyard database with optional filtering

        filter_type options:
        - 'all': All 441 parts
        - 'high_priority': Top 20-30 most profitable parts (RECOMMENDED)
        - 'interior': Interior and easy-to-carry parts only
        - 'light': Interior + light exterior parts
        """
        all_parts = self.junkyard.get_all_parts()

        if filter_type == "high_priority":
            # Return only high-priority parts that exist in junkyard database
            filtered = []
            for priority_part in self.HIGH_PRIORITY_PARTS:
                # Find matching parts in junkyard list (case-insensitive)
                for junkyard_part in all_parts:
                    if priority_part.upper() in junkyard_part.upper() or junkyard_part.upper() in priority_part.upper():
                        if junkyard_part not in filtered:
                            filtered.append(junkyard_part)
            return filtered[:30]  # Limit to 30 parts max

        if filter_type == "all":
            return all_parts

        # Filter for interior/easy parts
        filtered = []
        for part in all_parts:
            part_upper = part.upper()

            if filter_type == "interior":
                # Only interior parts
                if any(keyword in part_upper for keyword in self.INTERIOR_KEYWORDS):
                    filtered.append(part)

            elif filter_type == "light":
                # Interior + light exterior
                if any(keyword in part_upper for keyword in self.INTERIOR_KEYWORDS + self.LIGHT_EXTERIOR_KEYWORDS):
                    filtered.append(part)

        return filtered if filtered else all_parts

    def analyze_part(self, year: str, make: str, model: str, part_name: str) -> Dict:
        """
        Analyze a single part for ROI potential

        Returns:
            {
                'part_name': str,
                'junkyard_price': float,
                'median_sold_price': float,
                'average_sold_price': float,
                'sold_count': int,
                'active_listings': int,
                'roi': float,
                'roi_rating': str,
                'best_listing_title': str,
                'best_listing_url': str,
                'best_listing_image': str
            }
        """

        # Get junkyard price
        junkyard_price = self.junkyard.get_price(part_name)

        if junkyard_price is None:
            return {
                'part_name': part_name,
                'error': 'Part not found in junkyard price list'
            }

        # Get eBay market data
        ebay_data = self.ebay.search_sold_items(year, make, model, part_name)

        # Calculate ROI
        roi = 0
        if junkyard_price > 0 and ebay_data['median_price'] > 0:
            roi = ebay_data['median_price'] / junkyard_price

        # Determine ROI rating
        if roi < 2:
            roi_rating = "Low"
        elif roi < 5:
            roi_rating = "Medium"
        else:
            roi_rating = "High"

        # Build result
        result = {
            'part_name': part_name,
            'junkyard_price': junkyard_price,
            'median_sold_price': ebay_data['median_price'],
            'average_sold_price': ebay_data['average_price'],
            'sold_count': ebay_data['sold_count'],
            'active_listings': ebay_data['active_listings'],
            'roi': roi,
            'roi_rating': roi_rating,
            'best_listing_title': ebay_data['best_listing']['title'] if ebay_data['best_listing'] else '',
            'best_listing_url': ebay_data['best_listing']['url'] if ebay_data['best_listing'] else '',
            'best_listing_image': ebay_data['best_listing']['image'] if ebay_data['best_listing'] else ''
        }

        return result

    def analyze_vehicle(self, year: str, make: str, model: str, vehicle_type: str = "car", filter_type: str = "high_priority") -> List[Dict]:
        """
        Analyze all relevant parts for a vehicle

        filter_type:
        - 'high_priority': Top 20-30 most profitable parts (FAST - 2-3 min) [DEFAULT - RECOMMENDED]
        - 'light': Interior + light exterior parts (~120 parts, SLOW - 10+ min)
        - 'all': Analyze all 441 parts (VERY SLOW - 30+ min)

        Returns list of part analysis results
        """
        parts_list = self.get_parts_list(vehicle_type, filter_type)
        results = []

        total = len(parts_list)
        print(f"\n{'='*60}")
        print(f"Analyzing {total} parts for {year} {make} {model}")
        print(f"Filter: {filter_type.upper()}")
        print(f"Adding 1-second delay between searches to avoid rate limits")
        print(f"{'='*60}\n")

        for i, part in enumerate(parts_list, 1):
            print(f"[{i}/{total}] Analyzing: {part}...")
            result = self.analyze_part(year, make, model, part)

            if 'error' not in result:
                results.append(result)

            # Add delay to avoid eBay rate limiting (except on last item)
            if i < total:
                time.sleep(1)  # 1 second delay between searches

        print(f"\n{'='*60}")
        print(f"Analysis complete! Found {len(results)} parts with data")
        print(f"{'='*60}\n")

        # Sort by ROI (highest first)
        results.sort(key=lambda x: x['roi'], reverse=True)

        return results

    def filter_by_roi(self, results: List[Dict], min_roi: float = 5.0) -> List[Dict]:
        """Filter results by minimum ROI"""
        return [r for r in results if r['roi'] >= min_roi]

    def sort_by_frequency(self, results: List[Dict]) -> List[Dict]:
        """Sort results by sold frequency"""
        return sorted(results, key=lambda x: x['sold_count'], reverse=True)

    def get_top_parts(self, results: List[Dict], count: int = 5) -> List[Dict]:
        """Get top N parts by ROI"""
        return results[:count]
