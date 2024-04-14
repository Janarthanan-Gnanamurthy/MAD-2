from celery_app import celery
from celery.schedules import crontab
from datetime import datetime, timedelta
from models import User
import yagmail
from dotenv import load_dotenv
import os

load_dotenv()


@celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(hour=20, minute=48),
        send_daily_reminder.s(),
        name='Daily Remainder'
    )
    sender.add_periodic_task(
        30.0,
        send_daily_reminder.s(),
        name='Remainder'
    )

@celery.task()
def send_daily_reminder():
    print('inside Task')
    # Get the last 24 hours
    last_24_hours = datetime.now() - timedelta(days=1)
    # Get a list of users who haven't visited the app in the last 24 hours
    users_to_remind = User.query.filter(
        User.last_visited < last_24_hours).all()
    # Send reminders to each user
    for user in users_to_remind:
        send_reminder(user)


def send_reminder(user):
    subject = f"Daily Reminder: Hey {user.username}, we are missing you!"
    recipients = [user.email]
    body = f"Hi {user.username},\n\nThis is a friendly reminder to visit our app today. We hope you're having a great day!\n\nBest regards,\nThe App Team"

    yag = yagmail.SMTP(user=os.environ.get('MAIL_DEFAULT_SENDER'),
                       password=os.environ.get('MAIL_PASSWORD'))
    try:
        yag.send(to=recipients, subject=subject, contents=body)
    except yagmail.errors.YagmailSMTPError as e:
        print(f"Error sending email: {e}")
    except yagmail.errors.YagmailInvalidArguments as e:
        print(f"Invalid arguments provided: {e}")

    print(f'Sent Mail to User: {user.username}')

    return {'message': {f'sent Mail to all User: {user.username}'}}
