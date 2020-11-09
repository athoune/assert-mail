from io import StringIO
import re


EQUAL = re.compile(r" *= *")
SPACES = re.compile(r"^\s+")


def postfix_reader(iterator):
    current = StringIO()
    for line in iterator:
        if line.strip() == "" or line.startswith("#"):
            continue
        if not SPACES.search(line) and current.tell():
            current.seek(0)
            yield tuple(EQUAL.split(current.read(), 1))
            current = StringIO()
        current.write(line)
    if current.tell():
        current.seek(0)
        yield tuple(EQUAL.split(current.read(), 1))


def test_postfix(host):
    proto = dict(postfix_reader(
        host.file("/etc/postfix/main.cf.proto").content_string.split('\n')))
    main = host.file("/etc/postfix/main.cf")
    assert main.exists
    for key, value in postfix_reader(main.content_string.split('\n')):
        if value.startswith('hash:'):
            path = value.split(':', 1)[1]
            assert host.file(path).exists, "%s doesn't exist" % path
            assert host.file("%s.db" % path).exists, "%s.db doesn't exist" % path
        if value.startswith('regexp:'):
            path = value.split(':', 1)[1]
            assert host.file(path).exists, "%s doesn't exist" % path
