from flask import Blueprint, render_template, request, redirect, url_for, flash
from db import query, execute

doctors_bp = Blueprint("doctors", __name__, url_prefix="/doctors")


@doctors_bp.route("/")
def list_doctors():
    search = request.args.get("q", "").strip()
    department = request.args.get("department", "")
    specialization = request.args.get("specialization", "")

    sql = "SELECT * FROM doctors WHERE 1=1"
    params = []

    if search:
        sql += """
            AND (
                first_name LIKE %s
                OR last_name LIKE %s
                OR specialization LIKE %s
            )
        """
        like = f"%{search}%"
        params += [like, like, like]

    if department:
        sql += " AND department LIKE %s"
        params.append(f"%{department}%")

    if specialization:
        sql += " AND specialization=%s"
        params.append(specialization)

    sql += " ORDER BY first_name"

    all_doctors = query(sql, params)

    per_page = 10
    page = request.args.get("page", 1, type=int)
    if page < 1:
        page = 1
    total = len(all_doctors)
    total_pages = max(1, (total + per_page - 1) // per_page)
    if page > total_pages:
        page = total_pages
    start = (page - 1) * per_page
    doctors = all_doctors[start:start + per_page]

    specializations = query(
        "SELECT DISTINCT specialization FROM doctors "
        "WHERE specialization IS NOT NULL AND specialization <> '' "
        "ORDER BY specialization"
    )

    return render_template(
        "doctors/list.html",
        doctors=doctors,
        search=search,
        department=department,
        specialization=specialization,
        specializations=specializations,
        page=page,
        total_pages=total_pages,
        total=total,
    )


@doctors_bp.route("/new", methods=["GET", "POST"])
def new_doctor():

    if request.method == "POST":

        f = request.form

        execute(
            """
            INSERT INTO doctors
            (
                first_name,
                last_name,
                specialization,
                department,
                phone,
                email,
                status
            )

            VALUES
            (%s,%s,%s,%s,%s,%s,%s)
            """,
            (
                f["first_name"],
                f["last_name"],
                f["specialization"],
                f["department"],
                f["phone"],
                f["email"],
                f.get("status", "Active"),
            ),
        )

        flash("Doctor added successfully.", "success")

        return redirect(url_for("doctors.list_doctors"))

    return render_template("doctors/form.html", doctor=None)


@doctors_bp.route("/<int:doctor_id>")
def view_doctor(doctor_id):

    doctor = query(
        "SELECT * FROM doctors WHERE doctor_id=%s",
        (doctor_id,),
        one=True,
    )

    appointments = query(
        """
        SELECT
            a.*,
            p.first_name,
            p.last_name

        FROM appointments a

        JOIN patients p
        ON a.patient_id=p.patient_id

        WHERE doctor_id=%s

        ORDER BY appointment_date DESC
        """,
        (doctor_id,),
    )

    return render_template(
        "doctors/view.html",
        doctor=doctor,
        appointments=appointments,
    )


@doctors_bp.route("/<int:doctor_id>/edit", methods=["GET", "POST"])
def edit_doctor(doctor_id):

    if request.method == "POST":

        f = request.form

        execute(
            """
            UPDATE doctors

            SET
                first_name=%s,
                last_name=%s,
                specialization=%s,
                department=%s,
                phone=%s,
                email=%s,
                status=%s

            WHERE doctor_id=%s
            """,
            (
                f["first_name"],
                f["last_name"],
                f["specialization"],
                f["department"],
                f["phone"],
                f["email"],
                f["status"],
                doctor_id,
            ),
        )

        flash("Doctor updated.", "success")

        return redirect(
            url_for(
                "doctors.view_doctor",
                doctor_id=doctor_id,
            )
        )

    doctor = query(
        "SELECT * FROM doctors WHERE doctor_id=%s",
        (doctor_id,),
        one=True,
    )

    return render_template(
        "doctors/form.html",
        doctor=doctor,
    )


@doctors_bp.route("/<int:doctor_id>/delete", methods=["POST"])
def delete_doctor(doctor_id):

    execute(
        "DELETE FROM doctors WHERE doctor_id=%s",
        (doctor_id,),
    )

    flash("Doctor removed.", "success")

    return redirect(url_for("doctors.list_doctors"))
