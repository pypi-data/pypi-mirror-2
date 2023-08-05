# -*- coding: utf-8 -*-
# Copyright (C) 2010 Sebastian Wiesner <lunaryorn@googlemail.com>

# This library is free software; you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by the
# Free Software Foundation; either version 2.1 of the License, or (at your
# option) any later version.

# This library is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License
# for more details.

# You should have received a copy of the GNU Lesser General Public License
# along with this library; if not, write to the Free Software Foundation,
# Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA


import sys
import re
import random
import subprocess
import socket
from functools import wraps
from contextlib import contextmanager
from subprocess import check_call

import mock
import py.test

import pyudev


class FakeMonitor(object):
    """
    A dummy pyudev.Monitor class, which allows clients to trigger arbitrary
    events, emitting clearly defined device objects.
    """

    def __init__(self, device_to_emit):
        self.client, self.server = socket.socketpair(
            socket.AF_UNIX, socket.SOCK_DGRAM)
        if sys.version_info[0] >= 3:
            # in python 3 sockets returned by socketpair() lack the
            # ".makefile()" method, which is required by this class.  Work
            # around this limitation by wrapping these sockets in real
            # socket objects.
            import os
            def _wrap_socket(sock):
                wrapped = socket.socket(sock.family, sock.type,
                                        fileno=os.dup(sock.fileno()))
                sock.close()
                return wrapped
            self.client, self.server = (_wrap_socket(self.client),
                                        _wrap_socket(self.server))
        self.device_to_emit = device_to_emit

    def trigger_action(self, action):
        """
        Trigger the given ``action`` on clients of this monitor.
        """
        with self.server.makefile('w') as stream:
            stream.write(action)
            stream.write('\n')
            stream.flush()

    def fileno(self):
        return self.client.fileno()

    def enable_receiving(self):
        pass

    def filter_by(self, *args):
        pass

    start = enable_receiving

    def receive_device(self):
        with self.client.makefile('r') as stream:
            action = stream.readline().strip()
            return action, self.device_to_emit

    def close(self):
        """
        Close sockets acquired by this monitor.
        """
        try:
            self.client.close()
        finally:
            self.server.close()


def _read_udev_database(properties_blacklist):
    udevadm = subprocess.Popen(['udevadm', 'info', '--export-db'],
                               stdout=subprocess.PIPE)
    database = udevadm.communicate()[0].splitlines()
    devices = {}
    current_properties = None
    for line in database:
        line = line.strip().decode(sys.getfilesystemencoding())
        if not line:
            continue
        type, value = line.split(': ', 1)
        if type == 'P':
            current_properties = devices.setdefault(value, {})
        elif type == 'E':
            property, value = value.split('=', 1)
            if property in properties_blacklist:
                continue
            current_properties[property] = value
    return devices


def _get_device_attributes(device_path, attributes_blacklist):
    udevadm = subprocess.Popen(
        ['udevadm', 'info', '--attribute-walk', '--path', device_path],
        stdout=subprocess.PIPE)
    attribute_dump = udevadm.communicate()[0].splitlines()
    if udevadm.returncode != 0:
        raise IOError('could not read attributes')
    attributes = {}
    for line in attribute_dump:
        line = line.strip().decode(sys.getfilesystemencoding())
        if line.startswith('looking at parent device'):
            # we don't continue with attributes of parent devices, we only
            # want the attributes of the given device
            break
        if line.startswith('ATTR'):
            name, value = line.split('==', 1)
            # remove quotation marks from attribute value
            value = value[1:-1]
            # remove prefix from attribute name
            name = re.search('{(.*)}', name).group(1)
            if name in attributes_blacklist:
                continue
            attributes[name] = value
    return attributes


