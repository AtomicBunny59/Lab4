import requests

RISE_URL = "https://api.joinrise.io/api/v1/jobs/public"
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; Lab3/1.0)"}

def _coerce_jobs(payload):
    if isinstance(payload, list):
        return payload
    if not isinstance(payload, dict):
        return []
    if isinstance(payload.get("data"), list):
        return payload["data"]
    res = payload.get("result")
    if isinstance(res, list):
        return res
    if isinstance(res, dict) and isinstance(res.get("jobs"), list):
        return res["jobs"]
    return []

def query_rise(q: str, page: int = 1, limit: int = 25):
    try:
        params = {
            "q": q,
            "page": page,
            "limit": limit,
            "sort": "desc",
            "sortedBy": "createdAt",
            "includeDescription": "true",
        }
        resp = requests.get(RISE_URL, headers=HEADERS, params=params, timeout=15)
        resp.raise_for_status()
        return _coerce_jobs(resp.json())
    except Exception:
        return []