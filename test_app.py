"""Automated end-to-end verification tests for Nagar Nigam Flask Portal."""

import os
import re
import tempfile
import unittest

import db
from app import app


class NagarNigamPortalTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._tmp_dir = tempfile.TemporaryDirectory()
        db.DB_PATH = os.path.join(cls._tmp_dir.name, "test_nagar_nigam.db")
        db.init_db()
        app.config["TESTING"] = True
        cls.client = app.test_client()

    @classmethod
    def tearDownClass(cls):
        cls._tmp_dir.cleanup()

    def test_public_pages_render(self):
        for path in [
            "/",
            "/register-complaint",
            "/track-complaint",
            "/pay-tax",
            "/services/registration",
            "/notices",
            "/tenders",
            "/wards",
            "/aqi",
            "/faqs",
            "/contact",
            "/officer/login",
        ]:
            resp = self.client.get(path)
            self.assertEqual(resp.status_code, 200, f"Expected 200 for {path}")

    def test_api_endpoints(self):
        resp = self.client.get("/api/sub-problems/sanitation")
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertEqual(data["id"], "sanitation")
        self.assertGreaterEqual(len(data["sub_problems"]), 5)

        resp_wards = self.client.get("/api/wards/civil-lines")
        self.assertEqual(resp_wards.status_code, 200)
        self.assertEqual(len(resp_wards.get_json()["wards"]), 20)

    def test_zero_typing_complaint_registration_and_officer_update(self):
        resp = self.client.post(
            "/register-complaint",
            data={
                "category_id": "streetlights",
                "sub_problem_id": "elc-02",
                "severity": "High",
                "duration": "Happened Today",
                "location_type": "Residential Colony / Lane",
                "zone_id": "malviya-nagar",
                "ward": "Ward 45 - Malviya Nagar Block E",
                "landmark": "",
                "citizen_name": "Test Citizen",
                "citizen_phone": "9876543210",
                "citizen_email": "",
            },
            follow_redirects=True,
        )
        self.assertEqual(resp.status_code, 200)
        html = resp.get_data(as_text=True)
        match = re.search(r"NNJ-\d{4}-\d{6}", html)
        self.assertIsNotNone(match, "Tracking ID should appear on confirmation page")
        tracking_id = match.group(0)

        # Officer login
        login_resp = self.client.post(
            "/officer/login",
            data={"username": "admin", "password": "nagar123"},
            follow_redirects=True,
        )
        self.assertEqual(login_resp.status_code, 200)
        self.assertIn("Municipal Officer Dashboard", login_resp.get_data(as_text=True))

        # Officer updates complaint status
        upd_resp = self.client.post(
            f"/officer/complaint/{tracking_id}/update",
            data={
                "status": "Resolved",
                "assigned_officer": "JEN Electrical Test",
                "remarks": "Feeder fuse replaced and lights verified ON.",
            },
            follow_redirects=True,
        )
        self.assertEqual(upd_resp.status_code, 200)
        self.assertIn("Resolved", upd_resp.get_data(as_text=True))

        # Citizen tracks updated status
        track_resp = self.client.get(f"/complaint/{tracking_id}")
        self.assertEqual(track_resp.status_code, 200)
        self.assertIn("Feeder fuse replaced and lights verified ON.", track_resp.get_data(as_text=True))

    def test_tax_payment_and_service_application(self):
        resp = self.client.post(
            "/pay-tax",
            data={
                "assessment_id": "JMC-TEST-909",
                "owner_name": "Vanshika Test",
                "phone": "9812345678",
                "zone_id": "civil-lines",
                "ward": "Ward 1 - Civil Lines Sector 1",
                "property_type": "Residential",
                "area_sqft": "1000",
                "payment_mode": "UPI / BharatQR",
            },
            follow_redirects=True,
        )
        self.assertEqual(resp.status_code, 200)
        self.assertIn("Official Urban Development / Property Tax E-Receipt", resp.get_data(as_text=True))
        self.assertIn("1125.00", resp.get_data(as_text=True))

        srv_resp = self.client.post(
            "/services/registration",
            data={
                "service_type": "Pet Registration",
                "category_option": "New Registration",
                "applicant_name": "Vanshika Test",
                "phone": "9812345678",
                "zone_id": "civil-lines",
                "ward": "Ward 1 - Civil Lines Sector 1",
                "subject_name": "Bruno",
            },
            follow_redirects=True,
        )
        self.assertEqual(srv_resp.status_code, 200)
        self.assertIn("Application submitted!", srv_resp.get_data(as_text=True))


if __name__ == "__main__":
    unittest.main(verbosity=2)
