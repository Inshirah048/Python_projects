# Demo script — shows role-based access control (RBAC) in action:
# students and lecturers can only do what their role permits.

from lms import (
    Student,
    Lecturer,
    LearningManagementSystem,
    PermissionDeniedError,
    StudentNotFoundError,
    InvalidGradeError,
)


def main():
    lms = LearningManagementSystem(name="Greenfield LMS")

    # ----- Register users -----
    prof_smith = Lecturer("Dr. Smith", department="Computer Science")
    lms.register_lecturer(prof_smith)

    omkar = Student("Omkar", major="Computer Science", year=2)
    asha = Student("Asha", major="Mathematics", year=1)
    lms.register_student(omkar)
    lms.register_student(asha)

    print(lms, "\n")

    # ----- Lecturer uploads an assignment -----
    assignment = lms.upload_assignment(
        prof_smith, "Binary Trees", "Implement a BST with insert/delete", due_date="2026-08-01"
    )
    print(f"Uploaded: {assignment}\n")

    # ----- Student views assignments -----
    print("--- Omkar's view of assignments ---")
    for a in lms.view_assignments(omkar):
        print(a)
    print()

    # ----- A student TRIES to upload an assignment (should fail) -----
    print("--- Omkar tries to upload an assignment (should be denied) ---")
    try:
        lms.upload_assignment(omkar, "Cheating attempt", "Not allowed")
    except PermissionDeniedError as e:
        print(f"Denied: {e}\n")

    # ----- Lecturer publishes marks -----
    lms.publish_marks(prof_smith, omkar.user_id, "Data Structures", 92)
    lms.publish_marks(prof_smith, omkar.user_id, "Algorithms", 88)
    lms.publish_marks(prof_smith, asha.user_id, "Calculus", 75)
    print("Marks published.\n")

    # ----- A student TRIES to publish their own marks (should fail) -----
    print("--- Omkar tries to publish his own marks (should be denied) ---")
    try:
        lms.publish_marks(omkar, omkar.user_id, "Bonus", 100)
    except PermissionDeniedError as e:
        print(f"Denied: {e}\n")

    # ----- Student views their own marksheet -----
    print("--- Omkar's marksheet ---")
    print(lms.view_my_marksheet(omkar))
    print(f"Average: {omkar.get_average():.2f}\n")

    # ----- A student TRIES to view another student's marksheet -----
    # (Not directly possible since view_my_marksheet only returns the
    #  caller's own grades — this demonstrates the design is safe by
    #  construction, not just by a permission check.)

    # ----- Lecturer views ALL students' grades -----
    print("--- Dr. Smith's view of all grades ---")
    for student_id, (name, grades, avg) in lms.view_all_grades(prof_smith).items():
        print(f"{student_id} {name}: {grades} -> avg {avg:.2f}")
    print()

    # ----- Invalid grade validation still applies -----
    try:
        lms.publish_marks(prof_smith, omkar.user_id, "Bad Mark", 150)
    except InvalidGradeError as e:
        print(f"Error: {e}\n")

    # ----- Lecturer removes a student -----
    print("--- Dr. Smith removes Asha ---")
    removed = lms.remove_student(prof_smith, asha.user_id)
    print(f"Removed: {removed}")

    try:
        lms.get_student(asha.user_id)
    except StudentNotFoundError as e:
        print(f"Confirmed removed: {e}")

    print(f"\nFinal state: {lms}")


if __name__ == '__main__':
    main()