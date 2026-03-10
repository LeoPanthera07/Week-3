def main():
    while True:
        try:
            raw = input("Enter age: ").strip()
            if not raw:
                raise ValueError("Age cannot be empty")

            age = int(raw)

            if age < 0 or age > 150:
                raise ValueError(f"Age must be between 0 and 150, got {age}")

        except ValueError as e:
            print(f"Invalid input: {e}. Please try again.")
        else:
            print(f"In 10 years, you will be {age + 10}.")
            break
        finally:
            print("Age check completed.\n")


if __name__ == "__main__":
    main()