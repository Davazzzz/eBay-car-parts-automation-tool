import pandas as pd
from typing import Optional

class JunkyardPrices:
    """Manages junkyard pricing data"""

    def __init__(self, csv_path: str):
        self.csv_path = csv_path
        self.prices = {}
        self.load_prices()

    def load_prices(self):
        """Load prices from CSV file"""
        try:
            # Skip first row (empty) and use second row as header
            df = pd.read_csv(self.csv_path, skiprows=1)

            # Clean up the data
            df = df[['Part', 'Price']].dropna()

            # Remove dollar signs and convert to float
            df['Price'] = df['Price'].str.replace('$', '').str.replace(',', '').astype(float)

            # Create dictionary with uppercase keys for case-insensitive matching
            self.prices = {
                row['Part'].strip().upper(): row['Price']
                for _, row in df.iterrows()
            }

            print(f"[OK] Loaded {len(self.prices)} parts from junkyard price list")

        except Exception as e:
            print(f"[ERROR] Error loading junkyard prices: {e}")
            self.prices = {}

    def get_price(self, part_name: str) -> Optional[float]:
        """Get price for a specific part (case-insensitive)"""
        return self.prices.get(part_name.strip().upper())

    def search_part(self, search_term: str) -> dict:
        """Search for parts matching a term"""
        search_term = search_term.upper()
        matches = {
            name: price
            for name, price in self.prices.items()
            if search_term in name
        }
        return matches

    def get_all_parts(self) -> list:
        """Get list of all available parts"""
        return sorted(list(self.prices.keys()))
