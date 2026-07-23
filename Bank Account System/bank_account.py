
from abc import ABC, abstractmethod


class InsufficientBalanceError(Exception):
    pass


class Account(ABC):
    
    defaultAccNumber = 1  
    def __init__(self, name, balance=0):
        self.name = name
        self._balance = balance         
        self.accountNumber = Account.defaultAccNumber
        Account.defaultAccNumber += 1

    
    @property
    def balance(self):
        return self._balance

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        self._balance += amount
        return self._balance

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        if self._balance < amount:
            raise InsufficientBalanceError(
                f"Not enough balance! Available: {self._balance}, requested: {amount}"
            )
        self._balance -= amount
        return self._balance

    def getBalance(self):
        return self._balance

    @abstractmethod
    def account_type(self):
        pass

    def __str__(self):
        return (f"[{self.account_type()}] Acc#{self.accountNumber} | "
                f"{self.name} | Balance: {self._balance}")

    def __repr__(self):
        return (f"{self.__class__.__name__}(name={self.name!r}, "
                f"balance={self._balance!r})")

    def __eq__(self, other):
        if not isinstance(other, Account):
            return NotImplemented
        return self.accountNumber == other.accountNumber


class SavingsAccount(Account):
    
    def __init__(self, name, balance=0, interest_rate=0.04, min_balance=500):
        super().__init__(name, balance)
        self.interest_rate = interest_rate
        self.min_balance = min_balance

    def withdraw(self, amount):
        if self._balance - amount < self.min_balance:
            raise InsufficientBalanceError(
                f"Cannot withdraw {amount}. Minimum balance of "
                f"{self.min_balance} must be maintained."
            )
        return super().withdraw(amount)

    def apply_interest(self):
        interest = self._balance * self.interest_rate
        self._balance += interest
        return interest

    def account_type(self):
        return "Savings"


class CurrentAccount(Account):

    def __init__(self, name, balance=0, overdraft_limit=1000):
        super().__init__(name, balance)
        self.overdraft_limit = overdraft_limit

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        if self._balance - amount < -self.overdraft_limit:
            raise InsufficientBalanceError(
                f"Overdraft limit of {self.overdraft_limit} exceeded!"
            )
        self._balance -= amount
        return self._balance

    def account_type(self):
        return "Current"


class BankAccount(Account):
    def account_type(self):
        return "Basic"