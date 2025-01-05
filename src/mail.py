import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os



load_dotenv()
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD_EMAIL")


def send_email(to_email, subject, body):
    try:

        msg = MIMEMultipart()
        msg["From"] = EMAIL
        msg["To"] = to_email
        msg["Subject"] = subject


        msg.attach(MIMEText(body, "plain"))


        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL, PASSWORD)
            server.sendmail(EMAIL, to_email, msg.as_string())

        print("Письмо успешно отправлено!")
    except Exception as e:
        print(f"Ошибка при отправке письма: {e}")


send_email("pup0000000chek@gmail.com", "Лия", "Красотка")
