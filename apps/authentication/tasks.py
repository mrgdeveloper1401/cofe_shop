import sys
import time
from django.contrib.auth import get_user_model
from celery import shared_task
import random


@shared_task
def send_otp(user_id : str) : 
    sys.stdout.write("start getting user info ...")
    user = get_user_model().objects.filter(id=user_id).first()
    if user : 
        random_code = random.randint(9999,99999)
        sys.stdout.write(random_code)
        user.change_otp_code(random_code)
        time.sleep(120)

@shared_task
def check_user_is_active (user_id : str) : 

    try : 
        user = get_user_model().objects.get(id=user_id)
        if not user.is_active : 
            user.delete()
            sys.stdout.write("user has been deleted .")
        else : 
            sys.stdout.write("user has beed activate .")
    except : 
        sys.stdout.write("user with this id does not exist .")