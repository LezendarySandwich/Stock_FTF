import os
from threading import current_thread

import yagmail
from notify_run import Notify

from constants import auth, receiver_mail

notify = Notify()


def send_notification(mssg):
    notify.send(mssg)


def send_email(scrip, mssg):
    thread_name = current_thread().name
    file = os.path.join('.tmp', f'{thread_name}.csv')

    yag = yagmail.SMTP(user=auth['email'], password=auth['password'])
    subject = f'Reg: {scrip}'
    yag.send(
        to=receiver_mail,
        subject=subject,
        contents=mssg,
        attachments=file,
    )


def push_notification(scrip, mssg):
    send_notification(f'{scrip}: \n{mssg}')
    send_email(scrip, mssg)
