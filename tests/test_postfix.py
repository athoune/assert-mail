import re
from io import StringIO
from typing import Generator, Iterable, Tuple

EQUAL = re.compile(r" *= *")
SPACES = re.compile(r"^\s+")


def postfix_reader(lines: Iterable[str]) -> Generator[Tuple[str, ...], None, None]:
    """
    Read postfix config lines, and yield key, value.
    See https://www.oreilly.com/library/view/postfix-the-definitive/0596002122/ch04s02.html
    """
    current = StringIO()
    for line in lines:
        if line.strip() == "" or line.startswith("#"):
            # empty line or line starting with #
            continue
        if not SPACES.search(line) and current.tell():
            # line doesn't start with space, and current buffer is not empty
            current.seek(0)
            yield tuple(EQUAL.split(current.read(), 1))
            current = StringIO()  # reset the buffer
        current.write(line.lstrip())
    if current.tell():
        current.seek(0)
        yield tuple(EQUAL.split(current.read(), 1))


def test_postfix(host):
    if False:
        proto = dict(
            postfix_reader(
                host.file("/etc/postfix/main.cf.proto").content_string.split("\n")
            )
        )
        print(proto)
    main = host.file("/etc/postfix/main.cf")
    assert main.exists
    for key, value in postfix_reader(main.content_string.split("\n")):
        if value.startswith("hash:"):
            # assert that toto exists with hash:/toto
            path = value.split(":", 1)[1]
            assert host.file(path).exists, f"{path} doesn't exist"
            assert host.file(f"{path}.db").exists, f"{path}.db doesn't exist"
        if value.startswith("regexp:"):
            # assert that toto exists with regexp:/toto
            path = value.split(":", 1)[1]
            assert host.file(path).exists, f"{path} doesn't exist"
