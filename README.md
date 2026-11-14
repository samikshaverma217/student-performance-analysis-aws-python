# 📊 Student Performance Analysis using AWS and Python

A cloud-based web application to analyse student academic performance automatically using **AWS S3, AWS Lambda, Python & Streamlit**.

Upload marks CSV -> AWS S3 stores it -> Lambda auto-calculates Average, Grade, Pass/Fail -> Streamlit shows interactive dashboard with graphs.

## ✨ Features
- 🔐 Password Protected Dashboard (Password: `1234`)
- 📈 Subject-wise Average Bar Chart
- 🥧 Pass vs Fail Analysis
- 🏆 Top 5 & Bottom 5 Students
- 🔍 Search Any Student by Name
- 🤖 ML Risk Prediction (Low Attendance + Low Marks = Risk)
- 📉 Attendance vs Marks Scatter Chart
- 📥 Download Final Result as CSV
- ☁️ AWS S3 + Lambda Integration

## 🛠️ Tech Stack
- **Language:** Python
- **Dashboard:** Streamlit
- **Data Analysis:** Pandas
- **Cloud Storage:** AWS S3
- **Serverless:** AWS Lambda
- **Charts:** Streamlit Charts

## 📂 Dataset
- **Total Students:** 27
- **Subjects:** 10 - Data Mining Lab, Data Mining, CN Lab, Computer Network, DBMS Lab, DBMS, ADA, Software Engineering, Python Lab, Python
- **Extra Field:** Attendance %

## 🚀 How to Run
```bash
pip install streamlit pandas
streamlit run app.py
