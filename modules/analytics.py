"""
CBSE Class 12 Project

analytics.py — Hospital Management System Analytics Dashboard

PANDAS: Series, DataFrame, head(), tail(), describe(), shape,
        groupby(), sort_values(), value_counts(), to_csv(), read_csv()

MATPLOTLIB: plt.plot(), plt.bar(), plt.barh(), plt.hist(),
            plt.pie(), plt.scatter(), plt.title(), plt.xlabel(),
            plt.ylabel(), plt.legend(), plt.savefig()

SQL: COUNT(), SUM(), GROUP BY, ORDER BY, JOIN
"""

import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from flask import Blueprint, render_template
from db import query

analytics_bp = Blueprint("analytics", __name__, url_prefix="/analytics")

CHART_DIR = "static/charts"
CSV_DIR = "static/csv"
os.makedirs(CHART_DIR, exist_ok=True)
os.makedirs(CSV_DIR, exist_ok=True)

TEAL = "#0F6B64"
AMBER = "#E8A33D"
CORAL = "#E1604F"
SLATE = "#334155"
GRID = "#DCEAE7"
CHART_COLORS = [TEAL, AMBER, CORAL, "#4E9E8F", "#C98A2C", "#8FB8B3"]

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["DejaVu Sans"],
    "axes.edgecolor": GRID,
    "axes.labelcolor": SLATE,
    "text.color": SLATE,
    "xtick.color": SLATE,
    "ytick.color": SLATE,
    "figure.facecolor": "white",
    "axes.facecolor": "white",
    "savefig.facecolor": "white",
})

# Dark-mode chart styling (matches [data-theme="dark"] surface)
DARK_RCPARAMS = {
    "axes.edgecolor": "#3A554F",
    "axes.labelcolor": "#CFE0DC",
    "text.color": "#CFE0DC",
    "xtick.color": "#CFE0DC",
    "ytick.color": "#CFE0DC",
    "figure.facecolor": "#0E1B1A",
    "axes.facecolor": "#0E1B1A",
    "savefig.facecolor": "#0E1B1A",
}


def _style_dark():
    """Restyle the already-drawn figure/axes objects for dark mode.
    rcParams alone won't restyle existing artists, so set properties
    directly on the figure and each axes (fixes the white border bug)."""
    fig = plt.gcf()
    fig.patch.set_facecolor("#0E1B1A")
    for ax in fig.get_axes():
        ax.set_facecolor("#0E1B1A")
        ax.tick_params(colors="#CFE0DC")
        for spine in ax.spines.values():
            spine.set_edgecolor("#3A554F")
        if ax.xaxis.get_label():
            ax.xaxis.get_label().set_color("#CFE0DC")
        if ax.yaxis.get_label():
            ax.yaxis.get_label().set_color("#CFE0DC")
        for txt in ax.get_xticklabels() + ax.get_yticklabels():
            txt.set_color("#CFE0DC")
        leg = ax.get_legend()
        if leg:
            for text in leg.get_texts():
                text.set_color("#CFE0DC")
        for child in ax.get_children():
            if isinstance(child, plt.Text) and child.get_text():
                child.set_color("#CFE0DC")
    return fig


def _save(filename, dark=False):
    plt.tight_layout()
    if dark:
        _style_dark()
        save_name = filename.replace(".png", "_dark.png")
    else:
        fig = plt.gcf()
        fig.patch.set_facecolor("white")
        for ax in fig.get_axes():
            ax.set_facecolor("white")
        save_name = filename
    plt.savefig(CHART_DIR + "/" + save_name, dpi=150, bbox_inches="tight",
                facecolor=plt.gcf().get_facecolor())
    plt.close()


# ══════════════════════════════════════════════════════════════════
#  SECTION 1: PANDAS — Series Operations
#  Concept: Series creation, head(), tail(), mathematical ops
# ══════════════════════════════════════════════════════════════════

print("=" * 60)
print("SECTION 1: PANDAS — Series Operations")
print("=" * 60)


def _safe_query(sql, params=None, one=False):
    """Wrapper so a boot-time DB outage doesn't crash app import."""
    try:
        return query(sql, params, one)
    except Exception as _e:
        print(f"[analytics] DB unavailable at import: {_e}")
        return None if one else []


doctors_data = _safe_query("SELECT first_name, last_name, consultation_fee FROM doctors")

