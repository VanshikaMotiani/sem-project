"""Nagar Nigam Municipal Corporation Web Portal — Python / Flask Backend."""

from datetime import datetime
from functools import wraps
import json
import os
import random
from flask import (
    Flask,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from werkzeug.security import check_password_hash

from catalog import (
    DURATION_OPTIONS,
    LOCATION_TYPE_OPTIONS,
    PROBLEM_CATEGORIES,
    QUICK_SERVICE_TILES,
    SEVERITY_OPTIONS,
    STATUS_FLOW,
    ZONES,
    get_category_by_id,
    get_sub_problem,
    get_zone_by_id,
)
from db import get_db, get_site_stats, increment_visitor_count, init_db, parse_details

app = Flask(__name__, template_folder="template")
app.secret_key = os.environ.get("NMC_SECRET_KEY", "nagar-nigam-civic-portal-semester-project-2026")

# Ensure SQLite DB and seed data are ready on startup
init_db()


@app.context_processor
def inject_globals():
    stats = get_site_stats()
    return {
        "site_stats": stats,
        "current_year": datetime.now().year,
        "officer_user": session.get("officer"),
    }


def officer_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not session.get("officer"):
            flash("Please sign in with your Municipal Officer credentials.", "warning")
            return redirect(url_for("officer_login"))
        return fn(*args, **kwargs)

    return wrapper


def _generate_tracking_id(conn) -> str:
    row = conn.execute("SELECT MAX(id) AS max_id FROM complaints").fetchone()
    next_num = (row["max_id"] or 100) + 101
    return f"NMC-{datetime.now().year}-{next_num:06d}"


@app.route("/")
def home():
    if not session.get("visited"):
        session["visited"] = True
        stats = increment_visitor_count()
    else:
        stats = get_site_stats()

    conn = get_db()
    public_news = conn.execute(
        "SELECT * FROM notices WHERE category = 'Public News' ORDER BY id DESC LIMIT 8"
    ).fetchall()
    important_notices = conn.execute(
        "SELECT * FROM notices WHERE category = 'Important Notice' ORDER BY id DESC LIMIT 8"
    ).fetchall()
    total_complaints = conn.execute("SELECT COUNT(*) FROM complaints").fetchone()[0]
    resolved_complaints = conn.execute(
        "SELECT COUNT(*) FROM complaints WHERE status IN ('Resolved', 'Closed')"
    ).fetchone()[0]
    conn.close()

    return render_template(
        "index.html",
        quick_tiles=QUICK_SERVICE_TILES,
        categories=PROBLEM_CATEGORIES,
        public_news=public_news,
        important_notices=important_notices,
        total_complaints=total_complaints,
        resolved_complaints=resolved_complaints,
        site_stats=stats,
    )


@app.route("/register-complaint", methods=["GET", "POST"])
def register_complaint():
    preselected_cat = request.args.get("category", "")
    if request.method == "POST":
        category_id = request.form.get("category_id", "").strip()
        sub_problem_id = request.form.get("sub_problem_id", "").strip()
        severity = request.form.get("severity", "Medium").strip()
        duration = request.form.get("duration", DURATION_OPTIONS[0]).strip()
        location_type = request.form.get("location_type", LOCATION_TYPE_OPTIONS[0]).strip()
        zone_id = request.form.get("zone_id", "").strip()
        ward = request.form.get("ward", "").strip()
        landmark = request.form.get("landmark", "").strip()
        citizen_name = request.form.get("citizen_name", "").strip()
        citizen_phone = request.form.get("citizen_phone", "").strip()
        citizen_email = request.form.get("citizen_email", "").strip()

        cat, sub = get_sub_problem(category_id, sub_problem_id)
        zone = get_zone_by_id(zone_id)

        errors = []
        if not cat:
            errors.append("Please select a problem category.")
        if not sub:
            errors.append("Please select the specific problem from the list.")
        if not zone:
            errors.append("Please select your Municipal Zone.")
        if not ward:
            errors.append("Please select your Ward.")
        if not citizen_name or len(citizen_name) < 2:
            errors.append("Please enter your full name.")
        if not citizen_phone.isdigit() or len(citizen_phone) != 10:
            errors.append("Please enter a valid 10-digit mobile number.")

        if errors:
            for err in errors:
                flash(err, "danger")
            return render_template(
                "register_complaint.html",
                categories=PROBLEM_CATEGORIES,
                zones=ZONES,
                severities=SEVERITY_OPTIONS,
                durations=DURATION_OPTIONS,
                location_types=LOCATION_TYPE_OPTIONS,
                preselected_cat=category_id,
                form_data=request.form,
            )

        now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
        conn = get_db()
        tracking_id = _generate_tracking_id(conn)
        sla_hours = sub.get("sla_hours", cat.get("sla_hours", 24))
        auto_remark = (
            f"Registered under {cat['department']} ({zone['name']}). "
            f"Expected SLA resolution: {sla_hours} hours."
        )

        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO complaints (
                tracking_id, category_id, category_name, sub_problem_id, sub_problem_title,
                department, severity, duration, location_type, zone_id, zone_name, ward,
                landmark, citizen_name, citizen_phone, citizen_email, status,
                assigned_officer, officer_remarks, sla_hours, created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                tracking_id,
                cat["id"],
                cat["name"],
                sub["id"],
                sub["title"],
                cat["department"],
                severity,
                duration,
                location_type,
                zone["id"],
                zone["name"],
                ward,
                landmark,
                citizen_name,
                citizen_phone,
                citizen_email,
                "Registered",
                zone["officer"],
                auto_remark,
                sla_hours,
                now_str,
                now_str,
            ),
        )
        cid = cur.lastrowid
        cur.execute(
            "INSERT INTO complaint_history (complaint_id, status, remarks, updated_by, created_at) VALUES (?, ?, ?, ?, ?)",
            (cid, "Registered", auto_remark, citizen_name, now_str),
        )
        conn.commit()
        conn.close()

        flash(f"Grievance registered successfully! Tracking ID: {tracking_id}", "success")
        return redirect(url_for("complaint_detail", tracking_id=tracking_id, new=1))

    return render_template(
        "register_complaint.html",
        categories=PROBLEM_CATEGORIES,
        zones=ZONES,
        severities=SEVERITY_OPTIONS,
        durations=DURATION_OPTIONS,
        location_types=LOCATION_TYPE_OPTIONS,
        preselected_cat=preselected_cat,
        form_data={},
    )


