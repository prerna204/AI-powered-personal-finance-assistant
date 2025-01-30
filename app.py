import requests
from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from collections import defaultdict
from datetime import datetime
import json

app = Flask(__name__)
app.secret_key = "finwise_secret_key"  # Required for session management

# Database setup
def init_db():
    conn = sqlite3.connect('finwise.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS expenses
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  category TEXT NOT NULL,
                  amount REAL NOT NULL,
                  date TEXT NOT NULL)''')
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT NOT NULL,
                  salary REAL NOT NULL)''')
    conn.commit()
    conn.close()

# Start app by asking for name and salary
@app.route('/', methods=['GET', 'POST'])
def welcome():
    if request.method == 'POST':
        name = request.form['name']
        salary = float(request.form['salary'])

        # Store in session
        session['name'] = name
        session['salary'] = salary

        return redirect(url_for('index'))

    return render_template('welcome.html')

# Homepage (after entering name & salary)
@app.route('/home')
def index():
    if 'name' not in session or 'salary' not in session:
        return redirect(url_for('welcome'))  # Redirect to input page if missing data

    return render_template('index.html', name=session['name'], salary=session['salary'])

# Add expense
@app.route('/add', methods=['GET', 'POST'])
def add_expense():
    if request.method == 'POST':
        category = request.form['category']
        amount = float(request.form['amount'])
        date = request.form['date']

        conn = sqlite3.connect('finwise.db')
        c = conn.cursor()
        c.execute('INSERT INTO expenses (category, amount, date) VALUES (?, ?, ?)',
                  (category, amount, date))
        conn.commit()
        conn.close()
        return redirect(url_for('view_expenses'))
    return render_template('add_expense.html')

# View expenses
@app.route('/view')
def view_expenses():
    if 'name' not in session or 'salary' not in session:
        return redirect(url_for('welcome'))

    try:
        conn = sqlite3.connect('finwise.db')
        c = conn.cursor()
        
        # Get all expenses ordered by date
        c.execute('SELECT * FROM expenses ORDER BY date DESC')
        expenses = c.fetchall()

        # Calculate total spending
        total_spent = sum(expense[2] for expense in expenses)

        # Categorize expenses
        category_spending = defaultdict(float)
        for expense in expenses:
            category_spending[expense[1]] += expense[2]

        # Sort categories by amount spent (descending)
        category_spending = dict(sorted(category_spending.items(), 
                                     key=lambda x: x[1], 
                                     reverse=True))

        # Monthly trends
        monthly_data = defaultdict(float)
        for expense in expenses:
            date = datetime.strptime(expense[3], "%Y-%m-%d")
            month_year = date.strftime("%b %Y")
            monthly_data[month_year] += expense[2]

        # Sort monthly data chronologically
        sorted_months = sorted(monthly_data.keys(),
                             key=lambda x: datetime.strptime(x, "%b %Y"))
        monthly_spending = {month: monthly_data[month] for month in sorted_months}

        conn.close()

        return render_template(
            'view_expenses.html',
            expenses=expenses,
            total_spent=total_spent,
            category_spending=json.dumps(category_spending),
            monthly_spending=json.dumps(monthly_spending),
            name=session['name'],  # Pass name and salary to display
            salary=session['salary']
        )
    except Exception as e:
        print(f"Error in view_expenses: {str(e)}")
        if 'conn' in locals():
            conn.close()
        return render_template('error.html', error=str(e))

# Delete expense
@app.route('/delete/<int:id>')
def delete_expense(id):
    conn = sqlite3.connect('finwise.db')
    c = conn.cursor()
    c.execute('DELETE FROM expenses WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('view_expenses'))

# Fetch investment recommendations from API
def get_investment_suggestions():
    url = 'https://tradematic-cloud.p.rapidapi.com/taskmanager/tasks/0'
    headers = {
        'x-rapidapi-key': '76a8f2101cmsh8b82cff487bc52ap1e8f4ajsn0ba57ea6dd45',
        'x-rapidapi-host': 'tradematic-cloud.p.rapidapi.com'
    }
    
    try:
        response = requests.get(url, headers=headers)
        data = response.json()  # Parse JSON response
        return data  # Return API response
    except Exception as e:
        print(f"API Error: {e}")
        return None

# Investment Page
@app.route('/investment')
def investment():
    if 'name' not in session or 'salary' not in session:
        return redirect(url_for('welcome'))  # Redirect if not logged in

    # Fetch user's salary
    salary = session['salary']

    # Get total spending from the database
    conn = sqlite3.connect('finwise.db')
    c = conn.cursor()
    c.execute('SELECT SUM(amount) FROM expenses')
    total_spent = c.fetchone()[0] or 0  # Handle None if no expenses
    conn.close()

    # Calculate remaining savings
    savings = salary - total_spent

    # Get investment recommendations from API
    investment_data = get_investment_suggestions()

    # Define investment suggestions based on savings
    if savings < 5000:
        investment_tips = ["Fixed Deposit (FD)", "Recurring Deposit (RD)", "Emergency Fund"]
    elif 5000 <= savings < 20000:
        investment_tips = ["Mutual Funds (SIP)", "Debt Funds", "Gold Investment"]
    else:
        investment_tips = ["Stock Market", "Bonds", "Cryptocurrency", "Real Estate"]

    return render_template("investment.html", 
                           name=session['name'], 
                           salary=salary, 
                           savings=savings, 
                           investment_tips=investment_tips, 
                           api_data=investment_data)
    


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
