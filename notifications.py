import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_email(to_email, subject, body, enabled=True):
    """Send email using SMTP configuration from environment variables."""
    if not enabled:
        return False

    # Get SMTP configuration from environment variables
    smtp_host = os.getenv("SMTP_HOST", "")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_user = os.getenv("SMTP_USER", "")
    smtp_password = os.getenv("SMTP_PASS", "")
    from_email = os.getenv("FROM_EMAIL", smtp_user)
    smtp_timeout = float(os.getenv("SMTP_TIMEOUT", "30"))

    # Check if required config is present
    if not smtp_host or not smtp_user or not smtp_password or not to_email:
        print(f"Email not sent: missing SMTP config or recipient. To: {to_email}")
        return False

    msg = MIMEMultipart()
    msg["From"] = from_email
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
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
