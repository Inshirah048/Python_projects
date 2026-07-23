# Learning Management System (Python OOP)

A simple Learning Management System (LMS) with role-based access control,
built to practice Object-Oriented Programming in Python.

## Features
- Abstract `User` base class shared by `Student` and `Lecturer`
- Role-based access control (RBAC) enforced with decorators
  (`@student_only`, `@lecturer_only`) — students and lecturers can only
  perform the actions their role allows
- Lecturers can upload assignments, publish marks, remove students, and
  view all students' grades
- Students can view assignments and their own marksheet only
- Custom exceptions: `PermissionDeniedError`, `StudentNotFoundError`,
  `DuplicateStudentError`, `InvalidGradeError`, `AssignmentNotFoundError`
- Encapsulated grades (`_grades`) — only modified through validated
  methods
- Two entry points:
  - `main.py` — scripted demo showing every concept, including denied
    permission attempts
  - `interactive.py` — interactive CLI with login/registration menus for
    students and lecturers

## OOP concepts demonstrated
| Concept | Where |
|---|---|
| Abstraction | `User(ABC)` with `@abstractmethod role()` |
| Encapsulation | `_grades` dict, only changed via `add_grade()` |
| Inheritance | `Student`, `Lecturer` extend `User` |
| Polymorphism | `role()` returns different values per subclass |
| Composition | `LearningManagementSystem` *has* students, lecturers, assignments |

## Getting started
No external dependencies - standard library only.

```bash
python3 main.py          # run the scripted demo
python3 interactive.py   # run the interactive CLI
```

## Requirements
- Python 3.8+

## Possible next steps
- Add unit tests (`unittest` / `pytest`)
- Persist data to a file or SQLite database
- Add assignment submissions and due-date enforcement
