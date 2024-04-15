import gmail_api
import database
import rules
import config

def main():
    # Fetch emails
    emails = gmail_api.fetch_emails()

    # Store emails into database
    database.store_emails(emails)

    # Process emails based on rules
    rules.process_emails(config.RULES_FILE, emails)

if __name__ == "__main__":
    main()
