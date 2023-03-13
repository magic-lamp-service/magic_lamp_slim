from django.template.loader import get_template
from django.template import Context
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

import smtplib
import os
import base64
from django.conf.urls.static import static
from django.conf import settings

def send_email(to, subject, template_name, context_data):
    # Get the template and render it to HTML
    template = get_template(template_name)
    html = template.render((context_data))

    # Inline the CSS styles
    #    html = transform(html)
    # Create the email
    email = MIMEText(html, 'html')
    email['subject'] = subject
    email['to'] = to

    SMTP = os.getenv('SMTP')
    EMAIL = os.getenv('EMAIL')
    PASSWORD = os.getenv('PASSWORD')

    # Send the email
    smtp = smtplib.SMTP(SMTP)
    smtp.starttls()
    smtp.login(EMAIL, PASSWORD)
    smtp.send_message(email)
    smtp.quit()
