from django.core.mail import mail_managers
from django.db.models.signals import post_save
from django.dispatch import receiver
from .views import notify_comment_author
from .models import Comment


@receiver(post_save, sender=Comment)
def send_notification(sender, instance, created, **kwargs):
    if created:
        notify_comment_author(instance)
    else:
        subject = f'Пост был изменен{instance.title} {instance.text}'

    mail_managers(
        subject=subject,
        message=instance.text,
    )


post_save.connect(send_notification, sender=Comment)

