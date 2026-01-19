import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from typing import Optional

# Email configuration - using environment variables for security
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
FROM_EMAIL = os.getenv("FROM_EMAIL", SMTP_USER)
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")

def send_email(to_email: str, subject: str, html_content: str) -> bool:
    """Send an email using SMTP."""
    if not SMTP_USER or not SMTP_PASSWORD:
        print("Warning: SMTP credentials not configured. Email not sent.")
        print(f"Would have sent email to {to_email}: {subject}")
        return False

    try:
        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = FROM_EMAIL
        msg['To'] = to_email

        # Attach HTML content
        html_part = MIMEText(html_content, 'html')
        msg.attach(html_part)

        # Send email
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.send_message(msg)

        return True
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return False

def send_verification_email(to_email: str, participant_name: str, event_name: str, verification_token: str) -> bool:
    """Send email verification link to participant."""
    verification_url = f"{FRONTEND_URL}/verify-email?token={verification_token}"

    subject = f"Verify your registration for {event_name}"

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                color: #333;
            }}
            .container {{
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
            }}
            .header {{
                background: linear-gradient(135deg, #ec4899 0%, #ef4444 100%);
                color: white;
                padding: 30px;
                text-align: center;
                border-radius: 10px 10px 0 0;
            }}
            .content {{
                background: #f9fafb;
                padding: 30px;
                border-radius: 0 0 10px 10px;
            }}
            .button {{
                display: inline-block;
                background: linear-gradient(135deg, #ec4899 0%, #ef4444 100%);
                color: white;
                padding: 15px 30px;
                text-decoration: none;
                border-radius: 8px;
                margin: 20px 0;
                font-weight: bold;
            }}
            .footer {{
                text-align: center;
                margin-top: 30px;
                color: #666;
                font-size: 12px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>💘 Cupid's Matcher</h1>
            </div>
            <div class="content">
                <h2>Hi {participant_name}!</h2>
                <p>Thank you for registering for <strong>{event_name}</strong>!</p>
                <p>Please verify your email address by clicking the button below:</p>
                <div style="text-align: center;">
                    <a href="{verification_url}" class="button">Verify Email Address</a>
                </div>
                <p>Or copy and paste this link into your browser:</p>
                <p style="word-break: break-all; color: #666; font-size: 12px;">{verification_url}</p>
                <p><strong>Important:</strong> This link will expire in 24 hours.</p>
                <p>If you didn't register for this event, you can safely ignore this email.</p>
            </div>
            <div class="footer">
                <p>This is an automated email from Cupid's Matcher. Please do not reply.</p>
            </div>
        </div>
    </body>
    </html>
    """

    return send_email(to_email, subject, html_content)

def send_match_notification(to_email: str, participant_name: str, match_name: str, venue_name: Optional[str], event_name: str) -> bool:
    """Send notification when a participant is matched."""
    subject = f"You've been matched! - {event_name}"

    venue_info = f"<p><strong>Location:</strong> {venue_name}</p>" if venue_name else ""

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                color: #333;
            }}
            .container {{
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
            }}
            .header {{
                background: linear-gradient(135deg, #ec4899 0%, #ef4444 100%);
                color: white;
                padding: 30px;
                text-align: center;
                border-radius: 10px 10px 0 0;
            }}
            .content {{
                background: #f9fafb;
                padding: 30px;
                border-radius: 0 0 10px 10px;
            }}
            .match-card {{
                background: white;
                border: 2px solid #ec4899;
                border-radius: 10px;
                padding: 20px;
                margin: 20px 0;
                text-align: center;
            }}
            .footer {{
                text-align: center;
                margin-top: 30px;
                color: #666;
                font-size: 12px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>💘 You've Been Matched!</h1>
            </div>
            <div class="content">
                <h2>Hi {participant_name}!</h2>
                <p>Great news! You've been matched for <strong>{event_name}</strong>!</p>
                <div class="match-card">
                    <h3>Your Match</h3>
                    <p style="font-size: 24px; margin: 10px 0;">💖 {match_name} 💖</p>
                    {venue_info}
                </div>
                <p>We hope you have a wonderful time getting to know each other!</p>
                <p>Good luck! 🍀</p>
            </div>
            <div class="footer">
                <p>This is an automated email from Cupid's Matcher. Please do not reply.</p>
            </div>
        </div>
    </body>
    </html>
    """

    return send_email(to_email, subject, html_content)
