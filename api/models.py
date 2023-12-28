from django.db import models


class Customer(models.Model):
    # Other fields...
    
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    phone_number = models.IntegerField(null=True, blank=True)
    monthly_income = models.IntegerField(null=True, blank=True)
    approved_limit = models.IntegerField(null=True, blank=True)
    userid = models.IntegerField(null=True, blank=True)


    def save(self, *args, **kwargs):
        # If the instance is new and userid is not set, calculate the next userid
        if not self.userid:
            last_customer = Customer.objects.order_by('userid').first()
            if last_customer:
                self.userid = last_customer.userid + 1
            else:
                # If there is no existing data, start from 1
                self.userid = 1

        super().save(*args, **kwargs)
        
        
        
class Loan(models.Model):
    
    loan_id = models.IntegerField(null=True, blank=True)
    loan_amount = models.IntegerField(null=True, blank=True)
    tenure = models.IntegerField(null=True, blank=True)
    interest_rate = models.IntegerField(null=True, blank=True)
    monthly_repayment_emi = models.IntegerField(null=True, blank=True)
    emis_paid_on_time = models.IntegerField(null=True, blank=True)
    approval_date = models.CharField(max_length=255, null=True, blank=True)
    end_date = models.CharField(max_length=255, null=True, blank=True)
    userid = models.IntegerField(null=True, blank=True)
    





class Eligibility(models.Model):
    userid = models.IntegerField()
    loan_amount = models.FloatField()
    interest_rate = models.FloatField()
    tenure = models.IntegerField()

   