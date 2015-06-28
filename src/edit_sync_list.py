#!/usr/bin/env python3
import os
import sys

from executor import Executor


def main():
    current_os = sys.platform
    os_commands = {'linux': 'xdg-open', 'win32': 'start', 'darwin': 'open'}

    script_abs_path = os.path.dirname(os.path.abspath(__file__))
    script_parent_dir = script_abs_path.rsplit(os.sep, 1)[0]
    sys.path.append(script_parent_dir)

    # Check if settings directory exists and create it if it doesn't
    settings_dir = '{}{}settings'.format(script_abs_path, os.sep)
    if not os.path.exists(settings_dir):
        Executor.execute(["mkdir", settings_dir])

    # Check if sync_list file exists and create it if it doesn't
    sync_list_path = '{}{}sync_list.txt'.format(settings_dir, os.sep)
    if not os.path.exists(sync_list_path):
        Executor.execute(["touch", sync_list_path])

    # Get needed command to open default text editor depending on the OS
    command = None
    if 'linux' in current_os:
        command = os_commands['linux']
    elif 'win32' in current_os:
        command = os_commands['win']
    elif 'darwin' in current_os:
        command = os_commands['darwin']

    error_message = \
        """ERROR:    An error occured while trying to open
            "{}" for writing.

    REASON:   One possible reason is that your
            operating system is not supported.

            Your current operating system:  {}
            Supported operating systems:    {}

            If your operating system is not in the list or
            it is but you still see this error
            please give a feedback to support the development
            of this app and you to be able to use it.

    SOLUTION: For now you can edit the sync list manually
            as you open it with some text editor."""\
            .format(sync_list_path, current_os, ', '.join(os_commands.keys()))

    if command is None or not Executor.execute([command, sync_list_path]):
        print(error_message)


if __name__ == '__main__':
    main()
