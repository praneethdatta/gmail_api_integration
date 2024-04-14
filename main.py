import gmail_api
import database
import rules

def main():
    # Fetch emails
    emails = gmail_api.fetch_emails()

    # Store emails into database
    database.store_emails(emails)

    # Process emails based on rules
    rules.process_emails('rules.json', emails)

if __name__ == "__main__":
    main()
