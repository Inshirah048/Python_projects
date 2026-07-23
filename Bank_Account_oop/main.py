
from bank_account import (
    BankAccount,
    SavingsAccount,
    CurrentAccount,
    InsufficientBalanceError,
)


def basic_demo():
    print(" Basic BankAccount ")
    myObj = BankAccount('Omkar', 1000)
    myObj.deposit(1000)
    print(myObj.getBalance())
    myObj.withdraw(500)
    print(myObj.getBalance())
    print(myObj)         
    print()


def polymorphism_demo():
    accounts = [
        SavingsAccount('Asha', balance=2000, interest_rate=0.05, min_balance=500),
        CurrentAccount('Ravi', balance=1000, overdraft_limit=1500),
    ]

    for acc in accounts:
        print(acc)  

    print("\nTrying to withdraw 1800 from each account:")
    for acc in accounts:
        try:
            acc.withdraw(1800)
            print(f"{acc.name} withdrew 1800 -> new balance: {acc.getBalance()}")
        except InsufficientBalanceError as e:
            print(f"{acc.name}: {e}")
    print()


def interest_demo():
    savings = SavingsAccount('Meera', balance=10000, interest_rate=0.06)
    earned = savings.apply_interest()
    print(f"Interest earned: {earned:.2f}")
    print(savings)
    print()


def equality_and_repr_demo():
    a1 = BankAccount('Test1', 100)
    a2 = BankAccount('Test2', 200)
    print(f"a1 == a2 ? {a1 == a2}")
    print(repr(a1))
    print()


def account_numbering_demo():
    a = BankAccount('A', 0)
    b = SavingsAccount('B', 0)
    c = CurrentAccount('C', 0)
    print(a.accountNumber, b.accountNumber, c.accountNumber)


if __name__ == '__main__':
    basic_demo()
    polymorphism_demo()
    interest_demo()
    equality_and_repr_demo()
    account_numbering_demo()