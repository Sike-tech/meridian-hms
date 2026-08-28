"""
Analytics Dashboard — pre-generated static charts.

Chart generation happens on data changes (CRUD hooks).
The dashboard route serves static PNGs + pure-SQL KPIs.
Zero heavy imports (pandas/numpy/matplotlib) at module level.
"""

import os
import statistics
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

CHART_FILES = [
    "appointments_trend.png",
    "department_load.png",
    "revenue_by_month.png",
    "payment_status.png",
    "patient_admission_mix.png",
    "bill_histogram.png",
    "fee_vs_total_scatter.png",
    "gender_pie.png",
    "weekday_appointments.png",
]


def generate_all_charts():
    """Regenerate all 9 PNG charts + 4 CSV files. Called after data mutations."""
    try:
        import pandas as pd
        import numpy as np
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError as e:
        print(f"[analytics] skipped chart generation: {e}")
        return

    def _q(sql, params=None):
        try:
            return query(sql, params)
        except Exception:
            return []

    patients_df = pd.DataFrame(_q(
        "SELECT patient_id, first_name, last_name, gender, blood_group, "
        "admission_status, ward FROM patients"
    ))
    doctors_df = pd.DataFrame(_q(
        "SELECT doctor_id, first_name, last_name, specialization, "
        "department, consultation_fee, status FROM doctors"
    ))
    appointments_df = pd.DataFrame(_q(
        "SELECT appointment_id, appointment_date, appointment_time, "
        "status, patient_id, doctor_id FROM appointments"
    ))
    bills_df = pd.DataFrame(_q(
        "SELECT bill_id, patient_id, bill_date, consultation_fee, "
        "medicine_charges, room_charges, other_charges, total_amount, "
        "payment_status, payment_method FROM bills"
    ))

    for col in ["consultation_fee", "medicine_charges", "room_charges",
                "other_charges", "total_amount"]:
        if col in bills_df.columns:
            bills_df[col] = pd.to_numeric(bills_df[col], errors="coerce").fillna(0.0)

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

    def _save(filename):
        plt.tight_layout()
        plt.savefig(CHART_DIR + "/" + filename, dpi=150, bbox_inches="tight", facecolor="white")
        _style_dark()
        plt.savefig(CHART_DIR + "/" + filename.replace(".png", "_dark.png"),
                    dpi=150, bbox_inches="tight", facecolor=plt.gcf().get_facecolor())

    try:
        print("[analytics] Generating charts...")

        # 1 — Appointments Trend
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
        _save("appointments_trend.png")
        plt.close()

        # 2 — Department Workload
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
        _save("department_load.png")
        plt.close()

        # 3 — Revenue by Month
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
                plt.text(bar.get_x() + bar.get_width() / 2, h, f"Rs.{h:.0f}", ha="center", va="bottom", fontsize=9)
            plt.xlabel("Month", fontsize=10)
            plt.ylabel("Revenue (Rs.)", fontsize=10)
        else:
            plt.text(0.5, 0.5, "No billing data yet", ha="center", va="center", color=SLATE)
        plt.title("Revenue by Month", fontsize=12, fontweight="bold", loc="left")
        plt.grid(axis="y", color=GRID, linewidth=0.8)
        plt.gca().spines[["top", "right"]].set_visible(False)
        _save("revenue_by_month.png")
        plt.close()

        # 4 — Payment Status
        print("[4/9] Payment Status")
        sc = bills_df["payment_status"].value_counts()
        plt.figure(figsize=(5, 4))
        if not sc.empty:
            colors = {"Paid": TEAL, "Pending": CORAL, "Partially Paid": AMBER}
            wc = [colors.get(s, SLATE) for s in sc.index]
            wedges, texts, autotexts = plt.pie(sc.values, labels=sc.index, autopct="%1.0f%%",
                                                colors=wc, startangle=90,
                                                wedgeprops={"width": 0.42, "edgecolor": "white"},
                                                textprops={"fontsize": 9})
            for t in autotexts:
                t.set_fontsize(9)
                t.set_fontweight("bold")
        else:
            plt.text(0.5, 0.5, "No billing data yet", ha="center", va="center", color=SLATE)
        plt.title("Payment Status Distribution", fontsize=12, fontweight="bold", loc="left")
        _save("payment_status.png")
        plt.close()

        # 5 — Patient Admission Status
        print("[5/9] Patient Admission")
        sc = patients_df["admission_status"].value_counts()
        plt.figure(figsize=(6, 4.2))
        if not sc.empty:
            colors = [TEAL, AMBER, CORAL][:len(sc)]
            bars = plt.barh(sc.index, sc.values, color=colors)
            for bar in bars:
                w = bar.get_width()
                plt.text(w, bar.get_y() + bar.get_height() / 2, f"{int(w)}",
                         ha="left", va="center", fontsize=10, fontweight="bold")
            plt.xlabel("Number of Patients", fontsize=10)
            plt.legend(bars, sc.index, loc="upper center", bbox_to_anchor=(0.5, -0.18), ncol=3, fontsize=9, framealpha=0.9)
        else:
            plt.text(0.5, 0.5, "No patient data yet", ha="center", va="center", color=SLATE)
        plt.title("Patients by Admission Status", fontsize=12, fontweight="bold", loc="left")
        plt.grid(axis="x", color=GRID, linewidth=0.8)
        plt.gca().spines[["top", "right"]].set_visible(False)
        plt.subplots_adjust(bottom=0.25)
        _save("patient_admission_mix.png")
        plt.close()

        # 6 — Bill Amount Distribution
        print("[6/9] Bill Distribution")
        plt.figure(figsize=(7, 4.2))
        if not bills_df.empty and bills_df["total_amount"].notna().any():
            amounts = bills_df["total_amount"].dropna().astype(float)
            n_bins = min(8, len(amounts))
            if n_bins > 1:
                n_arr, bins, patches = plt.hist(amounts, bins=n_bins, edgecolor="white", alpha=0.85)
                for i, patch in enumerate(patches):
                    patch.set_facecolor(CHART_COLORS[i % len(CHART_COLORS)])
                bl = [f"Rs.{int(bins[i]):,}-Rs.{int(bins[i+1]):,}" for i in range(len(bins)-1)]
                plt.legend(patches, bl, loc="upper center", bbox_to_anchor=(0.5, -0.22), ncol=2, fontsize=7.5, framealpha=0.9)
            else:
                plt.hist(amounts, bins=1, color=TEAL, edgecolor="white", alpha=0.85)
            plt.xlabel("Total Bill Amount (Rs.)", fontsize=10)
            plt.ylabel("Frequency", fontsize=10)
        else:
            plt.text(0.5, 0.5, "No billing data yet", ha="center", va="center", color=SLATE)
        plt.title("Distribution of Bill Amounts", fontsize=12, fontweight="bold", loc="left")
        plt.grid(axis="y", color=GRID, linewidth=0.8)
        plt.gca().spines[["top", "right"]].set_visible(False)
        plt.subplots_adjust(bottom=0.25)
        _save("bill_histogram.png")
        plt.close()

        # 7 — Fee vs Total Bill
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
            plt.xlabel("Consultation Fee (Rs.)", fontsize=10)
            plt.ylabel("Total Bill Amount (Rs.)", fontsize=10)
            plt.legend(loc="upper left", fontsize=9, framealpha=0.9)
        else:
            plt.text(0.5, 0.5, "No data for scatter plot", ha="center", va="center", color=SLATE)
        plt.title("Consultation Fee vs Total Bill", fontsize=12, fontweight="bold", loc="left")
        plt.grid(color=GRID, linewidth=0.8)
        plt.gca().spines[["top", "right"]].set_visible(False)
        _save("fee_vs_total_scatter.png")
        plt.close()

        # 8 — Gender Distribution
        print("[8/9] Gender Distribution")
        gc = patients_df["gender"].value_counts()
        plt.figure(figsize=(5, 4))
        if not gc.empty:
            colors = [TEAL, AMBER, CORAL, "#4E9E8F"][:len(gc)]
            wedges, texts, autotexts = plt.pie(gc.values, labels=gc.index, autopct="%1.0f%%",
                                                colors=colors, startangle=90,
                                                explode=[0.03]*len(gc), textprops={"fontsize": 10})
            for t in autotexts:
                t.set_fontsize(10)
                t.set_fontweight("bold")
        else:
            plt.text(0.5, 0.5, "No patient data yet", ha="center", va="center", color=SLATE)
        plt.title("Patient Gender Distribution", fontsize=12, fontweight="bold", loc="left")
        _save("gender_pie.png")
        plt.close()

        # 9 — Weekday Appointments
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
            plt.text(bar.get_x() + bar.get_width() / 2, h, f"{int(h)}",
                     ha="center", va="bottom", fontsize=10, fontweight="bold")
        plt.xlabel("Day of the Week", fontsize=10)
        plt.ylabel("Number of Appointments", fontsize=10)
        plt.legend(bars, day_counts.index, loc="upper right", fontsize=8, ncol=2, framealpha=0.9)
        plt.title("Appointments by Day of Week", fontsize=12, fontweight="bold", loc="left")
        plt.grid(axis="y", color=GRID, linewidth=0.8)
        plt.gca().spines[["top", "right"]].set_visible(False)
        plt.xticks(ticks=range(len(day_counts)), labels=day_counts.index, rotation=30, ha="right", fontsize=9)
        _save("weekday_appointments.png")
        plt.close()

        # Export CSVs
        patients_df.to_csv(CSV_DIR + "/patients.csv", index=False)
        doctors_df.to_csv(CSV_DIR + "/doctors.csv", index=False)
        appointments_df.to_csv(CSV_DIR + "/appointments.csv", index=False)
        bills_df.to_csv(CSV_DIR + "/bills.csv", index=False)

        print("[analytics] All 9 charts + 4 CSV files generated.")
    except Exception as e:
        print(f"[analytics] chart generation failed: {e}")
    finally:
        plt.close("all")


