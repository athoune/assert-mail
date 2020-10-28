Assert Mail
===========

Test your mail ✉️  configuration with [TestInfra](https://testinfra.readthedocs.io/en/latest/).

## Build

Build the venv with `make` and set your environement variables,
you need a canary imap account.

 * MAIL_SENDER
 * MAIL_TARGET
 * MAIL_IMAP
 * MAIL_PASSWORD

## Test

Then run your tests with your favorite connection backend : https://testinfra.readthedocs.io/en/latest/invocation.html

### Test with ansible inventory

You need :

 * your ansible.cfg
 * target group
 * inventory

```
ANSIBLE_CONFIG=ansible.cfg py.test --hosts='ansible://all' --ansible-inventory=hosts.machin  -v tests/test_sendmail.py
```
