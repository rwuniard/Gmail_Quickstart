from dotenv import load_dotenv
import os
import uuid

from logger import setup_logging
import logging

from proton import Message, Delivery
from proton.utils import BlockingConnection, SendException
import json


setup_logging()
# Get logger for this module
logger = logging.getLogger(__name__)




class Producer:
    """
    Producer class to send messages to ActiveMQ.
    """


    def __init__(self, host: str, port: int, username: str, password: str, address: str, queue: str):
        """
        Initialize the Producer class.

        Args:
            host: The host of the ActiveMQ server.
            port: The port of the ActiveMQ server.
            username: The username to connect to the ActiveMQ server.
            password: The password to connect to the ActiveMQ server.
            destination: The destination of the message.

        Returns:
            None
        """
        logger.info("Initializing Producer class")
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.address = address
        self.queue = queue
        # Create a connection to ActiveMQ
        self.url = f"amqp://{self.username}:{self.password}@{self.host}:{self.port}"
        self.conn = BlockingConnection(self.url)
        self.amqp_destination = f"{self.address}::{self.queue}"
        self.sender = self.conn.create_sender(self.amqp_destination)
        logger.info("Connected to ActiveMQ via AMQP")

    def send_message(self, message: str):
        """
        Send a message to the ActiveMQ queue.
        Message is usually a JSON string.

        Args:
            message: The message to send to the ActiveMQ queue.

        Returns:
            None

        Raises:
            SendException: If the message is not successfully sent to the ActiveMQ queue.
            Exception: If the message is not successfully sent to the ActiveMQ queue. It could be a network error, a timeout, etc.
        """
        try:
            msg = Message(body=message, properties={'content-type': 'application/json'})
            msg.id = str(uuid.uuid4())
            delivery = self.sender.send(msg)
            if delivery.remote_state == Delivery.MODIFIED:
                logger.warning(
                    f"Message sent to ActiveMQ but the message was modified. "
                    f"Delivery body: {delivery.body}, "
                    f"delivery state: {delivery.remote_state}, "
                    f"message id: {delivery.message.id}"
                )
            logger.info("Message sent to ActiveMQ")
        except SendException as e:
            logger.error(f"Error sending message to ActiveMQ: {e}, "
                f"Delivery body: {delivery.body}, "
                f"delivery state: {delivery.remote_state}, "
                f"message id: {delivery.message.id}"
            )
            # raise the exception to the caller to handle the retry
            raise e
        except Exception as e:
            logger.error(f"Error sending message to ActiveMQ: {e}")
            raise e



    def close_connection(self):
        """
        Close the connection to ActiveMQ.

        Args:
            None

        Returns:
            None
        """
        self.sender.close()
        logger.info("Sender closed")
        self.conn.close()
        logger.info("Connection closed")




def main():
    """
    Main function to send messages to ActiveMQ.
    """
    import time
    load_dotenv()
    HOST = os.getenv('HOST')
    PORT = os.getenv('PORT')
    USERNAME = os.getenv('USERNAME')
    PASSWORD = os.getenv('PASSWORD')
    ADDRESS = os.getenv('ADDRESS')
    QUEUE = os.getenv('QUEUE')

    producer = Producer(
        host=HOST, 
        port=PORT, 
        username=USERNAME, 
        password=PASSWORD, 
        address=ADDRESS,
        queue=QUEUE)

    try:
        for i in range(10):
            producer.send_message(f"Hello, from Producer {i}!")
    except SendException as e:
        logger.error(f"Error sending message to ActiveMQ: {e}")
        # retry sending the message that is failing
    except Exception as e:
        logger.error(f"Error sending message to ActiveMQ: {e}")
        # retry sending the message that is failing
        
    finally:
        producer.close_connection()
        logger.info("Connection closed")

if __name__ == "__main__":
    main()