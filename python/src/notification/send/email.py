import json
import os
import smtplib
from email.message import EmailMessage


def notification(message):
    message = json.loads(message)
    mp3_fid = message.get("mp3_fid")
    sender_address = os.environ.get("EMAIL_ADDRESS")
    sender_password = os.environ.get("EMAIL_PASSWORD")
    receiver_address = message.get('username')

    try:
        msg = EmailMessage()
        msg.set_content("Your video has been converted to mp3")
        msg["Subject"] = "Video converted, ready for download"
        msg["To"] = message.get("username"),
        msg["From"] = sender_address

        session = smtplib.SMTP("smtp.gmail.com", 587)
        session.starttls()
        session.login(sender_address, sender_password)
        session.send_message(msg, sender_address, receiver_address)
        session.quit()

    except Exception as err:
        return {"message": str(err)}, 500

    return {"message": "success"}, 200