# Series creation from dictionary
fee_dict = {}
for row in doctors_data:
    fee_dict[f"Dr. {row['first_name']} {row['last_name']}"] = float(row["consultation_fee"])

fee_series = pd.Series(fee_dict, name="Consultation Fee (₹)", dtype=float)

# head(), tail()
print("\nSeries head(5):")
print(fee_series.head(5))
print("\nSeries tail(3):")
print(fee_series.tail(3))

# Mathematical operations on Series
print(f"\nMean:   ₹{fee_series.mean():.2f}")
print(f"Max:    ₹{fee_series.max():.2f}")
print(f"Min:    ₹{fee_series.min():.2f}")
print(f"Sum:    ₹{fee_series.sum():.2f}")
print(f"Std:    ₹{fee_series.std():.2f}")


# ══════════════════════════════════════════════════════════════════
#  SECTION 2: PANDAS — DataFrame Operations
#  Concept: DataFrame from SQL, head(), tail(), describe(),
#                shape, value_counts(), groupby(), sort_values(),
#                boolean filtering
# ══════════════════════════════════════════════════════════════════

print("\n" + "=" * 60)
print("SECTION 2: PANDAS — DataFrame Operations")
print("=" * 60)

# DataFrame creation from SQL query (list of dicts)
patients_df = pd.DataFrame(
    _safe_query("SELECT patient_id, first_name, last_name, gender, blood_group, "
                "admission_status, ward FROM patients")
)
doctors_df = pd.DataFrame(
    _safe_query("SELECT doctor_id, first_name, last_name, specialization, "
                "department, consultation_fee, status FROM doctors")
)
appointments_df = pd.DataFrame(
    _safe_query("SELECT appointment_id, appointment_date, appointment_time, "
                "status, patient_id, doctor_id FROM appointments")
)
bills_df = pd.DataFrame(
    _safe_query("SELECT bill_id, patient_id, bill_date, consultation_fee, "
                "medicine_charges, room_charges, other_charges, total_amount, "
                "payment_status, payment_method FROM bills")
)

# Convert decimal columns to float
for col in ["consultation_fee", "medicine_charges", "room_charges",
            "other_charges", "total_amount"]:
    if col in bills_df.columns:
        bills_df[col] = pd.to_numeric(bills_df[col], errors="coerce").fillna(0.0)

try:
    # head(), shape
    print("\nPatients DataFrame head(3):")
    print(patients_df.head(3))
    print(f"\nShape: {patients_df.shape}  (rows, columns)")

    # describe()
    print("\nBills DataFrame describe():")
    print(bills_df[["consultation_fee", "total_amount"]].describe().round(2))

    # value_counts()
    print("\nPayment Status value_counts():")
    print(bills_df["payment_status"].value_counts())

    # groupby() with aggregate
    print("\nBills groupby('payment_status').sum() (total_amount):")
    print(bills_df.groupby("payment_status")["total_amount"].sum().round(2))

    # sort_values()
    print("\nDoctors sorted by consultation_fee (descending):")
    print(doctors_df[["first_name", "last_name", "consultation_fee"]]
          .sort_values("consultation_fee", ascending=False).head(5))

    # Boolean indexing (filtering)
    print("\nPatients with admission_status == 'Admitted':")
    print(patients_df[patients_df["admission_status"] == "Admitted"]
          [["first_name", "last_name", "ward"]])
except Exception as _e:
    print(f"[analytics] summary prints skipped: {_e}")


# ══════════════════════════════════════════════════════════════════
#  SECTION 3: MATPLOTLIB — Graphs (one by one)
#  Concept: Line, Bar, Histogram, Pie, Scatter
# ══════════════════════════════════════════════════════════════════

print("\n" + "=" * 60)
print("SECTION 3: MATPLOTLIB — Generating 9 Charts")
print("=" * 60)


