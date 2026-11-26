import csv
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
employees = []

# Convert CSV values to numeric types for salary calculations.
with open(DATA_DIR / "employees.csv", "r", newline="") as file:
    reader = csv.DictReader(file)

    for row in reader:
        row["id"] = int(row["id"])
        row["salary"] = float(row["salary"])
        employees.append(row)

# Add extras to the percentage bonus, then apply an optional cap.
def bonus(salary, rate=0.1, *extras, **options):

    total_bonus = salary * rate + sum(extras)

    if "cap" in options:
        total_bonus = min(total_bonus, options["cap"])

    return total_bonus

# Raise this custom error when an employee salary is negative.
class InvalidSalaryError(Exception):
    pass

class Employee:

    def __init__(self, name, salary):

        if salary < 0:
            raise InvalidSalaryError(f"Invalid salary: {salary}")

        self.name = name
        self.salary = salary

    def annual_salary(self):
        return self.salary * 12

    def get_details(self):
        return f"Employee: {self.name}, Salary: {self.salary}"

# Extend employee details with the manager's team size.
class Manager(Employee):

    def __init__(self, name, salary, team_size):
        super().__init__(name, salary)
        self.team_size = team_size

    def get_details(self):
        return (
            f"Manager: {self.name}, "
            f"Salary: {self.salary}, "
            f"Team Size: {self.team_size}"
        )

bonus(50000)
bonus(50000, 0.1, 1000, 2000)
bonus(50000, 0.1, 1000, 2000, cap=6000)

emp = Employee("Arun", 30000)
emp.annual_salary()
emp.get_details()

manager = Manager("Priya", 80000, 5)
manager.annual_salary()
manager.get_details()

# Build the required salary and city selections.
above_50000 = [
    emp["name"]
    for emp in employees
    if emp["salary"] > 50000
]

increased_salaries = list(
    map(
        lambda emp: emp["salary"] * 1.10,
        employees
    )
)

chennai_employees = list(
    filter(
        lambda emp: emp["city"] == "Chennai",
        employees
    )
)

chennai_names = [
    emp["name"] for emp in chennai_employees
]

# Skip zero salaries and stop at the first salary above 85,000.
for emp in employees:

    salary = emp["salary"]

    if salary == 0:
        continue

    if salary > 85000:
        break

print("Above 50000:", above_50000)
print("Chennai:", chennai_names)

# Demonstrate salary validation and always report completion.
try:
    invalid_employee = Employee("Test", -500)

except InvalidSalaryError as e:
    print("Error:", e)

finally:
    print("Transaction finished")
