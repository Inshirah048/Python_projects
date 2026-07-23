# Learning Management System (Python OOP)

A simple Learning Management System built using Python to practice Object-Oriented Programming concepts and understand how real-world systems can be designed using classes and objects.

This project simulates a basic academic platform where lecturers and students have different responsibilities and access permissions.

The main focus of this project was learning how to organize code using OOP principles, handle user roles, and implement controlled access to system features.

## About the Project

The system supports two types of users:

- **Lecturers** can manage students, upload assignments, publish grades, and view student performance.
- **Students** can view available assignments and access their own grades.

Role-based access control is implemented to ensure that users can only perform actions allowed for their role.

## Features

- Abstract `User` base class for common user behavior
- Student and Lecturer classes extending the User class
- Role-based access control using decorators
- Different permissions for students and lecturers
- Custom exception handling for invalid operations
- Protected grade storage with controlled updates
- Student registration and management
- Interactive command-line interface

## Project Structure

```
Learning_Management_System/
│
├── main.py          # Demonstrates system functionality
├── interactive.py   # CLI version for user interaction
├── lms.py           # User, Student, Lecturer classes and custom exceptions
└── README.md
```

## OOP Concepts Practiced

### Abstraction
Created an abstract `User` class that defines common user behavior while allowing different user types to implement their own roles.

### Encapsulation
Student grades are protected and can only be modified through validated methods.

### Inheritance
`Student` and `Lecturer` inherit common properties and methods from the `User` class.

### Polymorphism
Different user types provide their own implementation of methods such as `role()`.

### Composition
The LMS system manages collections of students, lecturers, and assignments as part of the overall application.

## How to Run

No external libraries are required.

Run the demonstration:

```bash
python main.py
```

Run the interactive version:

```bash
python interactive.py
```

## What I Learned From This Project

Through this project, I practiced:

- Designing real-world systems using Python classes
- Implementing role-based permissions
- Using decorators for controlling access
- Creating reusable and maintainable code
- Handling errors using custom exceptions
- Applying OOP principles beyond simple examples