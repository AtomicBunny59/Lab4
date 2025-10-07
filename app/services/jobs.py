from typing import List, Dict, Any
from collections import Counter
from .rise import query_rise
from .keywords import get_keywords
from .relevance import has_match, dedupe_by_title

def find_jobs_for_major(major: str):
    keywords = get_keywords(major)
    if not keywords:
        return []

    jobs = []
    for keyword in keywords:
        jobs.extend(query_rise(keyword, page=1))

    jobs = [job for job in jobs if has_match(job, keywords)]
    jobs = [j for j in jobs if _has_location_and_salary(j)]
    jobs = dedupe_by_title(jobs)
    return jobs


def _has_location_and_salary(job):
    loc = job.get("locationAddress") or (
        job.get("owner", {}).get("locationAddress") if isinstance(job.get("owner"), dict) else None
    )
    db = job.get("descriptionBreakdown") or {}
    smin = db.get("salaryRangeMinYearly") or db.get("salaryRangeMinHourly")
    smax = db.get("salaryRangeMaxYearly") or db.get("salaryRangeMaxHourly")
    return bool(loc and (smin or smax))

def market_snapshot_for_major(major: str) -> Dict[str, Any]:
    keywords = get_keywords(major)
    if not keywords:
        return {"total": 0, "salary_min": None, "salary_max": None, "salary_avg": None,
                "remote_pct": None, "top_skills": []}

    rows: List[Dict[str, Any]] = []
    for keyword in keywords:
        rows.extend(query_rise(keyword, page=1))

    rows = [r for r in rows if has_match(r, keywords)]
    rows = dedupe_by_title(rows)

    mins: List[float] = []
    maxs: List[float] = []
    midpoints: List[float] = []
    work_models: List[str] = []
    skill_counts: Counter = Counter()

    for r in rows:
        db = r.get("descriptionBreakdown") or {}
        smin = db.get("salaryRangeMinYearly")
        smax = db.get("salaryRangeMaxYearly")
        if smin is not None:
            mins.append(smin)
        if smax is not None:
            maxs.append(smax)
        if smin is not None and smax is not None:
            midpoints.append((smin + smax) / 2.0)

        wm = r.get("type") or db.get("workModel") or ""
        if isinstance(wm, str) and wm:
            work_models.append(wm)

        for s in (db.get("keywords") or []):
            skill_counts[s] += 1
        for s in (db.get("skillRequirements") or []):
            skill_counts[s] += 1
        for s in (r.get("skills_suggest") or []):
            skill_counts[s] += 1

    salary_min = min(mins) if mins else None
    salary_max = max(maxs) if maxs else None
    salary_avg = int(round(sum(midpoints) / len(midpoints))) if midpoints else None
    remote_pct = (
        int(round(100 * sum(1 for m in work_models if isinstance(m, str) and "remote" in m.lower()) / len(work_models)))
        if work_models else None
    )
    top_skills = [name for name, _ in skill_counts.most_common(10)]

    return {
        "total": len(rows),
        "salary_min": salary_min,
        "salary_max": salary_max,
        "salary_avg": salary_avg,
        "remote_pct": remote_pct,
        "top_skills": top_skills,
    }

search_jobs = find_jobs_for_major
market_snapshot = market_snapshot_for_major
