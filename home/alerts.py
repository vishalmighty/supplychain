import time
from django.utils import timezone
from home.models import ManufacturerProduct, ProductAlert
from django.core.mail import send_mail
# from django_background_tasks import background

# @background(schedule=60*30)
def check_inventory():
    while True:
        products = ManufacturerProduct.objects.all()
        for product in products:
            recipient_list = []
            try:
                alert = ProductAlert.objects.get(product=product)
                if product.quantity < alert.alert_count:
                    subject = 'Alert'
                    message = f"ALERT: {product.name} has quantity({product.quantity}) less than alert count({alert.alert_count})."
                    from_email = 'vishal@example.com'
                    recipient_list.append(product.user.email)
                    print(f"ALERT: {product.name} has quantity({product.quantity}) less than alert count({alert.alert_count}).")
                    # print(product.user.email)
                    send_mail(subject, message, from_email, recipient_list)
            except:
                pass
        time.sleep(60) #60 sec for testing purpose

    
