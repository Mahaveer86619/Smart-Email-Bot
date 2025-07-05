from email_smtp import send_email_smtp

if __name__ == "__main__":
    # Change these values for your test
    test_recipients = ["psatyam86619@google.com"]
    test_subject = "Test Email from Smart Mail Bot"
    test_body = "This is a test email sent from the Smart Mail Bot SMTP test script."

    try:
        send_email_smtp(test_recipients, test_subject, test_body)
        print("✅ Test email sent successfully.")
    except Exception as e:
        print(f"❌ Failed to send test email: {e}")
