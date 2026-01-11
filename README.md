# Vendor Performance Analysis  
**Power BI | Python | SQL | SQLite**

## 📌 Project Overview
This project analyzes vendor performance to identify **cost inefficiencies, profit leakage, inventory risks, and high-value vendors**.  
It combines **Python-based ETL**, **SQL aggregation**, and **Power BI dashboards** to deliver actionable business insights.

The project simulates a **real-world analytics pipeline**, from raw data ingestion to executive-ready dashboards.

---

## 🎯 Business Objectives
- Identify **top and bottom performing vendors**
- Analyze **revenue, profit, and margin contribution**
- Compare **purchase cost vs selling price**
- Detect **inventory inefficiencies and stock turnover issues**
- Support **vendor selection and pricing strategy decisions**

---

## 🧰 Tools & Technologies
- **Python**: Pandas, NumPy  
- **SQL**: SQLite  
- **Visualization**: Power BI  
- **Data Storage**: CSV, SQLite  
- **Version Control**: Git & GitHub  
- **Logging**: Python `logging` module  

---

## 📊 Dataset Description
The analysis is based on multiple operational datasets:
- Vendor purchase data  
- Sales transactions  
- Purchase price lists  
- Inventory movement  
- Vendor invoice & freight costs  

Each dataset is ingested, cleaned, and transformed before analysis.

---


## 🔄 Data Pipeline Flow
1. **Raw CSV Ingestion**
   - Chunk-based loading into SQLite for performance  
   - Handles large datasets (~8,000+ records)

2. **SQL Aggregation Layer**
   - Vendor-level sales, purchase, and freight aggregation  
   - Joins across multiple fact tables  

3. **Feature Engineering (Python)**
   - Gross Profit  
   - Profit Margin (%)  
   - Sales-to-Purchase Ratio  
   - Stock Turnover  

4. **Data Visualization (Power BI)**
   - Executive KPIs  
   - Vendor concentration analysis  
   - Profitability and risk indicators  

---

## 📈 Key Metrics Created
- **Total Sales & Purchase Value**
- **Gross Profit**
- **Profit Margin (%)**
- **Stock Turnover Ratio**
- **Sales-to-Purchase Ratio**
- **Freight Cost Impact**

---

## 📊 Power BI Dashboard Highlights
- KPI Cards: Revenue, Profit, Margin  
- Top & Bottom Vendors by Sales and Profit  
- Vendor Revenue Concentration  
- Inventory Turnover Analysis  
- Cost vs Selling Price Comparison  

*Dashboard designed for executive-level decision making.*

---

## 🚀 How to Run the Project

### 1️⃣ Ingest Raw Data

### 2️⃣ Create Vendor Summary Table

### 3️⃣ Open Power BI
- Connect to `inventory.db`  
- Load `vendor_sales_summary` table  
- Build visuals and dashboards  

---

## 📌 Key Outcomes
- Identified **high-profit, low-volume vendors**
- Highlighted **vendors with high sales but poor margins**
- Detected **slow-moving inventory risks**
- Enabled **data-driven vendor negotiations and pricing optimization**

---

## 🔮 Future Enhancements
- Vendor risk scoring model  
- Time-series trend analysis  
- Automated refresh pipeline  
- Predictive demand forecasting  

---

## 👤 Author
**Anshika Digarse**  
Data Analyst | Aspiring Data Scientist  
Skills: Python • SQL • Power BI • Data Analytics  

---

⭐ If you found this project useful, feel free to star the repository!



