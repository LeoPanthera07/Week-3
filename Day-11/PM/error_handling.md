# Error Handling Checklist

## Program 1: `age_checker_safe.py`

### Exceptions caught
- `ValueError`

### What recovery action is taken
- The program asks the user to enter the age again.

### What the user sees
- A clear message like:
  - `Invalid input: Age cannot be empty. Please try again.`
  - `Invalid input: Age must be between 0 and 150, got 200. Please try again.`

### What gets logged internally
- Nothing is logged in this program.

---

## Program 2: `rotate_list_safe.py`

### Exceptions caught
- `ValueError`

### What recovery action is taken
- The program rejects invalid list input or invalid `k` and asks again.

### What the user sees
- A clear message like:
  - `Input error: Please enter at least one number`
  - `Input error: invalid literal for int() with base 10: 'abc'`
  - `Input error: k must be 0 or greater`

### What gets logged internally
- Nothing is logged in this program.

---

## Program 3: `student_system_safe.py`

### Exceptions caught
- `ValueError`
- `TypeError`
- `LookupError`
- `KeyboardInterrupt`

### What recovery action is taken
- Invalid menu input is rejected.
- Invalid student details are rejected.
- Duplicate records are blocked.
- Removing a missing student shows a safe message.
- Keyboard interrupt exits the program safely.

### What the user sees
- Friendly messages like:
  - `Invalid input: Choice must be 1, 2, 3, or 4`
  - `Invalid input: Marks must be between 0 and 100`
  - `Duplicate record: same name and subject already exists`
  - `No student records found for 'Amit'`

### What gets logged internally
- Validation errors
- Type errors
- Lookup errors
- Keyboard interrupt events

### Log file
- `student_system_errors.log`

---

## Notes

### Specific exceptions used
- No bare `except:` blocks are used.
- Each program catches only the exceptions it expects.

### Use of `raise`
- Used for:
  - empty inputs
  - invalid ranges
  - duplicate records
  - missing student removal

### Use of full exception structure
- `try / except / else / finally` is used where appropriate in all 3 programs.

### User experience
- Users see simple, friendly messages.
- Internal details are logged only in the logging-enabled program.