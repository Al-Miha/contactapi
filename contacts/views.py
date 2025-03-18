import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content
import os
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import ContactSerializer

@api_view(['POST'])
def contact_create(request):
    if request.method == 'POST':
        # Initialize the serializer with the incoming data
        serializer = ContactSerializer(data=request.data)

        # Check if the serializer is valid
        if serializer.is_valid():
            # Save the contact data (this will also create a Contact instance in the DB)
            contact = serializer.save()

            # Initialize the SendGrid client with the API key from environment variable
            # sg = sendgrid.SendGridAPIClient(api_key=os.getenv("SENDGRID_API_KEY"))
            sg = sendgrid.SendGridAPIClient(api_key='')

            # Create email content
            subject = f"New Contact Message from {contact.company_name}"
            body = f"""
            Company Name: {contact.company_name}
            Email: {contact.email}
            Markets: {contact.markets}
            Message: {contact.message}
            """

            from_email = Email("office@kita-analytics.com") # Sender email
            to_email = To("contact.kita@gmail.com")  # Recipient email
            content = Content("text/plain", body)

            mail = Mail(from_email, to_email, subject, content)

            try:
                # Send the email using SendGrid API
                response = sg.send(mail)
                if response.status_code == 202:
                    return Response({"message": "Your message has been sent successfully!"}, status=status.HTTP_201_CREATED)
                else:
                    return Response({"message": "Failed to send the message."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            # Return validation errors if the serializer is not valid
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
