from readgmail import GmailClient
from dotenv import load_dotenv
from logger import setup_logging  
import logging

import os

from messaging import Producer

load_dotenv()
# Setup logging
setup_logging()
# Get logger for this module
logger = logging.getLogger(__name__)



def main():
    """
    Main function to send the unread messages from the Gmail API to the ActiveMQ queue
    """
    READ_ONLY_SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
    gmail_client = GmailClient(READ_ONLY_SCOPES)
    gmail_client.authenticate()

    producer = Producer(
        host=os.getenv('HOST'),
        port=int(os.getenv('PORT')),
        username=os.getenv('USERNAME'),
        password=os.getenv('PASSWORD'),
        destination=os.getenv('DESTINATION')
    )

    # Get the unread messages from the Gmail API
    unread_messages = gmail_client.get_unread_messages_from_LinkedIn_JobAlerts(max_results=20)


    for unread_message in unread_messages:
        logger.info("########################################################")
        logger.info(unread_message.model_dump_json())
        # Send the unread messages to the ActiveMQ queue
        producer.send_message(unread_message.model_dump_json())
        # with open(f"unread_messages_debug_{unread_message.id}.json", "w") as f:
        #     f.write(unread_message.model_dump_json())
        # print("--------------------------------")
    logger.info("Unread messages sent to the ActiveMQ queue successfully")
    producer.close_connection()
    logger.info("Connection closed successfully")

# call the main function
if __name__ == "__main__":
    main()
    logger.info("Main function completed successfully")