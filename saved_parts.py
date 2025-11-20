import json
import os
from typing import List, Dict
from datetime import datetime

class SavedPartsList:
    """Manages saved parts list"""

    def __init__(self, db_file: str):
        self.db_file = db_file
        self.parts = []
        self.load()

    def load(self):
        """Load saved parts from JSON file"""
        if os.path.exists(self.db_file):
            try:
                with open(self.db_file, 'r') as f:
                    self.parts = json.load(f)
                print(f"[OK] Loaded {len(self.parts)} saved parts")
            except Exception as e:
                print(f"[ERROR] Error loading saved parts: {e}")
                self.parts = []
        else:
            self.parts = []

    def save(self):
        """Save parts to JSON file"""
        try:
            with open(self.db_file, 'w') as f:
                json.dump(self.parts, f, indent=2)
            print(f"[OK] Saved {len(self.parts)} parts")
        except Exception as e:
            print(f"[ERROR] Error saving parts: {e}")

    def add_part(self, part_data: Dict):
        """Add a part to the saved list"""
        # Add timestamp
        part_data['saved_at'] = datetime.now().isoformat()

        # Check if part already exists
        existing = self.find_part(
            part_data.get('year', ''),
            part_data.get('make', ''),
            part_data.get('model', ''),
            part_data['part_name']
        )

        if existing:
            print(f"[WARNING] Part already saved: {part_data['part_name']}")
            return False

        self.parts.append(part_data)
        self.save()
        print(f"[OK] Saved: {part_data['part_name']}")
        return True

    def add_manual(self, part_name: str, junkyard_price: float, ebay_sold_price: float):
        """Add a part manually with custom prices"""
        roi = ebay_sold_price / junkyard_price if junkyard_price > 0 else 0

        if roi < 2:
            roi_rating = "Low"
        elif roi < 5:
            roi_rating = "Medium"
        else:
            roi_rating = "High"

        part_data = {
            'part_name': part_name,
            'junkyard_price': junkyard_price,
            'ebay_sold_price': ebay_sold_price,
            'roi': roi,
            'roi_rating': roi_rating,
            'manual_entry': True,
            'saved_at': datetime.now().isoformat()
        }

        self.parts.append(part_data)
        self.save()

        return part_data

    def find_part(self, year: str, make: str, model: str, part_name: str) -> Dict:
        """Find a specific part in saved list"""
        for part in self.parts:
            if (part.get('year') == year and
                part.get('make') == make and
                part.get('model') == model and
                part['part_name'] == part_name):
                return part
        return None

    def get_all(self) -> List[Dict]:
        """Get all saved parts"""
        return self.parts

    def remove_part(self, index: int):
        """Remove a part by index"""
        if 0 <= index < len(self.parts):
            removed = self.parts.pop(index)
            self.save()
            print(f"[OK] Removed: {removed['part_name']}")
            return True
        return False

    def clear_all(self):
        """Clear all saved parts"""
        self.parts = []
        self.save()
        print("[OK] Cleared all saved parts")
