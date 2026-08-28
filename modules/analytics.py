"""
CBSE Class 12 Informatics Practices — Hospital Management System
Analytics Dashboard

Uses ONLY the pyplot (plt) state-machine interface as per the
Class 12 IP syllabus — no fig, ax = plt.subplots() object interface.
"""

import os
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

# Lazy-loaded globals (None until first dashboard visit)
_patients_df = None
_doctors_df = None
_appointments_df = None
_bills_df = None
_fee_series = None
_data_loaded = False
_charts_generated = False


def _safe_query(sql, params=None, one=False):
    try:
        return query(sql, params, one)
    except Exception as _e:
        print(f"[analytics] DB unavailable: {_e}")
        return None if one else []


def _load_data():
    global _patients_df, _doctors_df, _appointments_df, _bills_df
    global _fee_series, _data_loaded
    if _data_loaded:
        return

    import pandas as pd

    _patients_df = pd.DataFrame(
        _safe_query("SELECT patient_id, first_name, last_name, gender, blood_group, "
                    "admission_status, ward FROM patients")
    )
    _doctors_df = pd.DataFrame(
        _safe_query("SELECT doctor_id, first_name, last_name, specialization, "
                    "department, consultation_fee, status FROM doctors")
    )
    _appointments_df = pd.DataFrame(
        _safe_query("SELECT appointment_id, appointment_date, appointment_time, "
                    "status, patient_id, doctor_id FROM appointments")
    )
    _bills_df = pd.DataFrame(
        _safe_query("SELECT bill_id, patient_id, bill_date, consultation_fee, "
                    "medicine_charges, room_charges, other_charges, total_amount, "
                    "payment_status, payment_method FROM bills")
    )

    for col in ["consultation_fee", "medicine_charges", "room_charges",
                "other_charges", "total_amount"]:
        if col in _bills_df.columns:
            _bills_df[col] = pd.to_numeric(_bills_df[col], errors="coerce").fillna(0.0)

    doctors_data = _safe_query("SELECT first_name, last_name, consultation_fee FROM doctors")
    fee_dict = {}
    for row in (doctors_data or []):
        fee_dict[f"Dr. {row['first_name']} {row['last_name']}"] = float(row["consultation_fee"])
    _fee_series = pd.Series(fee_dict, name="Consultation Fee (₹)", dtype=float)

    _data_loaded = True


def _generate_all():
    global _charts_generated
    if _charts_generated:
        return
    _load_data()

    import numpy as np
    import pandas as pd
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

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

    def _style_dark():
        fig = plt.gcf()
        fig.patch.set_facecolor("#0E1B1A")
        ax = plt.gca()
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
            leg.get_frame().set_facecolor("#0E1B1A")
            leg.get_frame().set_edgecolor("#3A554F")
            for text in leg.get_texts():
                text.set_color("#CFE0DC")
        for child in ax.get_children():
            if isinstance(child, plt.Text) and child.get_text():
                child.set_color("#CFE0DC")

    def _save(filename, dark=False):
        plt.tight_layout()
        fig = plt.gcf()
        fig.patch.set_facecolor("white")
        plt.gca().set_facecolor("white")
        plt.savefig(CHART_DIR + "/" + filename, dpi=150, bbox_inches="tight", facecolor="white")
        if dark:
            _style_dark()
            plt.savefig(CHART_DIR + "/" + filename.replace(".png", "_dark.png"),
                        dpi=150, bbox_inches="tight", facecolor=plt.gcf().get_facecolor())

    try:
        print("[analytics] Generating charts...")
        _build_appointments_trend(plt, pd, _appointments_df)
        _build_department_load(plt, pd, _appointments_df, _doctors_df)
        _build_revenue_by_month(plt, pd, _bills_df)
        _build_payment_status(plt, pd, _bills_df)
        _build_patient_admission_mix(plt, pd, _patients_df)
        _build_bill_amount_histogram(plt, pd, _bills_df)
        _build_fee_vs_total_scatter(plt, np, pd, _bills_df)
        _build_gender_pie(plt, pd, _patients_df)
        _build_weekday_appointments(plt, pd, _appointments_df)
        _export_csv_files(pd)
        _charts_generated = True
        print("[analytics] All 9 charts + 4 CSV files generated.")
    except Exception as _e:
        print(f"[analytics] chart generation failed: {_e}")


