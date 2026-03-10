def parse_numbers(text):
    parts = [item.strip() for item in text.split(",") if item.strip()]
    if not parts:
        raise ValueError("Please enter at least one number")

    numbers = []
    for part in parts:
        numbers.append(int(part))
    return numbers


def rotate_list(lst, k):
    if not lst:
        raise ValueError("List cannot be empty")

    k = k % len(lst)
    return lst[-k:] + lst[:-k] if k else lst[:]


def main():
    while True:
        try:
            raw_list = input("Enter numbers separated by commas: ").strip()
            numbers = parse_numbers(raw_list)

            raw_k = input("Enter rotation value k: ").strip()
            if not raw_k:
                raise ValueError("k cannot be empty")

            k = int(raw_k)
            if k < 0:
                raise ValueError("k must be 0 or greater")

        except ValueError as e:
            print(f"Input error: {e}")
        else:
            rotated = rotate_list(numbers, k)
            print("Rotated list:", rotated)
            break
        finally:
            print("Rotation attempt finished.\n")


if __name__ == "__main__":
    main()