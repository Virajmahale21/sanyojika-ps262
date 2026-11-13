"""
AICTE Sanyojika - Direct Benefit Transfer (DBT) & Scholarship Disbursement Auditor
Cross-checks PMKVY, Pragati, Saksham, and PG-GATE stipend claims against student registration.
"""

from typing import List, Dict, Any


def audit_scholarship_claims(
    institution_pid: str,
    claims: List[Dict[str, Any]],
    valid_student_rolls: List[str]
) -> Dict[str, Any]:
    valid_roll_set = set(valid_student_rolls)
    seen_bank_accounts: Dict[str, str] = {}
    anomalies = []

    for claim in claims:
        roll = claim["student_roll_no"]
        bank_acc = claim["bank_account_no"]
        scholarship_type = claim["scheme"]

        # 1. Ghost student check
        if roll not in valid_roll_set:
            anomalies.append({
                "student_roll_no": roll,
                "type": "UNREGISTERED_STUDENT_CLAIM",
                "scheme": scholarship_type
            })

        # 2. Duplicate bank account check across distinct student rolls
        if bank_acc in seen_bank_accounts and seen_bank_accounts[bank_acc] != roll:
            anomalies.append({
                "student_roll_no": roll,
                "conflicting_roll_no": seen_bank_accounts[bank_acc],
                "type": "SHARED_BANK_ACCOUNT_ACROSS_STUDENTS",
                "bank_account_masked": f"****{bank_acc[-4:]}"
            })
        else:
            seen_bank_accounts[bank_acc] = roll

    is_clean = len(anomalies) == 0
    return {
        "institution_pid": institution_pid,
        "total_claims_audited": len(claims),
        "anomalies_detected": anomalies,
        "dbt_audit_status": "PASSED" if is_clean else "SUSPICIOUS_DBT_DISBURSEMENT"
    }
