from typing import Dict, Any, List

def _norm(s: str) -> str:
    return (s or "").strip().lower()

def _words(s: str) -> List[str]:
    return [w for w in _norm(s).split() if w]

def score(job: Dict[str, Any], phrases: List[str]) -> int:
    title = _norm(job.get("title"))
    db = job.get("descriptionBreakdown") or {}
    blob = _norm(" ".join((db.get("keywords") or []) + (job.get("skills_suggest") or [])))

    total = 0
    for p in phrases or []:
        ws = _words(p)
        if not ws:
            continue
        if all(w in title for w in ws):
            total += 2
        elif any(w in title for w in ws):
            total += 1
        if _norm(p) in blob:
            total += 1
    return total

def has_match(job: Dict[str, Any], phrases: List[str]) -> bool:
    return score(job, phrases) > 0

def dedupe_by_title(rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    seen, out = set(), []
    for j in rows or []:
        t = _norm(j.get("title"))
        if t and t not in seen:
            seen.add(t)
            out.append(j)
    return out