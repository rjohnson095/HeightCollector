from email.mime.text import MIMEText
import smtplib

def send_email(email, height, average_height, count):
    from_email = "r.johnson0693@gmail.com"
    from_password = "qwerty06"
    to_email = email


    subject = "Height data"
    message = "Results - your height is <strong>%s</strong> cm. The average height of all <strong>%s</strong> users is currently <strong>%s</strong> cm." % (height,count,average_height)

    msg = MIMEText(message, 'html')
    msg['Subject'] = subject
    msg['To'] = to_email
    msg['From'] = from_email

    gmail = smtplib.SMTP('smtp.gmail.com',587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(from_email,from_password)
    gmail.send_message(msg)
