# File used to store functions for scraper.py
import datetime
import hashlib
import smtplib, ssl
from static import PASSWORD, PORT, sender_email, receiver_email, MESSAGE_BODY
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText

# Use to convert epoch time to human readable string
def convert_epoch(time):
    time_string = datetime.datetime.fromtimestamp(time/1000).strftime('%c')
    return time_string


def hash_file():
    hasher = hashlib.md5() # Use MD5 Hashing
    with open("IPO_Filings.csv", 'rb') as open_file:
        content = open_file.read() # Read CSV contents
        hasher.update(content)
        hash_number = hasher.hexdigest() # Convert hash to hexidecimal output
        return hash_number
    open_file.close()


def check_duplicate(hash_number):
    stored_hashes = open("hash_data.txt", 'r+')

    if hash_number in stored_hashes.read():
        print("No new information found.")
    else:
        # Add the new hash number
        stored_hashes.write(f'\n{hash_number}')
        # Email the CSV file
        print("New information was found! Sending email.")
        send_email()
    stored_hashes.close()


def send_email():
    msg = MIMEMultipart()
    msg['Subject'] = "NYSE IPO Filings"
    msg['From'] = sender_email
    msg['To'] = receiver_email

    body = MIMEText(MESSAGE_BODY, 'plain')
    msg.attach(body)

    with open("IPO_Filings.csv", 'rb') as file:
        msg.attach(MIMEApplication(file.read(), Name="IPO_Filings.csv"))
    file.close()

    with smtplib.SMTP_SSL("smtp.gmail.com", PORT) as smtp:
        smtp.login(sender_email, PASSWORD)
        smtp.sendmail(msg['From'], msg['To'], msg.as_string())
