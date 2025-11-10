import json
import boto3

# Initialize SES client (change region if needed)
ses = boto3.client('ses', region_name='ap-south-1')

# Change this to your verified email in SES
SENDER_EMAIL = "rj704260@gmail.com"

def lambda_handler(event, context):
    try:
        # Parse form data from API Gateway
        body = json.loads(event['body'])
        name = body.get('name')
        email = body.get('email')
        phone = body.get('phone')
        service = body.get('service')
        message = body.get('message')

        # === Email to the user (confirmation) ===
        user_subject = "Thank You for Contacting Us!"
        user_body = f"""
Hi {name},

We’ve received your enquiry and our team will reach out to you soon.

Your submitted details:
Name: {name}
Email: {email}
Phone: {phone}
Service: {service}
Message: {message}

Thank you for reaching out!
Best regards,
Your Team
"""

        ses.send_email(
            Source=SENDER_EMAIL,
            Destination={'ToAddresses': [email]},
            Message={
                'Subject': {'Data': user_subject},
                'Body': {'Text': {'Data': user_body}}
            }
        )

        # === Email to the sender (you) with user data ===
        admin_subject = f"New Enquiry Received from {name}"
        admin_body = f"""
You have received a new enquiry:

Name: {name}
Email: {email}
Phone: {phone}
Service: {service}
Message: {message}
"""

        ses.send_email(
            Source=SENDER_EMAIL,
            Destination={'ToAddresses': [SENDER_EMAIL]},
            Message={
                'Subject': {'Data': admin_subject},
                'Body': {'Text': {'Data': admin_body}}
            }
        )

        # Return success
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST,OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps({'message': 'Emails sent successfully!'})
        }

    except Exception as e:
        print("Error:", e)
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST,OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps({'error': str(e)})
        }
