from celery_app import celery
from celery.schedules import crontab
from flask import render_template
from datetime import datetime, timedelta, date
from models import User, UserBooks
import yagmail
from dotenv import load_dotenv
import os

load_dotenv()


@celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(hour=22, minute=25),
        generate_monthly_report.s(),
        name='Monthly Remainder'
    )
    sender.add_periodic_task(   
        crontab(hour=22, minute=20),
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
    if len(users_to_remind) == 0:
        print("All Users Logged In")
        return
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

@celery.task()
def generate_monthly_report():
    users = User.query.all()
    for user in users:
        if not user:
            return
        acquired_books = []
        returned_books =[]
        for book in user.books:
            book_data = {
                'id': book.id,
                'name': book.name
            }

            user_book = UserBooks.query.filter_by(
                user_id=user.id, book_id=book.id).first()

            book_data['date_issued'] = user_book.date_issued
            if user_book.returned_on:
                book_data['returned_on'] = user_book.returned_on
                returned_books.append(book_data)
            else:
                book_data['return_date'] = str(user_book.return_date)
                # Check if return_date is passed
                if user_book.return_date < date.today():
                    returned_books.append(book_data)
                else:
                    acquired_books.append(book_data)


        report_html = render_template('report.html', user = user, books = acquired_books, returned_books = returned_books)
        print(type(report_html))
        # Send the report via email
        receiver_email = user.email
        subject = f'Monthly Report for {user.username}'
        body = 'Please find the monthly report attached.'

        # Configure yagmail
        yag = yagmail.SMTP(user=os.environ.get('MAIL_DEFAULT_SENDER'),
                        password=os.environ.get('MAIL_PASSWORD'))
        # Send email with HTML report as an attachment
        yag.send(
            to=receiver_email,
            subject=subject,
            contents=[report_html]
        )
        print(f"Email sent to {user.username}")
