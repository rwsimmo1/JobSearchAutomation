from SchoolSpringConfig import (
    BASE_URL,
    SEARCH_KEYWORDS,
    EMAIL_SETTINGS,
    SEEN_JOBS_FILE
)
from SchoolSpringSearch import search_jobs
from SchoolSpringNotifier import send_email_notification
from SchoolSpringStroage import load_seen_jobs, save_seen_jobs

def main():
    seen_jobs = load_seen_jobs(SEEN_JOBS_FILE)

    if seen_jobs is None:
        seen_jobs = set()

    jobs = search_jobs(BASE_URL, SEARCH_KEYWORDS)

    new_jobs = []
    for job in jobs:
        if job["title"] not in seen_jobs:
            new_jobs.append(job)
            seen_jobs.add(job["title"])

    send_email_notification(new_jobs, EMAIL_SETTINGS)
    save_seen_jobs(SEEN_JOBS_FILE, seen_jobs)

if __name__ == "__main__":
    main()
