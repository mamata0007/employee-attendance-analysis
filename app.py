import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="Employee Attendance Dashboard",
    page_icon="📊",
    layout="wide"
)

# =====================================================
# TITLE
# =====================================================

st.title("📊 Employee Attendance Dashboard")
st.write(
    "Interactive dashboard to analyze employee attendance, "
    "working hours and late arrivals."
)

# =====================================================
# LOAD DATA
# =====================================================

file_path = "employee_attendance.csv"

try:
    df = pd.read_csv(file_path)

except FileNotFoundError:
    st.error(
        "❌ employee_attendance.csv not found. "
        "Please keep the CSV file in the same folder as app.py."
    )
    st.stop()

# =====================================================
# DATA CLEANING
# =====================================================

df["Date"] = pd.to_datetime(
    df["Date"],
    errors="coerce"
)

df["Work_Hours"] = pd.to_numeric(
    df["Work_Hours"],
    errors="coerce"
)

df["Late_Minutes"] = pd.to_numeric(
    df["Late_Minutes"],
    errors="coerce"
)

# Remove duplicate rows
df = df.drop_duplicates()

# Remove rows where important values are missing
df = df.dropna(
    subset=[
        "Employee_ID",
        "Employee_Name",
        "Department",
        "Status"
    ]
)

# =====================================================
# SIDEBAR FILTERS
# =====================================================

st.sidebar.header("🔎 Filters")

# -----------------------------------------------------
# Department Filter
# -----------------------------------------------------

departments = ["All"] + sorted(
    df["Department"].unique().tolist()
)

selected_department = st.sidebar.selectbox(
    "Select Department",
    departments
)

# Apply department filter

if selected_department != "All":

    filtered_df = df[
        df["Department"] == selected_department
    ]

else:

    filtered_df = df.copy()

# -----------------------------------------------------
# Employee Filter
# -----------------------------------------------------

employees = ["All"] + sorted(
    filtered_df["Employee_Name"].unique().tolist()
)

selected_employee = st.sidebar.selectbox(
    "Select Employee",
    employees
)

# Apply employee filter

if selected_employee != "All":

    filtered_df = filtered_df[
        filtered_df["Employee_Name"] == selected_employee
    ]

# =====================================================
# KPI CALCULATIONS
# =====================================================

total_employees = filtered_df[
    "Employee_ID"
].nunique()

total_records = len(filtered_df)

# Convert status to lowercase for safe comparison

status_lower = (
    filtered_df["Status"]
    .astype(str)
    .str.strip()
    .str.lower()
)

present_count = (
    status_lower == "present"
).sum()

absent_count = (
    status_lower == "absent"
).sum()

# Attendance rate

if total_records > 0:

    attendance_rate = (
        present_count / total_records
    ) * 100

else:

    attendance_rate = 0

# Average work hours

average_work_hours = (
    filtered_df["Work_Hours"].mean()
)

# Average late minutes

average_late_minutes = (
    filtered_df["Late_Minutes"].mean()
)

# Handle empty values

if pd.isna(average_work_hours):
    average_work_hours = 0

if pd.isna(average_late_minutes):
    average_late_minutes = 0

# =====================================================
# KPI CARDS
# =====================================================

st.subheader("📌 Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "👥 Employees",
        total_employees
    )

with col2:

    st.metric(
        "✅ Present",
        present_count
    )

with col3:

    st.metric(
        "📅 Attendance Rate",
        f"{attendance_rate:.1f}%"
    )

with col4:

    st.metric(
        "⏰ Avg Late Minutes",
        f"{average_late_minutes:.1f}"
    )

# =====================================================
# SECOND KPI ROW
# =====================================================

col5, col6 = st.columns(2)

with col5:

    st.metric(
        "🕐 Average Work Hours",
        f"{average_work_hours:.2f} hrs"
    )

with col6:

    st.metric(
        "❌ Absent",
        absent_count
    )

st.divider()

# =====================================================
# ATTENDANCE STATUS CHART
# =====================================================

st.subheader("📊 Attendance Status")

status_counts = (
    filtered_df["Status"]
    .value_counts()
)

