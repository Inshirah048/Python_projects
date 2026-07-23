# Learning Management System (LMS)
# Demonstrates OOP concepts: abstraction, inheritance, polymorphism,
# encapsulation, composition, custom exceptions, and role-based
# access control (RBAC) — students and lecturers have different
# permissions enforced by the system.

from abc import ABC, abstractmethod
from datetime import datetime


# ---------------------- Custom Exceptions ----------------------
class PermissionDeniedError(Exception):
    """Raised when a user tries to perform an action their role doesn't allow."""
    pass


class StudentNotFoundError(Exception):
    pass


class DuplicateStudentError(Exception):
    pass


class InvalidGradeError(Exception):
    pass


class AssignmentNotFoundError(Exception):
    pass


# ---------------------- Roles (Users) ----------------------
class User(ABC):
    """
    Abstract base class for anyone using the LMS.
    ABSTRACTION: cannot be instantiated directly.
    """

    def __init__(self, name, user_id):
        self.name = name
        self.user_id = user_id

    @abstractmethod
    def role(self):
        """Every subclass must declare its role."""
        pass

    def __str__(self):
        return f"[{self.user_id}] {self.name} ({self.role()})"


class Student(User):
    """
    INHERITANCE: extends User.
    ENCAPSULATION: grades are private, only modified via add_grade()
    with validation.
    """

    defaultStudentId = 1001  # Class attribute, shared + auto-incrementing

    def __init__(self, name, major="Undeclared", year=1):
        super().__init__(name, Student.defaultStudentId)
        Student.defaultStudentId += 1
        self.major = major
        self.year = year
        self._grades = {}          # subject -> mark  (private/protected)
        self.enrolled_on = datetime.now().strftime("%Y-%m-%d")

    def role(self):
        return "Student"

    def add_grade(self, subject, mark):
        if not (0 <= mark <= 100):
            raise InvalidGradeError(f"Mark must be between 0-100, got {mark}")
        self._grades[subject] = mark

    def get_grades(self):
        return dict(self._grades)   # return a copy — protects internal state

    def get_average(self):
        if not self._grades:
            return 0.0
        return sum(self._grades.values()) / len(self._grades)

    def __repr__(self):
        return f"Student(name={self.name!r}, id={self.user_id})"


class Lecturer(User):
    """
    INHERITANCE + POLYMORPHISM: role() returns "Lecturer" instead of
    "Student". Lecturers are the only ones permitted (by the LMS class)
    to remove students, upload assignments, and publish marks.
    """

    defaultLecturerId = 2001

    def __init__(self, name, department="General"):
        super().__init__(name, Lecturer.defaultLecturerId)
        Lecturer.defaultLecturerId += 1
        self.department = department

    def role(self):
        return "Lecturer"

    def __repr__(self):
        return f"Lecturer(name={self.name!r}, id={self.user_id})"


# ---------------------- Assignment ----------------------
class Assignment:
    """A piece of coursework uploaded by a lecturer."""

    defaultAssignmentId = 1

    def __init__(self, title, description, uploaded_by, due_date=None):
        self.assignment_id = Assignment.defaultAssignmentId
        Assignment.defaultAssignmentId += 1
        self.title = title
        self.description = description
        self.uploaded_by = uploaded_by   # Lecturer's name
        self.due_date = due_date or "No due date set"
        self.uploaded_on = datetime.now().strftime("%Y-%m-%d")

    def __str__(self):
        return (f"[Assignment #{self.assignment_id}] {self.title} "
                f"(due: {self.due_date}) — uploaded by {self.uploaded_by}")


# ---------------------- The LMS itself ----------------------
def lecturer_only(method):
    """
    Decorator enforcing that only a Lecturer can call the wrapped method.
    The caller must be passed as the first argument after self.
    """
    def wrapper(self, acting_user, *args, **kwargs):
        if not isinstance(acting_user, Lecturer):
            raise PermissionDeniedError(
                f"Access denied: only lecturers can perform this action "
                f"(attempted by {acting_user.role()} '{acting_user.name}')"
            )
        return method(self, acting_user, *args, **kwargs)
    return wrapper


def student_only(method):
    """Decorator enforcing that only a Student can call the wrapped method."""
    def wrapper(self, acting_user, *args, **kwargs):
        if not isinstance(acting_user, Student):
            raise PermissionDeniedError(
                f"Access denied: only students can perform this action "
                f"(attempted by {acting_user.role()} '{acting_user.name}')"
            )
        return method(self, acting_user, *args, **kwargs)
    return wrapper


class LearningManagementSystem:
    """
    COMPOSITION: the LMS HAS students, lecturers, and assignments.
    Enforces role-based permissions (RBAC) using the decorators above.
    """

    def __init__(self, name="LMS"):
        self.name = name
        self._students = {}      # id -> Student
        self._lecturers = {}     # id -> Lecturer
        self._assignments = {}   # id -> Assignment

    # ---------- Registration (open to anyone joining the system) ----------
    def register_student(self, student):
        if student.user_id in self._students:
            raise DuplicateStudentError(f"Student ID {student.user_id} already exists")
        self._students[student.user_id] = student
        return student

    def register_lecturer(self, lecturer):
        self._lecturers[lecturer.user_id] = lecturer
        return lecturer

    # ---------- Student actions ----------
    @student_only
    def view_assignments(self, acting_user):
        return list(self._assignments.values())

    @student_only
    def view_my_marksheet(self, acting_user):
        return acting_user.get_grades()

    # ---------- Lecturer-only actions ----------
    @lecturer_only
    def upload_assignment(self, acting_user, title, description, due_date=None):
        assignment = Assignment(title, description, acting_user.name, due_date)
        self._assignments[assignment.assignment_id] = assignment
        return assignment

    @lecturer_only
    def remove_student(self, acting_user, student_id):
        if student_id not in self._students:
            raise StudentNotFoundError(f"No student with ID {student_id}")
        return self._students.pop(student_id)

    @lecturer_only
    def publish_marks(self, acting_user, student_id, subject, mark):
        if student_id not in self._students:
            raise StudentNotFoundError(f"No student with ID {student_id}")
        student = self._students[student_id]
        student.add_grade(subject, mark)
        return student

    @lecturer_only
    def view_all_grades(self, acting_user):
        return {s.user_id: (s.name, s.get_grades(), s.get_average())
                for s in self._students.values()}

    # ---------- Shared / read-only helpers ----------
    def list_students(self):
        return list(self._students.values())

    def get_student(self, student_id):
        if student_id not in self._students:
            raise StudentNotFoundError(f"No student with ID {student_id}")
        return self._students[student_id]

    def __len__(self):
        return len(self._students)

    def __str__(self):
        return (f"{self.name}: {len(self._students)} students, "
                f"{len(self._lecturers)} lecturers, "
                f"{len(self._assignments)} assignments")