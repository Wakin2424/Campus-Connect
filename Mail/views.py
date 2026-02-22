from django.shortcuts import render
from django.core.mail import send_mail, EmailMultiAlternatives
#from celery import shared_task
from Auth import models

# Create your views here.
def registrationRequest(request):
    pass 

def postTransactionMessage():
    pass

def clientNotification():
    pass


#@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=10, retry_kwargs={"max_retries": 5})
def sendForgotPasswordURL(reset_url, user_email, first_name):
    subject = "Reset Password - Campus Connect"
    to = [user_email]

    message = f"""
    Do you want to reset your password?
            Click the link below 👇👇👇


        {reset_url}

    """

    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Reset Your Password - Campus Connect</title>
</head>
<body style="margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f4f4f4;">
    <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" style="background-color: #f4f4f4;">
        <tr>
            <td style="padding: 40px 20px;">
                <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" style="max-width: 600px; margin: 0 auto; background-color: #ffffff; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                    
                    <!-- Header -->
                    <tr>
                        <td style="background-color: #0D1B2A; padding: 30px 40px; text-align: center; border-radius: 8px 8px 0 0;">
                            <h1 style="margin: 0; color: #ffffff; font-size: 28px; font-weight: 600; letter-spacing: 1px;">
                                Campus Connect
                            </h1>
                        </td>
                    </tr>
                    
                    <!-- Main Content -->
                    <tr>
                        <td style="padding: 40px 40px 30px 40px;">
                            <h2 style="margin: 0 0 20px 0; color: #0D1B2A; font-size: 22px; font-weight: 600;">
                                Hello {first_name},
                            </h2>
                            
                            <p style="margin: 0 0 20px 0; color: #333333; font-size: 16px; line-height: 1.6;">
                                We received a request to reset your Campus Connect account password.
                            </p>
                            
                            <p style="margin: 0 0 30px 0; color: #333333; font-size: 16px; line-height: 1.6;">
                                Click the button below to reset your password:
                            </p>
                            
                            <!-- Reset Button -->
                            <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%">
                                <tr>
                                    <td style="text-align: center; padding-bottom: 30px;">
                                        <a href="{reset_url}" style="display: inline-block; padding: 16px 40px; background-color: #0D1B2A; color: #ffffff; text-decoration: none; font-size: 16px; font-weight: 600; border-radius: 6px; transition: background-color 0.3s;">
                                            Reset Password
                                        </a>
                                    </td>
                                </tr>
                            </table>
                            
                            <!-- Fallback URL Section -->
                            <div style="background-color: #f8f9fa; padding: 20px; border-radius: 6px; margin-bottom: 30px; border-left: 4px solid #1E90FF;">
                                <p style="margin: 0 0 10px 0; color: #555555; font-size: 14px; line-height: 1.5;">
                                    If the button above does not work, copy and paste the following link into your browser:
                                </p>
                                <p style="margin: 0; word-break: break-all; color: #1E90FF; font-size: 13px; line-height: 1.5;">
                                        {reset_url}
                                </p>
                            </div>
                            
                            <!-- Security Notice -->
                            <div style="padding: 20px; background-color: #fff8e1; border-radius: 6px; border-left: 4px solid #ffc107;">
                                <p style="margin: 0 0 10px 0; color: #666666; font-size: 13px; line-height: 1.5;">
                                    <strong>Security Notice:</strong>
                                </p>
                                <p style="margin: 0 0 8px 0; color: #666666; font-size: 13px; line-height: 1.5;">
                                    If you did not request this password reset, please ignore this email.
                                </p>
                                <p style="margin: 0; color: #666666; font-size: 13px; line-height: 1.5;">
                                    This link will expire after a limited time for security reasons.
                                </p>
                            </div>
                        </td>
                    </tr>
                    
                    <!-- Footer -->
                    <tr>
                        <td style="padding: 30px 40px; border-top: 2px solid #e0e0e0;">
                            <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%">
                                <tr>
                                    <td style="text-align: center;">
                                        <p style="margin: 0 0 10px 0; color: #0D1B2A; font-size: 18px; font-weight: 600;">
                                            Campus Connect
                                        </p>
                                        <p style="margin: 0 0 10px 0; color: #666666; font-size: 13px;">
                                            Need help? <a href="mailto:support@campusconnect.com" style="color: #1E90FF; text-decoration: none;">Contact Support</a>
                                        </p>
                                        <p style="margin: 0; color: #999999; font-size: 12px;">
                                            © 2026 Campus Connect. All rights reserved.
                                        </p>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                    
                </table>
            </td>
        </tr>
    </table>
</body>
</html>
    """

    msg = EmailMultiAlternatives(subject, message, None, to)
    msg.attach_alternative(html_content, 'text/html')
    msg.send()
    pass