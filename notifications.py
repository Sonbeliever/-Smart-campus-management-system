import os
import smtplib
import threading
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def _send_email_sync(to_email, subject, body, smtp_host, smtp_port, smtp_user, smtp_password, from_email, smtp_timeout):
    """Synchronous email sending function to be run in a thread."""
    try:
        msg = MIMEMultipart()
        msg["From"] = from_email
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        # Port 465 expects implicit TLS, while 587 uses STARTTLS.
        if smtp_port == 465:
            with smtplib.SMTP_SSL(smtp_host, smtp_port, timeout=smtp_timeout) as server:
                server.login(smtp_user, smtp_password)
                server.sendmail(from_email, to_email, msg.as_string())
        else:
            with smtplib.SMTP(smtp_host, smtp_port, timeout=smtp_timeout) as server:
                server.starttls()
                server.login(smtp_user, smtp_password)
                server.sendmail(from_email, to_email, msg.as_string())
        print(f"Email sent to {to_email}")
        return True
    except Exception as exc:
        print(f"Email send failed: {exc}")
        return False


def send_email(to_email, subject, body, enabled=True):
    """Send email using SMTP configuration from environment variables (async)."""
    if not enabled:
        return False

    # Get SMTP configuration from environment variables
    smtp_host = os.getenv("SMTP_HOST", "")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_user = os.getenv("SMTP_USER", "")
    smtp_password = os.getenv("SMTP_PASS", "")
    from_email = os.getenv("FROM_EMAIL", smtp_user)
    smtp_timeout = float(os.getenv("SMTP_TIMEOUT", "10"))

    # Check if required config is present
    if not smtp_host or not smtp_user or not smtp_password or not to_email:
        print(f"Email not sent: missing SMTP config or recipient. To: {to_email}")
        return False

    # Send email asynchronously to avoid blocking the request
    thread = threading.Thread(
        target=_send_email_sync,
        args=(to_email, subject, body, smtp_host, smtp_port, smtp_user, smtp_password, from_email, smtp_timeout)
    )
    thread.daemon = True
    thread.start()
    
    # Return True immediately - email will be sent in background
    return True
