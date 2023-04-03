import os
import csv
from django.conf import settings
from home.models import SupplierOrderRecord, SupplierProduct, User, SupplierDetails,ManufacturerOrderRecord,ManufacturerProduct

def my_cron_job():
    # Fetch SupplierOrderRecord objects
    supplier_order_records = SupplierOrderRecord.objects.all()

    # Create directory to store CSV files
    csv_dir = os.path.join(settings.BASE_DIR, 'supplier_csv_files')
    if not os.path.exists(csv_dir):
        os.mkdir(csv_dir)

    # Create a separate CSV file for each supplier
    for supplier in User.objects.filter(role='SUPPLIER'):
        supplier_csv_path = os.path.join(csv_dir, f'{supplier.username}.csv')

        # Write SupplierOrderRecord details to CSV file
        with open(supplier_csv_path, mode='a', newline='') as csv_file:
            fieldnames = ['order_id', 'item_price','rating', 'credit_period']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            # Check if CSV file already exists and write headers only if new file is created
            if not os.path.exists(supplier_csv_path):
                writer.writeheader()

            # Filter records for the current supplier and write details to CSV file
            supplier_records = supplier_order_records.filter(supplier=supplier)
            for record in supplier_records:
                item_price = record.totalamount / record.quantity
                writer.writerow({'order_id': record.order_id,  'item_price':item_price,'rating': record.rating, 'credit_period': record.credit_period})

def my_manufacturer_cron_job():
    # Fetch SupplierOrderRecord objects
    supplier_order_records = ManufacturerOrderRecord.objects.all()

    # Create directory to store CSV files
    csv_dir = os.path.join(settings.BASE_DIR, 'manufacturer_csv_files')
    if not os.path.exists(csv_dir):
        os.mkdir(csv_dir)

    # Create a separate CSV file for each supplier
    for supplier in User.objects.filter(role='MANUFACTURER'):
        supplier_csv_path = os.path.join(csv_dir, f'{supplier.username}.csv')

        # Write SupplierOrderRecord details to CSV file
        with open(supplier_csv_path, mode='a', newline='') as csv_file:
            fieldnames = ['order_id', 'item_price','rating', 'credit_period']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            # Check if CSV file already exists and write headers only if new file is created
            if not os.path.exists(supplier_csv_path):
                writer.writeheader()

            # Filter records for the current supplier and write details to CSV file
            supplier_records = supplier_order_records.filter(supplier=supplier)
            for record in supplier_records:
                item_price = record.totalamount / record.quantity
                writer.writerow({'order_id': record.order_id,  'item_price':item_price,'rating': record.rating, 'credit_period': record.credit_period})