def _build_appointments_trend(plt, pd, appointments_df):
    print("[1/9] Appointments Trend")
    appt_by_date = appointments_df.groupby("appointment_date").size().reset_index(name="count")
    appt_by_date = appt_by_date.sort_values("appointment_date")
    plt.figure(figsize=(8, 3.8))
    if not appt_by_date.empty:
        dates = pd.to_datetime(appt_by_date["appointment_date"])
        counts = appt_by_date["count"]
        plt.plot(dates, counts, color=TEAL, linewidth=2.5, marker="o", markersize=5, label="Daily Appointments")
        plt.fill_between(dates, counts, color=TEAL, alpha=0.08)
        plt.xticks(ticks=dates, labels=[d.strftime("%b %d") for d in dates], rotation=40, ha="right", fontsize=8)
        plt.xlabel("Date", fontsize=10)
        plt.ylabel("Number of Appointments", fontsize=10)
        plt.legend(loc="upper left", fontsize=9, framealpha=0.9)
    else:
        plt.text(0.5, 0.5, "No appointment data yet", ha="center", va="center", color=SLATE)
    plt.title("Appointments — Last 30 Days", fontsize=12, fontweight="bold", loc="left")
    plt.grid(axis="y", color=GRID, linewidth=0.8)
    plt.gca().spines[["top", "right"]].set_visible(False)
    plt.tight_layout()
    _save("appointments_trend.png", dark=True)
    plt.close()


def _build_department_load(plt, pd, appointments_df, doctors_df):
    print("[2/9] Department Workload")
    merged = pd.merge(appointments_df, doctors_df, on="doctor_id", how="inner")
    dept_counts = merged.groupby("department").size().reset_index(name="total").sort_values("total", ascending=False)
    plt.figure(figsize=(8, 4.2))
    if not dept_counts.empty:
        bars = plt.bar(dept_counts["department"], dept_counts["total"], color=CHART_COLORS[:len(dept_counts)])
        for bar in bars:
            h = bar.get_height()
            plt.text(bar.get_x() + bar.get_width() / 2, h, f"{int(h)}", ha="center", va="bottom", fontsize=9)
        plt.xlabel("Department", fontsize=10)
        plt.ylabel("Number of Appointments", fontsize=10)
        plt.legend(bars, dept_counts["department"], loc="upper center", bbox_to_anchor=(0.5, -0.25), ncol=4, fontsize=8, framealpha=0.9)
    else:
        plt.text(0.5, 0.5, "No department data yet", ha="center", va="center", color=SLATE)
    plt.title("Appointment Load by Department", fontsize=12, fontweight="bold", loc="left")
    plt.grid(axis="y", color=GRID, linewidth=0.8)
    plt.gca().spines[["top", "right"]].set_visible(False)
    plt.xticks(ticks=range(len(dept_counts)), labels=dept_counts["department"], rotation=40, ha="right", fontsize=8)
    plt.subplots_adjust(bottom=0.35)
    _save("department_load.png", dark=True)
    plt.close()


def _build_revenue_by_month(plt, pd, bills_df):
    print("[3/9] Revenue by Month")
    bc = bills_df.copy()
    bc["bill_date"] = pd.to_datetime(bc["bill_date"])
    bc["month"] = bc["bill_date"].dt.to_period("M").astype(str)
    revenue = bc.groupby("month")["total_amount"].sum().reset_index().sort_values("month")
    plt.figure(figsize=(8, 3.8))
    if not revenue.empty:
        bars = plt.bar(revenue["month"], revenue["total_amount"].astype(float), color=AMBER)
        for bar in bars:
            h = bar.get_height()
            plt.text(bar.get_x() + bar.get_width() / 2, h, f"₹{h:.0f}", ha="center", va="bottom", fontsize=9)
        plt.xlabel("Month", fontsize=10)
        plt.ylabel("Revenue (₹)", fontsize=10)
    else:
        plt.text(0.5, 0.5, "No billing data yet", ha="center", va="center", color=SLATE)
    plt.title("Revenue by Month", fontsize=12, fontweight="bold", loc="left")
    plt.grid(axis="y", color=GRID, linewidth=0.8)
    plt.gca().spines[["top", "right"]].set_visible(False)
    plt.tight_layout()
    _save("revenue_by_month.png", dark=True)
    plt.close()


def _build_payment_status(plt, pd, bills_df):
    print("[4/9] Payment Status")
    sc = bills_df["payment_status"].value_counts()
    plt.figure(figsize=(5, 4))
    if not sc.empty:
        colors = {"Paid": TEAL, "Pending": CORAL, "Partially Paid": AMBER}
        wc = [colors.get(s, SLATE) for s in sc.index]
        wedges, texts, autotexts = plt.pie(sc.values, labels=sc.index, autopct="%1.0f%%", colors=wc, startangle=90, wedgeprops={"width": 0.42, "edgecolor": "white"}, textprops={"fontsize": 9})
        for t in autotexts:
            t.set_fontsize(9)
            t.set_fontweight("bold")
    else:
        plt.text(0.5, 0.5, "No billing data yet", ha="center", va="center", color=SLATE)
    plt.title("Payment Status Distribution", fontsize=12, fontweight="bold", loc="left")
    plt.tight_layout()
    _save("payment_status.png", dark=True)
    plt.close()


