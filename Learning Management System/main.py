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

    prof_smith = Lecturer("Dr. Smith", department="Computer Science")
    lms.register_lecturer(prof_smith)

    omkar = Student("Omkar", major="Computer Science", year=2)
    asha = Student("Asha", major="Mathematics", year=1)
    lms.register_student(omkar)
    lms.register_student(asha)

    print(lms, "\n")

    assignment = lms.upload_assignment(
        prof_smith, "Binary Trees", "Implement a BST with insert/delete", due_date="2026-08-01"
    )
    print(f"Uploaded: {assignment}\n")

    print("Omkar's view of assignments")
    for a in lms.view_assignments(omkar):
        print(a)
    print()

    print("Omkar tries to upload an assignment")
    try:
        lms.upload_assignment(omkar, "Cheating attempt", "Not allowed")
    except PermissionDeniedError as e:
        print(f"Denied: {e}\n")

   
    lms.publish_marks(prof_smith, omkar.user_id, "Data Structures", 92)
    lms.publish_marks(prof_smith, omkar.user_id, "Algorithms", 88)
    lms.publish_marks(prof_smith, asha.user_id, "Calculus", 75)
    print("Marks published.\n")


    print("Omkar tries to publish his own marks")
    try:
        lms.publish_marks(omkar, omkar.user_id, "Bonus", 100)
    except PermissionDeniedError as e:
        print(f"Denied: {e}\n")

   
    print("Omkar's marksheet")
    print(lms.view_my_marksheet(omkar))
    print(f"Average: {omkar.get_average():.2f}\n")


    print(" Dr. Smith's view of all grades ")
    for student_id, (name, grades, avg) in lms.view_all_grades(prof_smith).items():
        print(f"{student_id} {name}: {grades} -> avg {avg:.2f}")
    print()

    try:
        lms.publish_marks(prof_smith, omkar.user_id, "Bad Mark", 150)
    except InvalidGradeError as e:
        print(f"Error: {e}\n")
        
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