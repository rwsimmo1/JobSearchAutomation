from rwsimmo_email import send_email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from send_with_google_app_password import find_app_password

def send_email_notification(jobs, settings=None):
    if not jobs or settings is None:
        return

    # Create HTML formatted email
    html_lines = ["<html><body>"]
    
    for job in jobs:
        html_lines.append("<div style='margin-bottom: 20px; border-bottom: 1px solid #ccc; padding-bottom: 10px;'>")
        html_lines.append(f"<strong>{job['title']}</strong><br>")
        html_lines.append(f"{job['school']} – {job['location']}<br>")
        html_lines.append(f"<em>{job['date']}</em><br>")
        #html_lines.append(f"<a href='{job['url']}'>View Job</a>")
        html_lines.append("</div>")
    
    html_lines.append("</body></html>")
    body = "\n".join(html_lines)

    # Get gmail password from Google App Passwords
    google_app_service = "SmartFindAutomationGoogleApp"
    service_username = "SmartFindAutomation"
    password = find_app_password(google_app_service, service_username)
    if not password:
        raise ValueError("Google App password not found in Credential Manager.")

    send_email(
        to_address=settings["receiver_email"],
        subject="SchoolSpring Job Search Results",
        body=body,
        from_address=settings["sender_email"],
        password=password)
