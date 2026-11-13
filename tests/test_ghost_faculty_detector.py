"""
Unit tests for Ghost-Faculty Collision Detector.
"""

import unittest
from ai_engine.ghost_faculty_detector import detect_ghost_faculty_collisions


class TestGhostFacultyDetector(unittest.TestCase):
    def test_clean_roster_no_collision(self):
        target = [{"name": "Dr. Rajesh Sharma", "pan_or_aadhaar": "ABCDE1234F"}]
        external = [
            {
                "institution_pid": "1-998877",
                "faculty_list": [{"name": "Dr. Anita Desai", "pan_or_aadhaar": "XYZWV9876P"}]
            }
        ]
        res = detect_ghost_faculty_collisions("1-1049281", target, external)
        self.assertTrue(res["compliant"])
        self.assertEqual(res["collision_count"], 0)
        self.assertEqual(res["regulatory_alert"], "CLEAN_ROSTER")

    def test_detects_duplicate_ghost_faculty(self):
        target = [{"name": "Prof. S. K. Gupta", "pan_or_aadhaar": "AAAA1111B"}]
        external = [
            {
                "institution_pid": "1-554433",
                "faculty_list": [
                    {"name": "Prof. S. K. Gupta", "pan_or_aadhaar": "AAAA1111B", "designation": "Visiting Professor"}
                ]
            }
        ]
        res = detect_ghost_faculty_collisions("1-1049281", target, external)
        self.assertFalse(res["compliant"])
        self.assertEqual(res["collision_count"], 1)
        self.assertEqual(res["regulatory_alert"], "SHOW_CAUSE_GHOST_FACULTY")


if __name__ == "__main__":
    unittest.main()
