from flask import Blueprint, render_template, request, redirect, url_for, flash
from datetime import date
from db import query, execute

billing_bp = Blueprint("billing", __name__, url_prefix="/billing")


@billing_bp.route("/")
def list_bills():
    status = request.args.get("status", "")
    patient = request.args.get("patient", "").strip()
    bill_no = request.args.get("bill_no", "").strip()
    date_filter = request.args.get("date", "")

    sql = """SELECT b.*, p.first_name, p.last_name
              FROM bills b JOIN patients p ON b.patient_id = p.patient_id
              WHERE 1=1"""
    params = []
    if patient:
        sql += " AND (p.first_name LIKE %s OR p.last_name LIKE %s OR CONCAT(p.first_name,' ',p.last_name) LIKE %s)"
        like = f"%{patient}%"
        params += [like, like, like]
    if bill_no:
        sql += " AND b.bill_id = %s"
        params.append(bill_no)
    if date_filter:
        sql += " AND b.bill_date = %s"
        params.append(date_filter)
    if status:
        sql += " AND b.payment_status = %s"
        params.append(status)
    sql += " ORDER BY FIELD(b.payment_status, 'Pending', 'Partially Paid', 'Paid'), b.bill_date DESC"
    all_bills = query(sql, params)

    per_page = 10
    page = request.args.get("page", 1, type=int)
    if page < 1:
        page = 1
    total = len(all_bills)
    total_pages = max(1, (total + per_page - 1) // per_page)
    if page > total_pages:
        page = total_pages
    start = (page - 1) * per_page
    bills = all_bills[start:start + per_page]

    totals = query(
        """SELECT
             COALESCE(SUM(total_amount),0) AS total_billed,
             COALESCE(SUM(CASE WHEN payment_status='Paid' THEN total_amount ELSE 0 END),0) AS total_paid,
             COALESCE(SUM(CASE WHEN payment_status!='Paid' THEN total_amount ELSE 0 END),0) AS total_due
           FROM bills""",
        one=True,
    )
    return render_template("billing/list.html", bills=bills, status=status,
                           totals=totals, patient=patient, bill_no=bill_no,
                           date_filter=date_filter,
                           page=page, total_pages=total_pages, total=total)


@billing_bp.route("/new", methods=["GET", "POST"])
def new_bill():
    if request.method == "POST":
        f = request.form
        execute(
            """INSERT INTO bills (patient_id, appointment_id, bill_date, consultation_fee,
               medicine_charges, room_charges, other_charges, payment_status, payment_method)
               VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
            (f["patient_id"], f.get("appointment_id") or None, date.today().isoformat(),
             f.get("consultation_fee", 0), f.get("medicine_charges", 0),
             f.get("room_charges", 0), f.get("other_charges", 0),
             f.get("payment_status", "Pending"), f.get("payment_method")),
        )
        flash("Invoice created.", "success")
        return redirect(url_for("billing.list_bills"))

    patients = query("SELECT patient_id, first_name, last_name FROM patients ORDER BY first_name")
    appointments = query(
        """SELECT appointment_id, patient_id, appointment_date FROM appointments
           ORDER BY appointment_date DESC"""
    )
    return render_template("billing/form.html", patients=patients, appointments=appointments)


@billing_bp.route("/<int:bill_id>/status", methods=["POST"])
def update_payment_status(bill_id):
    new_status = request.form["payment_status"]
    method = request.form.get("payment_method")
    execute("UPDATE bills SET payment_status=%s, payment_method=%s WHERE bill_id=%s",
            (new_status, method, bill_id))
    flash("Payment status updated.", "success")
    return redirect(url_for("billing.list_bills"))


@billing_bp.route("/<int:bill_id>/delete", methods=["POST"])
def delete_bill(bill_id):
    execute("DELETE FROM bills WHERE bill_id=%s", (bill_id,))
    flash("Invoice deleted.", "success")
    return redirect(url_for("billing.list_bills"))
