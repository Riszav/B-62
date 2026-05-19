from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail


@shared_task
def add(x, y):
    print(f"<---------------------args {x} and {y}----------------------->")
    # from time import sleep

    # sleep(15)
    return x + y


@shared_task
def send_otp_mail(email, otp):
    print("sending " * 10)
    send_mail(
        subject="Your OTP code",
        message=f"opt code: {otp}",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email],
        fail_silently=False,
    )
    return "OK"


@shared_task
def send_report_mail():
    print("sending " * 10)
    send_mail(
        subject="Report data",
        message="что то супер пупер важное",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[
            "riszav.01@gmail.com",
            "quantumfoge@gmail.com",
            "azi.99kg.tls@gmail.com",
            "bkaizirek2002@gmail.com",
            "abdillaevamedina6@gmail.com",
        ],
        fail_silently=False,
    )
    return "OK"
