import psycopg2
import config


# Store emails into db
# Using Postgres in this case
def store_emails(emails):
    print("inside store emails")
    conn = psycopg2.connect(**config.DB_CONFIG)
    cursor = conn.cursor()

    if not table_exists(cursor, 'emails'):
        create_table(cursor)
    insert_records(cursor, emails)

    conn.commit()
    conn.close()


# Check to see if emails table already exists in db
def table_exists(cursor, table_name):
    cursor.execute("""
    SELECT EXISTS (
        SELECT FROM information_schema.tables 
        WHERE table_name = %s
    );
    """, (table_name,))
    return cursor.fetchone()[0]


# Create emails table service
def create_table(cursor):
    create_table_query = """
    CREATE TABLE emails (
        id SERIAL PRIMARY KEY,
        from_email TEXT NOT NULL,
        subject TEXT NOT NULL,
        message TEXT NOT NULL,
        received_at TEXT NOT NULL
    );
    """
    cursor.execute(create_table_query)


# insert records into the emails table
def insert_records(cursor, emails):
    print("inside insert records")
    insert_query = """
    INSERT INTO emails (from_email, subject, message, received_at)
    VALUES (%s, %s, %s, %s);
    """
    cursor.executemany(insert_query, [(email['from'], email['subject'], email['message'], email['received_at']) for email in emails])

