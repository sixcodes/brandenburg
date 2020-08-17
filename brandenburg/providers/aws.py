from typing import List

from brandenburg.config import settings
from brandenburg.interfaces import ProviderInterface


class AWS(ProviderInterface):
    """
    Services to be used such as SQS and Kinesis
    """

    def get_credentials(self):
        return boto3.Session(
            region_name="us-east-1",
            aws_access_key_id=settings.AWS_SERVER_PUBLIC_KEY,
            aws_secret_access_key=settings.AWS_SERVER_SECRET_KEY,
        )

    def publish(self, topic: str, data, **kwargs):
        raise NotImplementedError("publish method is not implemented!")

    def create_topics(self, topics: List[str]):
        raise NotImplementedError("create_topics method is not implemented!")

    def upload_file(self):
        pass

    @classmethod
    def send_sms(cls, phone: str, message: str, type: str = "Transactional") -> bool:
        # FIXME: Turn it generic to just send sms

        sns = cls.get_session.client("sns")

        try:
            response = sns.publish(
                PhoneNumber=phone,
                Message=message,
                MessageAttributes={
                    "AWS.SNS.SMS.SenderID": {"DataType": "String", "StringValue": "BRANDENBURG"},
                    "AWS.SNS.SMS.SMSType": {"DataType": "String", "StringValue": type.title()},
                },
            )
            logger.info(response)
            if response.get("ResponseMetadata", {}).get("HTTPStatusCode") == 200:

                return True
        except InvalidParameterException as ex:
            logger.info(ex)  # FIXME: temp dumb solution
            return False

    @classmethod
    def send_mail(cls, subject: str, sender: str, to_address: str, body: str) -> bool:
        ses = cls.get_session.client("ses")
        response = ses.send_email(
            Destination={"ToAddresses": [to_address]},
            Message={
                "Body": {"Html": {"Charset": "UTF-8", "Data": body}},
                "Subject": {"Charset": "UTF-8", "Data": subject},
            },
            Source=sender,
        )

        if response.get("ResponseMetadata", {}).get("HTTPStatusCode") == 200:
            return True
