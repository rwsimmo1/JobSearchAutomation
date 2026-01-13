
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib
import os

def send_email(to_address, subject, body, from_address=None, password=None, smtp_server="smtp.gmail.com", smtp_port=587, attachments=None):
    """
    Send an email to the specified address(es).
    
    Parameters:
    -----------
    to_address : str or list of str
        Recipient email address(es). If str, can be comma-separated.
    subject : str
        Email subject line
    body : str
        Email body content
    from_address : str, optional
        Sender's email address (defaults to environment variable EMAIL_ADDRESS)
    password : str, optional
        Sender's email password or app password (defaults to environment variable EMAIL_PASSWORD)
    smtp_server : str, optional
        SMTP server address (default: Gmail)
    smtp_port : int, optional
        SMTP server port (default: 587 for TLS)
    
    Returns:
    --------
    bool
        True if email sent successfully, False otherwise
    
    Example:
    --------
    # Set environment variables first:
    # export EMAIL_ADDRESS="your_email@gmail.com"
    # export EMAIL_PASSWORD="your_app_password"
    
    send_email(
        to_address="recipient@example.com",
        subject="Test Email",
        body="This is a test email."
    )
    
    # Multiple recipients:
    send_email(
        to_address="user1@example.com, user2@example.com",
        subject="Test Email",
        body="This is a test email."
    )
    """
    
    # Get credentials from parameters or environment variables
    from_address = from_address or os.getenv('EMAIL_ADDRESS')
    password = password or os.getenv('EMAIL_PASSWORD')
    
    if not from_address or not password:
        raise ValueError("Email credentials not provided. Set EMAIL_ADDRESS and EMAIL_PASSWORD environment variables or pass them as parameters.")
    
    # Parse to_address
    if isinstance(to_address, str):
        to_list = [addr.strip() for addr in to_address.split(',') if addr.strip()]
    else:
        to_list = list(to_address)
    
    if not to_list:
        raise ValueError("No valid recipient addresses provided.")
    
    try:
        # Create message
        msg = MIMEMultipart("alternative")
        msg['From'] = from_address
        msg['To'] = ", ".join(to_list)
        msg['Subject'] = subject
        
        # Attach Text body to email
        msg.attach(MIMEText(body, 'plain'))
        # Attach HTML body to email
        msg.attach(MIMEText(body, 'html'))

        # Attach files if provided
        if attachments:
            for file_path in attachments:
                if os.path.isfile(file_path):
                    with open(file_path, 'rb') as f:
                        part = MIMEBase('application', 'octet-stream')
                        part.set_payload(f.read())
                        encoders.encode_base64(part)
                        part.add_header('Content-Disposition', f'attachment; filename="{os.path.basename(file_path)}"')
                        msg.attach(part)
                else:
                    print(f"Warning: Attachment file '{file_path}' not found.")

        # Create SMTP session
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Enable TLS encryption
            server.login(from_address, password)
            
            # Send email
            text = msg.as_string()
            server.sendmail(from_address, to_list, text)
        
        print(f"Email sent successfully to {', '.join(to_list)}")
        return True
        
    except smtplib.SMTPAuthenticationError:
        print("Error: Authentication failed. Check your email and password.")
        return False
    except smtplib.SMTPException as e:
        print(f"SMTP error occurred: {e}")
        return False
    except Exception as e:
        print(f"Error sending email: {e}")
        return False