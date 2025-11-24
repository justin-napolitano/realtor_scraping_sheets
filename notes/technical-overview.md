---
slug: github-realtor-scraping-sheets-note-technical-overview
id: github-realtor-scraping-sheets-note-technical-overview
title: realtor_scraping_sheets
repo: justin-napolitano/realtor_scraping_sheets
githubUrl: https://github.com/justin-napolitano/realtor_scraping_sheets
generatedAt: '2025-11-24T18:44:56.125Z'
source: github-auto
summary: >-
  This repo is a Python tool for scraping real estate agent data from sites like
  realtor.com and rew.ca, then storing it in Google Sheets and Drive. It handles
  scraping, cleaning, and organizing realtor data.
tags: []
seoPrimaryKeyword: ''
seoSecondaryKeywords: []
seoOptimized: false
topicFamily: null
topicFamilyConfidence: null
kind: note
entryLayout: note
showInProjects: false
showInNotes: true
showInWriting: false
showInLogs: false
---

This repo is a Python tool for scraping real estate agent data from sites like realtor.com and rew.ca, then storing it in Google Sheets and Drive. It handles scraping, cleaning, and organizing realtor data.

### Key Components
- **Tech Stack**: Python 3, BeautifulSoup, requests, pandas, Google APIs.
- **Modules**:
  - Scraping modules for realtor.com and rew.ca.
  - Google Sheets and Drive integrations.
  
### Getting Started
1. Clone the repo:
    ```bash
    git clone https://github.com/justin-napolitano/realtor_scraping_sheets.git
    cd realtor_scraping_sheets
    ```
2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3. Configure `config.yaml` with your Google API credentials.

### Running It
Start the scraper:
```bash
python main.py
```

### Gotchas
Make sure to set up your Google API credentials correctly in `config.yaml`. Pay attention to directory structures; that’s crucial for data management.
