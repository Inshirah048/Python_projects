
from bank_account import (
    SavingsAccount,
    CurrentAccount,
    InsufficientBalanceError,
)


def create_account():
    print("\nWhat type of account would you like to open?")
    print("1. Savings Account")
    print("2. Current Account")
    choice = input("Enter your choice (1/2): ").strip()

    name = input("Enter your name: ").strip()
    balance = float(input("Enter opening balance: ").strip() or 0)

    if choice == '1':
        rate = input("Enter interest rate: ").strip()
        rate = float(rate) if rate else 0.04
        min_bal = input("Enter minimum balance to maintain : ").strip()
        min_bal = float(min_bal) if min_bal else 500
        account = SavingsAccount(name, balance, interest_rate=rate, min_balance=min_bal)
    elif choice == '2':
        limit = input("Enter overdraft limit: ").strip()
        limit = float(limit) if limit else 1000
        account = CurrentAccount(name, balance, overdraft_limit=limit)
    else:
        print("Invalid choice, defaulting to Savings Account.")
        account = SavingsAccount(name, balance)

    print(f"\nAccount created successfully!\n{account}")
    return account


BANK_NAME = "SecureTrust Bank"


def show_menu(account):
    print(f"\n {BANK_NAME} - ATM Services ")
    print(f" Welcome, {account.name} (Acc# {account.accountNumber})")
    print("-" * 46)
    print(" 1. Deposit Funds")
    print(" 2. Withdraw Funds")
    print(" 3. Check Balance")
    print(" 4. View Account Statement")
    print(" 5. Apply Interest (Savings only)")
    print(" 6. Exit / Log Out")
    print("=" * 46)


def main():
    print(f" Welcome to {BANK_NAME}")
    account = create_account()

    while True:
        show_menu(account)
        choice = input("Enter your choice: ").strip()

        if choice == '1':
            try:
                amount = float(input("Enter amount to deposit: "))
                new_balance = account.deposit(amount)
                print(f"Deposited {amount}. New balance: {new_balance}")
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == '2':
            try:
                amount = float(input("Enter amount to withdraw: "))
                new_balance = account.withdraw(amount)
                print(f"Withdrew {amount}. New balance: {new_balance}")
            except (ValueError, InsufficientBalanceError) as e:
                print(f"Error: {e}")

        elif choice == '3':
            print(f"Current balance: {account.getBalance()}")

        elif choice == '4':
            print(account)         
            print(repr(account))    

        elif choice == '5':
            if isinstance(account, SavingsAccount):
                interest = account.apply_interest()
                print(f"Interest applied: {interest:.2f}. New balance: {account.getBalance():.2f}")
            else:
                print("Interest can only be applied to Savings accounts.")

        elif choice == '6':
            print(f"Thank you for banking with {BANK_NAME}. Have a Nice Day!")
            break

        else:
            print("Invalid choice, please try again.")


if __name__ == '__main__':
    main()