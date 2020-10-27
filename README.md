Assert Mail
===========

Test your mail configuration with [TestInfra](https://testinfra.readthedocs.io/en/latest/)

Build the venv with `make` and set your environements, you need a canary imap account.

 * MAIL_SENDER
 * MAIL_TARGET
 * MAIL_IMAP
 * MAIL_PASSWORD

Then run your tests with your favorite connection backend : https://testinfra.readthedocs.io/en/latest/invocation.html