# ── Graph 1: Line Plot ───────────────────────────────────────────
# plt.plot() — shows trend over time
def build_appointments_trend():
    print("\n[1/9] Line Plot — plt.plot() — Appointments Trend")

    appt_by_date = appointments_df.groupby("appointment_date").size()
    appt_by_date = appt_by_date.reset_index(name="count")
    appt_by_date = appt_by_date.sort_values("appointment_date")

    plt.figure(figsize=(7, 3.2))

    if not appt_by_date.empty:
        dates = pd.to_datetime(appt_by_date["appointment_date"])
        counts = appt_by_date["count"]
        plt.plot(dates, counts, color=TEAL, linewidth=2.5,
                 marker="o", markersize=5, label="Daily Appointments")
        plt.fill_between(dates, counts, color=TEAL, alpha=0.08)
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
        plt.xticks(rotation=30)
        plt.xlabel("Date", fontsize=10)
        plt.ylabel("Number of Appointments", fontsize=10)
        plt.legend(loc="upper left", fontsize=9)
    else:
        plt.text(0.5, 0.5, "No appointment data yet",
                 ha="center", va="center", color=SLATE)

    plt.title("Appointments — Last 30 Days", fontsize=12,
              fontweight="bold", loc="left")
    plt.grid(axis="y", color=GRID, linewidth=0.8)
    plt.gca().spines[["top", "right"]].set_visible(False)
    _save("appointments_trend.png", dark=False)
    _save("appointments_trend.png", dark=True)


# ── Graph 2: Bar Graph ───────────────────────────────────────────
# plt.bar() — compares categories
def build_department_load():
    print("[2/9] Bar Graph — plt.bar() — Department Workload")

    merged = pd.merge(appointments_df, doctors_df, on="doctor_id", how="inner")
    dept_counts = merged.groupby("department").size().reset_index(name="total")
    dept_counts = dept_counts.sort_values("total", ascending=False)

    plt.figure(figsize=(7, 3.2))

    if not dept_counts.empty:
        bars = plt.bar(dept_counts["department"], dept_counts["total"],
                       color=CHART_COLORS[:len(dept_counts)])
        plt.bar_label(bars, padding=3, fontsize=9)
        plt.xlabel("Department", fontsize=10)
        plt.ylabel("Number of Appointments", fontsize=10)
        plt.legend(bars, dept_counts["department"], loc="upper right", fontsize=8)
    else:
        plt.text(0.5, 0.5, "No department data yet",
                 ha="center", va="center", color=SLATE)

    plt.title("Appointment Load by Department", fontsize=12,
              fontweight="bold", loc="left")
    plt.grid(axis="y", color=GRID, linewidth=0.8)
    plt.gca().spines[["top", "right"]].set_visible(False)
    plt.xticks(rotation=20, ha="right")
    _save("department_load.png", dark=False)
    _save("department_load.png", dark=True)


# ── Graph 3: Bar Graph ───────────────────────────────────────────
# plt.bar() — revenue per month
def build_revenue_by_month():
    print("[3/9] Bar Graph — plt.bar() — Revenue by Month")

    bills_copy = bills_df.copy()
    bills_copy["bill_date"] = pd.to_datetime(bills_copy["bill_date"])
    bills_copy["month"] = bills_copy["bill_date"].dt.to_period("M").astype(str)
    revenue = bills_copy.groupby("month")["total_amount"].sum().reset_index()
    revenue = revenue.sort_values("month")

    plt.figure(figsize=(7, 3.2))

    if not revenue.empty:
        bars = plt.bar(revenue["month"], revenue["total_amount"].astype(float),
                       color=AMBER)
        plt.bar_label(bars, fmt="₹%.0f", padding=3, fontsize=9)
        plt.xlabel("Month", fontsize=10)
        plt.ylabel("Revenue (₹)", fontsize=10)
    else:
        plt.text(0.5, 0.5, "No billing data yet",
                 ha="center", va="center", color=SLATE)

    plt.title("Revenue by Month", fontsize=12, fontweight="bold", loc="left")
    plt.grid(axis="y", color=GRID, linewidth=0.8)
    plt.gca().spines[["top", "right"]].set_visible(False)
    _save("revenue_by_month.png", dark=False)
    _save("revenue_by_month.png", dark=True)


