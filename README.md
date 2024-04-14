Standalone Python script that integrates with Gmail API and performs some rule based operations on emails

Steps to install - 
1. Clone the repository: 
```bash
    git clone https://github.com/your-username/gmail-api-email-rule-processor.git
    ```

2. Navigate to the project directory
```bash
    cd gmail-api-email-rule-processor
    ```

3. Install the required packages
```bash
    pip install -r requirements.txt
    ```
## Configuration

1. Replace the `credentials.json` file with your Gmail API credentials file.
2. Update the `config.py` file with your database credentials.

## Usage


Run the following command to fetch emails from Gmail, store them in DB and process the email with the rules:

```bash
python main.py
