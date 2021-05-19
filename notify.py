import os
from threading import current_thread

import yagmail
from notify_run import Notify

from util.constants import AUTH, RECEIVER_MAIL, TMP_FILE

notify = Notify()


def send_notification(mssg):
    notify.send(mssg)


def send_email(scrip, mssg):
    thread_name = current_thread().name
    file = os.path.join(TMP_FILE, f'{thread_name}.csv')

    yag = yagmail.SMTP(user=AUTH['email'], password=AUTH['password'])
    subject = f'Reg: {scrip}'
    yag.send(
        to=RECEIVER_MAIL,
        subject=subject,
        contents=mssg,
        attachments=file,
    )


def push_notification(scrip, mssg):
    send_notification(f'{scrip}: \n{mssg}')
    send_email(scrip, mssg)
