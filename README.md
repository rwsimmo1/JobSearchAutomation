# Job Search Automation

This project automates job searching for drama teacher positions using SerpApi and sends email notifications with results.

## Features

- Searches Google Jobs for drama teacher positions
- Filters and scores jobs based on relevance
- Sends email with high-confidence matches and CSV attachment

## Setup

1. Install dependencies:
   ```
   pip install requests pandas python-dotenv serpapi
   ```

2. Set up environment variables in `.env`:
   ```
   SERP_API_KEY=your_serpapi_key_here
   EMAIL_ADDRESS=your_email@gmail.com
   EMAIL_PASSWORD=your_app_password
   ```

3. Run the script:
   ```
   python JobSearch.py
   ```

## Files

- `JobSearch.py`: Main script
- `JobSearchScripts.py`: Job search and processing functions
- `rwsimmo_email.py`: Email sending utility
- `send_with_google_app_password.py`: Password retrieval utility