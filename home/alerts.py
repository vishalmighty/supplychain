import time
from django.utils import timezone
from home.models import ManufacturerProduct, ProductAlert
# from django_background_tasks import background

# @background(schedule=60*30)
def check_inventory():
    while True:
        products = ManufacturerProduct.objects.all()
        for product in products:
            try:
                alert = ProductAlert.objects.get(product=product)
                if product.quantity < alert.alert_count:
                    print(f"ALERT: {product.name} has quantity less than alert count.")
                    # You can also create a log entry, send an email or notification, etc.
                else:
                    print("HII alert")
            except:
                pass
        time.sleep(6)

    
