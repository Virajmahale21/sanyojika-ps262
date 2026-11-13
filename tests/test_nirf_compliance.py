"""
Unit tests for Institutional NIRF Ranking & Research Compliance Auditor.
"""

import unittest
from ai_engine.nirf_compliance import audit_research_productivity


class TestNirfCompliance(unittest.TestCase):
    def test_high_productivity_institution(self):
        res = audit_research_productivity(
            total_faculty=50,
            scopus_wos_publications_3yr=120,
            patents_granted_or_published=10,
            phd_graduated_3yr=8
        )
        self.assertTrue(res["meets_minimum_research_norms"])
        self.assertGreaterEqual(res["composite_research_score"], 70.0)
        self.assertEqual(res["status"], "RESEARCH_EXCELLENT")

    def test_deficit_institution_flags_findings(self):
        res = audit_research_productivity(
            total_faculty=60,
            scopus_wos_publications_3yr=20,
            patents_granted_or_published=0,
            phd_graduated_3yr=0
        )
        self.assertFalse(res["meets_minimum_research_norms"])
        self.assertIn("deficit", res["audit_findings"][0].lower())
        self.assertEqual(res["status"], "RESEARCH_DEFICIT")


if __name__ == "__main__":
    unittest.main()
