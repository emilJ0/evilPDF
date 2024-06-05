import smtplib
from email import message
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

email = input("Deine Email Adresse: ")
password = input("Dein Passwort: ")
opfer_mail = input("Gib die Email Adresse des Opfers ein: ")

message = MIMEMultipart()
message["Subject"] = "TestMail"
message["From"] = email
message["To"] = opfer_mail

html = """\
<html>
  <body>
    <p>Hallo Herr Dahnke!
    </p>
  </body>
</html>
"""

htmlPart = MIMEText(html, "html")
message.attach(htmlPart)

with smtplib.SMTP_SSL("smtp.gmail.com") as server:
    server.login(email, password)
    server.sendmail(email, opfer_mail, message.as_string())
