import smtplib
from email.message import EmailMessage

email_sender = 'mohdamaliman.jamal@gmail.com'
email_password = 'jmaiman87'  # Guna App Password Gmail!
email_receiver = 'amaliman@armstrong-auto.com'

msg = EmailMessage()
msg['Subject'] = 'Daily Quality Monitoring Report'
msg['From'] = email_sender
msg['To'] = email_receiver
msg.set_content('Hi, attached is today’s X̄ and R chart report.\n\nRegards,\nYour Monitoring System')

# Attach PDF
with open('monitoring_report.pdf', 'rb') as f:
    file_data = f.read()
    msg.add_attachment(file_data, maintype='application', subtype='pdf', filename='monitoring_report.pdf')

# Send email
with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login(email_sender, email_password)
    smtp.send_message(msg)

print("📤 Email report dihantar!")
