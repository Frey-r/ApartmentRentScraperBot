# Rental Property Scraper

A Python web scraper that monitors rental property listings from Portal Inmobiliario and stores them in a SQLite database.

## Description

This scraper is designed to:

- Track rental properties within specific price ranges and locations
- Store property details including price, location, and availability
- Monitor changes in listings over time
- Keep historical data of property listings

## Requirements

- Python 3.x
- Firefox browser
- Required Python packages:
  - pandas
  - selenium
  - openpyxl

## Installation

1. Clone this repository
2. Create venv:
   `python -m venv venv`
3. Activate venv:
   `.\venv\Scripts\activate`
4. Install required packages:
   `pip install -r requirements.txt`
5. Make sure you have Firefox browser installed
6. The Selenium WebDriver for Firefox will be automatically installed with selenium

## Project Structure

```
Scrapper arriendo/
├── launcher.bat*     # Recomended way to execute, look Usage section for more information
├── scarpper.py       # Main scraper script
├── requirements.txt  # Python dependencies
└── sql/
    ├── bdd.db       # SQLite database (created on first run)
    └── create.sql   # Database schema
```

## Database Schema

The scraper stores data in a SQLite database with the following structure:

* id: Unique identifier (auto-incrementing)
* name: Property title
* URL: Link to the property listing
* divisa: Currency
* precio: Price
* desc: Property description
* ubicacion: Location
* source: Source URL of the listing
* disponible: Availability status (boolean)
* fecha_creacion: Creation date
* fecha_modificacion: Last modification date

## Usage

#### Run the scraper with Launcher file (**recomended way)**

Run the scraper with Launcher file by creating a `launcher.bat` with the following content:

```
@echo off
cd "project absolute path"
".\venv\Scripts\python.exe" "scarpper.py"
pause
```

This way make easier automatize this program using windosw tasks or other programs.

#### Using Python Directly

Alternatively, you can run the scraper directly with Python:

```
python scarpper.py
```

The script will:

1. Check for existing database and create if needed
2. Scrape property listings from configured URLs
3. Update database with new listings
4. Mark unavailable listings
5. Close browser when complete

## Configuration

To modify search parameters, edit the **URLS** list in **scarpper.py**. The current configuration searches for:

* Property type: Apartments
* Transaction type: Rent
* Price range: CLP 1 - 450,000
* Location: Specific coordinates
