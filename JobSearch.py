
from JobSearchScripts import search_jobs
from send_with_google_app_password import find_app_password
from rwsimmo_email import send_email
import pandas as pd

def main():
    location = "Ashburn, Virginia, United States"

    jobs = search_jobs(location)
    jobs = sorted(
        jobs,
        key=lambda j: j["confidence_score"],
        reverse=True
    )

    df = pd.DataFrame(jobs)
    print(df)

    # Optional: save to CSV
    df.to_csv("drama_teacher_jobs.csv", index=False)

    # Filter high-confidence jobs
    high_confidence_jobs = [job for job in jobs if job.get("confidence_label") in ["High", "Very High"]]

    # Create HTML table
    if high_confidence_jobs:
        table_html = """
        <table border="1" style="border-collapse: collapse;">
            <tr>
                <th>Job Title</th>
                <th>Company</th>
                <th>Location</th>
                <th>Source</th>
            </tr>
        """
        for job in high_confidence_jobs:
            table_html += f"""
            <tr>
                <td>{job.get('title', 'N/A')}</td>
                <td>{job.get('company', 'N/A')}</td>
                <td>{job.get('location', 'N/A')}</td>
                <td>{job.get('source', 'N/A')}</td>
            </tr>
            """
        table_html += "</table>"
    else:
        table_html = "<p>No high-confidence jobs found.</p>"

    # Get gmail password from Google App Passwords
    google_app_service = "SmartFindAutomationGoogleApp"
    service_username = "SmartFindAutomation"
    password = find_app_password(google_app_service, service_username)

    send_email(
        to_address="rwsimmo@gmail.com, ksimmons525600@gmail.com",
        # to_address="rwsimmo@gmail.com",
        subject="Automated Job Search Results",
        body=f"<h2>High-Confidence Job Matches</h2>{table_html}",
        from_address="rwsimmo@gmail.com",
        password=password,
        attachments=["drama_teacher_jobs.csv"])

if __name__ == "__main__":
    main()
