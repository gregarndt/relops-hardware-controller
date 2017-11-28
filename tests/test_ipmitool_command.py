# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, you can obtain one at http://mozilla.org/MPL/2.0/.

import subprocess
import pytest

from django.core.exceptions import ValidationError
from django.core.management import call_command
from django.core.management.base import CommandError
from django.utils.six import StringIO


def test_ipmitool_requires_command():
    with pytest.raises(CommandError):
        call_command('ipmitool', ['mc', 'info'], address='127.0.0.1')


# def test_ipmitool_rejects_invalid_host():
#     with pytest.raises(ValidationError):
#         call_command('ipmitool', '; echo foo')


# @pytest.mark.slowtest
# def test_ipmitool_localhost_works():
#     call_command('ipmitool', 'localhost', count=1)


# @pytest.mark.slowtest
# def test_ipmitool_unroutable_ip_timesout():
#     with pytest.raises(subprocess.TimeoutExpired):
#         # Note: IP won't necessarily be unroutable
#         call_command('ipmitool', '198.51.100.0', count=1)
