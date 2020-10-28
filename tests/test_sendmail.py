import os
import uuid
import time

from imap_tools import MailBox, AND


def test_sendmail(host):
    """
    Use `sendmail` command on the host to send a mail, and spot it with IMAP

    Env:
        MAIL_TARGET canary email
        MAIL_SENDER from email
        MAIL_IMAP IMAP server address
        MAIL_PASSWORD password
    """
    target = os.getenv("MAIL_TARGET")
    sender = os.getenv("MAIL_SENDER")
    token = uuid.uuid4().hex  # link between emission and reception

    t = host.run( # shell command with `sendmail`
        (
            'echo "'
            "From: TestInfra <{sender}>\n"
            "To: Canary `hostname` <{target}>\n"
            "Subject: Test from `hostname` {token}\n"
            'Hello world of `hostname`."'
            " | sendmail -r {sender} {target}"
        ).format(sender=sender, target=target, token=token)
    )
    print(t)
    assert t.exit_status == 0

    with MailBox(os.getenv("MAIL_IMAP")).login(
        target, os.getenv("MAIL_PASSWORD")
    ) as mailbox:  # Connect and auth to IMAP
        for i in range(10):  # Test 10 times
            messages = list( # Search email from its subject
                mailbox.fetch(AND(from_=sender, subject=token), headers_only=True)
            )
            print(messages)
            if len(messages) > 0:
                return  # Stop the loop, the test is ok
            time.sleep(1) # Wait before retry
    assert False
