from datetime import datetime, timedelta

import pytz
from apscheduler.schedulers.background import BackgroundScheduler
from django.core.mail import send_mail

from cw_6 import settings
from mailing.models import Mailing, AttemptMailing

frequency_time = {
    'daily': timedelta(days=1),
    'weekly': timedelta(days=7),
    'monthly': timedelta(days=30),
}


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(job, 'interval', seconds=10)
    scheduler.start()


def send(mailing, current_datetime):
    try:
        send_mail(
            subject=mailing.message.theme,
            message=mailing.message.text,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[client.email for client in mailing.clients.all()]
        )
        response = f"Рассылка была успешна проведена"
        status = True
    except Exception as e:
        response = f"Error {e}"
        status = False
    AttemptMailing.objects.create(
        mailing=mailing,
        status=status,
        date=current_datetime,
        server_response=response
    )


def update_status(mailing, current_datetime):
    if current_datetime < mailing.start_sending:
        mailing.status = 'created'
    elif mailing.start_sending <= current_datetime <= mailing.end_sending:
        mailing.status = 'started'
        attempt = AttemptMailing.objects.filter(mailing=mailing).order_by('-date').first()
        if attempt is None or attempt.date + frequency_time[
            mailing.frequency] <= current_datetime:
            send(mailing, current_datetime)
    else:
        mailing.status = 'finished'
    mailing.save()


def job():
    zone = pytz.timezone(settings.TIME_ZONE)
    current_datetime = datetime.now(zone)
    mailings = Mailing.objects.all()
    for mailing in mailings:
        update_status(mailing, current_datetime)
