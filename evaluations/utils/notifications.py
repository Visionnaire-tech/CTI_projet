from django.core.mail import send_mail

def notify_teacher(user, message):
    if user.email:
        send_mail(
            subject="Notification CTI",
            message=message,
            from_email="kumikusky02@gmail.com",
            recipient_list=[user.email],
            fail_silently=True
        )