# FinWise - AI-Powered Personal Finance Assistant

FinWise is an **AI-powered personal finance assistant** designed to help users manage their finances efficiently. The assistant offers **personalized budgeting**, **expense tracking**, and **savings recommendations**. The project focuses on **transaction classification using AI** and delivers **actionable insights** for better financial control. Currently, transactions are entered manually, but future versions will integrate with **bank APIs** for automation.

## 🌟 Key Features

### 1. 📊 Transaction Classification and Budget Tracking

- Categorizes manually entered transactions into predefined categories (e.g., **Food, Transport, Entertainment**).
- Provides **budget suggestions** based on user spending history.
- Visualizes **monthly expenses** to help users stay on budget.

### 2. 💡 Personalized Financial Insights and Recommendations

- Analyzes **spending patterns** to offer personalized **saving tips**.
- Suggests areas where users can **cut expenses** or allocate more funds for **savings and investments**.
- Provides **investment suggestions** tailored to user preferences (**Conservative, Balanced, Aggressive**).

### 3. 📊 Real-Time Financial Dashboard

- Interactive **dashboard** with expense summaries, spending trends, and savings progress.
- **Real-time charts** 📈 for better visualization of expenses and income.
- Allows users to set and track **financial goals** (e.g., ✈️ Travel Fund, 🏠 Emergency Fund).

## 🛠️ Technology Stack

- **Programming Language:** Python  
- **Frameworks & Libraries:** Flask, Pandas, Scikit-learn  
- **Front-End:** HTML, CSS, JavaScript  
- **AI Models:** Machine Learning (**Random Forest Classifier** for transaction classification)  
- **Data Visualization:** Matplotlib, Plotly  
- **Database:** SQLite (for storing user transactions and budget data)

## ⚙️ Implementation Details

- **Manual Transaction Input:** Users manually enter transactions, which are categorized using a trained **Random Forest Classifier** model.
- **AI-based Insights:** The system analyzes spending patterns and generates actionable insights for **budgeting** and **saving**.
- **Dashboard:** Provides a **real-time**, user-friendly interface for monitoring financial health and tracking goals.
- **Data Security:** Strong **encryption methods** ensure secure data storage and handling.

## 🔧 Setup and Installation

### 🔧 Prerequisites

Ensure you have **Python 3** installed on your system along with the following dependencies:

```bash
pip install flask pandas scikit-learn matplotlib plotly sqlite3
```

### 🏃 Steps to Run the Project

1. **Run the application:**

```bash
python app.py
```

2. **Open your browser and go to:**

```url
http://localhost:5000
```
![image](https://github.com/user-attachments/assets/157cd2dc-0754-4deb-8ade-4768a85553a6)
![image](https://github.com/user-attachments/assets/7cf3a5a6-5606-49eb-8032-1c025ab5f44b)

