# from django.core.mail import EmailMessage
# import threading


# class EmailThread(threading.Thread):
    
#     def __init__(self, email):
#         self.email = email
#         # self.email = email
#         threading.Thread.__init__(self)

#     def run(self):
#         self.email.send()
        
# class Util:
#     @staticmethod
#     def send_email(data):
#         email = EmailMessage(
#             subject=data['email_subject'],
#             body=data['email_body'],
#             to=data['to_email']
#         )
#         EmailThread(email).start()
                
import pyotp
from datetime import datetime, timedelta

def generate_otp():
    totp = pyotp.TOTP(pyotp.random_base32(), interval=30)  # 30 seconds validity
    return totp.now()

def verify_otp(otp, user_otp):
    return otp == user_otp                