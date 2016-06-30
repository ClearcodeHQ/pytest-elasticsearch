# Copyright (C) 2013 by Clearcode <http://clearcode.cc>
# and associates (see AUTHORS).

# This file is part of pytest-dbfixtures.

# pytest-dbfixtures is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# pytest-dbfixtures is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License
# along with pytest-dbfixtures.  If not, see <http://www.gnu.org/licenses/>.
"""Port parsing helpers."""
import port_for


class InvalidPortsDefinition(Exception):
    """Exception raised if ports definition is not a valid string."""
    def __init__(self, ports):
        """
        Exception initalisation.

        :param ports: passed exception value.
        """
        self.ports = ports

    def __str__(self):
        """String representation of a method."""
        return ('Unknown format of ports: %s.\n'
                'You should provide an exact port, ports range "4000-5000"'
                'or a comma-separated ports list "4000,5000,6000-8000".'
                % self.ports)


def get_port(ports):
    """
    Return a random available port.

    If there's only one port passed (e.g. 5000 or '5000') function
    does not check if port is available.  When a range or list
    of ports is passed `port_for` external package is used in order
    to find a free port.

    :param int|str ports: e.g. 3000, '3000', '3000-3100', '3000,3002', '?'
    :returns: a random free port
    """
    try:
        return int(ports)
    except ValueError:
        pass

    return port_for.select_random(parse_ports(ports))


def parse_ports(ports):
    """
    Parse ports expression.

    :param str ports: e.g. '3000', '3000-3100', '3000,3002', '?'
    :returns: ports set reflecting specifified ports list/range.
    :rtype set
    """
    if ports == '?':
        return None

    port_set = set()

    for p in ports.split(','):
        if '-' not in p:
            # single, comma-separated port:
            try:
                port_set.add(int(p))
            except ValueError:
                raise InvalidPortsDefinition(ports)
        else:
            # range of ports:
            try:
                start, end = p.split('-')
            except ValueError:
                raise InvalidPortsDefinition(ports)
            if end < start:
                raise InvalidPortsDefinition(ports)
            port_set.update(range(int(start), int(end) + 1))

    return port_set