# ── Graph 4: Pie Chart ───────────────────────────────────────────
# plt.pie() — shows percentage distribution
def build_payment_status():
    print("[4/9] Pie Chart — plt.pie() — Payment Status")

    status_counts = bills_df["payment_status"].value_counts()

    plt.figure(figsize=(4.5, 3.5))

    if not status_counts.empty:
        colors = {"Paid": TEAL, "Pending": CORAL, "Partially Paid": AMBER}
        wedge_colors = [colors.get(s, SLATE) for s in status_counts.index]
        wedges, texts, autotexts = plt.pie(
            status_counts.values,
            labels=status_counts.index,
            autopct="%1.0f%%",
            colors=wedge_colors,
            startangle=90,
            wedgeprops={"width": 0.42, "edgecolor": "white"},
            textprops={"fontsize": 9},
        )
        plt.legend(wedges, status_counts.index, loc="lower center",
                   bbox_to_anchor=(0.5, -0.15), fontsize=9)
    else:
        plt.text(0.5, 0.5, "No billing data yet",
                 ha="center", va="center", color=SLATE)

    plt.title("Payment Status Distribution", fontsize=12,
              fontweight="bold", loc="left")
    _save("payment_status.png", dark=False)
    _save("payment_status.png", dark=True)


# ── Graph 5: Horizontal Bar ──────────────────────────────────────
# plt.barh() — horizontal comparison
def build_patient_admission_mix():
    print("[5/9] Horizontal Bar — plt.barh() — Patient Admission")

    status_counts = patients_df["admission_status"].value_counts()

    plt.figure(figsize=(5, 3.2))

    if not status_counts.empty:
        colors = [TEAL, AMBER, CORAL][:len(status_counts)]
        bars = plt.barh(status_counts.index, status_counts.values, color=colors)
        plt.bar_label(bars, padding=3, fontsize=9)
        plt.xlabel("Number of Patients", fontsize=10)
        plt.ylabel("Admission Status", fontsize=10)
        plt.legend(bars, status_counts.index, loc="lower right", fontsize=9)
    else:
        plt.text(0.5, 0.5, "No patient data yet",
                 ha="center", va="center", color=SLATE)

    plt.title("Patients by Admission Status", fontsize=12,
              fontweight="bold", loc="left")
    plt.grid(axis="x", color=GRID, linewidth=0.8)
    plt.gca().spines[["top", "right"]].set_visible(False)
    _save("patient_admission_mix.png", dark=False)
    _save("patient_admission_mix.png", dark=True)


# ── Graph 6: Histogram ───────────────────────────────────────────
# plt.hist() — shows frequency distribution
def build_bill_amount_histogram():
    print("[6/9] Histogram — plt.hist() — Bill Amount Distribution")

    plt.figure(figsize=(6, 3.5))

    if not bills_df.empty and bills_df["total_amount"].notna().any():
        amounts = bills_df["total_amount"].dropna().astype(float)
        n, bins, patches = plt.hist(amounts, bins=8, color=TEAL,
                                     edgecolor="white", alpha=0.85)
        for i, patch in enumerate(patches):
            patch.set_facecolor(CHART_COLORS[i % len(CHART_COLORS)])
        plt.xlabel("Total Bill Amount (₹)", fontsize=10)
        plt.ylabel("Frequency", fontsize=10)
    else:
        plt.text(0.5, 0.5, "No billing data yet",
                 ha="center", va="center", color=SLATE)

    plt.title("Distribution of Bill Amounts", fontsize=12,
              fontweight="bold", loc="left")
    plt.grid(axis="y", color=GRID, linewidth=0.8)
    plt.gca().spines[["top", "right"]].set_visible(False)
    _save("bill_histogram.png", dark=False)
    _save("bill_histogram.png", dark=True)


# ── Graph 7: Scatter Plot ────────────────────────────────────────
# plt.scatter() — shows relationship between two variables
def build_fee_vs_total_scatter():
    print("[7/9] Scatter Plot — plt.scatter() — Fee vs Total Bill")

    plt.figure(figsize=(6, 3.5))

    if not bills_df.empty and bills_df["consultation_fee"].notna().any():
        fees = bills_df["consultation_fee"].astype(float)
        totals = bills_df["total_amount"].astype(float)
        plt.scatter(fees, totals, c=TEAL, s=60, alpha=0.7,
                    edgecolors="white", linewidths=0.8, label="Bills")
        if len(fees) > 1:
            z = np.polyfit(fees, totals, 1)
            p = np.poly1d(z)
            margin = (fees.max() - fees.min()) * 0.1 if fees.max() != fees.min() else 100
            x_line = np.linspace(fees.min() - margin, fees.max() + margin, 100)
            y_line = np.clip(p(x_line), 0, None)
            plt.plot(x_line, y_line, "--", color=CORAL, linewidth=1.5,
                     alpha=0.7, label="Trend Line")
        plt.xlabel("Consultation Fee (₹)", fontsize=10)
        plt.ylabel("Total Bill Amount (₹)", fontsize=10)
        plt.legend(loc="upper left", fontsize=9)
    else:
        plt.text(0.5, 0.5, "No data for scatter plot",
                 ha="center", va="center", color=SLATE)

    plt.title("Consultation Fee vs Total Bill", fontsize=12,
              fontweight="bold", loc="left")
    plt.grid(color=GRID, linewidth=0.8)
    plt.gca().spines[["top", "right"]].set_visible(False)
    _save("fee_vs_total_scatter.png", dark=False)
    _save("fee_vs_total_scatter.png", dark=True)


