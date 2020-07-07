from typing import Dict
from smtplib import SMTP


class EmailSMTP:

    def get_credentials() -> Dict[str, str]:
        return {
            'client_id': 'salesseixasgabriel@gmail.com',
            'client_password': 'VamosEnviarEmail@22'
        }

    @classmethod
    def get_session(cls) -> SMTP:
        return SMTP('smtp.sendgrid.net', 587)

    @classmethod
    def send(cls, subject: str, sender: str, to_address: str, body: str) -> bool:
        credentials = cls.get_credentials()
        mail_client = cls.get_session()
        mail_client.starttls()

        message = """From: Sixcodes <opensource@sixcodes.com>
        To: Gabriel Sales Seixas <salesseixasgabriel@gmail.com>
        MIME-Version: 1.0
        Content-type: text/html
        Subject: {subject}
        {body}
        """.format(subject=subject, body=body)

        mail_client.login(
            user=credentials['client_id'],
            password=credentials['client_password']
        )

        mail_client.sendmail(
            'opensource@sixcodes.com',
            to_address,
            message,
        )

        mail_client.quit()

        return True
