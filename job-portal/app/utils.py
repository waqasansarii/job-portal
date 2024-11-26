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
    secret = pyotp.random_base32()
    totp = pyotp.TOTP(secret, interval=30)  # 30 seconds validity
    return {'otp':totp.now(),'totp':secret}

def verify_otp(otp, user_otp,totp):
    verify_totp=pyotp.TOTP(totp,interval=30)
    verify = verify_totp.verify(user_otp)
    print(verify,user_otp,totp,verify_totp.now(),otp)
    return verify               