def _query_device(device_path, query_type):
    if query_type not in ('symlink', 'name'):
        raise ValueError(query_type)
    udevadm = subprocess.Popen(
        ['udevadm', 'info', '--path', device_path, '--query', query_type],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    query_result = udevadm.communicate()[0].strip().decode(
        sys.getfilesystemencoding())
    if query_type == 'symlink':
        return query_result.split()
    else:
        return query_result or None


def get_device_sample(config):
    if config.getvalue('device'):
        return [config.getvalue('device')]
    if config.getvalue('all_devices'):
        return config.udev_database
    else:
        device_sample_size = config.getvalue('device_sample_size')
        actual_size = min(device_sample_size, len(config.udev_database))
        return random.sample(list(config.udev_database), actual_size)


@contextmanager
def patch_libudev(funcname):
    with mock.patch('pyudev._libudev.libudev.{0}'.format(funcname)) as func:
        yield func


def _need_privileges(func):
    @wraps(func)
    def wrapped(*args):
        if not py.test.config.getvalue('allow_privileges'):
            py.test.skip('privileges disabled')
        return func(*args)
    return wrapped


@_need_privileges
def load_dummy():
    """
    Load the ``dummy`` module or raise :exc:`ValueError` if sudo are not
    allowed.
    """
    check_call(['sudo', 'modprobe', 'dummy'])

@_need_privileges
def unload_dummy():
    """
    Unload the ``dummy`` module or raise :exc:`ValueError` if sudo are not
    allowed.
    """
    check_call(['sudo', 'modprobe', '-r', 'dummy'])


def is_unicode_string(value):
    """
    Return ``True``, if ``value`` is of a real unicode string type
    (``unicode`` in python 2, ``str`` in python 3), ``False`` otherwise.
    """
    if sys.version_info[0] >= 3:
        unicode_type = str
    else:
        unicode_type = unicode
    return isinstance(value, unicode_type)


def pytest_namespace():
    return dict((func.__name__, func) for func in
                (get_device_sample, patch_libudev, load_dummy,
                 unload_dummy, is_unicode_string))


def pytest_addoption(parser):
    parser.addoption('--all-devices', action='store_true',
                     help='Run device tests against *all* devices in the '
                     'database.  By default, only a random sample will be '
                     'checked.', default=False)
    parser.addoption('--device', metavar='DEVICE',
                     help='Run the device tests only against the given '
                     'DEVICE', default=None)
    parser.addoption('--device-sample-size', type='int', metavar='N',
                     help='Use a random sample of N elements (default: 10)',
                     default=10)
    parser.addoption('--allow-privileges', action='store_true',
                     help='Permit execution of tests, which require '
                     'root privileges.  This affects all monitor tests, '
                     'that need to load or unload modules to trigger udev '
                     'events.  "sudo" will be used to execute privileged '
                     'code, be sure to have proper privileges before '
                     'enabling this option!', default=False)

def pytest_configure(config):
    # these are volatile, frequently changing properties and attributes,
    # which lead to bogus failures during tests, and therefore they are
    # masked and shall be ignored for test runs.
    config.properties_blacklist = frozenset(
        ['POWER_SUPPLY_CURRENT_NOW', 'POWER_SUPPLY_VOLTAGE_NOW',
         'POWER_SUPPLY_CHARGE_NOW'])
    config.attributes_blacklist = frozenset(
        ['power_on_acct', 'temp1_input', 'charge_now', 'current_now',
         'urbnum'])
    config.udev_database = _read_udev_database(config.properties_blacklist)


def pytest_funcarg__database(request):
    """
    The complete udev database parsed from the output of ``udevadm info
    --export-db``.

    Return a dictionary, mapping the devpath of a device *without* sysfs
    mountpoint to a dictionary of properties of the device.
    """
    return request.config.udev_database


def pytest_funcarg__context(request):
    """
    Return a useable :class:`pyudev.Context` object.  The context is cached
    with session scope.
    """
    return request.cached_setup(setup=pyudev.Context, scope='session')

def pytest_funcarg__device_path(request):
    """
    Return a device path as string.

    The device path must be available as ``request.param``.
    """
    return request.param

def pytest_funcarg__all_properties(request):
    """
    Get all properties from the exported database (as returned by the
    ``database`` funcarg) of the device pointed to by the ``device_path``
    funcarg.
    """
    device_path = request.getfuncargvalue('device_path')
    return dict(request.getfuncargvalue('database')[device_path])

def pytest_funcarg__properties(request):
    """
    Same as the ``all_properties`` funcarg, but with the special ``DEVNAME``
    property removed.
    """
    properties = request.getfuncargvalue('all_properties')
    properties.pop('DEVNAME', None)
    return properties

def pytest_funcarg__attributes(request):
    """
    Return a dictionary of all attributes for the device pointed to by the
    ``device_path`` funcarg.
    """
    device_path = request.getfuncargvalue('device_path')
    return _get_device_attributes(
        device_path, request.config.attributes_blacklist)

def pytest_funcarg__device_node(request):
    """
    Return the name of the device node for the device pointed to by the
    ``device_path`` funcarg.
    """
    device_path = request.getfuncargvalue('device_path')
    return _query_device(device_path, 'name')

def pytest_funcarg__device_links(request):
    """
    Return a list of symlink to the device node (``device_node`` funcarg)
    for the device pointed to by the ``device_path`` funcarg.
    """
    device_path = request.getfuncargvalue('device_path')
    return _query_device(device_path, 'symlink')

def pytest_funcarg__sys_path(request):
    """
    Return the sys_path including the sysfs mountpoint for the device path
    returned by the ``device_path`` funcarg.
    """
    context = request.getfuncargvalue('context')
    device_path = request.getfuncargvalue('device_path')
    return context.sys_path + device_path

def pytest_funcarg__device(request):
    """
    Create and return a :class:`pyudev.Device` object for the sys_path
    returned by the ``sys_path`` funcarg, and the context from the
    ``context`` funcarg.
    """
    sys_path = request.getfuncargvalue('sys_path')
    context = request.getfuncargvalue('context')
    return pyudev.Device.from_sys_path(context, sys_path)

def pytest_funcarg__platform_device(request):
    """
    Return the platform device at ``/sys/devices/platform``.  This device
    object exists on all systems, and is therefore suited to for testing
    purposes.
    """
    context = request.getfuncargvalue('context')
    return pyudev.Device.from_sys_path(context, '/sys/devices/platform')

def pytest_funcarg__socket_path(request):
    """
    Return a socket path for :meth:`pyudev.Monitor.from_socket`.  The path
    is unique for each test.
    """
    tmpdir = request.getfuncargvalue('tmpdir')
    return tmpdir.join('monitor-socket')

def pytest_funcarg__monitor(request):
    """
    Return a netlink monitor for udev source.
    """
    return pyudev.Monitor.from_netlink(request.getfuncargvalue('context'))

def pytest_funcarg__fake_monitor(request):
    """
    Return a FakeMonitor, which emits the platform device as returned by
    the ``platform_device`` funcarg on all triggered actions.
    """
    return FakeMonitor(request.getfuncargvalue('platform_device'))

