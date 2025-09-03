import os, smtplib
from email.message import EmailMessage
from datetime import datetime
from sqlalchemy.orm import Session
from .models import Notification

SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT", "25"))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")
SMTP_FROM = os.getenv("SMTP_FROM", "lims@example.com")

def queue_notification(db: Session, user_id: int, deviation_id: int, message: str, channel: str='PORTAL'):
    notif = Notification(user_id=user_id, deviation_id=deviation_id, message=message, channel=channel, status='PENDING', created_at=datetime.utcnow())
    db.add(notif)
    db.commit()
    db.refresh(notif)
    return notif

def send_email(recipient: str, subject: str, body: str) -> bool:
    if not SMTP_HOST:
        # No SMTP configured; act as a no-op success (logged to file)
        log_path = "/mnt/data/email_log.txt"
        with open(log_path, "a") as f:
            f.write(f"""[{datetime.utcnow().isoformat()}] TO:{recipient} SUBJECT:{subject}\n{body}\n\n""" )
        return True
    try:
        msg = EmailMessage()
        msg["From"] = SMTP_FROM
        msg["To"] = recipient
        msg["Subject"] = subject
        msg.set_content(body)
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as s:
            if SMTP_USER:
                s.starttls()
                s.login(SMTP_USER, SMTP_PASS or "")
            s.send_message(msg)
        return True
    except Exception as e:
        return False
