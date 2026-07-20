from flask import Blueprint, render_template, request, redirect, url_for, flash
from db import query, execute

appointments_bp = Blueprint("appointments", __name__, url_prefix="/appointments")


@appointments_bp.route("/")
def list_appointments():
    date_filter = request.args.get("date", "")
    status = request.args.get("status", "")
    patient = request.args.get("patient", "").strip()
    doctor = request.args.get("doctor", "").strip()

    sql = """SELECT a.*, p.first_name AS p_first, p.last_name AS p_last,
                     d.first_name AS d_first, d.last_name AS d_last, d.specialization
              FROM appointments a
              JOIN patients p ON a.patient_id = p.patient_id
              JOIN doctors d ON a.doctor_id = d.doctor_id
              WHERE 1=1"""
    params = []
    if patient:
        sql += " AND (p.first_name LIKE %s OR p.last_name LIKE %s OR CONCAT(p.first_name,' ',p.last_name) LIKE %s)"
        like = f"%{patient}%"
        params += [like, like, like]
    if doctor:
        sql += " AND (d.first_name LIKE %s OR d.last_name LIKE %s OR CONCAT(d.first_name,' ',d.last_name) LIKE %s)"
        like = f"%{doctor}%"
        params += [like, like, like]
    if date_filter:
        sql += " AND a.appointment_date = %s"
        params.append(date_filter)
    if status:
        sql += " AND a.status = %s"
        params.append(status)
    sql += " ORDER BY FIELD(a.status, 'Scheduled', 'Completed', 'No-Show', 'Cancelled'), a.appointment_date DESC, a.appointment_time"

    all_appts = query(sql, params)

    stats = query(
        """SELECT
             COUNT(*) AS total,
             COALESCE(SUM(appointment_date = CURDATE()),0) AS today,
             COALESCE(SUM(status='Scheduled'),0) AS scheduled,
             COALESCE(SUM(status='Completed'),0) AS completed
           FROM appointments""",
        one=True,
    )

    per_page = 10
    page = request.args.get("page", 1, type=int)
    if page < 1:
        page = 1
    total = len(all_appts)
    total_pages = max(1, (total + per_page - 1) // per_page)
    if page > total_pages:
        page = total_pages
    start = (page - 1) * per_page
    appts = all_appts[start:start + per_page]

    return render_template("appointments/list.html", appointments=appts,
                           date_filter=date_filter, status=status,
                           patient=patient, doctor=doctor,
                           page=page, total_pages=total_pages, total=total,
                           stats=stats)


@appointments_bp.route("/new", methods=["GET", "POST"])
def new_appointment():
    if request.method == "POST":
        f = request.form
        execute(
            """INSERT INTO appointments (patient_id, doctor_id, appointment_date,
               appointment_time, reason, status)
               VALUES (%s,%s,%s,%s,%s,%s)""",
            (f["patient_id"], f["doctor_id"], f["appointment_date"],
             f["appointment_time"], f.get("reason"), f.get("status", "Scheduled")),
        )
        flash("Appointment scheduled.", "success")
        return redirect(url_for("appointments.list_appointments"))

    patients = query("SELECT patient_id, first_name, last_name FROM patients ORDER BY first_name")
    doctors = query("SELECT doctor_id, first_name, last_name, specialization FROM doctors WHERE status='Active' ORDER BY first_name")
    return render_template("appointments/form.html", appointment=None, patients=patients, doctors=doctors)


@appointments_bp.route("/<int:appointment_id>/status", methods=["POST"])
def update_status(appointment_id):
    new_status = request.form["status"]
    execute("UPDATE appointments SET status=%s WHERE appointment_id=%s", (new_status, appointment_id))
    flash(f"Appointment marked as {new_status}.", "success")
    return redirect(url_for("appointments.list_appointments"))


@appointments_bp.route("/<int:appointment_id>/delete", methods=["POST"])
def delete_appointment(appointment_id):
    execute("DELETE FROM appointments WHERE appointment_id=%s", (appointment_id,))
    flash("Appointment cancelled and removed.", "success")
    return redirect(url_for("appointments.list_appointments"))
