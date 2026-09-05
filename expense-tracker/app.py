"""A no-dependency SQLite expense tracker. Run: python app.py"""
import sqlite3
from datetime import date

DB = "expenses.db"

def connect():
    db = sqlite3.connect(DB)
    db.execute("CREATE TABLE IF NOT EXISTS expenses (id INTEGER PRIMARY KEY, spent_on TEXT, category TEXT, amount REAL, note TEXT)")
    return db

def add(db):
    category = input("Category: ").strip() or "Other"
    amount = float(input("Amount: "))
    note = input("Note: ").strip()
    db.execute("INSERT INTO expenses (spent_on, category, amount, note) VALUES (?, ?, ?, ?)", (date.today().isoformat(), category, amount, note))
    db.commit()
    print("Expense saved.\n")

def report(db):
    rows = db.execute("SELECT category, ROUND(SUM(amount), 2) FROM expenses GROUP BY category ORDER BY SUM(amount) DESC").fetchall()
    total = sum(amount for _, amount in rows)
    print("\nSPENDING BY CATEGORY")
    for category, amount in rows:
        print(f"{category:<18} {amount:>10.2f}")
    print(f"{'TOTAL':<18} {total:>10.2f}\n")

def main():
    db = connect()
    while True:
        choice = input("[A]dd  [R]eport  [Q]uit: ").strip().lower()
        if choice == "a": add(db)
        elif choice == "r": report(db)
        elif choice == "q": break
        else: print("Choose A, R, or Q.")
    db.close()

if __name__ == "__main__":
    main()
