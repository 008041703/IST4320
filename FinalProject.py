import tkinter as tk
from tkinter import messagebox
import sqlite3
from collections import defaultdict
from datetime import datetime
from tkinter import font

# Function to set up the SQLite database
def setup_database():
    conn = sqlite3.connect('expenses.db') # Connect to the SQLite database file or create it if it doesn't exist
    cursor = conn.cursor() # Create a cursor object to execute SQL commands
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY,
            name TEXT,
            amount REAL,
            date TEXT
        )
    ''') # Create the 'expenses' table if it doesn't exist
    conn.commit()   # Commit the changes to the database    
    conn.close()    # Close the database connection

# Function to add an expense to the database
def add_expense(name, amount, date):
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO expenses (name, amount, date) VALUES (?, ?, ?)
    ''', (name, amount, date))
    conn.commit()
    conn.close()

# Function to delete an expense from the database
def delete_expense(entry_id):
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    cursor.execute('''
        DELETE FROM expenses WHERE id = ?
    ''', (entry_id,))
    conn.commit()
    conn.close()
    update_expense_list()

# Function to clear the entire expense history from the database
def clear_expense_history():
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM expenses')
    conn.commit()
    conn.close()
    update_expense_list()

# Function to calculate monthly totals of expenses
def calculate_monthly_totals():
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    cursor.execute('SELECT date, amount FROM expenses')
    expenses = cursor.fetchall()
    conn.close()

    monthly_totals = defaultdict(float) # Create a defaultdict to store monthly totals
    for date, amount in expenses:
        month = datetime.strptime(date, '%Y-%m-%d').strftime('%Y-%m')
        monthly_totals[month] += amount

    return monthly_totals

# Function to display monthly totals using a messagebox
def display_monthly_totals():
    monthly_totals = calculate_monthly_totals()
    result = '\n'.join([f"{month}: ${total:.2f}" for month, total in monthly_totals.items()])
    messagebox.showinfo("Monthly Totals", result)

# Function to update the expense list displayed in the GUI
def update_expense_list():
    listbox_expenses.delete(0, tk.END)
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM expenses')
    for row in cursor.fetchall():
        listbox_expenses.insert(tk.END, f"{row[0]} - {row[1]} - ${row[2]} on {row[3]}")
    conn.close()

# Set up the SQLite database
setup_database()

# Create the main GUI window
root = tk.Tk()
root.title("IST4320 - App Project")

# Custom Fonts and Colors
title_font = font.Font(family="Helvetica", size=20, weight="bold")
label_font = font.Font(family="Helvetica", size=10)
entry_font = font.Font(family="Helvetica", size=10)
button_font = font.Font(family="Helvetica", size=10)

# Configure root window
root.configure(bg="#f0f0f0")

# Create and place widgets in the GUI window
tk.Label(root, text="Expense Tracker", font=title_font, bg="#f0f0f0", fg="green").grid(row=0, columnspan=2, padx=10, pady=10)


# Labels and entry fields for expense details
tk.Label(root, text="Expense Name", font=label_font, bg="#f0f0f0", fg="#333333").grid(row=1, column=0, padx=10, pady=5)
entry_name = tk.Entry(root, font=entry_font)
entry_name.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Amount", font=label_font, bg="#f0f0f0", fg="#333333").grid(row=2, column=0, padx=10, pady=5)
entry_amount = tk.Entry(root, font=entry_font)
entry_amount.grid(row=2, column=1, padx=10, pady=5)

tk.Label(root, text="Date (YYYY-MM-DD)", font=label_font, bg="#f0f0f0", fg="#333333").grid(row=3, column=0, padx=10, pady=5)
entry_date = tk.Entry(root, font=entry_font)
entry_date.grid(row=3, column=1, padx=10, pady=5)

# Function to handle adding an expense
def on_add_expense():
    name = entry_name.get()
    amount = entry_amount.get()
    date = entry_date.get()
    if name and amount and date:
        add_expense(name, float(amount), date)
        entry_name.delete(0, tk.END)
        entry_amount.delete(0, tk.END)
        entry_date.delete(0, tk.END)
        update_expense_list()
    else:
        messagebox.showwarning("Warning", "All fields are required.")


# Button to add an expense
tk.Button(root, text="Add Expense", font=button_font, command=on_add_expense, bg="#4CAF50", fg="black").grid(row=4, columnspan=2, pady=10)

# Button to show monthly totals
tk.Button(root, text="Show Monthly Totals", font=button_font, command=display_monthly_totals, bg="#2196F3", fg="green").grid(row=5, columnspan=2, pady=10)

# Button to clear expense history
tk.Button(root, text="Clear History", font=button_font, command=clear_expense_history, bg="#FF5733", fg="red").grid(row=6, columnspan=2, pady=10)

# Listbox to display expenses
listbox_expenses = tk.Listbox(root, font=entry_font, height=10, width=50)
listbox_expenses.grid(row=7, columnspan=2, padx=10, pady=10)

# Function to handle deleting the selected expense
def on_delete_selected():
    selected = listbox_expenses.curselection()
    if selected:
        entry_id = selected[0] + 1  # Adding 1 because listbox index starts from 0 but DB id starts from 1
        delete_expense(entry_id)
    else:
        messagebox.showwarning("Warning", "Select an expense to delete.")

tk.Button(root, text="Delete Selected", font=button_font, command=on_delete_selected, bg="#FF5733", fg="black").grid(row=8, columnspan=2, pady=10)


# Update the expense list when the application starts
update_expense_list()

# Run the main loop
root.mainloop()