@app.route("/api/sub-problems/<category_id>")
def api_sub_problems(category_id):
    cat = get_category_by_id(category_id)
    if not cat:
        return jsonify({"error": "Category not found"}), 404
    return jsonify(cat)


@app.route("/api/wards/<zone_id>")
def api_wards(zone_id):
    zone = get_zone_by_id(zone_id)
    if not zone:
        return jsonify({"error": "Zone not found"}), 404
    return jsonify({"zone": zone["name"], "wards": zone["wards"], "officer": zone["officer"]})


@app.route("/track-complaint")
def track_complaint():
    query = request.args.get("q", "").strip()
    results = []
    if query:
        conn = get_db()
        results = conn.execute(
            """
            SELECT * FROM complaints
            WHERE UPPER(tracking_id) = UPPER(?) OR citizen_phone = ?
            ORDER BY id DESC
            """,
            (query, query),
        ).fetchall()
        conn.close()
        if len(results) == 1 and query.upper().startswith("NMC-"):
            return redirect(url_for("complaint_detail", tracking_id=results[0]["tracking_id"]))
    else:
        conn = get_db()
        results = conn.execute(
            "SELECT * FROM complaints ORDER BY id DESC LIMIT 5"
        ).fetchall()
        conn.close()

    return render_template("track_complaint.html", query=query, results=results)


