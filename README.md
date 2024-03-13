# openIMIS ETL Module

This module facilitates the extraction, transformation, and loading (ETL) of data from the openIMIS production server to a designated target database. It empowers you to schedule data movement for seamless integration and analysis.

## Features:

- **Data Extractions:**

  - Extracts aggregated data from the production server

- **Data Transformation:**

  - Cleaning and pre-processing capabilities (e.g. handling missing values, formatting data)

- **Data Loading:**

  - Flexible target database configuration (e.g. MS SQL, PostgreSQL)
  - Efficient loading mechanism to minimize data transfer time.

- **Scheduling:**
  - Integrated with openIMIS schedulers or external scheduling tools like cron

## Installation:

1.  **Prerequisites**

    - Python (version 3.10 or later)
    - Django (version 4.2 or later)

2.  **Clone Repository:**

    git clone https://github.com/openimis/openimis-be-dashboard_etl_py
