# Nagar Nigam Municipal Corporation Portal (JaipurMC Style)

A full-stack **Python (Flask) + SQLite** municipal corporation web portal modeled after the **Nagar Nigam Jaipur (`jaipurmc.org`)** design system and **Samadhan Public Grievance Portal**.

## Key Features
- **Zero-Typing Problem Selection (`/register-complaint`)**: Citizens never have to write out their complaint. They choose from **8 Municipal Departments** and **52+ predefined civic sub-problems** (Sanitation, Water & Sewerage, Street Lights, Roads & Encroachment, Stray Animals & Fogging, Parks & Environment, Building/Tax/Certificates, Public Health), along with clickable Severity, Duration, and Location Type chips, and dynamic Zone/Ward (150 wards) selection.
- **Live Grievance Tracking (`/track-complaint`)**: Track any complaint by Tracking ID (`NNJ-2026-XXXXXX`) or 10-digit mobile number with a printable receipt and step-by-step resolution timeline.
- **JaipurMC-Inspired UI**: Top accessibility bar (`+A`, `A`, `-A`, high-contrast theme toggle), navy-to-cyan gradient navbar, hero carousel, 6×2 quick-access service grid, `About Us` 3×2 card grid, `Public News` & `Important Notices` tickers, and heritage-styled footer with live visitor counter.
- **Online Municipal Services**:
  - **Property / UD Tax Calculator & E-Receipt (`/pay-tax`)**
  - **Birth, Death, Trade/Meat License, Dairy Booth & Pet Registration (`/services/registration`)**
  - **Tenders & e-Auctions (`/tenders`)**, **Public Notices (`/notices`)**, **150 Ward Directory (`/wards`)**, **CAAQMS Air Quality Index (`/aqi`)**
- **Officer Resolution Dashboard (`/officer/login`)**:
  - Demo Nodal Admin: `admin` / `nagar123`
  - Demo Ward Officer: `wardofficer` / `ward123`
  - Filter complaints by Status, Category, or Zone, update resolution status & remarks, and publish new Public News / Notices to the homepage.

## Project Structure
- `app.py` — Flask routes, session authentication, JSON APIs, and grievance workflow
- `catalog.py` — Predefined 8 categories, 52+ sub-problems, 7 zones, 150 wards, SLA hours
- `db.py` — SQLite schema (`nagar_nigam.db`) and initial seed data
- `templates/` — Jinja2 HTML templates (`base.html`, `index.html`, `register_complaint.html`, etc.)
- `static/` — `css/style.css` and `js/main.js`
- `test_app.py` — Automated backend route & workflow tests

## How to Run Locally
```powershell
cd C:\Users\Vanshika\.gemini\antigravity\scratch\nagar-nigam-portal
.\.venv\Scripts\python.exe app.py
```
Then open `http://127.0.0.1:5000` in your browser.