@app.route("/complaint/<tracking_id>")
def complaint_detail(tracking_id):
    conn = get_db()
    complaint = conn.execute(
        "SELECT * FROM complaints WHERE UPPER(tracking_id) = UPPER(?)", (tracking_id,)
    ).fetchone()
    if not complaint:
        conn.close()
        flash(f"No complaint found with Tracking ID '{tracking_id}'.", "danger")
        return redirect(url_for("track_complaint"))

    history = conn.execute(
        "SELECT * FROM complaint_history WHERE complaint_id = ? ORDER BY id ASC",
        (complaint["id"],),
    ).fetchall()
    conn.close()

    is_new = request.args.get("new") == "1"
    return render_template(
        "complaint_detail.html",
        complaint=complaint,
        history=history,
        status_flow=STATUS_FLOW,
        is_new=is_new,
    )


@app.route("/pay-tax", methods=["GET", "POST"])
def pay_tax():
    if request.method == "POST":
        assessment_id = request.form.get("assessment_id", "").strip()
        owner_name = request.form.get("owner_name", "").strip()
        phone = request.form.get("phone", "").strip()
        zone_id = request.form.get("zone_id", "").strip()
        ward = request.form.get("ward", "").strip()
        property_type = request.form.get("property_type", "Residential").strip()
        area_raw = request.form.get("area_sqft", "0").strip()
        payment_mode = request.form.get("payment_mode", "UPI / QR").strip()

        zone = get_zone_by_id(zone_id)
        try:
            area_sqft = float(area_raw)
        except ValueError:
            area_sqft = 0

        if not assessment_id or not owner_name or not phone.isdigit() or len(phone) != 10 or not zone or not ward or area_sqft <= 0:
            flash("Please complete all property tax fields with valid details.", "danger")
            return render_template("pay_tax.html", zones=ZONES)

        rate_map = {"Residential": 1.25, "Commercial": 3.50, "Industrial": 2.75, "Vacant Plot": 0.90}
        rate = rate_map.get(property_type, 1.25)
        base_tax = round(area_sqft * rate, 2)
        rebate = round(base_tax * 0.10, 2)
        total_paid = round(max(250.0, base_tax - rebate), 2)

        conn = get_db()
        receipt_no = f"TAX-{datetime.now().year}-{random.randint(100000, 999999)}"
        paid_at = datetime.now().strftime("%Y-%m-%d %H:%M")
        conn.execute(
            """
            INSERT INTO tax_payments (
                receipt_no, assessment_id, owner_name, phone, zone_name, ward,
                property_type, area_sqft, amount_inr, payment_mode, paid_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                receipt_no,
                assessment_id,
                owner_name,
                phone,
                zone["name"],
                ward,
                property_type,
                area_sqft,
                total_paid,
                payment_mode,
                paid_at,
            ),
        )
        conn.commit()
        conn.close()
        flash(f"Property Tax payment successful! Receipt No: {receipt_no}", "success")
        return redirect(url_for("tax_receipt", receipt_no=receipt_no))

    return render_template("pay_tax.html", zones=ZONES)


@app.route("/tax-receipt/<receipt_no>")
def tax_receipt(receipt_no):
    conn = get_db()
    receipt = conn.execute(
        "SELECT * FROM tax_payments WHERE receipt_no = ?", (receipt_no,)
    ).fetchone()
    conn.close()
    if not receipt:
        flash("Tax receipt not found.", "danger")
        return redirect(url_for("pay_tax"))
    return render_template("tax_receipt.html", receipt=receipt)


@app.route("/services/registration", methods=["GET", "POST"])
def service_registration():
    selected_type = request.args.get("type", "Birth Certificate")
    service_types = [
        "Birth Certificate",
        "Death Certificate",
        "Trade License",
        "Meat License Registration",
        "Dairy Booth Permit",
        "Pet Registration",
    ]
    conn = get_db()

    if request.method == "POST":
        service_type = request.form.get("service_type", "Birth Certificate").strip()
        applicant_name = request.form.get("applicant_name", "").strip()
        phone = request.form.get("phone", "").strip()
        zone_id = request.form.get("zone_id", "").strip()
        ward = request.form.get("ward", "").strip()
        category_option = request.form.get("category_option", "New Registration").strip()
        subject_name = request.form.get("subject_name", "").strip()

        zone = get_zone_by_id(zone_id)
        if not applicant_name or not phone.isdigit() or len(phone) != 10 or not zone or not ward:
            flash("Please select zone/ward and enter valid applicant details.", "danger")
        else:
            app_no = f"SRV-{datetime.now().year}-{random.randint(10000, 99999)}"
            details = json.dumps(
                {
                    "application_category": category_option,
                    "subject_or_business_name": subject_name or "Standard Request",
                }
            )
            conn.execute(
                """
                INSERT INTO service_applications (
                    application_no, service_type, applicant_name, phone, zone_name, ward, details_json, status, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    app_no,
                    service_type,
                    applicant_name,
                    phone,
                    zone["name"],
                    ward,
                    details,
                    "Submitted for Verification",
                    datetime.now().strftime("%Y-%m-%d %H:%M"),
                ),
            )
            conn.commit()
            flash(f"Application submitted! Reference No: {app_no}", "success")
            selected_type = service_type

    recent_apps = conn.execute(
        "SELECT * FROM service_applications ORDER BY id DESC LIMIT 6"
    ).fetchall()
    conn.close()

    parsed_apps = []
    for row in recent_apps:
        item = dict(row)
        item["details"] = parse_details(row["details_json"])
        parsed_apps.append(item)

    return render_template(
        "service_registration.html",
        service_types=service_types,
        selected_type=selected_type,
        zones=ZONES,
        recent_apps=parsed_apps,
    )


