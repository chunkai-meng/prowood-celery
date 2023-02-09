from celery import shared_task
from urllib import parse
from django.core.mail import EmailMultiAlternatives
import smtplib
import requests


@shared_task
def mass_send(task_sn, msg_from: str, msg_to: list, subject: str, text_content: str, html_content, callback=None):
    try:
        msg = EmailMultiAlternatives(
            subject, text_content, msg_from, msg_to)
        msg.attach_alternative(html_content, "text/html")
        print(f"task_sn:{task_sn}")
        msg.send()
    except smtplib.SMTPException as e:
        return str(callback) + '&error=smtp-exception'
    return callback


# add.apply_async((7,30), link=on_success.s())
@shared_task
def email_on_success(callback):
    if callback:
        try:
            print(callback)
            x = requests.get(callback)
        except requests.exceptions.Timeout as errt:
            print(errt)
        except requests.exceptions.HTTPError as errh:
            print(errh)
        except requests.exceptions.ConnectionError as errc:
            print(errc)
        return str(x)
    else:
        return "callback failed, callback url not provided or not a url"

# @shared_task
# def sms_send(task_sn, phone_number, text):
#     password = 'a'
#     url = 'http://192.168.40.75:8060/send?'
#     try:
#         print(f"task_sn:{task_sn}")
#         data = parse.urlencode({'password': password, 'text': text, 'recipient': phone_number, 'encoding': 'U'})
#         x = requests.get(url=url, params=data)
#         r = xmltodict.parse(x.text)
#         msg_id = r['result']['send']['msg_id']
#         return x.status_code, msg_id, phone_number
#     except requests.exceptions.RequestException as e:
#         return 0, f"Fail: {e}"