if len(status_counts) > 0:

    fig1, ax1 = plt.subplots()

    ax1.bar(
        status_counts.index,
        status_counts.values
    )

    ax1.set_xlabel("Attendance Status")

    ax1.set_ylabel("Number of Records")

    ax1.set_title(
        "Present vs Absent Employees"
    )

    st.pyplot(fig1)

    plt.close(fig1)

else:

    st.info(
        "No attendance data available."
    )

# =====================================================
# DEPARTMENT ANALYSIS
# =====================================================

st.subheader("🏢 Department-wise Analysis")

department_data = (
    filtered_df
    .groupby("Department")
    .agg(
        Employees=("Employee_ID", "nunique"),
        Avg_Work_Hours=("Work_Hours", "mean"),
        Avg_Late_Minutes=("Late_Minutes", "mean")
    )
    .reset_index()
)

# Round numbers

department_data["Avg_Work_Hours"] = (
    department_data["Avg_Work_Hours"]
    .round(2)
)

department_data["Avg_Late_Minutes"] = (
    department_data["Avg_Late_Minutes"]
    .round(2)
)

st.dataframe(
    department_data,
    use_container_width=True,
    hide_index=True
)

# =====================================================
# WORK HOURS BY DEPARTMENT
# =====================================================

st.subheader(
    "🕐 Average Work Hours by Department"
)

work_hours = (
    filtered_df
    .groupby("Department")["Work_Hours"]
    .mean()
    .sort_values(
        ascending=False
    )
)

if len(work_hours) > 0:

    fig2, ax2 = plt.subplots()

    ax2.bar(
        work_hours.index,
        work_hours.values
    )

    ax2.set_xlabel(
        "Department"
    )

    ax2.set_ylabel(
        "Average Work Hours"
    )

    ax2.set_title(
        "Average Work Hours by Department"
    )

    plt.xticks(
        rotation=45
    )

    plt.tight_layout()

    st.pyplot(fig2)

    plt.close(fig2)

else:

    st.info(
        "No work-hour data available."
    )

# =====================================================
# LATE MINUTES BY DEPARTMENT
# =====================================================

st.subheader(
    "⏰ Average Late Minutes by Department"
)

late_data = (
    filtered_df
    .groupby("Department")["Late_Minutes"]
    .mean()
    .sort_values(
        ascending=False
    )
)

if len(late_data) > 0:

    fig3, ax3 = plt.subplots()

    ax3.bar(
        late_data.index,
        late_data.values
    )

    ax3.set_xlabel(
        "Department"
    )

    ax3.set_ylabel(
        "Average Late Minutes"
    )

    ax3.set_title(
        "Average Late Minutes by Department"
    )

    plt.xticks(
        rotation=45
    )

    plt.tight_layout()

    st.pyplot(fig3)

    plt.close(fig3)

else:

    st.info(
        "No late-minute data available."
    )

# =====================================================
# ATTENDANCE DATA TABLE
# =====================================================

st.subheader("📋 Attendance Data")

st.dataframe(
    filtered_df,
    use_container_width=True,
    hide_index=True
)

# =====================================================
# DOWNLOAD BUTTON
# =====================================================

st.subheader("⬇️ Download Data")

csv_data = filtered_df.to_csv(
    index=False
)

st.download_button(
    label="Download Filtered CSV",
    data=csv_data,
    file_name="filtered_attendance.csv",
    mime="text/csv"
)

# =====================================================
# PROJECT INSIGHTS
# =====================================================

st.divider()

st.subheader("💡 Quick Insights")

if len(filtered_df) > 0:

    st.write(
        f"• Total employees: **{total_employees}**"
    )

    st.write(
        f"• Attendance rate: **{attendance_rate:.1f}%**"
    )

    st.write(
        f"• Average work hours: "
        f"**{average_work_hours:.2f} hours**"
    )

    st.write(
        f"• Average late minutes: "
        f"**{average_late_minutes:.1f} minutes**"
    )

else:

    st.info(
        "No data available for the selected filters."
    )

# =====================================================
# FOOTER
# =====================================================

st.divider()

st.caption(
    "Employee Attendance Analytics Dashboard | "
    "Python • Pandas • Streamlit"
)