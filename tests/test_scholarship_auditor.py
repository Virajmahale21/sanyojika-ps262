"""
Unit tests for Scholarship Disbursement & DBT Anomaly Auditor.
"""

import unittest
from ai_engine.scholarship_auditor import audit_scholarship_claims


class TestScholarshipAuditor(unittest.TestCase):
    def test_clean_claims_pass(self):
        claims = [
            {"student_roll_no": "2026-CS-01", "bank_account_no": "1122334455", "scheme": "PRAGATI"},
            {"student_roll_no": "2026-CS-02", "bank_account_no": "9988776655", "scheme": "GATE_PG"}
        ]
        valid_rolls = ["2026-CS-01", "2026-CS-02", "2026-CS-03"]
        res = audit_scholarship_claims("1-1049281", claims, valid_rolls)
        self.assertEqual(res["dbt_audit_status"], "PASSED")
        self.assertEqual(len(res["anomalies_detected"]), 0)

    def test_shared_bank_account_flagged(self):
        claims = [
            {"student_roll_no": "2026-CS-01", "bank_account_no": "1122334455", "scheme": "PRAGATI"},
            {"student_roll_no": "2026-CS-02", "bank_account_no": "1122334455", "scheme": "PRAGATI"}
        ]
        valid_rolls = ["2026-CS-01", "2026-CS-02"]
        res = audit_scholarship_claims("1-1049281", claims, valid_rolls)
        self.assertEqual(res["dbt_audit_status"], "SUSPICIOUS_DBT_DISBURSEMENT")
        self.assertEqual(res["anomalies_detected"][0]["type"], "SHARED_BANK_ACCOUNT_ACROSS_STUDENTS")


if __name__ == "__main__":
    unittest.main()
