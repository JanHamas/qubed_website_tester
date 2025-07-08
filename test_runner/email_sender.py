import yagmail
import os
from dotenv import load_dotenv

load_dotenv()

def send_email(subject, body):
    try:
        yag = yagmail.SMTP(os.getenv("EMAIL"), os.getenv("EMAIL_PASSWORD"))
        yag.send(to=os.getenv("TO_EMAIL"), subject=subject, contents=body)
        print("✅ Email sent.")
    except Exception as e:
        print(f"❌ Email send failed: {e}")