# ── Graph 8: Pie Chart ───────────────────────────────────────────
# plt.pie() — gender distribution
def build_gender_pie():
    print("[8/9] Pie Chart — plt.pie() — Gender Distribution")

    gender_counts = patients_df["gender"].value_counts()

    plt.figure(figsize=(4.5, 3.5))

    if not gender_counts.empty:
        colors = [TEAL, AMBER, CORAL, "#4E9E8F"][:len(gender_counts)]
        wedges, texts, autotexts = plt.pie(
            gender_counts.values,
            labels=gender_counts.index,
            autopct="%1.0f%%",
            colors=colors,
            startangle=90,
            explode=[0.03] * len(gender_counts),
            shadow=True,
            textprops={"fontsize": 10},
        )
        plt.legend(wedges, gender_counts.index, loc="lower center",
                   bbox_to_anchor=(0.5, -0.15), fontsize=9)
    else:
        plt.text(0.5, 0.5, "No patient data yet",
                 ha="center", va="center", color=SLATE)

    plt.title("Patient Gender Distribution", fontsize=12,
              fontweight="bold", loc="left")
    _save("gender_pie.png", dark=False)
    _save("gender_pie.png", dark=True)


# ── Graph 9: Bar Graph ───────────────────────────────────────────
# plt.bar() — weekday pattern
def build_weekday_appointments():
    print("[9/9] Bar Graph — plt.bar() — Weekday Appointments")

    appts = appointments_df.copy()
    appts["appointment_date"] = pd.to_datetime(appts["appointment_date"])
    appts["day_name"] = appts["appointment_date"].dt.day_name()

    day_order = ["Monday", "Tuesday", "Wednesday", "Thursday",
                 "Friday", "Saturday", "Sunday"]
    day_counts = appts["day_name"].value_counts().reindex(day_order, fill_value=0)

    plt.figure(figsize=(7, 3.2))

    bars = plt.bar(day_counts.index, day_counts.values,
                   color=CHART_COLORS[:len(day_counts)])
    plt.bar_label(bars, padding=3, fontsize=9)
    plt.xlabel("Day of the Week", fontsize=10)
    plt.ylabel("Number of Appointments", fontsize=10)
    plt.legend(bars, day_counts.index, loc="upper right", fontsize=8)

    plt.title("Appointments by Day of Week", fontsize=12,
              fontweight="bold", loc="left")
    plt.grid(axis="y", color=GRID, linewidth=0.8)
    plt.gca().spines[["top", "right"]].set_visible(False)
    plt.xticks(rotation=20, ha="right")
    _save("weekday_appointments.png", dark=False)
    _save("weekday_appointments.png", dark=True)


# ══════════════════════════════════════════════════════════════════
#  SECTION 4: CSV Import / Export
#  Concept: to_csv() to save, read_csv() to load back
# ══════════════════════════════════════════════════════════════════

def export_csv_files():
    print("\n" + "=" * 60)
    print("SECTION 4: CSV Import / Export")
    print("=" * 60)

    # to_csv() — export DataFrame to CSV
    patients_df.to_csv(CSV_DIR + "/patients.csv", index=False)
    doctors_df.to_csv(CSV_DIR + "/doctors.csv", index=False)
    appointments_df.to_csv(CSV_DIR + "/appointments.csv", index=False)
    bills_df.to_csv(CSV_DIR + "/bills.csv", index=False)
    print("\nExported 4 CSV files to static/csv/")

    # read_csv() — import CSV back into DataFrame
    patients_verify = pd.read_csv(CSV_DIR + "/patients.csv")
    print(f"Re-read patients.csv — {len(patients_verify)} rows loaded")
    print(patients_verify.head(3))

    return {
        "patients_rows": len(patients_verify),
        "exported_files": ["patients.csv", "doctors.csv",
                           "appointments.csv", "bills.csv"],
    }


