import csv
import json
import os
from pathlib import Path

import requests

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
REPORTS_DIR = PROJECT_ROOT / "reports"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

# Read local credentials without hardcoding them in the script.
load_dotenv(PROJECT_ROOT / ".env")

API_KEY = os.getenv("API_KEY")

employees = []

# Load employee records and convert numeric fields.
with open(DATA_DIR / "employees.csv", "r", newline="") as file:

    reader = csv.DictReader(file)

    for row in reader:
        row["id"] = int(row["id"])
        row["salary"] = float(row["salary"])

        employees.append(row)

# Export all records to JSON and high earners to CSV.
with open(REPORTS_DIR / "employees.json", "w") as file:

    json.dump(employees, file, indent=4)

high_earners = [
    emp for emp in employees
    if emp["salary"] > 50000
]

with open(REPORTS_DIR / "high_earners.csv", "w", newline="") as file:

    fieldnames = [
        "id", "name", "department", "salary", "city"
    ]

    writer = csv.DictWriter(
        file,
        fieldnames=fieldnames
    )

    writer.writeheader()
    writer.writerows(high_earners)

print(f"Rows read: {len(employees)} | High earners: {len(high_earners)}")

# Fetch users with a timeout and handle request failures.
url = "https://jsonplaceholder.typicode.com/users"

try:

    response = requests.get(url, timeout=5)

    response.raise_for_status()

    users = response.json()

    for user in users[:1]:

        print(
            user["id"],
            "-",
            user["name"],
            "-",
            user["email"]
        )

except requests.exceptions.Timeout:
    print("Error: API request timed out")

except requests.exceptions.ConnectionError:
    print("Error: Unable to connect to API")

except requests.exceptions.HTTPError as e:
    print("HTTP Error:", e)

# Verify the missing-user endpoint returns a 404.
try:

    response = requests.get(
        "https://jsonplaceholder.typicode.com/users/9999",
        timeout=5
    )

    if response.status_code == 404:
        print("/users/9999 -> 404 Not found")

    else:
        response.raise_for_status()

except requests.exceptions.Timeout:
    print("Error: Request timed out")

except requests.exceptions.ConnectionError:
    print("Error: Connection failed")

except requests.exceptions.HTTPError as e:
    print("HTTP Error:", e)

# Extract optional nested company fields and save the selected data.
try:
    response = requests.get(url, timeout=5)

    response.raise_for_status()

    users = response.json()

    parsed_users = []

    for user in users:
        company = user.get("company", {})
        user_data = {
            "id": user.get("id"),
            "name": user.get("name"),
            "email": user.get("email"),
            "company_name": company.get("name"),
            "company_bs": company.get("bs")
        }

        parsed_users.append(user_data)

    with open(REPORTS_DIR / "users.json", "w") as file:

        json.dump(
            parsed_users,
            file,
            indent=4
        )

except requests.exceptions.Timeout:
    print("Error: API request timed out")

except requests.exceptions.ConnectionError:
    print("Error: Unable to connect to API")

except requests.exceptions.HTTPError as e:
    print("HTTP Error:", e)
