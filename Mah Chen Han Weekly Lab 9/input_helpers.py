"""Lab 9 Section 5.1: input helpers that keep asking until the input is valid."""


def get_positive_float(prompt: str) -> float:
    """Asks until the user enters a number greater than zero."""
    while True:
        try:
            value = float(input(prompt))
            if value <= 0:                       # validation
                print("Please enter a number greater than zero.")
                continue
            return value
        except ValueError:                       # exception handling
            print("Please enter a valid number, e.g. 12.50")


def get_non_negative_int(prompt: str) -> int:
    """Asks until the user enters a whole number that is zero or more."""
    while True:
        try:
            value = int(input(prompt))
            if value < 0:                        # validation
                print("Please enter a whole number of zero or more.")
                continue
            return value
        except ValueError:                       # exception handling
            print("Please enter a whole number, e.g. 10")
