"""
ip_project.py — Meridian Hospital Management System
CBSE Class 12 Informatics Practices (065) — Data Handling Project

Topics demonstrated (all from the 065 syllabus):
  1. Pandas Series
  2. Pandas DataFrame
  3. Importing and Exporting CSV files (read_csv / to_csv)
  4. Data Visualization with Matplotlib (line, bar, histogram)
  
"""

import pandas as pd
import matplotlib.pyplot as plt


# ======================================================================
#  1. PANDAS SERIES
# ======================================================================
print("=" * 55)
print("1. PANDAS SERIES")
print("=" * 55) 

# Creating a Series from a list
marks = pd.Series([120, 90, 75, 150, 60],
                  index=["Cardiology", "Neurology", "Ortho", "ENT", "Skin"])
print("\nConsultation fees Series:")
print(marks)

# Series attributes and functions
print("\nhead(3):")
print(marks.head(3))
print("\ntail(2):")
print(marks.tail(2))

print("\nMean :", marks.mean())
print("Max  :", marks.max())
print("Min  :", marks.min())
print("Sum  :", marks.sum())


# ======================================================================
#  2. IMPORTING CSV FILES (read_csv)
# ======================================================================
print("\n" + "=" * 55)
print("2. READING CSV FILES INTO DATAFRAMES")
print("=" * 55)

patients = pd.read_csv("../static/csv/patients.csv")
doctors = pd.read_csv("../static/csv/doctors.csv")
appointments = pd.read_csv("../static/csv/appointments.csv")
bills = pd.read_csv("../static/csv/bills.csv")

print("\nPatients loaded:", len(patients), "rows")
print("Doctors loaded :", len(doctors), "rows")


# ======================================================================
#  3. PANDAS DATAFRAME OPERATIONS
# ======================================================================
print("\n" + "=" * 55)
print("3. DATAFRAME OPERATIONS")
print("=" * 55)

# head()
print("\nPatients head(5):")
print(patients.head())

# shape and columns
print("\nShape (rows, columns):", patients.shape)
print("Columns:", list(patients.columns))

# describe() — statistics on numeric columns
print("\nBills describe():")
print(bills["total_amount"].describe())

# Boolean indexing (filtering)
print("\nAdmitted patients only:")
admitted = patients[patients["admission_status"] == "Admitted"]
print(admitted[["first_name", "last_name", "ward"]].head())

# Sorting
print("\nDoctors sorted by consultation fee (highest first):")
top = doctors.sort_values("consultation_fee", ascending=False)
print(top[["first_name", "last_name", "consultation_fee"]].head())

# Grouping and aggregation
print("\nTotal revenue by payment status:")
print(bills.groupby("payment_status")["total_amount"].sum())


# ======================================================================
#  4. EXPORTING CSV FILE (to_csv)
# ======================================================================
print("\n" + "=" * 55)
print("4. EXPORTING A DATAFRAME TO CSV")
print("=" * 55)

admitted.to_csv("admitted_patients.csv", index=False)
print("\nSaved admitted_patients.csv (", len(admitted), "rows )")


# ======================================================================
#  5. DATA VISUALIZATION — MATPLOTLIB
# ======================================================================
print("\n" + "=" * 55)
print("5. GRAPHS (close each window to see the next)")
print("=" * 55)

# ---- Graph 1: LINE CHART — appointments per date ----
appt_count = appointments.groupby("appointment_date").size()
plt.plot(appt_count.index, appt_count.values, color="teal",
         marker="o", label="Appointments")
plt.title("Appointments Over Time")
plt.xlabel("Date")
plt.ylabel("Number of Appointments")
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.savefig("graph_line.png")
plt.show()

# ---- Graph 2: BAR CHART — doctors per department ----
dept_count = doctors["department"].value_counts()
plt.bar(dept_count.index, dept_count.values, color="orange", label="Doctors")
plt.title("Number of Doctors per Department")
plt.xlabel("Department")
plt.ylabel("Count")
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.savefig("graph_bar.png")
plt.show()

# ---- Graph 3: HISTOGRAM — distribution of bill amounts ----
plt.hist(bills["total_amount"], bins=8, color="green",
         edgecolor="black", label="Bills")
plt.title("Distribution of Bill Amounts")
plt.xlabel("Total Bill Amount")
plt.ylabel("Frequency")
plt.legend()
plt.tight_layout()
plt.savefig("graph_histogram.png")
plt.show()

print("\nDone! 3 graphs saved as PNG files.")
