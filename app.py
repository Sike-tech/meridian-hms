import pandas as pd
from flask import Flask, render_template, redirect, url_for
from config import SECRET_KEY
from db import query
from modules.patients import patients_bp
from modules.doctors import doctors_bp
from modules.appointments import appointments_bp
from modules.billing import billing_bp
from modules.analytics import analytics_bp, compute_kpis


def create_app():
    app = Flask(__name__)
    app.secret_key = SECRET_KEY

    app.register_blueprint(patients_bp)
    app.register_blueprint(doctors_bp)
    app.register_blueprint(appointments_bp)
    app.register_blueprint(billing_bp)
    app.register_blueprint(analytics_bp)

    @app.context_processor
    def inject_employee():
        return {
            "employee_name": "Dr. Sarang Vishnu",
            "employee_role": "Owner",
        }

    @app.route("/")
    def home():
        return render_template("home.html")

    @app.route("/logout")
    def logout():
        return redirect(url_for("home"))

    @app.errorhandler(404)
    def not_found(e):
        return render_template("404.html"), 404

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5000)
