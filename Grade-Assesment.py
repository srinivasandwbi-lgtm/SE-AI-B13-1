
# Grade Assessment Program

students = [
    ("Priya", 92),
    ("Arun", 78),
    ("Divya", 59)
]

def calculate_grade(mark):
    if mark >= 90:
        return "A"
    elif mark >= 80:
        return "B"
    elif mark >= 70:
        return "C"
    elif mark >= 60:
        return "D"
    else:
        return "E"

marks = []

print(f"{'Name':<12}{'Mark':<8}{'Grade'}")

for name, mark in students:
    grade = calculate_grade(mark)
    marks.append(mark)
    print(f"{name:<12}{mark:<8}{grade}")

average = sum(marks) / len(marks)
highest = max(marks)
lowest = min(marks)

print(f"Average: {average:.1f}    Highest: {highest}    Lowest: {lowest}")
