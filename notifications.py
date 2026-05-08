import os
import requests


def send_email(to_email, subject, body, enabled=True):
    """Send email using Brevo HTTP API to avoid SMTP IP blocking."""
    if not enabled:
        return False

    # Get Brevo API configuration
    api_key = os.getenv("BREVO_API_KEY", "")
    from_email = os.getenv("FROM_EMAIL", "")
    
    # Check if required config is present
    if not api_key or not from_email or not to_email:
        print(f"Email not sent: missing Brevo API config or recipient. To: {to_email}")
        return False

    try:
        res = requests.post(
            "https://api.brevo.com/v3/smtp/email",
            headers={
                "accept": "application/json",
                "api-key": api_key,
                "content-type": "application/json",
            },
            json={
                "sender": {"email": from_email},
                "to": [{"email": to_email}],
                "subject": subject,
                "textContent": body,
            },
            timeout=10,
        )
        if 200 <= res.status_code < 300:
            print(f"Email sent to {to_email}")
            return True
        else:
            print(f"Email send failed: Brevo API returned {res.status_code}: {res.text[:200]}")
            return False
    except Exception as exc:
        print(f"Email send failed: {exc}")
        return False
