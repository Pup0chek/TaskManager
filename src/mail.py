import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os

# Конфигурация

load_dotenv()
SMTP_SERVER = "smtp.gmail.com"  # Адрес SMTP сервера (например, для Gmail)
SMTP_PORT = 587  # Порт для SMTP сервера
EMAIL = os.getenv("EMAIL")  # Ваш адрес электронной почты
PASSWORD = os.getenv("PASSWORD_EMAIL")  # Пароль или App Password для почты

# Функция отправки письма
def send_email(to_email, subject, body):
    try:
        # Создание сообщения
        msg = MIMEMultipart()
        msg["From"] = EMAIL
        msg["To"] = to_email
        msg["Subject"] = subject

        # Добавление текста письма
        msg.attach(MIMEText(body, "plain"))

        # Установка соединения с SMTP-сервером
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  # Шифрование соединения
            server.login(EMAIL, PASSWORD)  # Аутентификация
            server.sendmail(EMAIL, to_email, msg.as_string())  # Отправка письма

        print("Письмо успешно отправлено!")
    except Exception as e:
        print(f"Ошибка при отправке письма: {e}")


# Использование функции
send_email("pup0000000chek@gmail.com", "Лия", "Красотка")
