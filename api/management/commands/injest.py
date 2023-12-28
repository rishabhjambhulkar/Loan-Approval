# import_data.py
import csv
from ...models import Customer

def import_data(file_path):
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)

        for row in reader:
            # Create or update records based on your requirements
            _, created = Customer.objects.update_or_create(
                first_name=row['first_name'],
                last_name=row['last_name'],
                defaults={
                    'age': int(row['age']),
                    'monthly_income': int(row['monthly_income']),
                    'phone_number': int(row['phone_number']),
                    'approved_limit': int(row['approved_limit']),
                    'customer_id': int(row['customer_id']),
                }
            )

if __name__ == '__main__':
    import_data(r"C:\Users\jambh\Desktop\Django\Credit system\customer.csv")
