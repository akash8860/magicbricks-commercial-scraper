# 🏢 MagicBricks Commercial Property Scraper

This project is a powerful web scraping tool built using Python to extract commercial real estate listings from [MagicBricks](https://www.magicbricks.com). It scrapes essential details such as property name, price, area, summary details, and more from multiple Indian cities and saves the data in structured Excel sheets.

---

## 🚀 Features

- Scrapes listings from multiple cities in India  
- Extracts structured property data (Name, Summary, Price, Sqft)  
- Handles pagination up to a defined number of pages  
- Saves results in city-wise Excel files  
- User-Agent spoofing to avoid basic anti-scraping blocks  
- Clean and reusable functions with error handling  

---

## 📁 Project Structure

MagicBricks_Scraper/
├── MagicBricks_Commercial_Scraper.ipynb # Interactive Jupyter Notebook version
├── output/ # Directory for storing Excel files
└── README.md # Project documentation

## 🧰 Technologies Used

- Python 3  
- Requests  
- BeautifulSoup (bs4)  
- Pandas  
- openpyxl  
- Regex (re)  
- Jupyter Notebook  

---

## ⚙️ Setup Instructions

### Step 1: Clone the Repository
```bash
git clone https://github.com/your-username/MagicBricks_Scraper.git
cd MagicBricks_Scraper

### Step 2: Create a Virtual Environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

### Step 3: Install Dependencies
pip install -r requirements.txt

If requirements.txt is not present, manually install the dependencies:

pip install requests beautifulsoup4 pandas openpyxl





