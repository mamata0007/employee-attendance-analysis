import pandas as pd
import numpy as np

np.random.seed(42)

employees = [f"EMP{i:03d}" for i in range(1, 51)]

names = [
    "Aarav", "Ananya", "Rahul", "Priya", "Rohan",
    "Sneha", "Vikram", "Neha", "Arjun", "Pooja",
    "Aditya", "Kavya", "Sanjay", "Meera", "Karan",
    "Nisha", "Amit", "Riya", "Suresh", "Isha",
    "Manish", "Simran", "Naveen", "Asha", "Varun",
    "Divya", "Raj", "Shreya", "Akash", "Anjali",
    "Ravi", "Swati", "Mohit", "Payal", "Deepak",
    "Komal", "Nikhil", "Tanya", "Vivek", "Sakshi",
    "Anil", "Mansi", "Rakesh", "Preeti", "Harish",
    "Sonali", "Gaurav", "Tanvi", "Abhishek", "Muskan"
]

departments = [
    "IT",
    "HR",
    "Finance",
    "Sales",
    "Marketing"
]

department = np.random.choice(
    departments,
    size=50,
    p=[0.32, 0.12, 0.16, 0.25, 0.15]
)

dates = pd.bdate_range(
    start="2026-01-01",
    end="2026-06-30"
)

rows = []

for emp_id, name, dept in zip(
    employees, names, department
):

    for date in dates:

        absent_rate = {
            "IT": 0.07,
            "HR": 0.06,
            "Finance": 0.05,
            "Sales": 0.10,
            "Marketing": 0.08
        }[dept]

        # Attendance status
        if np.random.random() < absent_rate:

            status = "Absent"
            work_hours = 0
            late_minutes = 0

        else:

            status = "Present"

            work_hours = round(
                np.clip(
                    np.random.normal(8.1, 0.65),
                    6,
                    10
                ),
                1
            )

            # Late arrival
            late_minutes = int(
                np.random.choice(
                    [0, 5, 10, 15, 20, 30, 45],
                    p=[
                        0.82,
                        0.04,
                        0.04,
                        0.03,
                        0.03,
                        0.02,
                        0.02
                    ]
                )
            )

        rows.append([
            emp_id,
            name,
            dept,
            date.date(),
            status,
            work_hours,
            late_minutes
        ])

# Create DataFrame
df = pd.DataFrame(
    rows,
    columns=[
        "Employee_ID",
        "Employee_Name",
        "Department",
        "Date",
        "Status",
        "Work_Hours",
        "Late_Minutes"
    ]
)

# Save CSV
df.to_csv(
    "employee_attendance.csv",
    index=False
)

print("--------------------------------")
print("Dataset created successfully!")
print("--------------------------------")
print("Total records:", len(df))
print("Total employees:", df["Employee_ID"].nunique())
print("Departments:", df["Department"].nunique())
print("CSV file: employee_attendance.csv")
print()
print(df.head(10))