# ══════════════════════════════════════════════════════════════════
#  SECTION 5: KPI Computation + Main Route
# ══════════════════════════════════════════════════════════════════

def compute_kpis(p_df=None, a_df=None, b_df=None):
    p = p_df if p_df is not None else patients_df
    a = a_df if a_df is not None else appointments_df
    b = b_df if b_df is not None else bills_df

    total_patients = len(p)
    admitted = int((p["admission_status"] == "Admitted").sum()) if not p.empty else 0

    today = pd.Timestamp.now().strftime("%Y-%m-%d")
    todays_appts = len(a[a["appointment_date"] == today]) if not a.empty else 0

    current_month = pd.Timestamp.now().strftime("%Y-%m")
    b = b.copy()
    if not b.empty and "bill_date" in b.columns:
        b["bill_date"] = pd.to_datetime(b["bill_date"])
        b["month"] = b["bill_date"].dt.to_period("M").astype(str)
        month_bills = b[b["month"] == current_month]
        month_revenue = float(month_bills["total_amount"].astype(float).sum()) if not month_bills.empty else 0.0
        pending_dues = float(
            b.loc[b["payment_status"] != "Paid", "total_amount"].astype(float).sum()
        )
    else:
        month_revenue = 0.0
        pending_dues = 0.0

    return {
        "total_patients": total_patients,
        "admitted": admitted,
        "todays_appointments": todays_appts,
        "month_revenue": round(month_revenue, 2),
        "pending_dues": round(pending_dues, 2),
    }


@analytics_bp.route("/")
def dashboard():
    series_head = fee_series.head(5)
    series_tail = fee_series.tail(3)
    series_stats = {
        "mean": round(fee_series.mean(), 2),
        "max": round(fee_series.max(), 2),
        "min": round(fee_series.min(), 2),
        "sum": round(fee_series.sum(), 2),
        "std": round(fee_series.std(), 2),
    }

    patients_display = patients_df.head(5).copy()
    patients_display["Name"] = patients_df["first_name"].str.cat(patients_df["last_name"], sep=" ")
    patients_display = patients_display.rename(columns={
        "first_name": "Name", "gender": "Gender", "blood_group": "Blood",
        "admission_status": "Status", "ward": "Ward",
    })
    patients_display = patients_display[["Name", "Gender", "Blood", "Status", "Ward"]]
    patients_summary = {
        "head": patients_display.to_dict("records"),
        "columns": list(patients_display.columns),
        "shape": patients_df.shape,
    }

    bills_summary = {
        "head": bills_df.head(5).to_dict("records"),
        "tail": bills_df.tail(3).to_dict("records"),
        "shape": bills_df.shape,
        "describe": bills_df[["consultation_fee", "medicine_charges",
                               "room_charges", "other_charges", "total_amount"]
                             ].describe().round(2).to_dict() if not bills_df.empty else {},
    }

    kpis = compute_kpis()

    import time
    v = int(time.time())

    return render_template(
        "analytics.html",
        kpis=kpis,
        v=v,
        fee_series_head=series_head.to_dict(),
        fee_series_tail=series_tail.to_dict(),
        series_stats=series_stats,
        patients_summary=patients_summary,
        bills_summary=bills_summary,
        csv_info={"exported_files": ["patients.csv", "doctors.csv",
                                      "appointments.csv", "bills.csv"]},
    )


# ══════════════════════════════════════════════════════════════════
#  Generate all charts and CSV files (runs in both IDLE and Flask)
# ══════════════════════════════════════════════════════════════════

try:
    build_appointments_trend()
    build_department_load()
    build_revenue_by_month()
    build_payment_status()
    build_patient_admission_mix()
    build_bill_amount_histogram()
    build_fee_vs_total_scatter()
    build_gender_pie()
    build_weekday_appointments()
    export_csv_files()
except Exception as _e:
    print(f"[analytics] chart/CSV generation skipped at startup: {_e}")
print("\nAll 9 charts (light + dark) + 4 CSV files generated successfully.")
