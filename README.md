# eBay Car Parts Profit Analyzer

Identify profitable car parts to flip by analyzing eBay sold listings and comparing them to junkyard fixed pricing.

## 🚀 Quick Start (When You Have eBay API Credentials)

### 1. Install Python Dependencies

```bash
cd Ebay_Car_Automation_Project
pip install -r requirements.txt
```

### 2. Set Up eBay API Credentials

1. Copy the template file:
   ```bash
   copy .env.template .env
   ```

2. Open `.env` and add your eBay API credentials:
   ```
   EBAY_APP_ID=your_app_id_here
   EBAY_CERT_ID=your_cert_id_here
   EBAY_DEV_ID=your_dev_id_here
   EBAY_ENVIRONMENT=production
   ```

### 3. Run the Application

```bash
python app.py
```

Open your browser to: **http://localhost:5000**

---

## 📋 Features

✅ **Automated eBay Analysis**
- Searches eBay sold listings for each part
- Calculates median, average, and ROI
- Shows competition (active listings)
- Provides best listing links and images

✅ **Junkyard Price Database**
- 443 parts pre-loaded from your CSV
- Automatic price matching
- Case-insensitive search

✅ **ROI Calculator**
- Low: under 2x
- Medium: 2x–4.9x
- High: 5x+

✅ **Saved Parts List**
- Save high-ROI parts for junkyard trips
- Manual entry mode
- Export-ready format

✅ **Smart Filtering**
- Filter by ROI (5x+, all)
- Sort by frequency or ROI
- Vehicle type detection (car vs truck/SUV)

---

## 🔑 Getting eBay API Credentials

1. Go to: https://developer.ebay.com/
2. Sign in with your eBay account
3. Navigate to: **My Account → Application Keys**
4. Create a new app:
   - Choose "Production" environment
   - Accept the terms
5. Copy your credentials:
   - **App ID (Client ID)**
   - **Cert ID (Client Secret)**
   - **Dev ID**

**Note:** Approval usually takes 1 business day.

---

## 📖 How to Use

### Analyze a Vehicle

1. Enter vehicle info (Year, Make, Model, optional Trim)
2. Select vehicle type (Car or Truck/SUV)
3. Click "Analyze Parts"
4. Review the results table with ROI ratings
5. Save high-ROI parts to your list

### Manual Add

1. Go to "Manual Add" tab
2. Enter part name, junkyard price, and eBay sold price
3. System calculates ROI automatically
4. Saved to your parts list

### View Saved Parts

1. Go to "Saved List" tab
2. See all your saved parts
3. Remove parts as needed
4. Take this list to the junkyard!

---

## 📂 Project Structure

```
Ebay_Car_Automation_Project/
├── app.py                      # Main Flask application
├── config.py                   # Configuration settings
├── junkyard_prices.py          # Price database loader
├── ebay_api.py                 # eBay API integration
├── parts_analyzer.py           # ROI calculation engine
├── saved_parts.py              # Saved parts manager
├── requirements.txt            # Python dependencies
├── .env.template               # Environment template
├── Junkyard Pricing.csv        # Your price database (443 parts)
├── templates/
│   └── index.html              # Web interface
└── saved_parts.json            # Saved parts database (auto-created)
```

---

## 🎯 Example Usage

**Input:**
```
Year: 2013
Make: Honda
Model: Accord
Trim: EX-L 2.4L
Type: Car
```

**Output:**
```
Part: HEADLIGHT
Median Sold: $125.00
Junkyard Price: $39.99
ROI: 3.13x (Medium)
Sold (30d): 47
Active Listings: 213
```

---

## ⚙️ Advanced Features

### Filter Results
- **Show ROI 5x+**: Only high-profit parts
- **Show All**: All analyzed parts
- **Sort by Frequency**: Most-sold parts first

### Export Saved List
Your saved parts are stored in `saved_parts.json` for easy access.

---

## 🛠️ Troubleshooting

**Problem: "eBay API credentials not configured"**
- Make sure you've created `.env` file from `.env.template`
- Verify your API credentials are correct
- Wait for eBay developer approval (1 business day)

**Problem: "Part not found in junkyard price list"**
- The part may use a different name in the CSV
- Check `Junkyard Pricing.csv` for exact part names

**Problem: "No results found"**
- eBay may have no sold listings for that part
- Try a different year/make/model
- Check if part name is too specific

---

## 💡 Tips for Best Results

1. **Start with popular vehicles** (Honda, Toyota, Ford F-150)
2. **Focus on electronic parts** (ECU, TCM, radios) - higher ROI
3. **Check multiple trims** of the same model
4. **Save parts with ROI 5x+** for maximum profit
5. **Verify condition** matches eBay listings at junkyard

---

## 📞 Next Steps

When you return with your eBay API credentials:

1. Open Claude Code
2. Say: **"I'm back with the API credentials"**
3. Paste your credentials
4. I'll help you set them up!

---

**Built with:** Python, Flask, eBay API, Pandas

**Ready to find profitable car parts?** 🚗💰
