import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import EMAIL_HOST, EMAIL_PORT, EMAIL_USER, EMAIL_PASSWORD

def send_invoice_email(partner_email, invoice_id, amount, currency, status):
    """Send email notification for invoices"""
    subject = f"NEURA-SYNC Invoice: {status.upper()} - {invoice_id}"
    body = f"""
    Hello,

    Your NEURA-SYNC invoice has been generated.

    Invoice ID: {invoice_id}
    Amount: {amount} {currency}
    Status: {status.upper()}

    Thank you for being an OEM partner.

    Regards,
    NEURA-SYNC Team
    """

    msg = MIMEMultipart()
    msg['From'] = EMAIL_USER
    msg['To'] = partner_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()

        print(f"Invoice email sent to {partner_email}")
    except Exception as e:
        print(f"Failed to send invoice email: {e}")
