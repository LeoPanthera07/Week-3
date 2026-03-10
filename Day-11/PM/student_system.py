import logging


logging.basicConfig(
    filename="student_system_errors.log",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

records = []


def add_student(name, subject, marks):
    if not name.strip():
        raise ValueError("Name cannot be empty")
    if not subject.strip():
        raise ValueError("Subject cannot be empty")
    if not isinstance(marks, int):
        raise TypeError("Marks must be an integer")
    if marks < 0 or marks > 100:
        raise ValueError("Marks must be between 0 and 100")

    duplicate = any(
        r[0].lower() == name.lower() and r[1].lower() == subject.lower()
        for r in records
    )
    if duplicate:
        raise ValueError("Duplicate record: same name and subject already exists")

    records.append([name, subject, marks])


def remove_student(name):
    if not name.strip():
        raise ValueError("Name cannot be empty")

    new_records = [r for r in records if r[0].lower() != name.lower()]
    removed = len(records) - len(new_records)

    if removed == 0:
        raise LookupError(f"No student records found for '{name}'")

    records.clear()
    records.extend(new_records)


def show_students():
    if not records:
        print("No records available.")
        return

    for name, subject, marks in records:
        print(f"{name:10s} | {subject:10s} | {marks}")


def main():
    while True:
        try:
            print("\n1. Add student")
            print("2. Remove student")
            print("3. Show students")
            print("4. Exit")

            choice = input("Enter choice: ").strip()
            if choice not in {"1", "2", "3", "4"}:
                raise ValueError("Choice must be 1, 2, 3, or 4")

            if choice == "1":
                name = input("Name: ").strip()
                subject = input("Subject: ").strip()
                raw_marks = input("Marks: ").strip()

                if not raw_marks:
                    raise ValueError("Marks cannot be empty")

                marks = int(raw_marks)
                add_student(name, subject, marks)

            elif choice == "2":
                name = input("Enter student name to remove: ").strip()
                remove_student(name)

            elif choice == "3":
                show_students()

            elif choice == "4":
                print("Exiting program.")
                break

        except ValueError as e:
            logging.error("Validation error: %s", e)
            print(f"Invalid input: {e}")
        except TypeError as e:
            logging.error("Type error: %s", e)
            print(f"Type error: {e}")
        except LookupError as e:
            logging.error("Lookup error: %s", e)
            print(e)
        except KeyboardInterrupt:
            logging.error("Program interrupted by user")
            print("\nProgram interrupted. Exiting safely.")
            break
        else:
            if choice in {"1", "2"}:
                print("Operation completed successfully.")
        finally:
            print("Menu cycle finished.")


if __name__ == "__main__":
    main()