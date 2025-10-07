# Employment Quiz Web App (Lab 4)

## Usage
Run wsgi.py

## Overview
This Flask web app predicts whether a user is likely employed based on a short lifestyle quiz.  
Depending on the score, it either displays current job listings or shows job market data related to the user’s major.  
All job data comes from the Rise Public Jobs API.

------------------------------------

## How It Works
The user answers a series of indirect lifestyle questions (alarm habits, meetings, start times, etc.).  
Each answer is scored from +1 (employed) to –1 (not employed).  
The total score determines the result:

| Score | Classification | Result |
------------------------------------
| 6 or higher | Likely Employed | Market snapshot |
| 3–5 | Unclear / Mixed | Job listings |
| 2 or lower | Likely Not Employed | Job listings |

If the user is employed, the app shows average salary, salary range, remote percentage, and top skills for their field.  
If not, it shows relevant open job listings.

------------------------------------

## API Information
**Endpoint:** `https://api.joinrise.io/api/v1/jobs/public`  
**Auth:** None required  
**Returned fields:** title, company, location, salary ranges, skills, and work type (Onsite/Hybrid/Remote).  

Job results are filtered to remove listings without a valid location or salary.