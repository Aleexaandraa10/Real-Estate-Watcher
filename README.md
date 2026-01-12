# 🏠 Real-Estate Watcher – UiPath RPA Automation

<br>

## 1. Project Overview
**Real-Estate Watcher** is an RPA (Robotic Process Automation) project built with **UiPath**, designed to monitor and centralize real estate listings from three major Romanian platforms: **OLX.ro**, **Storia.ro**, and **Imobiliare.ro**.

The automation extracts listings based on **user-defined preferences**, processes and filters the data, generates an **AI-powered market summary**, creates reports in **HTML, DOCX and PDF formats** and automatically sends the final report to the user via **email**.

The project demonstrates practical UiPath concepts such as modular workflows, web scraping, retry logic, exception handling, Excel processing, logging and Generative AI integration.


<br>

## 2. Key Features & Implementation

### 🔍 Multi-Platform Data Collection
- Scrapes real estate listings from **OLX**, **Storia** and **Imobiliare.ro**.
- Implemented in:
  - `Scrape_OLX.xaml`
  - `Scrape_Storia.xaml`
  - `Scrape_Imobiliare.xaml`
- Each platform is handled by a dedicated workflow using web automation and dynamic selectors.

### ⚙️ Flexible User Configuration
- User preferences are loaded from a **Config Excel file**.
- Implemented in:
  - `GetUserPreferences.xaml`
- Supported criteria:
  - Price range (minimum & maximum)
  - Number of rooms
  - Minimum surface area
  - Bucharest sector
  - Email address for receiving the report

### 🤖 AI-Powered Market Summary
- Uses **UiPath Generative AI activities** to generate an intelligent summary and insights based on the extracted data.
- Implemented in:
  - `AI_Summary.xaml`

### 📄 Automated Report Generation
- Automatically generates reports in:
  - **HTML**
  - **DOCX**
  - **PDF**
- Reports include both raw listings and AI-generated insights.
- Implemented in:
  - `AI_Summary.xaml`

### 📧 Email Notification
- Sends the final **PDF report** as an email attachment to the user.
- Implemented in:
  - `Send_Email.xaml`

### 🔁 Robustness, Retry & Logging
- Uses **Retry Scope** for unstable pages and temporary loading issues.
- Uses **Try-Catch blocks** for controlled handling of system and business exceptions.
- Implements **Log Message** activities to track execution progress, extracted row counts, retry attempts and errors.
- Implemented mainly in:
  - `Main.xaml`


<br>

## 3. Project Architecture

The project follows a **modular design**, orchestrated from a single entry point:

- **Main.xaml** – Entry point of the automation. Orchestrates the entire process:
  - Retrieves user preferences
  - Invokes scraping workflows
  - Handles retries, exceptions and logging
  - Calls AI summarization and email modules

- **GetUserPreferences.xaml** – Reads search criteria from `Config.xlsx`.

- **Scrape_OLX.xaml / Scrape_Storia.xaml / Scrape_Imobiliare.xaml** – Dedicated scraping workflows, one per platform.

- **AI_Summary.xaml** – Combines Excel data, generates AI summaries, and creates HTML, DOCX and PDF reports.

- **Send_Email.xaml** – Sends the final PDF report via email.


<br>

## 4. How to Use the Automation

1. **Configuration (Optional)**  
   Edit `Config.xlsx` to define the desired search criteria.

2. **Run the Automation**  
   Run `Main.xaml` from **UiPath Studio**, **UiPath Assistant** or **UiPath Orchestrator**.

3. **Output**
   - Raw scraped data is saved as Excel files in:
     ```
     ScrapedData/
     ```
   - Final reports are generated in:
     ```
     Reports/
     ```
     (HTML, DOCX and PDF formats)
   - The PDF report is sent automatically to the specified email address.

<br>

## 5. Technologies Used
UiPath Studio, UiPath UI Automation, UiPath Excel Activities, UiPath GenAI Activities, Web Scraping with Dynamic Selectors, Email Automation.

<br>

## 6. Conclusion
**Real-Estate Watcher** is a complete end-to-end RPA solution that combines web automation, data processing, AI-powered insights and automated reporting and notification.  
The project reflects real-world automation scenarios and demonstrates clean workflow design, robustness and practical AI integration within UiPath.
