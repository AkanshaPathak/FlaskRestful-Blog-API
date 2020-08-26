import datetime
import random


def generate_otp():
    code = random.randint(1000, 9999)
    expire_time = datetime.datetime.now() + datetime.timedelta(minutes=15)
    return code, expire_time