def _build_patient_admission_mix(plt, pd, patients_df):
    print("[5/9] Patient Admission")
    sc = patients_df["admission_status"].value_counts()
    plt.figure(figsize=(6, 4.2))
    if not sc.empty:
        colors = [TEAL, AMBER, CORAL][:len(sc)]
        bars = plt.barh(sc.index, sc.values, color=colors)
        for bar in bars:
            w = bar.get_width()
            plt.text(w, bar.get_y() + bar.get_height() / 2, f"{int(w)}", ha="left", va="center", fontsize=10, fontweight="bold")
        plt.xlabel("Number of Patients", fontsize=10)
        plt.legend(bars, sc.index, loc="upper center", bbox_to_anchor=(0.5, -0.18), ncol=3, fontsize=9, framealpha=0.9)
    else:
        plt.text(0.5, 0.5, "No patient data yet", ha="center", va="center", color=SLATE)
    plt.title("Patients by Admission Status", fontsize=12, fontweight="bold", loc="left")
    plt.grid(axis="x", color=GRID, linewidth=0.8)
    plt.gca().spines[["top", "right"]].set_visible(False)
    plt.subplots_adjust(bottom=0.25)
    _save("patient_admission_mix.png", dark=True)
    plt.close()


def _build_bill_amount_histogram(plt, pd, bills_df):
    print("[6/9] Bill Distribution")
    plt.figure(figsize=(7, 4.2))
    if not bills_df.empty and bills_df["total_amount"].notna().any():
        amounts = bills_df["total_amount"].dropna().astype(float)
        n, bins, patches = plt.hist(amounts, bins=8, color=TEAL, edgecolor="white", alpha=0.85)
        for i, patch in enumerate(patches):
            patch.set_facecolor(CHART_COLORS[i % len(CHART_COLORS)])
        bl = [f"₹{int(bins[i]):,}–₹{int(bins[i+1]):,}" for i in range(len(bins)-1)]
        plt.legend(patches, bl, loc="upper center", bbox_to_anchor=(0.5, -0.22), ncol=2, fontsize=7.5, framealpha=0.9)
        plt.xlabel("Total Bill Amount (₹)", fontsize=10)
        plt.ylabel("Frequency", fontsize=10)
    else:
        plt.text(0.5, 0.5, "No billing data yet", ha="center", va="center", color=SLATE)
    plt.title("Distribution of Bill Amounts", fontsize=12, fontweight="bold", loc="left")
    plt.grid(axis="y", color=GRID, linewidth=0.8)
    plt.gca().spines[["top", "right"]].set_visible(False)
    plt.subplots_adjust(bottom=0.25)
    _save("bill_histogram.png", dark=True)
    plt.close()


def _build_fee_vs_total_scatter(plt, np, pd, bills_df):
    print("[7/9] Fee vs Total Bill")
    plt.figure(figsize=(7, 3.8))
    if not bills_df.empty and bills_df["consultation_fee"].notna().any():
        fees = bills_df["consultation_fee"].astype(float)
        totals = bills_df["total_amount"].astype(float)
        plt.scatter(fees, totals, c=TEAL, s=60, alpha=0.7, edgecolors="white", linewidths=0.8, label="Bills")
        if len(fees) > 1:
            z = np.polyfit(fees, totals, 1)
            p = np.poly1d(z)
            margin = (fees.max() - fees.min()) * 0.1 if fees.max() != fees.min() else 100
            x_line = np.linspace(fees.min() - margin, fees.max() + margin, 100)
            y_line = np.clip(p(x_line), 0, None)
            plt.plot(x_line, y_line, "--", color=CORAL, linewidth=1.5, alpha=0.7, label="Trend Line")
        plt.xlabel("Consultation Fee (₹)", fontsize=10)
        plt.ylabel("Total Bill Amount (₹)", fontsize=10)
        plt.legend(loc="upper left", fontsize=9, framealpha=0.9)
    else:
        plt.text(0.5, 0.5, "No data for scatter plot", ha="center", va="center", color=SLATE)
    plt.title("Consultation Fee vs Total Bill", fontsize=12, fontweight="bold", loc="left")
    plt.grid(color=GRID, linewidth=0.8)
    plt.gca().spines[["top", "right"]].set_visible(False)
    plt.tight_layout()
    _save("fee_vs_total_scatter.png", dark=True)
    plt.close()


