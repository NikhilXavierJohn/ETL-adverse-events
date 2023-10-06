# ETL Adverse Events


## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Running the Application](#running-the-application)

---

## Introduction

The **ETL Adverse Events** repository is a simple data pipeline designed to extract, transform, and load (ETL) adverse events data. This repository provides a comprehensive set of tools and scripts to help you efficiently collect, process, and store adverse event data for further analysis and reporting.

---

## Features

- **Data Extraction**: Easily collect adverse events data from Adverse events API.
- **Data Transformation**: Standardize and clean the collected data to ensure consistency and quality.
- **Data Loading**: Load the transformed data into a HDFS system.
---

## Getting Started

Follow these instructions to get the **ETL Adverse Events** project up and running on your Windows 11 machine with Hadoop 3.3.6, HDFS, Java JDK 1.8.0, and Python environment.

### Prerequisites

Before you begin, ensure you have met the following requirements:

- Hadoop 3.3.6 installed and configured.
- HDFS set up.
- Java JDK 1.8.0 installed.
- Python 3.6+ installed.
- Pip package manager installed.
- Knowledge of the data sources and formats you want to work with.

### Installation

1. Clone the repository:

   ```shell
   git clone https://github.com/NikhilXavierJohn/ETL-adverse-events.git
   ```

2. Navigate to the project directory:

   ```shell
   cd ETL-adverse-events
   ```

3. Install the required Python dependencies:

   ```shell
   make setup
   ```

### Running the Application

To run the ETL pipeline on your Windows 11 machine with Hadoop and HDFS:

1. Customize the ETL pipeline configuration file or makefile data sources, and destination specifications.

2. Start Hadoop and HDFS services.

3. Run the ETL pipeline using the following command:

   ```shell
   make etl
   ```

4. Monitor the ETL process through the logs and output messages.

5. Access the transformed data in your HDFS, or in the read_data stage where it is displayed as a pyspark-dataframe and can be manipulated to see the data of your choice.

---

**Disclaimer**: This repository is intended for educational and research purposes only. It is essential to comply with all applicable laws and regulations when working with healthcare data and adverse event reporting.
