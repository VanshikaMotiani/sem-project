"""SQLite database initialization, schema, and realistic Nagar Nigam seed data."""

from datetime import datetime, timedelta
import json
import os
import sqlite3
from werkzeug.security import generate_password_hash

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "nagar_nigam.db")


def get_db() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def init_db() -> None:
    conn = get_db()
    cur = conn.cursor()

    cur.executescript(
        """
        CREATE TABLE IF NOT EXISTS complaints (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tracking_id TEXT UNIQUE NOT NULL,
            category_id TEXT NOT NULL,
            category_name TEXT NOT NULL,
            sub_problem_id TEXT NOT NULL,
            sub_problem_title TEXT NOT NULL,
            department TEXT NOT NULL,
            severity TEXT NOT NULL,
            duration TEXT NOT NULL,
            location_type TEXT NOT NULL,
            zone_id TEXT NOT NULL,
            zone_name TEXT NOT NULL,
            ward TEXT NOT NULL,
            landmark TEXT DEFAULT '',
            citizen_name TEXT NOT NULL,
            citizen_phone TEXT NOT NULL,
            citizen_email TEXT DEFAULT '',
            status TEXT NOT NULL DEFAULT 'Registered',
            assigned_officer TEXT NOT NULL DEFAULT 'Control Room Auto-Assigned',
            officer_remarks TEXT DEFAULT 'Complaint received and routed to concerned Zonal Wing.',
            sla_hours INTEGER NOT NULL DEFAULT 24,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS complaint_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            complaint_id INTEGER NOT NULL,
            status TEXT NOT NULL,
            remarks TEXT NOT NULL,
            updated_by TEXT NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY (complaint_id) REFERENCES complaints(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS notices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            category TEXT NOT NULL,
            department TEXT NOT NULL,
            published_date TEXT NOT NULL,
            is_new INTEGER NOT NULL DEFAULT 1,
            details TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS tenders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tender_no TEXT UNIQUE NOT NULL,
            title TEXT NOT NULL,
            department TEXT NOT NULL,
            estimated_cost TEXT NOT NULL,
            closing_date TEXT NOT NULL,
            status TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS tax_payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            receipt_no TEXT UNIQUE NOT NULL,
            assessment_id TEXT NOT NULL,
            owner_name TEXT NOT NULL,
            phone TEXT NOT NULL,
            zone_name TEXT NOT NULL,
            ward TEXT NOT NULL,
            property_type TEXT NOT NULL,
            area_sqft REAL NOT NULL,
            amount_inr REAL NOT NULL,
            payment_mode TEXT NOT NULL,
            paid_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS service_applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            application_no TEXT UNIQUE NOT NULL,
            service_type TEXT NOT NULL,
            applicant_name TEXT NOT NULL,
            phone TEXT NOT NULL,
            zone_name TEXT NOT NULL,
            ward TEXT NOT NULL,
            details_json TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Submitted',
            created_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS officers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            full_name TEXT NOT NULL,
            designation TEXT NOT NULL,
            zone_name TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS site_stats (
            id INTEGER PRIMARY KEY CHECK (id = 1),
            visitor_count INTEGER NOT NULL DEFAULT 12450,
            last_updated TEXT NOT NULL
        );
        """
    )

    # Seed site stats if empty
    if cur.execute("SELECT COUNT(*) FROM site_stats").fetchone()[0] == 0:
        cur.execute(
            "INSERT INTO site_stats (id, visitor_count, last_updated) VALUES (1, 12450, ?)",
            (datetime.now().strftime("%d %b %Y %I:%M %p"),),
        )

    # Seed officers if empty
    if cur.execute("SELECT COUNT(*) FROM officers").fetchone()[0] == 0:
        officers = [
            (
                "admin",
                generate_password_hash("nagar123"),
                "Sh. Arvind Kulkarni",
                "Nodal Officer & Dy. Director (IT)",
                "All Zones (HQ)",
            ),
            (
                "wardofficer",
                generate_password_hash("ward123"),
                "Sh. Rajendra Sharma",
                "Zonal Commissioner",
                "Central Zone (Zone 1)",
            ),
        ]
        cur.executemany(
            "INSERT INTO officers (username, password_hash, full_name, designation, zone_name) VALUES (?, ?, ?, ?, ?)",
            officers,
        )

    # Seed notices & public news if empty
    if cur.execute("SELECT COUNT(*) FROM notices").fetchone()[0] == 0:
        notices = [
            (
                "Gazette Notification of Ward Delimitation 2026 — Zones 1 to 7",
                "Important Notice",
                "Election & Delimitation Cell",
                "25 Nov 2026",
                1,
                "Updated ward boundary maps and ward office schedules across all 150 wards are now available under the Ward & Zone Directory.",
            ),
            (
                "Special Swachhata & Door-to-Door Waste Segregation Drive Across All 150 Wards",
                "Public News",
                "Swachhata & Health Wing",
                "24 Nov 2026",
                1,
                "Citizens are requested to segregate wet and dry waste before handing over to morning Nagar Nigam tipper vans. Helpline: 14420.",
            ),
            (
                "Online Urban Development (UD) Tax Rebate — 10% Early Payment Discount Extended",
                "Public News",
                "Revenue & Tax Branch",
                "22 Nov 2026",
                1,
                "Residential and commercial property owners paying annual UD/House Tax online before 31 December receive an instant 10% rebate.",
            ),
            (
                "Dairy Booth Monthly Rent & Smart Kiosk Renewal Schedule (FY 2026–27)",
                "Important Notice",
                "Estate & Licensing Branch",
                "20 Nov 2026",
                1,
                "All authorized dairy booth operators can submit renewal requests and pay monthly rent online via the Citizen Services portal.",
            ),
            (
                "NCAP Dust Mitigation & Green Belt Plantation Circular for Construction Sites",
                "Important Notice",
                "NCAP Environment Cell",
                "18 Nov 2026",
                0,
                "All construction sites above 500 sq. m. must install green net covering and water sprinklers to curb PM10/PM2.5 dust.",
            ),
            (
                "Mandatory Pet Dog & Cat Vaccination Registration Drive — Free Anti-Rabies Camp",
                "Public News",
                "Veterinary & Cattle Pound Cell",
                "15 Nov 2026",
                0,
                "Pet owners can register dogs and cats online and avail free vaccination at Zonal Veterinary Centers.",
            ),
        ]
        cur.executemany(
            "INSERT INTO notices (title, category, department, published_date, is_new, details) VALUES (?, ?, ?, ?, ?, ?)",
            notices,
        )

    # Seed tenders if empty
    if cur.execute("SELECT COUNT(*) FROM tenders").fetchone()[0] == 0:
        tenders = [
            (
                "NMC/ELC/2026/104",
                "Supply, Installation & Maintenance of 2,500 Smart LED Street Lights in South & Industrial Zones",
                "Electrical & Street Light Cell",
                "₹ 1,45,00,000",
                "12 Dec 2026",
                "Open",
            ),
            (
                "NMC/SWM/2026/089",
                "Procurement of 40 Hydraulic CNG Auto-Tippers for Door-to-Door Garbage Collection",
                "Swachhata & Health Wing",
                "₹ 3,20,00,000",
                "18 Dec 2026",
                "Open",
            ),
            (
                "NMC/CIV/2026/211",
                "Resurfacing of Arterial Roads & Interlocking Paver Footpaths in Central Zone Wards 1–12",
                "Civil Engineering Wing",
                "₹ 2,10,50,000",
                "05 Dec 2026",
                "Open",
            ),
            (
                "NMC/AUC/2026/032",
                "e-Auction of Commercial Parking Lots & Municipal Kiosks (North & Main Market Zones)",
                "Estate & e-Auction Cell",
                "₹ 65,00,000",
                "28 Nov 2026",
                "Closing Soon",
            ),
        ]
        cur.executemany(
            "INSERT INTO tenders (tender_no, title, department, estimated_cost, closing_date, status) VALUES (?, ?, ?, ?, ?, ?)",
            tenders,
        )

    # Seed sample complaints if empty
    if cur.execute("SELECT COUNT(*) FROM complaints").fetchone()[0] == 0:
        now = datetime.now()
        samples = [
            (
                "NMC-2026-000101",
                "sanitation",
                "Sanitation & Solid Waste",
                "san-02",
                "Overflowing community dustbin / garbage point",
                "Swachhata & Health Wing",
                "High",
                "Since 2–3 Days",
                "Public Market / Bazaar",
                "market-zone",
                "Main Market & Civic Zone (Zone 7)",
                "Ward 128 - Market Circle 3",
                "Near Main Bazaar Gate",
                "Ramesh Gupta",
                "9829011223",
                "ramesh.g@example.com",
                "In Progress",
                "Sanitary Inspector — Ward 128",
                "Compactor vehicle dispatched for immediate clearance and sanitization.",
                12,
                (now - timedelta(hours=18)).strftime("%Y-%m-%d %H:%M"),
                (now - timedelta(hours=3)).strftime("%Y-%m-%d %H:%M"),
            ),
            (
                "NMC-2026-000102",
                "streetlights",
                "Street Lights & Electrical",
                "elc-02",
                "Entire stretch of colony street lights off (Phase fault)",
                "Electrical & Street Light Cell",
                "High",
                "Happened Today",
                "Residential Colony / Lane",
                "south-zone",
                "South Zone (Zone 3)",
                "Ward 45 - South Block E",
                "Sector 4 Main Lane",
                "Ananya Sharma",
                "9829044556",
                "ananya.s@example.com",
                "Assigned to Ward Officer",
                "Junior Engineer (Electrical) — South Zone",
                "Assigned to night-shift electrical maintenance van for feeder check.",
                24,
                (now - timedelta(hours=6)).strftime("%Y-%m-%d %H:%M"),
                (now - timedelta(hours=2)).strftime("%Y-%m-%d %H:%M"),
            ),
            (
                "NMC-2026-000103",
                "water-sewer",
                "Water Supply & Sewerage",
                "wat-02",
                "Broken, missing, or sunken manhole cover (Safety hazard)",
                "Public Health & Sewerage Engineering",
                "Emergency",
                "Happened Today",
                "Main Arterial Road",
                "central-zone",
                "Central Zone (Zone 1)",
                "Ward 5 - Central Sector 5",
                "Near Civic Pillar 42",
                "Suresh Pareek",
                "9829077889",
                "",
                "Resolved",
                "AEN Sewerage — Central Zone",
                "New heavy-duty RCC manhole cover installed and barricading removed.",
                6,
                (now - timedelta(days=2)).strftime("%Y-%m-%d %H:%M"),
                (now - timedelta(days=1)).strftime("%Y-%m-%d %H:%M"),
            ),
        ]
        for row in samples:
            cur.execute(
                """
                INSERT INTO complaints (
                    tracking_id, category_id, category_name, sub_problem_id, sub_problem_title,
                    department, severity, duration, location_type, zone_id, zone_name, ward,
                    landmark, citizen_name, citizen_phone, citizen_email, status,
                    assigned_officer, officer_remarks, sla_hours, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                row,
            )
            cid = cur.lastrowid
            cur.execute(
                "INSERT INTO complaint_history (complaint_id, status, remarks, updated_by, created_at) VALUES (?, ?, ?, ?, ?)",
                (cid, "Registered", "Complaint registered online via Nagar Nigam e-Samadhan.", row[13], row[20]),
            )
            if row[16] != "Registered":
                cur.execute(
                    "INSERT INTO complaint_history (complaint_id, status, remarks, updated_by, created_at) VALUES (?, ?, ?, ?, ?)",
                    (cid, row[16], row[18], row[17], row[21]),
                )

    conn.commit()
    conn.close()


def increment_visitor_count() -> dict:
    conn = get_db()
    conn.execute("UPDATE site_stats SET visitor_count = visitor_count + 1 WHERE id = 1")
    conn.commit()
    row = conn.execute("SELECT visitor_count, last_updated FROM site_stats WHERE id = 1").fetchone()
    conn.close()
    return dict(row) if row else {"visitor_count": 12450, "last_updated": datetime.now().strftime("%d %b %Y %I:%M %p")}


def get_site_stats() -> dict:
    conn = get_db()
    row = conn.execute("SELECT visitor_count, last_updated FROM site_stats WHERE id = 1").fetchone()
    conn.close()
    return dict(row) if row else {"visitor_count": 12450, "last_updated": datetime.now().strftime("%d %b %Y %I:%M %p")}


def parse_details(details_json: str) -> dict:
    try:
        return json.loads(details_json)
    except Exception:
        return {}
