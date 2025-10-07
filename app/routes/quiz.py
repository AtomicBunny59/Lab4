from flask import Blueprint, request, render_template
from ..services.jobs import search_jobs, market_snapshot

bp = Blueprint("quiz", __name__)

QUESTION_FIELDS = (
    "alarm", "meetings", "weekenddiff", "fivepm",
    "starttime", "emailvssocial", "pto", "timeoff", "notifs"
)

def get_number(form, field, default=0):
    try:
        return int(form.get(field, default))
    except (TypeError, ValueError):
        return default

def get_employment_status(score: int) -> str:
    if score >= 6:
        return "Likely Employed"
    if 3 <= score <= 5:
        return "Unclear / Mixed"
    return "Likely Not Employed"

@bp.route("/", methods=["GET"])
def show_quiz_page():
    return render_template("quiz.html")

@bp.route("/result", methods=["POST"])
def show_result_page():
    form = request.form
    major = (form.get("major") or "not listed").strip().lower()

    total_score = sum(get_number(form, field) for field in QUESTION_FIELDS)
    status = get_employment_status(total_score)
    is_employed = status == "Likely Employed"

    page_data = {
        "result": status,
        "score": total_score,
        "major": major,
        "snapshot": market_snapshot(major) if is_employed else None,
        "jobs": None if is_employed else search_jobs(major),
    }

    return render_template("result.html", **page_data)
