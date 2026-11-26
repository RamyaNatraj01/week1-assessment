from io import StringIO
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
REPORTS_DIR = PROJECT_ROOT / "reports"
CHARTS_DIR = REPORTS_DIR / "charts"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

# Calculate averages, add grace marks by broadcasting, and apply weights.
marks = np.array(
    [
        [85, 90, 80],
        [75, 80, 85],
        [90, 95, 92],
        [60, 70, 65],
    ]
)
student_averages = marks.mean(axis=1)
subject_averages = marks.mean(axis=0)
graced_marks = marks + 5
weights = np.array([0.3, 0.3, 0.4])
weighted_scores = np.dot(graced_marks, weights)

# Explore the source data and demonstrate Pandas selection and filtering.
employees = pd.read_csv(DATA_DIR / "employees.csv")
employees.info(buf=StringIO())
employee_description = employees.describe()
loc_preview = employees.loc[0:2, ["name", "salary"]]
iloc_preview = employees.iloc[0:3, 0:3]
high_salary_employees = employees.loc[employees["salary"] > 50000]

# Create a cleaning example with two missing salaries and one duplicate.
dirty_employees = employees.copy()
dirty_employees.loc[dirty_employees["id"].isin([1, 2]), "salary"] = np.nan

duplicate_row = dirty_employees.loc[dirty_employees["id"] == 7]
dirty_employees = pd.concat(
    [dirty_employees, duplicate_row],
    ignore_index=True,
)
dirty_file = DATA_DIR / "employees_with_issues.csv"
dirty_employees.to_csv(dirty_file, index=False)

dirty_employees = pd.read_csv(dirty_file)

# Remove duplicates before using the remaining salaries to calculate the median.
dirty_employees = dirty_employees.drop_duplicates().copy()
dirty_employees["id"] = pd.to_numeric(
    dirty_employees["id"], errors="raise"
).astype("int64")
dirty_employees["salary"] = pd.to_numeric(
    dirty_employees["salary"], errors="coerce"
)

median_salary = dirty_employees["salary"].median()
dirty_employees["salary"] = dirty_employees["salary"].fillna(median_salary)
dirty_employees["salary"] = dirty_employees["salary"].astype("float64")

cleaned_file = REPORTS_DIR / "cleaned_employees.csv"
dirty_employees.to_csv(cleaned_file, index=False)

# Include Legal to show how the outer join identifies an unstaffed department.
departments = pd.DataFrame(
    {
        "department": ["Sales", "HR", "IT", "Finance", "Legal"],
        "head": [
            "Sales Head",
            "HR Head",
            "IT Head",
            "Finance Head",
            "Legal Head",
        ],
        "budget": [1000000, 500000, 2500000, 1500000, 400000],
    }
)
departments_file = DATA_DIR / "departments.csv"
departments.to_csv(departments_file, index=False)
departments = pd.read_csv(departments_file)

# Summarize cleaned headcount and salaries in the assessment's expected order.
department_order = ["Sales", "HR", "IT", "Finance"]

department_summary = (
    dirty_employees.groupby("department")
    .agg(
        headcount=("id", "size"),
        average_salary=("salary", "mean"),
        maximum_salary=("salary", "max"),
    )
    .reindex(department_order)
    .reset_index()
)

inner_join = pd.merge(
    dirty_employees, departments, on="department", how="inner"
)
left_join = pd.merge(
    dirty_employees, departments, on="department", how="left"
)
outer_join = pd.merge(
    department_summary,
    departments,
    on="department",
    how="outer",
    indicator=True,
)

no_employee_departments = outer_join.loc[
    outer_join["_merge"] == "right_only", "department"
].tolist()

# Save each requested chart as a PNG.
CHARTS_DIR.mkdir(parents=True, exist_ok=True)

# Bar chart: employee headcount by department.
plt.figure(figsize=(8, 5))
plt.bar(
    department_summary["department"],
    department_summary["headcount"],
    color="skyblue",
    label="Headcount",
)
plt.title("Employee Headcount by Department")
plt.xlabel("Department")
plt.ylabel("Number of employees")
plt.legend()
plt.tight_layout()
plt.savefig(CHARTS_DIR / "department_headcount.png", dpi=150)
plt.close()

# Histogram: distribution of cleaned employee salaries.
plt.figure(figsize=(8, 5))
plt.hist(
    dirty_employees["salary"],
    bins=5,
    color="orange",
    edgecolor="black",
    label="Employees",
)
plt.title("Employee Salary Distribution")
plt.xlabel("Salary")
plt.ylabel("Number of employees")
plt.legend()
plt.tight_layout()
plt.savefig(CHARTS_DIR / "salary_distribution.png", dpi=150)
plt.close()

# Scatter plot: salary by employee ID, grouped by department.
plt.figure(figsize=(8, 5))
for department in department_order:
    department_data = dirty_employees.loc[
        dirty_employees["department"] == department
    ]
    plt.scatter(
        department_data["id"],
        department_data["salary"],
        label=department,
    )

plt.title("Salary by Employee ID and Department")
plt.xlabel("Employee ID")
plt.ylabel("Salary")
plt.legend(title="Department")
plt.tight_layout()
plt.savefig(CHARTS_DIR / "salary_vs_id.png", dpi=150)
plt.close()

# Line chart: average salary by department.
plt.figure(figsize=(8, 5))
plt.plot(
    department_summary["department"],
    department_summary["average_salary"],
    marker="o",
    color="green",
    label="Average salary",
)
plt.title("Average Salary by Department")
plt.xlabel("Department")
plt.ylabel("Average salary")
plt.legend()
plt.tight_layout()
plt.savefig(CHARTS_DIR / "average_salary_by_department.png", dpi=150)
plt.close()

highest_headcount = department_summary.loc[
    department_summary["headcount"].idxmax(), "department"
]
highest_salary_row = dirty_employees.loc[dirty_employees["salary"].idxmax()]
highest_average_row = department_summary.loc[
    department_summary["average_salary"].idxmax()
]

# Format the assessment summary with departments in the required order.
headcount_output = " | ".join(
    f"{row.department} {int(row.headcount)}"
    for row in department_summary.itertuples(index=False)
)

print("Student averages:", student_averages)
print("Headcount:", headcount_output)
print("Outer join: department with no employees listed")





