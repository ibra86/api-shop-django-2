from django.core.mail import send_mail


def send_email_buying_confirmation():
    subject = 'Subject here'
    message = 'Here is the message.'
    from_email = 'from_me@email.com'
    recipient_list = ['ibrahimov.ag@gmail.com']

    # send_mail(subject + " - " + from_email,
    #           message,
    #           from_email,
    #           recipient_list,
    #           fail_silently=False)
    print('e-mail sent')
