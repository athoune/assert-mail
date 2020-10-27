import os
import uuid
from imap_tools import MailBox, AND


def test_sendmail(host):
    target = os.getenv("MAIL_TARGET")
    sender = os.getenv("MAIL_SENDER")
    token = uuid.uuid4().hex

    t = host.run(
        (
            'echo "'#Return-Path: <{sender}>\n'
            'From: TestInfra <{sender}>\n'
            'Subject: Test {token}\n'
            'Hello world"'
            " | sendmail -r {sender} {target}"
        ).format(sender=sender, target=target, token=token)
    )
    print(t)
    assert t.exit_status == 0

    with MailBox(os.getenv("MAIL_IMAP")).login(
        target, os.getenv("MAIL_PASSWORD")
    ) as mailbox:
        for i in range(10):
            messages = list(mailbox.fetch(AND(from_=sender, subject=token), headers_only=True))
            print(messages)
            if len(messages) > 0:
                return
            time.sleep(1)
    assert False
