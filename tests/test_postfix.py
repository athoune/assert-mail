from io import StringIO
import re


EQUAL = re.compile(" += +")


def postfix_reader(iterator):
    current = StringIO()
    for line in iterator:
        if line.strip() == "" or line.startswith("#"):
            continue
        if line[0] != " " and current.tell():
            current.seek(0)
            yield tuple(EQUAL.split(current.read(), 1))
            current = StringIO()
        current.write(line)
    if current.tell():
        current.seek(0)
        yield tuple(EQUAL.split(current.read(), 1))


def test_postfix(host):
    main = host.file("/etc/postfix/main.cf")
    assert main.exists
    for key, value in postfix_reader(main.content_string.split('\n')):
        if value.startswith('hash:'):
            path = value.split(':', 1)[1]
            assert host.file(path).exists, "%s doesn't exist" % path
            assert host.file("%s.db" % path).exists, "%s.db doesn't exist" % path