def _build_gender_pie(plt, pd, patients_df):
    print("[8/9] Gender Distribution")
    gc = patients_df["gender"].value_counts()
    plt.figure(figsize=(5, 4))
    if not gc.empty:
        colors = [TEAL, AMBER, CORAL, "#4E9E8F"][:len(gc)]
        wedges, texts, autotexts = plt.pie(gc.values, labels=gc.index, autopct="%1.0f%%", colors=colors, startangle=90, explode=[0.03]*len(gc), textprops={"fontsize": 10})
        for t in autotexts:
            t.set_fontsize(10)
            t.set_fontweight("bold")
    else:
        plt.text(0.5, 0.5, "No patient data yet", ha="center", va="center", color=SLATE)
    plt.title("Patient Gender Distribution", fontsize=12, fontweight="bold", loc="left")
    plt.tight_layout()
    _save("gender_pie.png", dark=True)
    plt.close()


def _build_weekday_appointments(plt, pd, appointments_df):
    print("[9/9] Weekday Appointments")
    appts = appointments_df.copy()
    appts["appointment_date"] = pd.to_datetime(appts["appointment_date"])
    appts["day_name"] = appts["appointment_date"].dt.day_name()
    day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    day_counts = appts["day_name"].value_counts().reindex(day_order, fill_value=0)
    plt.figure(figsize=(8, 3.8))
    bars = plt.bar(day_counts.index, day_counts.values, color=CHART_COLORS[:len(day_counts)])
    for bar in bars:
        h = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, h, f"{int(h)}", ha="center", va="bottom", fontsize=10, fontweight="bold")
    plt.xlabel("Day of the Week", fontsize=10)
    plt.ylabel("Number of Appointments", fontsize=10)
    plt.legend(bars, day_counts.index, loc="upper right", fontsize=8, ncol=2, framealpha=0.9)
    plt.title("Appointments by Day of Week", fontsize=12, fontweight="bold", loc="left")
    plt.grid(axis="y", color=GRID, linewidth=0.8)
    plt.gca().spines[["top", "right"]].set_visible(False)
    plt.xticks(ticks=range(len(day_counts)), labels=day_counts.index, rotation=30, ha="right", fontsize=9)
    plt.tight_layout()
    _save("weekday_appointments.png", dark=True)
    plt.close()


def _export_csv_files(pd):
    _patients_df.to_csv(CSV_DIR + "/patients.csv", index=False)
    _doctors_df.to_csv(CSV_DIR + "/doctors.csv", index=False)
    _appointments_df.to_csv(CSV_DIR + "/appointments.csv", index=False)
    _bills_df.to_csv(CSV_DIR + "/bills.csv", index=False)
    print("Exported 4 CSV files")


def compute_kpis(p_df=None, a_df=None, b_df=None):
    import pandas as pd
    _load_data()
    p = p_df if p_df is not None else _patients_df
    a = a_df if a_df is not None else _appointments_df
    b = b_df if b_df is not None else _bills_df

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
        pending_dues = float(b.loc[b["payment_status"] != "Paid", "total_amount"].astype(float).sum())
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
    import pandas as pd
    _load_data()
    _generate_all()

    series_head = _fee_series.head(5)
    series_tail = _fee_series.tail(3)
    series_stats = {
        "mean": round(_fee_series.mean(), 2),
        "max": round(_fee_series.max(), 2),
        "min": round(_fee_series.min(), 2),
        "sum": round(_fee_series.sum(), 2),
        "std": round(_fee_series.std(), 2),
    }

    patients_display = _patients_df.head(5).copy()
    patients_display["Name"] = _patients_df["first_name"].str.cat(_patients_df["last_name"], sep=" ")
    patients_display = patients_display.rename(columns={
        "first_name": "Name", "gender": "Gender", "blood_group": "Blood",
        "admission_status": "Status", "ward": "Ward",
    })
    patients_display = patients_display[["Name", "Gender", "Blood", "Status", "Ward"]]
    patients_summary = {
        "head": patients_display.to_dict("records"),
        "columns": list(patients_display.columns),
        "shape": _patients_df.shape,
    }

    bills_summary = {
        "head": _bills_df.head(5).to_dict("records"),
        "tail": _bills_df.tail(3).to_dict("records"),
        "shape": _bills_df.shape,
        "describe": _bills_df[["consultation_fee", "medicine_charges",
                                "room_charges", "other_charges", "total_amount"]
                              ].describe().round(2).to_dict() if not _bills_df.empty else {},
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
