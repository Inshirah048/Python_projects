# Bank Account System

A simple banking system project I created to practice and understand Object-Oriented Programming concepts in Python.

While building this project, I focused on applying concepts like abstraction, encapsulation, inheritance, and polymorphism in a practical scenario.

## About the Project

This project simulates a basic banking system where users can create different types of bank accounts and perform common banking operations such as depositing and withdrawing money.

The main goal of this project was not to build a real banking application, but to improve my understanding of Python classes, object relationships, and OOP design principles.

## Features

- Abstract `Account` class using Python's ABC module
- Savings account with interest calculation and minimum balance validation
- Current account with overdraft facility
- Custom exception handling for insufficient balance cases
- Protected balance attribute with controlled access using `@property`
- Automatic account number generation
- Implementation of special methods:
  - `__str__`
  - `__repr__`
  - `__eq__`

## Project Structure

```
Bank-Account-System/
│
├── main.py          # Demonstrates OOP concepts with sample scenarios
├── interactive.py   # Allows users to interact with the banking system
├── bank_account.py  # Account-related classes
└── README.md
```

## OOP Concepts Used

### Abstraction
Created an abstract `Account` class that defines the common structure for all accounts while allowing subclasses to implement their own account behavior.

### Encapsulation
The account balance is protected and can only be modified through controlled methods such as `deposit()` and `withdraw()`.

### Inheritance
`SavingsAccount` and `CurrentAccount` inherit common properties and methods from the base `Account` class.

### Polymorphism
Different account types implement their own withdrawal behavior according to their rules.

## How to Run

Clone the repository and run:

```bash
python main.py
```

For the interactive version:

```bash
python interactive.py
```

## What I Practiced From This Project

Through this project, I practiced:

- Designing classes and objects in Python
- Understanding relationships between classes
- Applying OOP principles to a real-world scenario
- Using abstract classes and custom exceptions
- Writing cleaner and more maintainable Python code