@app.route("/notices")
def notices():
    category_filter = request.args.get("category", "All")
    conn = get_db()
    if category_filter in ("Public News", "Important Notice"):
        rows = conn.execute(
            "SELECT * FROM notices WHERE category = ? ORDER BY id DESC", (category_filter,)
        ).fetchall()
    else:
        rows = conn.execute("SELECT * FROM notices ORDER BY id DESC").fetchall()
    conn.close()
    return render_template("notices.html", notices=rows, category_filter=category_filter)


@app.route("/tenders")
def tenders():
    conn = get_db()
    rows = conn.execute("SELECT * FROM tenders ORDER BY id DESC").fetchall()
    conn.close()
    return render_template("tenders.html", tenders=rows)


@app.route("/wards")
def wards():
    return render_template("wards.html", zones=ZONES)


@app.route("/aqi")
def aqi():
    stations = [
        {"station": "Central Civic Square (CAAQMS)", "aqi": 112, "pm25": 43, "pm10": 98, "status": "Moderate"},
        {"station": "North Enclave Sector 2", "aqi": 96, "pm25": 36, "pm10": 84, "status": "Satisfactory"},
        {"station": "West Residential Colony", "aqi": 124, "pm25": 49, "pm10": 116, "status": "Moderate"},
        {"station": "Industrial Zone Phase 1", "aqi": 158, "pm25": 64, "pm10": 144, "status": "Moderate"},
        {"station": "South Green Belt Park", "aqi": 84, "pm25": 31, "pm10": 75, "status": "Satisfactory"},
        {"station": "Main Market Circle", "aqi": 138, "pm25": 55, "pm10": 129, "status": "Moderate"},
    ]
    return render_template("aqi.html", stations=stations)


@app.route("/faqs")
def faqs():
    return render_template("faqs.html", categories=PROBLEM_CATEGORIES)


@app.route("/contact")
def contact():
    return render_template("contact.html", zones=ZONES)


