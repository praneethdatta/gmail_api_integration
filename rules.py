import json
from datetime import datetime
from gmail_api import mark_email_as_read, mark_email_as_unread, move_email_to_folder

# Convert date string to datetime object
def convert_to_datetime(date_str):
    try:
        # Try parsing the date string with custom format
        return datetime.strptime(date_str, '%a, %d %b %Y %H:%M:%S %z')
    except ValueError:
        return None


# Apply condition to email
def apply_condition(condition, email):
    field = condition['field']
    predicate = condition['predicate']
    value = condition['value']

    if field == 'received_at':
        email_value = convert_to_datetime(email['received_at'])
        value = convert_to_datetime(value)

        if email_value and value:
            if predicate == 'less than':
                return email_value < value
            elif predicate == 'greater than':
                return email_value > value
    else:
        email_value = email[field]

        if predicate == 'contains':
            return value in email_value
        elif predicate == 'does not contain':
            return value not in email_value
        elif predicate == 'equals':
            return email_value == value
        elif predicate == 'does not equal':
            return email_value != value

# Apply rule to email based on conditions and actions
def apply_rule(rule, email):
    print("inside apply rules")
    predicate_type = rule['predicate']
    conditions = rule.get('conditions', [])
    action = rule.get('action', {})

    if predicate_type == 'all':
        if all(apply_condition(condition, email) for condition in conditions):
            perform_action(action, email)
            return True
    elif predicate_type == 'any':
        if any(apply_condition(condition, email) for condition in conditions):
            perform_action(action, email)
            return True
    return False


# Perform action on email
def perform_action(action, email):
    
    if action.get('mark_as') == 'read':
        mark_email_as_read(email['id'])  # 'id' is the unique identifier for the email - uuid
    elif action.get('mark_as') == 'unread':
        mark_email_as_unread(email['id'])
    if action.get('move'):
        move_email_to_folder(email['id'], action['move'])


# Process emails based on rules
def process_emails(rule_file_path, emails):
    print("inside rules.py")
    with open(rule_file_path, 'r') as file:
        rules_data = json.load(file)
        rules = rules_data.get('rules', [])

    for email in emails:
        for rule in rules:
            if apply_rule(rule, email):
                break
    return emails