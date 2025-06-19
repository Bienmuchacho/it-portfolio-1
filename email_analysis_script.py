import email  # Import the email module to parse email messages
import re  # Import the regular expression module to detect patterns in email headers
from email.policy import default  # Import default policy for email parsing

def analyze_email(email_data):
    """
    Analyzes the provided raw email data to check for suspicious email headers and patterns.

    :param email_data: Raw email content in bytes or string format
    :return: None, prints analysis results
    """

    try:
        # Step 1: Parse the raw email data into a message object
        msg = email.message_from_bytes(email_data, policy=default)  # Parse the email using the default policy

        print("Analyzing Email Headers...
")

        # Step 2: Check basic email header information for suspicious patterns
        from_header = msg["From"]
        to_header = msg["To"]
        subject_header = msg["Subject"]
        date_header = msg["Date"]

        print(f"From: {from_header}")
        print(f"To: {to_header}")
        print(f"Subject: {subject_header}")
        print(f"Date: {date_header}
")

        # Step 3: Check if the "From" address matches a suspicious pattern (e.g., random names or domains)
        if re.search(r"(\d{3,})|[!#$%&'*+/=?^_`{|}~-]+(\.[!#$%&'*+/=?^_`{|}~-]+)*@", from_header):
            print("Suspicious 'From' address pattern detected!")

        # Step 4: Check for any unexpected or unusual subject lines (e.g., common phishing terms)
        phishing_keywords = ["urgent", "security alert", "verify", "claim prize"]
        if any(keyword.lower() in subject_header.lower() for keyword in phishing_keywords):
            print("Suspicious 'Subject' detected! Possible phishing attempt.")

        # Step 5: Scan the email body (if available) for malicious links or attachments
        # For simplicity, just checking if the email body contains URLs
        body = msg.get_payload(decode=True).decode(errors="ignore")  # Decode the email body
        urls_found = re.findall(r"https?://[^\s]+", body)

        if urls_found:
            print("Malicious URLs detected in email body:")
            for url in urls_found:
                print(url)

        # Step 6: Check for attachments (often used in malicious emails)
        if msg.is_multipart():  # Check if the email contains multiple parts (attachments)
            print("This email has attachments.")
            for part in msg.iter_parts():
                if part.get_content_disposition() == "attachment":
                    print(f"Attachment found: {part.get_filename()}")

    except Exception as e:
        # Handle errors during the email parsing or analysis
        print(f"Error analyzing the email: {e}")

# Example Usage: Simulating an email analysis
# For real-world usage, the email data would come from your email server or a file.
# Here's an example raw email in bytes format (a basic example).
raw_email = b"From: phishing@example.com
To: victim@domain.com
Subject: Urgent - Verify your account
Date: Tue, 5 Oct 2021 14:55:02 -0400

Please click on the following link: http://malicious-link.com
"

# Calling the analysis function with the sample email data
analyze_email(raw_email)
