import requests
import os
from dotenv import load_dotenv
import serpapi

load_dotenv()

SERP_API_KEY = os.getenv("SERP_API_KEY")

ROLE_KEYWORDS_STRONG = [
    "drama teacher",
    "theatre teacher",
    "theater teacher",
    "theatre arts",
    "theater arts",
    "performing arts teacher"
]

ROLE_KEYWORDS_WEAK = [
    "drama",
    "theatre",
    "theater",
    "performing arts",
    "stagecraft",
    "acting"
]

HIGH_SCHOOL_KEYWORDS = [
    "high school",
    "hs",
    "secondary",
    "grades 9",
    "grades 10",
    "grades 11",
    "grades 12",
    "9-12"
]

PENALTY_KEYWORDS = [
    "assistant",
    "aide",
    "coach",
    "after school",
    "stipend",
    "club",
    "community theater",
    "adjunct",
    "elementary",
    "middle school",
    "part-time"
]

EMPLOYER_KEYWORDS = [
    "loudoun county public schools",
    "lcps",
    "fairfax county public schools",
    "fcps"
]

EMPLOYER_DOMAINS = [
    "lcps.org",
    "fcps.edu"
]

QUERIES = [
    "High School Drama Teacher Theatre Performing Arts Teacher",
    "Secondary Theatre Arts Drama Education"
]

def run_query(query, location):
    if not SERP_API_KEY:
        raise ValueError("SERP_API_KEY environment variable is not set. Please set your SerpApi key as an environment variable.")
    
    # url = "https://serpapi.com/search.json"
    params = {
        "engine": "google_jobs",
        "q": query,
        "location": location,
        "hl": "en",
        "gl": "us"
 #       "api_key": SERP_API_KEY
    }

    #response = requests.get(url, params=params)
    client = serpapi.Client(api_key=SERP_API_KEY)
    search_results = client.search(params)
    return search_results

def search_jobs(location):
    all_jobs = []

    for q in QUERIES:
        data = run_query(q, location)
        if data:
            jobs = parse_jobs(data)

            for job in jobs:
                job["role_score"] = score_role(job)
                job["employer_score"] = score_employer(job)
                job["confidence_score"] = min(
                    100,
                    int(job["role_score"] * 0.6 + job["employer_score"] * 0.4)
                )
                job["confidence_label"] = classify(job["confidence_score"])
                job["source_query"] = q

            all_jobs.extend(jobs)

    return dedupe_jobs(all_jobs)

def parse_jobs(data):
    jobs = []

    # If there are jobs, add them to the list
    if "jobs_results" in data:
        for job in data.get("jobs_results", []):
            jobs.append({
                "title": job.get("title"),
                "company": job.get("company_name"),
                "location": job.get("location"),
                "Target District": "Yes" if is_target_district(job) else "No",
                "confidence_score": job.get("confidence_score"),
                "confidence_label": job.get("confidence_label"),
                "description": job.get("description"),
                "source": job.get("via"),
                "apply_link": job.get("related_links", [{}])[0].get("link"),
                "posted_date": job.get("detected_extensions", {}).get("posted_at")
            })

    return jobs

def score_role(job):
    score = 0
    title = (job.get("title") or "").lower()
    description = (job.get("description") or "").lower()

    for kw in ROLE_KEYWORDS_STRONG:
        if kw in title:
            score += 35
            break

    for kw in ROLE_KEYWORDS_STRONG:
        if kw in description:
            score += 25
            break

    for kw in ROLE_KEYWORDS_WEAK:
        if kw in title or kw in description:
            score += 10
            break

    for kw in HIGH_SCHOOL_KEYWORDS:
        if kw in title or kw in description:
            score += 15
            break

    for kw in PENALTY_KEYWORDS:
        if kw in title or kw in description:
            score -= 15

    return max(0, min(score, 100))

def score_employer(job):
    score = 0
    company = (job.get("company") or "").lower()
    description = (job.get("description") or "").lower()
    apply_link = (job.get("apply_link") or "").lower()

    for domain in EMPLOYER_DOMAINS:
        if domain in apply_link:
            score += 25
            break

    for kw in EMPLOYER_KEYWORDS:
        if kw in company:
            score += 20
            break

    for kw in EMPLOYER_KEYWORDS:
        if kw in description:
            score += 15
            break

    if "loudoun" in job["location"].lower() or "fairfax" in job["location"].lower():
        score += 10

    return max(0, min(score, 100))

def classify(score):
    if score >= 80:
        return "Very High"
    elif score >= 60:
        return "High"
    elif score >= 40:
        return "Medium"
    else:
        return "Low"

def compute_confidence(job):
    score = 0

    title = (job.get("title") or "").lower()
    description = (job.get("description") or "").lower()
    company = (job.get("company") or "").lower()
    apply_link = (job.get("apply_link") or "").lower()

    # --- Role relevance ---
    for kw in ROLE_KEYWORDS_STRONG:
        if kw in title:
            score += 35
            break

    for kw in ROLE_KEYWORDS_STRONG:
        if kw in description:
            score += 25
            break

    for kw in ROLE_KEYWORDS_WEAK:
        if kw in title or kw in description:
            score += 10
            break

    # --- High school indicator ---
    for kw in HIGH_SCHOOL_KEYWORDS:
        if kw in title or kw in description:
            score += 15
            break

    # --- Employer confidence ---
    for kw in EMPLOYER_KEYWORDS:
        if kw in company:
            score += 15
            break

    for domain in EMPLOYER_DOMAINS:
        if domain in apply_link:
            score += 20
            break

    # --- Penalties ---
    for kw in PENALTY_KEYWORDS:
        if kw in title or kw in description:
            score -= 15

    return max(0, min(score, 100))

def dedupe_jobs(jobs):
    seen = {}

    for job in jobs:
        key = (
            (job.get("title") or "").lower(),
            (job.get("company") or "").lower(),
            (job.get("location") or "").lower()
        )
        if key not in seen:
            seen[key] = job

    return list(seen.values())

def is_target_district(job):
    company = (job.get("company") or "").lower()
    description = (job.get("description") or "").lower()
    apply_link = (job.get("apply_link") or "").lower()

    if "loudoun county public schools" in company:
        return True
    if "fairfax county public schools" in company:
        return True

    for keyword in ["lcps", "fcps", "loudoun county public schools", "fairfax county public schools"]:
        if keyword in description:
            return True

    if "lcps.org" in apply_link or "fcps.edu" in apply_link:
        return True

    return False
