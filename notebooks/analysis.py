#!/usr/bin/env python
# coding: utf-8

# # Week 1 Assessment: HR Employee Analysis
# 
# This notebook explores employee data with NumPy and Pandas, cleans an intentionally imperfect dataset, compares departments, and saves four charts.

# ## Setup and project paths
# 
# The paths below work when the notebook kernel starts either in the project folder or in `notebooks/`.

# In[1]:


from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

PROJECT_ROOT = Path.cwd()
if not (PROJECT_ROOT / "data" / "employees.csv").exists():
    PROJECT_ROOT = PROJECT_ROOT.parent

DATA_DIR = PROJECT_ROOT / "data"
CHARTS_DIR = PROJECT_ROOT / "reports" / "charts"
CHARTS_DIR.mkdir(parents=True, exist_ok=True)

print("Project folder:", PROJECT_ROOT)


# ## 1. NumPy: student marks
# 
# Calculate student and subject averages, add five grace marks by broadcasting, then calculate weighted scores with `np.dot`.

# In[2]:


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

print("Shape:", marks.shape)
print("Student averages:", student_averages)
print("Subject averages:", subject_averages)
print("Marks after 5 grace marks:\n", graced_marks)
print("Weighted scores after grace marks:", weighted_scores)


# ## 2. Load and explore employee data
# 
# Use Pandas `info`, `describe`, label-based and position-based selection, and a salary filter.

# In[3]:


employees = pd.read_csv(DATA_DIR / "employees.csv")

employees.info()
display(employees.describe())

display(employees.loc[0:2, ["name", "salary"]])
display(employees.iloc[0:3, 0:3])
high_salary_employees = employees.loc[employees["salary"] > 50000]
display(high_salary_employees)


# ## 3. Timing a Pandas operation
# 
# Use the notebook `%timeit` magic once to time the mean salary calculation.

# In[4]:


get_ipython().run_line_magic('timeit', 'employees["salary"].mean()')


# ## 4. Clean the employee data
# 
# The provided `employees_with_issues.csv` includes two missing salaries and one duplicate row. Drop duplicates, fill missing salaries with the median, and set numeric column types.

# In[5]:


dirty_employees = pd.read_csv(DATA_DIR / "employees_with_issues.csv")
print("Missing salaries before cleaning:", dirty_employees["salary"].isna().sum())
print("Duplicate rows before cleaning:", dirty_employees.duplicated().sum())

cleaned_employees = dirty_employees.drop_duplicates().copy()
cleaned_employees["id"] = pd.to_numeric(
    cleaned_employees["id"], errors="raise"
).astype("int64")
cleaned_employees["salary"] = pd.to_numeric(
    cleaned_employees["salary"], errors="coerce"
)
median_salary = cleaned_employees["salary"].median()
cleaned_employees["salary"] = cleaned_employees["salary"].fillna(median_salary)
cleaned_employees["salary"] = cleaned_employees["salary"].astype("float64")

print("Median salary used for missing values:", median_salary)
display(cleaned_employees)


# ## 5. Department summary and joins
# 
# Aggregate headcount, average salary, and maximum salary. Compare employees with the department table using inner, left, and outer joins.

# In[6]:


departments = pd.read_csv(DATA_DIR / "departments.csv")
department_order = ["Sales", "HR", "IT", "Finance"]

department_summary = (
    cleaned_employees.groupby("department")
    .agg(
        headcount=("id", "size"),
        average_salary=("salary", "mean"),
        maximum_salary=("salary", "max"),
    )
    .reindex(department_order)
    .reset_index()
)
display(department_summary)

inner_join = pd.merge(
    cleaned_employees, departments, on="department", how="inner"
)
left_join = pd.merge(
    cleaned_employees, departments, on="department", how="left"
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
print("Rows in inner, left, and outer joins:", len(inner_join), len(left_join), len(outer_join))
print("Departments with no employees:", no_employee_departments)
display(outer_join)


# ## 6. Charts
# 
# Create a bar chart, histogram, scatter plot, and line chart. Each chart has a title, axis labels, and a legend; PNG files are saved in `reports/charts/`.

# In[7]:


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
plt.show()

plt.figure(figsize=(8, 5))
plt.hist(
    cleaned_employees["salary"],
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
plt.show()

plt.figure(figsize=(8, 5))
for department in department_order:
    department_data = cleaned_employees.loc[
        cleaned_employees["department"] == department
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
plt.show()

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
plt.show()


# ## 7. Findings
# 
# - IT has the largest headcount, with three employees.
# - Finance has the highest average and maximum salary in this dataset.
# - The two missing salaries are filled with the median after the duplicate row is removed.
# - Legal is listed in the department data but has no employees.

# In[8]:


headcount_output = " | ".join(
    f"{row.department} {int(row.headcount)}"
    for row in department_summary.itertuples(index=False)
)

print("Student averages:", student_averages)
print("Headcount:", headcount_output)
print("Outer join: department with no employees listed")
for department in no_employee_departments:
    print(department)

