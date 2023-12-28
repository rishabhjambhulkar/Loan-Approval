


from rest_framework import status

from rest_framework.response import Response
from .models import Customer
from .serializers import CustomerSerializer
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Loan
from .serializers import LoanSerializer, EligibilitySerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime


class Register(APIView):
    def post(self, request, format=None):
        monthly_income = float(request.data.get('monthly_income'))
        approved_limit = round(36 * monthly_income / 100000) * 100000

        # Get the phone_number from the request data
        requested_phone_number = request.data.get('phone_number')

        # Check if the user with the requested_phone_number already exists
        if Customer.objects.filter(phone_number=requested_phone_number).exists():
            return Response({"error": f"User with phone number {requested_phone_number} already exists"}, status=status.HTTP_400_BAD_REQUEST)

        # If the user is not present, proceed with generating next_userid
        last_customer = Customer.objects.order_by('-userid').first()
        if last_customer:
            next_userid = last_customer.userid + 1
        else:
            # If there is no existing data, start from 1
            next_userid = 1

        # Include 'approved_limit' and 'userid' in the request data
        request.data['approved_limit'] = approved_limit
        request.data['userid'] = next_userid

        # Create a serializer instance with the modified data
        serializer = CustomerSerializer(data=request.data)

        # Validate the data
        if serializer.is_valid():
            # Save the data
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            # Return detailed error information
            return Response({"error": "Invalid data", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)




class LoanUtils:
    @staticmethod
    def calculate_loan_details(userid,interest_rate,tenure,New_loan):
        # Your common logic here
                # Convert annual interest rate to monthly interest rate
        interest_monthly = (interest_rate / 12) / 100

        # Calculate EMI
        emi_numerator = New_loan * interest_monthly
        emi_denominator = 1 - (1 + interest_monthly) ** -tenure
        Emi = emi_numerator / emi_denominator
        
        
        
        

        # Example: Find related loan records using 'userid'
        loans = Loan.objects.filter(userid=userid)
        loan_serializer = LoanSerializer(loans, many=True) 
        loan_data=loan_serializer.data
        total_loans = 0
        total_approved_loan = 0
        loans_repaid_count = 0
        
        
        user= Customer.objects.filter(userid=userid).first()
        monthly_salary=user.monthly_income
        sum_current_emis=0
        current_date = datetime.now().date()

        # Iterate through each loan entry
        for loan_entry in loan_data:
            loan_amount = loan_entry['loan_amount']
            emi = loan_entry['monthly_repayment_emi']
            emis_paid_on_time = loan_entry['emis_paid_on_time']
            enddate=loan_entry['end_date']
            given_date = datetime.strptime(enddate, "%d-%m-%Y").date()
            current_date = datetime.now().date()


            if given_date > current_date:
                sum_current_emis+=emi
                

            

            # Calculate total number of EMIs
            total_emis = loan_amount / emi

            # Calculate total repayment amount
            total_repayment = emi * total_emis

            # Check if the number of EMIs paid on time is equal to or greater than the total number of EMIs
            loan_repaid = emis_paid_on_time >= total_emis

            # Increment counters
            total_loans += 1
            total_approved_loan += loan_amount
            if loan_repaid:
                loans_repaid_count += 1

        print(f"Number of loans: {total_loans}")
        print(f"Total approved loan amount: {total_approved_loan}")
        print(f"Count of loans repaid: {loans_repaid_count}")
        credit_score = (
        (loans_repaid_count / total_loans) * 30 +
        (total_approved_loan / 1000000) * 40 +
        (total_loans / 5) * 30)
      

# Print the credit score
        print(f"Credit Score: {credit_score}")
        
      
        
        corrected_interest_rate= interest_rate
        
        if credit_score > 50:
    # Approve the loan
            loan_approval_status = "Approved"
        elif 50 > credit_score > 30:
            # Check interest rate condition
            if interest_rate > 12:
                loan_approval_status = "Approved"
            else:
                # Correct the interest rate in the response
                corrected_interest_rate = 16  # Lowest slab
                loan_approval_status = "Interest Rate Corrected"
        else:
            # Credit rating is 30 or lower, don't approve any loans
            loan_approval_status = "Not Approved, Credit rating is 30 or lower"

        # Check the sum of all current EMIs condition
        if sum_current_emis > 0.5 * monthly_salary:
            loan_approval_status = "Not Approved, sum of current Emis is greater than limit"

        # Print the loan approval status and corrected interest rate
        print(f"Loan Approval Status: {loan_approval_status}")
        
        
        response_data = {
                    'customer_id': userid,
                    'approval': loan_approval_status,
                    'interest_rate': interest_rate,
                    'corrected_interest_rate': corrected_interest_rate,
                    'tenure': tenure,
                    'monthly_installment': Emi
                }
        return response_data







class Eligibility(APIView):
    def post(self, request, format=None):
      
            # Deserialize the data sent in the request body
        serializer = EligibilitySerializer(data=request.data)
        if serializer.is_valid():
      
            userid = serializer.data.get('userid')
            interest_rate=serializer.data.get('interest_rate')
            tenure=serializer.data.get('tenure')
            New_loan=serializer.data.get('loan_amount')
        
        
        response_data = LoanUtils.calculate_loan_details(userid,interest_rate,tenure,New_loan)

        return Response(response_data, status=status.HTTP_200_OK)
        
        
         

class CreateLoan(APIView):
    def post(self, request, format=None):
      
            # Deserialize the data sent in the request body
        serializer = EligibilitySerializer(data=request.data)
        if serializer.is_valid():
      
            userid = serializer.data.get('userid')
            interest_rate=serializer.data.get('interest_rate')
            tenure=serializer.data.get('tenure')
            New_loan=serializer.data.get('loan_amount')
        
        
        response_data = LoanUtils.calculate_loan_details(userid,interest_rate,tenure,New_loan)

        import random
        from datetime import datetime, timedelta
        from django.utils import timezone

        # Generate a random 4-digit loan ID
        loanid = random.randint(1000, 9999)

        # Approval date is today's date
        approvaldate = datetime.now().date()

        # Assuming tenure is specified in months
        tenure_in_months = 18  # Replace with the actual tenure value

        # Calculate end date by adding the tenure to today's date
        enddate = approvaldate + timedelta(days=tenure_in_months * 30)  # Assuming 30 days in a month

        # EMIs paid on time starts with 0
        

         # Create a dictionary with loan data
        loan_data = {
            'loan_id': loanid,
            'loan_amount': response_data.get('loan_amount'),
            'tenure': response_data.get('tenure'),
            'interest_rate': response_data.get('interest_rate'),
            'monthly_repayment_emi': response_data.get('monthly_installment'),
            'emis_paid_on_time': 0,
            'approval_date': approvaldate,
            'end_date': enddate,
            'userid': response_data.get('customer_id')
        }

            # Create a LoanSerializer instance with the loan data
        loan_serializer = LoanSerializer(data=loan_data)

        # Validate and save the loan data
        if loan_serializer.is_valid():
            loan_serializer.save()

        return Response(loan_serializer.data, status=status.HTTP_200_OK)
       

        