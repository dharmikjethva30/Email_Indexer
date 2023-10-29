from elasticsearch import Elasticsearch 
import mailbox
import os
import re

# Connect to Elasticsearch
es = Elasticsearch("https://localhost:9200/", ca_certs="E:\Elastic-stack\elasticsearch-8.10.4\config\certs\http_ca.crt", basic_auth=("elastic", "LVZoeD*lowJfc=JiD7x4"))


# Open the mbox file
mbox = mailbox.mbox('Takeout\Mail\All mail Including Spam and Trash.mbox')

# Function to format email addresses and names
def format_email(email):
    if email:
        parts = re.findall(r'[\w\.-]+@[\w\.-]+', email)
        names = re.findall(r'([A-Za-z\s]+) <', email)
        formatted_emails = []
        for i, part in enumerate(parts):
            if i < len(names):
                formatted_emails.append(f"{names[i]} <{part}>")
            else:
                formatted_emails.append(part)
        return ', '.join(formatted_emails)
    else:
        return None

# Iterate through the email messages in the mbox file and index them
for message in mbox:
    subject = message['subject']
    date = message['date']
    from_field = format_email(message['from'])
    to_field = format_email(message['to'])
    body = ""

    # Process the email body, which may be multipart
    for part in message.walk():
        if part.get_content_type() == "text/plain":
            # Remove special characters using regular expressions
            body += re.sub(r'[^\w\s]', '', part.get_payload(decode=True).decode("utf-8", errors="ignore"))
        elif part.get_content_type() == "text/html":
            # You can handle HTML content here if needed
            pass

    # Remove special characters from the subject as well
    subject = re.sub(r'[^\w\s]', '', subject)

    # Create a JSON document for indexing
    email_data = {
        "subject": subject,
        "from": from_field,
        "to": to_field,
        "body": body,
        "date": date,
    }

    # Index the JSON-serializable email_data
    es.index(index="email_index123", body=email_data)