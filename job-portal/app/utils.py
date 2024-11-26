from django.core.mail import EmailMessage,send_mail
# import threading
from django.conf import settings


# class EmailThread(threading.Thread):
    
#     def __init__(self, email):
#         self.email = email
#         # self.email = email
#         threading.Thread.__init__(self)

#     def run(self):
#         self.email.send()
        
class Util:
    @staticmethod
    def send_email(data):
        send_mail(
            data['subject'],
            data['body'],
            settings.EMAIL_HOST_USER,
            data['to_email'],
            fail_silently=False,
        )
        # EmailThread(email).start()
                
import pyotp
from datetime import datetime, timedelta

def generate_otp():
    secret = pyotp.random_base32()
    totp = pyotp.TOTP(secret, interval=60)  # 30 seconds validity
    return {'otp':totp.now(),'totp':secret}

def verify_otp(otp, user_otp,totp):
    verify_totp=pyotp.TOTP(totp,interval=60)
    verify = verify_totp.verify(user_otp)
    print(verify,user_otp,totp,verify_totp.now(),otp)
    return verify               