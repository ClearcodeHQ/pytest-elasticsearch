
def pytest_addoption(parser):
    parser.addoption(
        '--elasticsearch-logsdir',
        action='store',
        default='/tmp',
        metavar='path',
        dest='logsdir',
    )