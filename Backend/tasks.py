from celery import shared_task
from datetime import datetime, timedelta
from models import User
import yagmail
from dotenv import load_dotenv
import os

load_dotenv()


@shared_task
def send_daily_reminder():
    # Get the last 24 hours
    last_24_hours = datetime.now() - timedelta(days=1)

    # Get a list of users who haven't visited the app in the last 24 hours
    users_to_remind = User.query.filter(
        User.last_visited < last_24_hours).all()

    # Send reminders to each user
    for user in users_to_remind:
        send_reminder(user)


def send_reminder(user):
    subject = "Daily Reminder: Visit the App"
    recipients = [user.email]
    body = f"Hi Sangeetha,\n\nThis is a friendly reminder to visit our app today. We hope you're having a great day!\n\nBest regards,\nThe App Team"

    yag = yagmail.SMTP(user=os.environ.get('MAIL_DEFAULT_SENDER'),
                       password=os.environ.get('MAIL_PASSWORD'))
    yag.send(to=recipients, subject=subject, contents=body)
    return {'message': {f'sent Mail to all User: {user.username}'}}
