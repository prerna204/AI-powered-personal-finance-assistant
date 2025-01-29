from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from collections import defaultdict
from datetime import datetime

app = Flask(__name__)

# Database setup
def init_db():
    conn = sqlite3.connect('finwise.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS expenses
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  category TEXT NOT NULL,
                  amount REAL NOT NULL,
                  date TEXT NOT NULL)''')
    conn.commit()
    conn.close()

# Homepage
@app.route('/')
def index():
    return render_template('index.html')

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
    try:
        conn = sqlite3.connect('finwise.db')
        c = conn.cursor()
        c.execute('SELECT * FROM expenses')
        expenses = c.fetchall()

        # Calculate total spending
        total_spent = sum(expense[2] for expense in expenses)

        # Categorize expenses
        category_spending = defaultdict(float)
        for expense in expenses:
            category_spending[expense[1]] += expense[2]

        # Monthly trends
        monthly_spending = defaultdict(float)
        for expense in expenses:
            date = datetime.strptime(expense[3], "%Y-%m-%d")
            month_year = f"{date.month}-{date.year}"
            monthly_spending[month_year] += expense[2]

        conn.close()

        # Pass all variables to the template
        return render_template(
            'view_expenses.html',
            expenses=expenses,
            total_spent=total_spent,
            category_spending=dict(category_spending),
            monthly_spending=dict(monthly_spending)
        )
    except Exception as e:
        print(f"Error in view_expenses: {str(e)}")
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

if __name__ == '__main__':
    init_db()
    app.run(debug=True)