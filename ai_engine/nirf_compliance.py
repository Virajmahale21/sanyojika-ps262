"""
AICTE Sanyojika - Institutional NIRF Ranking & Research Output Compliance Auditor
Evaluates peer-reviewed publications, patent disclosures, and PhD scholar velocity against AICTE guidelines.
"""

from typing import Dict, Any


def audit_research_productivity(
    total_faculty: int,
    scopus_wos_publications_3yr: int,
    patents_granted_or_published: int,
    phd_graduated_3yr: int
) -> Dict[str, Any]:
    if total_faculty <= 0:
        return {"compliant": False, "error": "Faculty headcount must be positive"}

    pubs_per_faculty = round(scopus_wos_publications_3yr / total_faculty, 2)
    min_pubs_required = round(total_faculty * 1.5, 1)  # Minimum 1.5 publications per faculty over 3 years

    meets_publication_norm = scopus_wos_publications_3yr >= min_pubs_required
    has_intellectual_property = patents_granted_or_published >= max(1, total_faculty // 10)
    has_doctoral_output = phd_graduated_3yr >= max(1, total_faculty // 15)

    composite_score = min(
        100.0,
        round((pubs_per_faculty * 30.0) + (patents_granted_or_published * 4.0) + (phd_graduated_3yr * 5.0), 2)
    )

    findings = []
    if not meets_publication_norm:
        findings.append(f"Research publication deficit: {scopus_wos_publications_3yr} indexed papers vs {min_pubs_required} expected")
    if not has_intellectual_property:
        findings.append("Inadequate patent disclosures for institution category")
    if not has_doctoral_output:
        findings.append("Low doctoral completion velocity in accredited postgraduate departments")

    return {
        "composite_research_score": composite_score,
        "meets_minimum_research_norms": len(findings) == 0,
        "publications_per_faculty": pubs_per_faculty,
        "audit_findings": findings,
        "status": "RESEARCH_EXCELLENT" if composite_score >= 70.0 else ("RESEARCH_ADEQUATE" if composite_score >= 40.0 else "RESEARCH_DEFICIT")
    }
