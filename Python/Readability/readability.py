from cs50 import get_string

text = get_string("insert text here: ")

total_letters = 0
for char in text:
    if char.isalpha():
        total_letters = total_letters + 1

spaces = 0
for char in text:
    if char == " ":
        spaces = spaces + 1

sentences = 0
for char in text:
    if char in [".","!","?"]:
        sentences = sentences + 1



total_words = spaces + 1

L = (total_letters) * (100/total_words)
S = sentences * (100/total_words)


grade = (0.0588 * L) - (0.296 * S) - 15.8

rounded_grade = round(grade)

if grade >= 16:
    print("Grade: 16+")
elif grade < 1:
    print("Before Grade 1")
else:
    print(f"Grade {rounded_grade}")




















