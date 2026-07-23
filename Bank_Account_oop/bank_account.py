# Author: OMKAR PATHAK (extended)
# This module illustrates OOP concepts: encapsulation, abstraction,
# inheritance, polymorphism, class vs instance attributes, dunder methods,
# and custom exceptions.

from abc import ABC, abstractmethod


class InsufficientBalanceError(Exception):
    """Custom exception raised when a withdrawal exceeds the balance."""
    pass


class Account(ABC):
    """
    Abstract base class for all account types.

    Demonstrates ABSTRACTION: this class can never be instantiated
    directly. It only defines the contract (methods) that subclasses
    must implement.
    """

    defaultAccNumber = 1  # Class Attribute shared by ALL accounts

    def __init__(self, name, balance=0):
        self.name = name
        self._balance = balance          # "protected" attribute (encapsulation)
        self.accountNumber = Account.defaultAccNumber
        Account.defaultAccNumber += 1

    # ---------- Encapsulation via property ----------
    @property
    def balance(self):
        """Read-only access to balance from outside the class."""
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
        """Every subclass MUST say what type of account it is."""
        pass

    # ---------- Dunder methods ----------
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
    """
    INHERITANCE: reuses everything from Account.
    POLYMORPHISM: overrides withdraw() with its own rule (minimum balance).
    """

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
    """
    INHERITANCE + POLYMORPHISM: overrides withdraw() to allow overdraft
    up to a limit, unlike the base Account behaviour.
    """

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


# Keep the original simple class name available too, for backward
# compatibility with the very first version of this script.
class BankAccount(Account):
    def account_type(self):
        return "Basic"