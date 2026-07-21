from flask import Blueprint, render_template, request, redirect, url_for, flash
from datetime import date
from db import query, execute

patients_bp = Blueprint("patients", __name__, url_prefix="/patients")


@patients_bp.route("/")
def list_patients():
    search = request.args.get("q", "").strip()
    status = request.args.get("status", "")

    sql = "SELECT * FROM patients WHERE 1=1"
    params = []
    if search:
        sql += " AND (CONCAT(first_name, ' ', last_name) LIKE %s OR phone LIKE %s)"
        like = f"%{search}%"
        params += [like, like]
    if status:
        sql += " AND admission_status = %s"
        params.append(status)
    sql += " ORDER BY FIELD(admission_status, 'Outpatient', 'Admitted', 'Discharged'), created_at DESC"

    all_patients = query(sql, params)

    stats = query(
        """SELECT
             COUNT(*) AS total,
             COALESCE(SUM(admission_status='Outpatient'),0) AS outpatient,
             COALESCE(SUM(admission_status='Admitted'),0) AS admitted,
             COALESCE(SUM(admission_status='Discharged'),0) AS discharged
           FROM patients""",
        one=True,
    )

    per_page = 10
    page = request.args.get("page", 1, type=int)
    if page < 1:
        page = 1
    total = len(all_patients)
    total_pages = max(1, (total + per_page - 1) // per_page)
    if page > total_pages:
        page = total_pages
    start = (page - 1) * per_page
    patients = all_patients[start:start + per_page]

    return render_template("patients/list.html", patients=patients, search=search,
                           status=status, page=page, total_pages=total_pages,
                           total=total, stats=stats)


@patients_bp.route("/new", methods=["GET", "POST"])
def new_patient():
    if request.method == "POST":
        f = request.form
        execute(
            """INSERT INTO patients
               (first_name, last_name, date_of_birth, gender, blood_group, phone,
                email, address, emergency_contact, admission_status, ward, registered_on)
               VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
            (f["first_name"], f["last_name"], f["date_of_birth"], f["gender"],
             f.get("blood_group"), f.get("phone"), f.get("email"), f.get("address"),
             f.get("emergency_contact"), f.get("admission_status", "Outpatient"),
             f.get("ward"), date.today().isoformat()),
        )
        flash("Patient registered successfully.", "success")
        return redirect(url_for("patients.list_patients"))
    return render_template("patients/form.html", patient=None)


@patients_bp.route("/<int:patient_id>")
def view_patient(patient_id):
    patient = query("SELECT * FROM patients WHERE patient_id=%s", (patient_id,), one=True)
    appointments = query(
        """SELECT a.*, d.first_name AS doc_first, d.last_name AS doc_last
           FROM appointments a JOIN doctors d ON a.doctor_id = d.doctor_id
           WHERE a.patient_id=%s ORDER BY appointment_date DESC""",
        (patient_id,),
    )
    bills = query("SELECT * FROM bills WHERE patient_id=%s ORDER BY bill_date DESC", (patient_id,))
    return render_template("patients/view.html", patient=patient, appointments=appointments, bills=bills)


@patients_bp.route("/<int:patient_id>/edit", methods=["GET", "POST"])
def edit_patient(patient_id):
    if request.method == "POST":
        f = request.form
        execute(
            """UPDATE patients SET first_name=%s, last_name=%s, date_of_birth=%s, gender=%s,
               blood_group=%s, phone=%s, email=%s, address=%s, emergency_contact=%s,
               admission_status=%s, ward=%s WHERE patient_id=%s""",
            (f["first_name"], f["last_name"], f["date_of_birth"], f["gender"],
             f.get("blood_group"), f.get("phone"), f.get("email"), f.get("address"),
             f.get("emergency_contact"), f.get("admission_status"), f.get("ward"), patient_id),
        )
        flash("Patient record updated.", "success")
        return redirect(url_for("patients.view_patient", patient_id=patient_id))
    patient = query("SELECT * FROM patients WHERE patient_id=%s", (patient_id,), one=True)
    return render_template("patients/form.html", patient=patient)


@patients_bp.route("/<int:patient_id>/delete", methods=["POST"])
def delete_patient(patient_id):
    execute("DELETE FROM patients WHERE patient_id=%s", (patient_id,))
    flash("Patient record removed.", "success")
    return redirect(url_for("patients.list_patients"))
