from lms import (
    Student,
    Lecturer,
    LearningManagementSystem,
    PermissionDeniedError,
    StudentNotFoundError,
    DuplicateStudentError,
    InvalidGradeError,
)

LMS_NAME = "Greenfield LMS"


def student_menu(lms, student):
    while True:
        print(f"\n Student Portal - {student.name} (ID {student.user_id})")
        print(" 1. View Assignments")
        print(" 2. View My Marksheet")
        print(" 3. Log Out")
        choice = input("Enter choice: ").strip()

        if choice == '1':
            assignments = lms.view_assignments(student)
            if not assignments:
                print("No assignments uploaded yet.")
            for a in assignments:
                print(a)

        elif choice == '2':
            grades = lms.view_my_marksheet(student)
            if not grades:
                print("No grades published yet.")
            else:
                for subject, mark in grades.items():
                    print(f"  {subject}: {mark}")
                print(f"Average: {student.get_average():.2f}")

        elif choice == '3':
            print("Logged out.\n")
            break

        else:
            print("Invalid choice, try again.")

def lecturer_menu(lms, lecturer):
    while True:
        print(f"\n Lecturer Portal - {lecturer.name} (ID {lecturer.user_id})")
        print(" 1. Upload Assignment")
        print(" 2. Publish Marks")
        print(" 3. Remove Student")
        print(" 4. View All Students' Grades")
        print(" 5. List All Students")
        print(" 6. Log Out")
        choice = input("Enter choice: ").strip()

        if choice == '1':
            title = input("Assignment title: ").strip()
            desc = input("Description: ").strip()
            due = input("Due date : ").strip() or None
            assignment = lms.upload_assignment(lecturer, title, desc, due)
            print(f"Uploaded: {assignment}")

        elif choice == '2':
            try:
                sid = int(input("Student ID: ").strip())
                subject = input("Subject: ").strip()
                mark = float(input("Mark (0-100): ").strip())
                student = lms.publish_marks(lecturer, sid, subject, mark)
                print(f"Published. {student.name}'s new average: {student.get_average():.2f}")
            except StudentNotFoundError as e:
                print(f"Error: {e}")
            except InvalidGradeError as e:
                print(f"Error: {e}")
            except ValueError:
                print("Error: please enter valid numbers.")

        elif choice == '3':
            try:
                sid = int(input("Student ID to remove: ").strip())
                removed = lms.remove_student(lecturer, sid)
                print(f"Removed: {removed}")
            except StudentNotFoundError as e:
                print(f"Error: {e}")
            except ValueError:
                print("Error: please enter a valid numeric ID.")

        elif choice == '4':
            grades = lms.view_all_grades(lecturer)
            if not grades:
                print("No students enrolled yet.")
            for sid, (name, marks, avg) in grades.items():
                print(f"[{sid}] {name}: {marks} -> avg {avg:.2f}")

        elif choice == '5':
            students = lms.list_students()
            if not students:
                print("No students enrolled yet.")
            for s in students:
                print(s)

        elif choice == '6':
            print("Logged out.\n")
            break

        else:
            print("Invalid choice, try again.")


def student_login_or_register(lms):
    choice = input("1. I'm a new student \n2. I already have a Student ID\nChoice: ").strip()
    if choice == '1':
        name = input("Enter your name: ").strip()
        major = input("Enter your department: ").strip() or "Undeclared"
        year = input("Enter year of study : ").strip()
        year = int(year) if year else 1
        student = Student(name, major, year)
        try:
            lms.register_student(student)
            print(f"\nEnrolled successfully! Your Student ID is {student.user_id} —  remember it.")
            return student
        except DuplicateStudentError as e:
            print(f"Error: {e}")
            return None
    else:
        try:
            sid = int(input("Enter your Student ID: ").strip())
            return lms.get_student(sid)
        except (StudentNotFoundError, ValueError) as e:
            print(f"Error: {e}")
            return None


def lecturer_login_or_register(lms):
    choice = input("1. I'm a new lecturer \n2. I already have a Lecturer ID\nChoice: ").strip()
    if choice == '1':
        name = input("Enter your name: ").strip()
        dept = input("Enter your department: ").strip() or "General"
        lecturer = Lecturer(name, dept)
        lms.register_lecturer(lecturer)
        print(f"\nRegistered successfully! Your Lecturer ID is {lecturer.user_id} — remember it.")
        return lecturer
    else:
        lid = input("Enter your Lecturer ID: ").strip()
        for lect in lms._lecturers.values():
            if str(lect.user_id) == lid:
                return lect
        print("Lecturer ID not found.")
        return None


def main():
    lms = LearningManagementSystem(name=LMS_NAME)
    print(f" Welcome to {LMS_NAME} ")

    while True:
        print("\n1. Log in as Student")
        print("2. Log in as Lecturer")
        print("3. Exit")
        choice = input("Enter choice: ").strip()

        if choice == '1':
            student = student_login_or_register(lms)
            if student:
                student_menu(lms, student)

        elif choice == '2':
            lecturer = lecturer_login_or_register(lms)
            if lecturer:
                lecturer_menu(lms, lecturer)

        elif choice == '3':
            print(f"Thank you for using {LMS_NAME}.")
            break

        else:
            print("Invalid choice, try again.")


if __name__ == '__main__':
    main()