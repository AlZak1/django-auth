from django.core.mail import send_mass_mail
import environ

from users.models import User


def send_email_to_users():
    env = environ.Env()
    users = User.objects.filter(is_active=True)
    mails_to_send = []
    for user in users:
        message1 = ('Subject here', 'Here is the message', env('EMAIL_HOST'), [user.email])
        mails_to_send.append(message1)
    send_mass_mail(mails_to_send, fail_silently=True)
