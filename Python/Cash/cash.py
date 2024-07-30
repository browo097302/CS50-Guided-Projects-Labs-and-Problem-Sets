from cs50 import get_float


def get_cents():
    while True:
        try:
            cents = get_float("enter amount owed: ")
            if cents < 0.01:
                print("value must be greater than 0")
            else:
                return cents
        except ValueError:
            print("value must be a number")


cents = get_cents()


def calculate_quarter(cents):
    quarters = 0
    while cents >= 0.25:
        cents = cents - 0.25
        quarters += 1
    return quarters


def calculate_dimes(cents):
    dimes = 0
    cents = round(cents - quarters * 0.25,2)
    while cents >= 0.10:
        cents = cents - 0.10
        dimes += 1
    return dimes

def calculate_nickels(cents):
    nickels = 0
    cents = round(cents - quarters * 0.25 - dimes * 0.1, 2)
    while cents >= 0.05:
        cents = cents - 0.05
        nickels += 1
    return nickels

def calculate_pennies(cents):
    pennies = 0
    cents = round(cents - quarters * 0.25 - dimes * 0.1 - nickels * 0.05, 2)
    while cents > 0.00:
        cents = cents - 0.01
        pennies += 1
    return pennies




quarters = calculate_quarter(cents)
dimes = calculate_dimes(cents)
nickels = calculate_nickels(cents)
pennies = calculate_pennies(cents)

total = quarters + dimes + nickels + pennies

print("quarters: " + str(quarters))
print("dimes: " + str(dimes))
print("nickels: " + str(nickels))
print("pennies: " + str(pennies))
print("total: " + str(total))

























