import smtplib
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging
from flask import current_app

class NotificationService:
    """
    A service for handling notifications such as email and Slack alerts.
    """

    @staticmethod
    def send_email(recipient_email, subject, body):
        """
        Sends an email using SMTP.
        Args:
            recipient_email (str): The email address of the recipient.
            subject (str): The subject of the email.
            body (str): The body of the email.
        """
        try:
            smtp_host = current_app.config.get("SMTP_HOST")
            smtp_port = current_app.config.get("SMTP_PORT")
            smtp_user = current_app.config.get("SMTP_USER")
            smtp_password = current_app.config.get("SMTP_PASSWORD")
            sender_email = current_app.config.get("SENDER_EMAIL")

            if not all([smtp_host, smtp_port, smtp_user, smtp_password, sender_email]):
                raise ValueError("Missing SMTP configuration in app settings")

            # Create email content
            message = MIMEMultipart()
            message["From"] = sender_email
            message["To"] = recipient_email
            message["Subject"] = subject
            message.attach(MIMEText(body, "plain"))

            # Connect to SMTP server and send email
            with smtplib.SMTP(smtp_host, smtp_port) as server:
                server.starttls()
                server.login(smtp_user, smtp_password)
                server.sendmail(sender_email, recipient_email, message.as_string())
                logging.info(f"Email sent to {recipient_email}")

        except Exception as e:
            logging.error(f"Failed to send email: {e}")
            raise

    @staticmethod
    def send_slack_message(channel, message):
        """
        Sends a Slack message to a specified channel.
        Args:
            channel (str): The Slack channel to send the message to.
            message (str): The message content.
        """
        try:
            slack_webhook_url = current_app.config.get("SLACK_WEBHOOK_URL")

            if not slack_webhook_url:
                raise ValueError("Missing Slack webhook URL in app settings")

            payload = {"channel": channel, "text": message}
            response = requests.post(slack_webhook_url, json=payload)

            if response.status_code == 200:
                logging.info(f"Slack message sent to {channel}")
            else:
                logging.error(f"Failed to send Slack message: {response.text}")
                raise Exception(f"Slack API error: {response.status_code} {response.text}")

        except Exception as e:
            logging.error(f"Failed to send Slack message: {e}")
            raise

    @staticmethod
    def send_notification(notification_type, recipient, subject=None, body=None):
        """
        Sends a notification based on the type (e.g., email, Slack).
        Args:
            notification_type (str): Type of notification ('email' or 'slack').
            recipient (str): Recipient's email or Slack channel.
            subject (str): Email subject (required for email notifications).
            body (str): Notification content (required for both email and Slack).
        """
        try:
            if notification_type == "email":
                if not all([recipient, subject, body]):
                    raise ValueError("Recipient, subject, and body are required for email notifications")
                NotificationService.send_email(recipient, subject, body)

            elif notification_type == "slack":
                if not all([recipient, body]):
                    raise ValueError("Recipient and body are required for Slack notifications")
                NotificationService.send_slack_message(recipient, body)

            else:
                raise ValueError(f"Unsupported notification type: {notification_type}")

        except Exception as e:
            logging.error(f"Failed to send notification: {e}")
            raise
