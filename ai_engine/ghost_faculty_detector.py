"""
AICTE Sanyojika - Student-Faculty Ratio & Ghost-Faculty Collision Detector
Identifies duplicate faculty profiles across concurrent institutional rosters using secure hash fingerprinting.
"""

import hashlib
from typing import List, Dict, Any, Set


def hash_identifier(identifier: str) -> str:
    cleaned = identifier.strip().upper().replace(" ", "")
    return hashlib.sha256(cleaned.encode("utf-8")).hexdigest()[:16]


def detect_ghost_faculty_collisions(
    target_institution_pid: str,
    target_faculty: List[Dict[str, str]],
    all_external_rosters: List[Dict[str, Any]]
) -> Dict[str, Any]:
    target_hashes: Dict[str, str] = {}
    for member in target_faculty:
        fingerprint = hash_identifier(member["pan_or_aadhaar"])
        target_hashes[fingerprint] = member.get("name", "Unknown")

    collisions = []
    for ext_inst in all_external_rosters:
        ext_pid = ext_inst.get("institution_pid", "Unknown")
        if ext_pid == target_institution_pid:
            continue

        for ext_faculty in ext_inst.get("faculty_list", []):
            ext_fingerprint = hash_identifier(ext_faculty["pan_or_aadhaar"])
            if ext_fingerprint in target_hashes:
                collisions.append({
                    "faculty_name": target_hashes[ext_fingerprint],
                    "fingerprint": ext_fingerprint,
                    "target_institution": target_institution_pid,
                    "colliding_institution": ext_pid,
                    "designation": ext_faculty.get("designation", "Faculty")
                })

    is_compliant = len(collisions) == 0
    return {
        "compliant": is_compliant,
        "collision_count": len(collisions),
        "collisions_detected": collisions,
        "regulatory_alert": "SHOW_CAUSE_GHOST_FACULTY" if not is_compliant else "CLEAN_ROSTER"
    }