@app.route("/officer/login", methods=["GET", "POST"])
def officer_login():
    if session.get("officer"):
        return redirect(url_for("officer_dashboard"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        conn = get_db()
        user = conn.execute("SELECT * FROM officers WHERE username = ?", (username,)).fetchone()
        conn.close()

        if user and check_password_hash(user["password_hash"], password):
            session["officer"] = {
                "username": user["username"],
                "full_name": user["full_name"],
                "designation": user["designation"],
                "zone_name": user["zone_name"],
            }
            flash(f"Welcome, {user['full_name']}!", "success")
            return redirect(url_for("officer_dashboard"))

        flash("Invalid username or password.", "danger")

    return render_template("officer_login.html")


@app.route("/officer/logout")
def officer_logout():
    session.pop("officer", None)
    flash("You have been logged out of the Officer Portal.", "info")
    return redirect(url_for("home"))


@app.route("/officer/dashboard")
@officer_required
def officer_dashboard():
    status_filter = request.args.get("status", "All")
    category_filter = request.args.get("category", "All")
    zone_filter = request.args.get("zone", "All")

    conn = get_db()
    query = "SELECT * FROM complaints WHERE 1=1"
    params = []
    if status_filter != "All":
        query += " AND status = ?"
        params.append(status_filter)
    if category_filter != "All":
        query += " AND category_id = ?"
        params.append(category_filter)
    if zone_filter != "All":
        query += " AND zone_id = ?"
        params.append(zone_filter)
    query += " ORDER BY id DESC"

    complaints = conn.execute(query, params).fetchall()
    counts = {
        "total": conn.execute("SELECT COUNT(*) FROM complaints").fetchone()[0],
        "registered": conn.execute("SELECT COUNT(*) FROM complaints WHERE status = 'Registered'").fetchone()[0],
        "in_progress": conn.execute(
            "SELECT COUNT(*) FROM complaints WHERE status IN ('Assigned to Ward Officer', 'In Progress')"
        ).fetchone()[0],
        "resolved": conn.execute(
            "SELECT COUNT(*) FROM complaints WHERE status IN ('Resolved', 'Closed')"
        ).fetchone()[0],
    }
    conn.close()

    return render_template(
        "officer_dashboard.html",
        complaints=complaints,
        counts=counts,
        categories=PROBLEM_CATEGORIES,
        zones=ZONES,
        status_flow=STATUS_FLOW,
        status_filter=status_filter,
        category_filter=category_filter,
        zone_filter=zone_filter,
    )


@app.route("/officer/complaint/<tracking_id>/update", methods=["POST"])
@officer_required
def officer_update_complaint(tracking_id):
    new_status = request.form.get("status", "In Progress").strip()
    assigned_officer = request.form.get("assigned_officer", "").strip()
    remarks = request.form.get("remarks", "").strip()

    if new_status not in STATUS_FLOW:
        flash("Invalid status value.", "danger")
        return redirect(url_for("officer_dashboard"))

    conn = get_db()
    complaint = conn.execute(
        "SELECT * FROM complaints WHERE tracking_id = ?", (tracking_id,)
    ).fetchone()
    if not complaint:
        conn.close()
        flash("Complaint not found.", "danger")
        return redirect(url_for("officer_dashboard"))

    now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
    officer_name = session["officer"]["full_name"]
    final_assigned = assigned_officer or complaint["assigned_officer"]
    final_remarks = remarks or f"Status updated to {new_status} by {officer_name}."

    conn.execute(
        """
        UPDATE complaints
        SET status = ?, assigned_officer = ?, officer_remarks = ?, updated_at = ?
        WHERE id = ?
        """,
        (new_status, final_assigned, final_remarks, now_str, complaint["id"]),
    )
    conn.execute(
        "INSERT INTO complaint_history (complaint_id, status, remarks, updated_by, created_at) VALUES (?, ?, ?, ?, ?)",
        (complaint["id"], new_status, final_remarks, officer_name, now_str),
    )
    conn.commit()
    conn.close()

    flash(f"Complaint {tracking_id} updated to '{new_status}'.", "success")
    return redirect(url_for("officer_dashboard"))


@app.route("/officer/notices/add", methods=["POST"])
@officer_required
def officer_add_notice():
    title = request.form.get("title", "").strip()
    category = request.form.get("category", "Public News").strip()
    department = request.form.get("department", "Nagar Nigam Administration").strip()
    details = request.form.get("details", "").strip()

    if not title or not details:
        flash("Please provide notice title and details.", "danger")
        return redirect(url_for("officer_dashboard"))

    conn = get_db()
    conn.execute(
        "INSERT INTO notices (title, category, department, published_date, is_new, details) VALUES (?, ?, ?, ?, 1, ?)",
        (title, category, department, datetime.now().strftime("%d %b %Y"), details),
    )
    conn.commit()
    conn.close()
    flash("New municipal notice published to homepage!", "success")
    return redirect(url_for("officer_dashboard"))


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True, use_reloader=False)
