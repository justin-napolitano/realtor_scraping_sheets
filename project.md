---
slug: github-realtor-scraping-sheets
id: github-realtor-scraping-sheets
title: Real Estate Data Scraping with Python and Google Sheets
repo: justin-napolitano/realtor_scraping_sheets
githubUrl: https://github.com/justin-napolitano/realtor_scraping_sheets
generatedAt: '2025-11-24T21:36:10.667Z'
source: github-auto
summary: >-
  A Python project for scraping realtor data and managing it via Google Sheets
  and Drive, focusing on realtor.com and rew.ca.
tags:
  - python
  - web scraping
  - google sheets
  - google drive
  - beautifulsoup
  - pandas
  - real estate
seoPrimaryKeyword: realtor data scraping
seoSecondaryKeywords:
  - python web scraping
  - google sheets integration
  - real estate scraping
  - data cleaning utilities
  - realtor.com scraping
  - rew.ca scraping
  - API integration
seoOptimized: true
topicFamily: null
topicFamilyConfidence: null
kind: project
entryLayout: project
showInProjects: true
showInNotes: false
showInWriting: false
showInLogs: false
---

A Python-based project designed for scraping real estate agent data from multiple real estate listing websites and managing the data through Google Sheets and Google Drive. The repository contains various modules to scrape, clean, filter, and organize data related to realtors, primarily focusing on realtor.com and rew.ca.

## Features

- Web scraping of realtor data from multiple sources including realtor.com and rew.ca.
- Data cleaning and filtering utilities to process scraped data.
- Integration with Google Sheets and Google Drive APIs for data storage and management.
- Batch downloading and file management utilities.
- Configurable scraping parameters and folder structures.

## Tech Stack

- Python 3
- Libraries: BeautifulSoup, requests, pandas, lxml, PyYAML
- Google APIs: Google Drive and Google Sheets API

## Getting Started

### Prerequisites

- Python 3.x installed
- Google API credentials for Drive and Sheets access

### Installation

1. Clone the repository:

```bash
git clone https://github.com/justin-napolitano/realtor_scraping_sheets.git
cd realtor_scraping_sheets
```

2. Install required Python packages:

```bash
pip install -r requirements.txt
```

(Note: `requirements.txt` is assumed to be created with necessary packages such as `beautifulsoup4`, `requests`, `pandas`, `google-api-python-client`, `PyYAML`, etc.)

3. Configure `config.yaml` with appropriate Google API credentials and folder IDs.

### Running the Project

Run the main entry point:

```bash
python main.py
```

This will execute the program skeleton which orchestrates the scraping and data processing tasks based on the configuration.

## Project Structure

- `main.py`: Entry point to load configurations and run the program skeleton.
- `load_vars.py`: Loads and sets environment variables and configuration from YAML.
- `realtor_scraper.py`, `realtorscraper2.py`, `realtorscraper3.py`: Modules for scraping realtor.com data.
- `rew_scraper.py`, `rew_scraper.3.0.py`, `rew_scraper_about.py`: Modules for scraping rew.ca data.
- `realtor_scraper_sheets.py`, `realtor_scraper_sheets_2.py`, `realtor_scraper_sheets_3.py`: Scraping integrated with Google Sheets and Drive.
- `google_drive.py`, `goog_sheets.py`: Google Drive and Sheets API integration utilities.
- `load_df.py`, `clean_df.py`, `df_filter.py`: Data loading, cleaning, and filtering utilities.
- `batch_download.py`, `download.py`, `save.py`, `fix_files.py`: File management and batch processing utilities.
- `confirm_drcts.py`: Folder structure validation and creation.
- `json_log.py`: JSON logging utility.
- `config.yaml`: YAML configuration file for environment variables and task settings.
- `cities/`, `dnn/`, `mapped_data/`, `merged_data/`, `log/`, `folder/`: Directories for organizing data and logs.

## Future Work / Roadmap

- Improve error handling and logging throughout scraping modules.
- Modularize scraping logic into classes for better maintainability.
- Add unit and integration tests.
- Enhance configuration flexibility, including dynamic input of cities and states.
- Implement parallel scraping to improve performance.
- Add documentation for Google API credential setup.
- Create a requirements file for easier environment setup.
- Refine data cleaning and filtering criteria.
- Expand support to additional real estate listing platforms.

---

*Note: This documentation is based on the current state of the repository and inferred functionality from source files.*
