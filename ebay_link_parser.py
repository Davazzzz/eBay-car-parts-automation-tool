import requests
from bs4 import BeautifulSoup
import re
from typing import Dict, Optional

class EbayLinkParser:
    """Parse eBay listing links to extract part info and price"""

    @staticmethod
    def parse_link(ebay_url: str) -> Dict:
        """
        Parse an eBay listing URL to extract:
        - Item title
        - Price
        - Vehicle year/make/model (if detectable)

        Returns dict with extracted info
        """
        try:
            # Send request to eBay
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(ebay_url, headers=headers, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')

            # Extract title
            title = None
            title_elem = soup.find('h1', {'class': 'x-item-title__mainTitle'})
            if not title_elem:
                title_elem = soup.find('h1', {'id': 'itemTitle'})
            if title_elem:
                title = title_elem.get_text().strip()

            # Extract price
            price = None
            # Try sold/completed listing price first
            price_elem = soup.find('div', {'class': 'x-price-primary'})
            if not price_elem:
                price_elem = soup.find('span', {'id': 'prcIsum'})
            if not price_elem:
                price_elem = soup.find('span', {'class': 'notranslate'})

            if price_elem:
                price_text = price_elem.get_text().strip()
                # Extract numeric price
                price_match = re.search(r'\$?([\d,]+\.?\d*)', price_text)
                if price_match:
                    price = float(price_match.group(1).replace(',', ''))

            # Try to detect vehicle info from title
            year = None
            make = None
            model = None

            if title:
                # Look for year (4 digits)
                year_match = re.search(r'\b(19\d{2}|20[0-2]\d)\b', title)
                if year_match:
                    year = year_match.group(1)

                # Common makes
                makes = ['Honda', 'Toyota', 'Ford', 'Chevy', 'Chevrolet', 'Dodge',
                        'Nissan', 'BMW', 'Mercedes', 'Audi', 'Volkswagen', 'VW',
                        'Mazda', 'Subaru', 'Kia', 'Hyundai', 'Jeep', 'GMC', 'RAM']
                for make_name in makes:
                    if re.search(rf'\b{make_name}\b', title, re.IGNORECASE):
                        make = make_name
                        break

            return {
                'success': True,
                'title': title or 'Unknown',
                'price': price or 0.0,
                'year': year,
                'make': make,
                'model': model,
                'url': ebay_url
            }

        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'title': 'Error',
                'price': 0.0,
                'year': None,
                'make': None,
                'model': None,
                'url': ebay_url
            }

    @staticmethod
    def extract_part_name(title: str) -> str:
        """
        Try to extract the part name from the title
        e.g., "2013 Honda Accord Headlight Left" -> "Headlight"
        """
        # Common part keywords
        parts = [
            'headlight', 'taillight', 'bumper', 'fender', 'hood', 'door',
            'mirror', 'grille', 'radio', 'stereo', 'cluster', 'speedometer',
            'wheel', 'rim', 'seat', 'console', 'dashboard', 'steering wheel',
            'ECM', 'TCM', 'PCM', 'module', 'sensor', 'switch', 'airbag'
        ]

        title_lower = title.lower()
        for part in parts:
            if part in title_lower:
                return part.title()

        # If no match, return first 3 words
        words = title.split()[:3]
        return ' '.join(words)
