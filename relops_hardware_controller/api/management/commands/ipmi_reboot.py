
import re
import subprocess
from time import sleep

from django.core.exceptions import ValidationError
from django.core.management import (
    call_command,
    load_command_class,
)
from django.core.management.base import BaseCommand, CommandError
from django.core.validators import validate_ipv46_address


class Command(BaseCommand):
    help = 'Runs a command with ipmitool. Raises for exception for a timeout.'

    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument(
            '-H',
            dest='address',
            type=str,
            help='Remote server address, can be IP address or hostname. This option is required for lan and lanplus interfaces.',
        )
        parser.add_argument(
            '-I',
            dest='interface',
            type=str,
            default='lanplus',
            help='Selects IPMI interface to use. Supported interfaces that are compiled in are visible in the usage help output.',
        )
        parser.add_argument(
            '-L',
            dest='privlvl',
            type=str,
            default='ADMINISTRATOR',
            help='Force session privilege level. Can be CALLBACK, USER, OPERATOR, ADMINISTRATOR. Default is ADMINISTRATOR.',
        )
        parser.add_argument(
            '-p',
            dest='port',
            type=int,
            default=623
            help='Remote server UDP port to connect to. Default is 623.',
        )
        parser.add_argument(
            '-P',
            dest='password',
            type=str,
            help='Remote server password is specified on the command line. If supported it will be obscured in the process list. Note! Specifying the password as a command line option is not recommended.',
        )
        parser.add_argument(
            '-U',
            dest='username',
            type=str,
            help='Remote server username, default is NULL user.',
        )

        # Not ipmitool options
        parser.add_argument(
            '--delay',
            dest='delay',
            default=5,
            type=int,
            help='Wait N seconds before turning the power back on.',
        )

    def get_args_and_kwargs_from_job(self, tc_worker, machine):
        args = []
        kwargs = {'address': machine.get('host', None) or machine.get('ip', None)}

        # TODO: get username and password from tc_worker and machine
        return args, kwargs

    def handle(self, *args, **options):
        cmd_class = load_command_class('relops_hardware_controller.api', 'ipmitool')

        # only running are ipmitool commands
        args, kwargs = self.get_args_and_kwargs_from_job(tc_worker, machine)

        # check "fqdn" has a working IPMI interface raises on failure
        call_command(cmd_class, 'mc info', *args, **options)

        ## for working IPMI

        # try a soft reboot
        try:
            call_command(cmd_class, 'power soft', *args, **options)
        except CommandError:
            # TODO: log the error
            call_command(cmd_class, 'power off', *args, **options)

        # TODO: poll until 'off' in power status result or 120 seconds elapses
        call_command(cmd_class, 'power status', *args, **options)

        ## if either shutdown method succeeds

        # sleep for configurable delay (default 5s)
        time.sleep(options['delay'])

        call_command(cmd_class, 'power on', *args, **options)  # turn back on
