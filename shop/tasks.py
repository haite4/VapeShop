from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from shop.models import NotificationSubscription,Product


@shared_task
def send_notification_email():

      
        notity = NotificationSubscription.objects.all()
        for subscription in notity:
                if subscription.product.quantity > 0 and not subscription.notification_sent:

                        try:
                                validate_email(subscription.email)
                        except ValidationError:
                                continue

                        subject = f"Product Back in Stock"
                        message = f"Hello {subscription.name}.The product you subscribed to is back in stock.{subscription.product.title}"
                                                

                                
                        mail_sent = send_mail(
                        subject=subject,
                        message=message,
                        from_email=settings.EMAIL_HOST_USER,
                        recipient_list=[subscription.email],
                        fail_silently=True,
                        )


                        if mail_sent:
                                
                                subscription.notification_sent = True
                                subscription.delete()


                        print(mail_sent)

        return "Success"


