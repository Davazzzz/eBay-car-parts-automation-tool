from ebaysdk.finding import Connection as Finding
from typing import List, Dict, Optional
import statistics
from config import Config

class EbayAPI:
    """Handles eBay API interactions"""

    def __init__(self):
        self.api = None
        self.connect()

    def connect(self):
        """Initialize eBay API connection"""
        try:
            if not Config.EBAY_APP_ID:
                print("[WARNING] eBay API credentials not configured - using demo mode")
                return

            self.api = Finding(
                appid=Config.EBAY_APP_ID,
                config_file=None,
                domain='svcs.ebay.com' if Config.EBAY_ENVIRONMENT == 'production' else 'svcs.sandbox.ebay.com'
            )
            print("[OK] Connected to eBay API")

        except Exception as e:
            print(f"[ERROR] Error connecting to eBay API: {e}")
            self.api = None

    def search_sold_items(self, year: str, make: str, model: str, part_name: str, days: int = 30) -> Dict:
        """
        Search eBay sold listings for a specific part

        Returns:
            {
                'median_price': float,
                'average_price': float,
                'sold_count': int,
                'active_listings': int,
                'best_listing': {
                    'title': str,
                    'price': float,
                    'url': str,
                    'image': str
                },
                'all_prices': list
            }
        """

        if not self.api:
            return self._demo_data(part_name)

        try:
            # Build search query
            query = f"{year} {make} {model} {part_name} used"

            # Search sold items
            sold_response = self.api.execute('findCompletedItems', {
                'keywords': query,
                'itemFilter': [
                    {'name': 'SoldItemsOnly', 'value': True},
                    {'name': 'EndTimeFrom', 'value': f'2024-{30-days:02d}-01T00:00:00.000Z'}
                ],
                'sortOrder': 'PricePlusShippingLowest',
                'paginationInput': {'entriesPerPage': 100}
            })

            # Search active items
            active_response = self.api.execute('findItemsAdvanced', {
                'keywords': query,
                'paginationInput': {'entriesPerPage': 100}
            })

            # Process sold items
            sold_items = self._parse_sold_items(sold_response)
            active_count = self._count_active_items(active_response)

            return self._calculate_metrics(sold_items, active_count)

        except Exception as e:
            print(f"[ERROR] Error searching eBay: {e}")
            return self._demo_data(part_name)

    def _parse_sold_items(self, response) -> List[Dict]:
        """Parse eBay API response for sold items"""
        items = []

        try:
            search_result = response.dict()
            if 'searchResult' in search_result:
                item_list = search_result['searchResult'].get('item', [])

                for item in item_list:
                    price = float(item['sellingStatus']['currentPrice']['value'])

                    items.append({
                        'title': item.get('title', ''),
                        'price': price,
                        'url': item.get('viewItemURL', ''),
                        'image': item.get('galleryURL', '')
                    })
        except Exception as e:
            print(f"[ERROR] Error parsing sold items: {e}")

        return items

    def _count_active_items(self, response) -> int:
        """Count active listings from response"""
        try:
            search_result = response.dict()
            return int(search_result.get('paginationOutput', {}).get('totalEntries', 0))
        except:
            return 0

    def _calculate_metrics(self, sold_items: List[Dict], active_count: int) -> Dict:
        """Calculate price metrics from sold items"""

        if not sold_items:
            return {
                'median_price': 0,
                'average_price': 0,
                'sold_count': 0,
                'active_listings': active_count,
                'best_listing': None,
                'all_prices': []
            }

        prices = [item['price'] for item in sold_items]

        # Remove outliers (prices > 3 standard deviations from mean)
        if len(prices) > 3:
            mean = statistics.mean(prices)
            stdev = statistics.stdev(prices)
            prices = [p for p in prices if abs(p - mean) <= 3 * stdev]

        return {
            'median_price': statistics.median(prices) if prices else 0,
            'average_price': statistics.mean(prices) if prices else 0,
            'sold_count': len(sold_items),
            'active_listings': active_count,
            'best_listing': sold_items[0] if sold_items else None,
            'all_prices': prices
        }

    def _demo_data(self, part_name: str) -> Dict:
        """Return demo data when API is not configured"""
        return {
            'median_price': 0,
            'average_price': 0,
            'sold_count': 0,
            'active_listings': 0,
            'best_listing': {
                'title': f'[DEMO MODE] {part_name}',
                'price': 0,
                'url': 'https://ebay.com',
                'image': ''
            },
            'all_prices': []
        }
