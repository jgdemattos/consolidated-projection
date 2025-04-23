
# Consolidated Projection
## Marketing Ads Spend Aggregator & Projection API

---

## Overview

This is a Python-based Flask API designed to automate the retrieval, aggregation, and projection of advertising spend data from **Meta Ads (Facebook/Instagram)** and **Google Ads**.

I built this tool to streamline reporting workflows, provide near real-time budget pacing insights, and enable more data-driven decision-making.

There are 2 endpoints: 
- "/get-projection": returns a simple Json object with total spend, current budget and e a projection for the current month. 
- "/get-full-report": returns a full text report, detailing spend for each account and campaign.

A extended implementation, integrating with Monday.com API and Slack API can be seen in [this repository](https://github.com/jgdemattos/raiox).

---

## The Challenge: Manual Reporting & Delayed Insights

Marketing teams often manage campaigns across multiple platforms like Meta Ads and Google Ads. Tracking consolidated spend and projecting month-end totals typically involves:

1.  Manually logging into each platform.
2.  Exporting spend data for specific date ranges.
3.  Combining data in spreadsheets.
4.  Manually calculating current pace and projecting future spend.

This process is **time-consuming, prone to errors, and delays access to crucial budget pacing information**, potentially leading to under- or over-spending.

---

## The Solution: An Automated Reporting API

This Flask application provides a centralized solution by:

1.  **Connecting directly** to the Meta Ads and Google Ads APIs using official SDKs/libraries.
2.  **Fetching account and campaign-level spend data** programmatically.
3.  **Aggregating total spend** across both platforms for a given client/account structure.
4.  **Calculating a simple month-end spend projection** based on current daily averages.
5.  **Exposing this data** through two clear API endpoints.

---

## Key Features & Endpoints

This application offers two primary functionalities accessible via API endpoints:

1.  **`/get-projection`**:
    * **Method:** `GET`
    * **Description:** Returns a concise JSON object containing:
        * `account_cost`: The aggregated total spend across Meta and Google Ads for the current month-to-date.
        * `account_budget`: The pre-defined total budget for the month (can be configured).
        * `total_spend_projected`: A calculated projection of the total spend by the end of the current month based on the average daily spend so far.
    * **Use Case:** Quick budget health checks, dashboard integrations, automated alerts.
    * **Example Response:**
        ```json
        {
          "account_cost": 15234.56,
          "account_budget": 30000.00,
          "total_spend_projected": 31487.90
        }
        ```

2.  **`/get-full-report`**:
    * **Method:** `GET`
    * **Description:** Returns a detailed text-based report outlining:
        * Spend breakdown per platform (Meta Ads, Google Ads).
        * Spend details for individual accounts and potentially campaigns within each platform (depending on implementation granularity).
    * **Use Case:** Deeper dive analysis, identifying high/low spending campaigns, generating detailed summaries for stakeholders.
    * **Example Response (Conceptual):**
        ```text
      [🍊 Consolidated Projection - ExampleClientName - 23/04/25 🍊]
      
      👥 Daily Budget: R$ 385.12;
      💸 Total spent: R$ 9227.63;
      📈 Spend Projection: R$ 13268.47;
      
      [Meta Ads]
      1 Business Managers watched:
      ➡️ BM - ExampleMetaBusinessManagerName
      💸 Total spent: R$ 9027.63
      💰 Current budget: R$ 320.12
      
      2 ad accounts:
      
      ➡️ ExampleMetaAccountName - 0 campaigns
      💸 Total spent: R$ 0.0
      💰 Current budget: R$ 0.00
      no campaigns
  
      
      ➡️ ExampleMetaAccountName2 - 9 campaigns
      💸 Total spent: R$ 9027.63
      💰 Current budget: R$ 320.12
        
      ➡️ ExampleMetaCampaignName🟡
      💸: R$ 522.46 - 💰: R$ 23.6 - 🟢: ACTIVE
      ➡️ ExampleMetaCampaignName2 
      💸: R$ 709.34 - 💰: R$ 0.0 - 🔴: PAUSED
      ➡️ ExampleMetaCampaignName3 
      💸: R$ 149.21 - 💰: R$ 0.0 - 🔴: PAUSED
      ➡️ ExampleMetaCampaignName4
      💸: R$ 1959.82 - 💰: R$ 61.23 - 🟢: ACTIVE
      ➡️ ExampleMetaCampaignName5
      💸: R$ 146.39 - 💰: R$ 0.0 - 🔴: PAUSED
      ➡️ ExampleMetaCampaignName6
      💸: R$ 3128.54 - 💰: R$ 140.0 - 🟢: ACTIVE
      ➡️ ExampleMetaCampaignName7
      💸: R$ 314.88 - 💰: R$ 0.0 - 🔴: PAUSED
      ➡️ ExampleMetaCampaignName8
      💸: R$ 759.07 - 💰: R$ 30.0 - 🟢: ACTIVE
      ➡️ ExampleMetaCampaignName9
      💸: R$ 1337.92 - 💰: R$ 65.29 - 🟢: ACTIVE
  
   
      [Google Ads]
      1 Google accounts:
      ➡️ 5650657493 - 0 campaigns
      💸 Total spent: R$ 0.0
      💰 Current budget: R$ 0
        
      ➡️ ExampleGoogleCampaignName1
      💸: R$ 2332.92 - 💰: R$ 65.29 - 🟢: ACTIVE
        ----------------------------------------
        ```

---

## Technical Stack

* **Language:** Python 3.x
* **Framework:** Flask
* **Key Libraries:**
    * `requests` (for interacting with Meta Ads Marketing API)
    * `google-ads` (Google Ads API Client Library)
    * `python-dotenv` (for managing API credentials securely)
    * Standard Python libraries for date/time manipulation and calculations.

---

## Marketing Value & Application

This project directly addresses key marketing operational needs:

* **Efficiency:** Automates repetitive data collection, freeing up marketer time for strategic analysis and optimization.
* **Timely Insights:** Provides near real-time spend data and projections, enabling proactive budget management.
* **Data Accuracy:** Reduces manual errors associated with copying/pasting or spreadsheet formulas.
* **Cross-Platform Visibility:** Offers a consolidated view of spend across major advertising channels.
* **Technical Proficiency:** Demonstrates the ability to leverage APIs and code to build practical marketing technology solutions.

This tool serves as a foundation that could be expanded for more complex analysis, visualization (e.g., integrating with BI tools), or automated alerting systems.

---

## Setup & Installation

1.  **Clone the repository:**
    ```bash
    git clone [your-repository-url]
    cd [repository-directory]
    ```
2.  **Create a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate # On Windows use `venv\Scripts\activate`
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Configure Environment Variables:**
    * Create a `.env` file in the root directory.
    * Add your API credentials and any necessary configuration variables (e.g., Client IDs, Account IDs, Developer Tokens, Refresh Tokens, Monthly Budget). **Never commit your `.env` file or credentials directly to Git.**
    ```dotenv
    # .env file example
    developer_token=XXX
    client_id=XXX
    client_secret=XXX
    refresh_token=XXX
    mcc_id=XXX
    access_token=XXX
    agencies_bm_id=XXX(optional)
    ```
5.  **Configure Environment Variables:**
    * Provide a id, busines manager id, google account id for each client. It's also possible to provide meta adaccount ids direcly, for querying ad accounts linked to your business manager, informed at .env's "agencies_bm_id" key.
    ```csv
    # clients.csv file example
      id;name;meta_id;google_id;meta_adaccount_ids
      XX;XXX;XXX;XXX;
      XX;XXX;XXX;XXX;XXX;
    ```
6.  **Run the Flask application:**
    ```bash
    flask run
    ```
    The API will typically be available at `http://127.0.0.1:5000`.

---

## Future Enhancements (Potential Ideas)

* Integration with additional marketing platforms (LinkedIn Ads, TikTok Ads, etc.).
* Implementing more sophisticated projection algorithms.
* Adding automated email/Slack notifications for budget pacing alerts.

---

## About Me & Contact

I am a results-oriented marketing professional passionate about leveraging technology and data to drive growth and efficiency. This project is one example of how I bridge the gap between marketing strategy and technical execution.

* **LinkedIn:** [My LinkedIn Profile](https://www.linkedin.com/in/joaomattos-marketing-manager/)
* **Portfolio:** [Other projects I'm working on](https://joaomattos.pro/)

---
