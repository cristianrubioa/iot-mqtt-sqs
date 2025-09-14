import json
import logging
from typing import Any
import boto3
from botocore.exceptions import ClientError
from src.sqs_client.base import BaseSQSClient
from config import config

logger = logging.getLogger(__name__)

class AWSSQSClient(BaseSQSClient):
    def __post_init__(self) -> None:
        self.sqs = boto3.client(
            "sqs", 
            region_name=config.aws_sqs.region,
            aws_access_key_id=config.aws_access_key_id,
            aws_secret_access_key=config.aws_secret_access_key
        )
        self.queue_url = config.aws_sqs.queue_url
    
    def send_message(self, data: Any) -> bool:
        try:
            if hasattr(data, "model_dump"):
                message_body = json.dumps(data.model_dump())
            elif hasattr(data, "to_json"):
                message_body = data.to_json()
            else:
                message_body = json.dumps(str(data))
            
            response = self.sqs.send_message(
                QueueUrl=self.queue_url,
                MessageBody=message_body
            )
            
            logger.debug(f"Message sent to SQS: {response['MessageId']}")
            logger.info(f"SQS message body: {message_body}")
            return True
            
        except ClientError as e:
            logger.error(f"SQS send failed: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return False
    
    def is_connected(self) -> bool:
        try:
            self.sqs.get_queue_attributes(QueueUrl=self.queue_url)
            return True
        except:
            return False
