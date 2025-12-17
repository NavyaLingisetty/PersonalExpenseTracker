import csv
import os
from datetime import datetime
from typing import List, Dict, Optional

Expense = Dict[str, object]
CSV_HEADERS = ["date", "category", "amount", "description"]


def is_valid_date(date_str: str) -> bool:
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def is_complete_expense(exp: Expense) -> bool:
    return all(
        k in exp and exp[k] not in (None, "", [])
        for k in ["date", "category", "amount", "description"]
    )


def add_expense(expenses: List[Expense]) -> None:
    date = input("Enter date (YYYY-MM-DD): ").strip()
    if not is_valid_date(date):
        print("Invalid date format. Please use YYYY-MM-DD.")
        return

    category = input("Enter category (e.g., Food, Travel): ").strip()
    if not category:
        print("Category cannot be empty.")
        return

    amount_str = input("Enter amount spent: ").strip()
    try:
        amount = float(amount_str)
        if amount <= 0:
            print("Amount must be greater than 0.")
            return
    except ValueError:
        print("Amount must be a valid number.")
        return

    description = input("Enter a brief description: ").strip()
    if not description:
        print("Description cannot be empty.")
        return

    expense = {
        "date": date,
        "category": category,
        "amount": round(amount, 2),
        "description": description,
    }
    expenses.append(expense)
    print("Expense added successfully.")


def view_expenses(expenses: List[Expense]) -> None:
    if not expenses:
        print("No expenses recorded yet.")
        return

    print("\n--- All Expenses ---")
    shown = 0
    for idx, exp in enumerate(expenses, start=1):
        if not is_complete_expense(exp):
            print(f"Skipping incomplete entry at index {idx}.")
            continue

        print(
            f"{idx}. Date: {exp['date']} | "
            f"Category: {exp['category']} | "
            f"Amount: {exp['amount']:.2f} | "
            f"Description: {exp['description']}"
        )
        shown += 1

    if shown == 0:
        print("No complete expense entries to display.")


def total_expenses(expenses: List[Expense]) -> float:
    total = 0.0
    for exp in expenses:
        if is_complete_expense(exp):
            try:
                total += float(exp["amount"])
            except (ValueError, TypeError):
                pass
    return round(total, 2)


def set_budget() -> Optional[float]:
    budget_str = input("Enter monthly budget amount: ").strip()
    try:
        budget = float(budget_str)
        if budget <= 0:
            print("Budget must be greater than 0.")
            return None
        return round(budget, 2)
    except ValueError:
        print("Budget must be a valid number.")
        return None


def track_budget(expenses: List[Expense], budget: Optional[float]) -> Optional[float]:
    if budget is None:
        print("No budget set yet.")
        budget = set_budget()
        if budget is None:
            return None

    spent = total_expenses(expenses)
    print(f"Total spent so far: {spent:.2f}")
    print(f"Monthly budget: {budget:.2f}")

    if spent > budget:
        print("WARNING: You have exceeded your budget!")
    else:
        remaining = round(budget - spent, 2)
        print(f"You have {remaining:.2f} left for the month.")
    return budget


def save_expenses(expenses: List[Expense], filename: str = "expenses.csv") -> None:
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_HEADERS)
        writer.writeheader()
        for exp in expenses:
            if not is_complete_expense(exp):
                continue
            writer.writerow(
                {
                    "date": exp["date"],
                    "category": exp["category"],
                    "amount": f"{float(exp['amount']):.2f}",
                    "description": exp["description"],
                }
            )
    print(f"Expenses saved to {filename}")


def load_expenses(filename: str = "expenses.csv") -> List[Expense]:
    expenses: List[Expense] = []
    if not os.path.exists(filename):
        return expenses

    try:
        with open(filename, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                date = (row.get("date") or "").strip()
                category = (row.get("category") or "").strip()
                amount_str = (row.get("amount") or "").strip()
                description = (row.get("description") or "").strip()

                if not (date and category and amount_str and description):
                    continue
                if not is_valid_date(date):
                    continue

                try:
                    amount = float(amount_str)
                except ValueError:
                    continue

                expenses.append(
                    {
                        "date": date,
                        "category": category,
                        "amount": round(amount, 2),
                        "description": description,
                    }
                )
    except Exception as e:
        print(f"Failed to load expenses: {e}")

    return expenses


def show_menu() -> None:
    print("\n=== Personal Expense Tracker ===")
    print("1. Add expense")
    print("2. View expenses")
    print("3. Track budget")
    print("4. Save expenses")
    print("5. Exit")


def main() -> None:
    expenses = load_expenses("expenses.csv")
    budget: Optional[float] = None

    if expenses:
        print(f"Loaded {len(expenses)} expense(s) from expenses.csv")

    while True:
        show_menu()
        choice = input("Choose an option (1-5): ").strip()

        if choice == "1":
            add_expense(expenses)
        elif choice == "2":
            view_expenses(expenses)
        elif choice == "3":
            budget = track_budget(expenses, budget)
        elif choice == "4":
            save_expenses(expenses, "expenses.csv")
        elif choice == "5":
            save_expenses(expenses, "expenses.csv")
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please enter a number from 1 to 5.")


if __name__ == "__main__":
    main()