def _safe_query(sql, params=None, one=False):
    try:
        return query(sql, params, one)
    except Exception:
        return None if one else []


def _percentile(sorted_vals, p):
    if not sorted_vals:
        return 0
    k = (len(sorted_vals) - 1) * p
    f = int(k)
    c = f + 1
    if c >= len(sorted_vals):
        return sorted_vals[f]
    return sorted_vals[f] + (k - f) * (sorted_vals[c] - sorted_vals[f])


def _compute_describe(columns):
    result = {}
    for col in columns:
        rows = _safe_query(f"SELECT `{col}` AS val FROM bills WHERE `{col}` IS NOT NULL")
        if not rows:
            result[col] = {}
            continue
        vals = sorted(float(r["val"]) for r in rows)
        n = len(vals)
        result[col] = {
            "count": n,
            "mean": round(statistics.mean(vals), 2),
            "std": round(statistics.stdev(vals), 2) if n > 1 else 0,
            "min": vals[0],
            "25%": round(_percentile(vals, 0.25), 2),
            "50%": round(_percentile(vals, 0.50), 2),
            "75%": round(_percentile(vals, 0.75), 2),
            "max": vals[-1],
        }
    return result


@analytics_bp.route("/")
def dashboard():
    import time

    # KPIs — pure SQL
    total_patients = _safe_query("SELECT COUNT(*) AS c FROM patients", one=True)["c"]
    admitted = _safe_query(
        "SELECT COUNT(*) AS c FROM patients WHERE admission_status='Admitted'", one=True
    )["c"]
    todays_appts = _safe_query(
        "SELECT COUNT(*) AS c FROM appointments WHERE appointment_date=CURDATE()", one=True
    )["c"]
    month_rev_row = _safe_query(
        "SELECT COALESCE(SUM(total_amount),0) AS s FROM bills "
        "WHERE MONTH(bill_date)=MONTH(CURDATE()) AND YEAR(bill_date)=YEAR(CURDATE())",
        one=True,
    )
    month_revenue = float(month_rev_row["s"]) if month_rev_row else 0.0
    pending_row = _safe_query(
        "SELECT COALESCE(SUM(total_amount),0) AS s FROM bills WHERE payment_status!='Paid'",
        one=True,
    )
    pending_dues = float(pending_row["s"]) if pending_row else 0.0

    kpis = {
        "total_patients": total_patients,
        "admitted": admitted,
        "todays_appointments": todays_appts,
        "month_revenue": round(month_revenue, 2),
        "pending_dues": round(pending_dues, 2),
    }

    # Fee schedule — top 5
    fee_rows = _safe_query(
        "SELECT CONCAT('Dr. ', first_name, ' ', last_name) AS name, consultation_fee "
        "FROM doctors ORDER BY consultation_fee DESC LIMIT 5"
    )
    fee_series_head = {r["name"]: float(r["consultation_fee"]) for r in fee_rows}

    # Fee schedule — bottom 3
    fee_tail = _safe_query(
        "SELECT CONCAT('Dr. ', first_name, ' ', last_name) AS name, consultation_fee "
        "FROM doctors ORDER BY consultation_fee ASC LIMIT 3"
    )
    fee_series_tail = {r["name"]: float(r["consultation_fee"]) for r in fee_tail}

    # Fee stats — pure SQL
    fee_stats_row = _safe_query(
        "SELECT ROUND(AVG(consultation_fee),2) AS mean, "
        "ROUND(MAX(consultation_fee),2) AS max, "
        "ROUND(MIN(consultation_fee),2) AS min, "
        "ROUND(SUM(consultation_fee),2) AS sum, "
        "ROUND(STDDEV(consultation_fee),2) AS std "
        "FROM doctors",
        one=True,
    )
    series_stats = {
        "mean": float(fee_stats_row.get("mean") or 0),
        "max": float(fee_stats_row.get("max") or 0),
        "min": float(fee_stats_row.get("min") or 0),
        "sum": float(fee_stats_row.get("sum") or 0),
        "std": float(fee_stats_row.get("std") or 0),
    }

    # Patient registry summary — top 5 recent
    patients_rows = _safe_query(
        "SELECT CONCAT(first_name, ' ', last_name) AS Name, "
        "gender AS Gender, blood_group AS Blood, "
        "admission_status AS Status, ward AS Ward "
        "FROM patients ORDER BY created_at DESC LIMIT 5"
    )
    patients_summary = {
        "head": patients_rows,
        "columns": ["Name", "Gender", "Blood", "Status", "Ward"],
        "shape": (total_patients,),
    }

    # Billing summary
    bills_head = _safe_query(
        "SELECT b.bill_id, CONCAT(p.first_name, ' ', p.last_name) AS patient_name, "
        "b.bill_date, b.total_amount, b.payment_status, b.payment_method "
        "FROM bills b JOIN patients p ON b.patient_id=p.patient_id "
        "ORDER BY b.bill_date DESC LIMIT 5"
    )
    bills_tail = _safe_query(
        "SELECT b.bill_id, CONCAT(p.first_name, ' ', p.last_name) AS patient_name, "
        "b.bill_date, b.total_amount, b.payment_status, b.payment_method "
        "FROM bills b JOIN patients p ON b.patient_id=p.patient_id "
        "ORDER BY b.bill_date ASC LIMIT 3"
    )
    bills_count = _safe_query("SELECT COUNT(*) AS c FROM bills", one=True)["c"]
    bills_describe = _compute_describe(
        ["consultation_fee", "medicine_charges", "room_charges", "other_charges", "total_amount"]
    )
    bills_summary = {
        "head": bills_head,
        "tail": bills_tail,
        "shape": (bills_count,),
        "describe": bills_describe,
    }

    # CSV info
    patients_total = _safe_query("SELECT COUNT(*) AS c FROM patients", one=True)["c"]
    csv_info = {
        "exported_files": ["patients.csv", "doctors.csv", "appointments.csv", "bills.csv"],
        "patients_rows": patients_total,
    }

    v = int(time.time())

    return render_template(
        "analytics.html",
        kpis=kpis,
        v=v,
        fee_series_head=fee_series_head,
        fee_series_tail=fee_series_tail,
        series_stats=series_stats,
        patients_summary=patients_summary,
        bills_summary=bills_summary,
        csv_info=csv_info,
    )
