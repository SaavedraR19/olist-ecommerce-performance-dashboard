# Olist E-commerce Performance Dashboard

## Overview
This project analyzes the commercial performance of **Olist**, a real e-commerce company, using public data from Kaggle.

The goal of the analysis is to evaluate:
- monthly revenue trends
- regional performance
- category contribution
- customer payment preferences

The project follows a business-oriented approach similar to what is used in business intelligence and e-commerce analytics teams.

---

## Business Questions
This dashboard was designed to answer questions such as:

- How does revenue evolve over time?
- Which states concentrate the highest revenue?
- Which categories drive sales the most?
- What payment methods do customers prefer?
- Are there smaller markets with higher average order values?

---

## Tools Used
- **Python**
- **Pandas**
- **Power BI**
- **DAX**

---

## Data Source
- **Dataset:** Olist public dataset
- **Source:** Kaggle

This project uses public e-commerce data from Olist, including orders, payments, products, customers, and geolocation-related fields.

---

## Data Preparation
The dataset was prepared in **Python** before being loaded into Power BI.

Main preparation steps:
- data loading from multiple CSV files
- joins between orders, items, customers, products, and payments
- category translation
- payment type standardization
- revenue calculations
- filtering delivered orders only
- creation of a final analytical dataset for reporting

---

## Dashboard Structure

### Page 1 — Executive Overview
This page focuses on the general business performance of the e-commerce operation.

Main elements:
- Total Revenue
- Total Orders
- Average Order Value
- Monthly Growth %
- Revenue trend over time
- Payment method breakdown
- Revenue by state
- Revenue by category

### Page 2 — Regional & Category Performance
This page focuses on geographical concentration and category behavior.

Main elements:
- Revenue by state
- Orders by state
- Revenue vs AOV by state
- Revenue share by state
- Category share
- Revenue by category and state

---

## Key Insights
- **São Paulo** accounts for the largest share of total revenue
- Some lower-volume markets show **higher average order values**
- **Health & Beauty** is one of the leading categories
- Payment mix helps explain customer purchasing behavior and regional differences

---

## Repository Contents
```text
olist-ecommerce-performance-dashboard/
│
├── README.md
├── olist_preparacion.py
├── Olist_Dashboard.pbix
└── images/
    ├── dashboard_page_1.png
    ├── dashboard_page_2.png
    └── data_flow.png
