# check_local_user_environment.py
import os
import grp
import pwd
import sys

class SudoPrivileges:
    @staticmethod
    def check_user_and_abort_if_root_or_sudo():
        """
        Check if the user executing the script is root or if the script is run with sudo.
        If either condition is met, the script will abort. Otherwise, the function
        will check if the user is a member of the 'www-data' group.
        """
        # Get the current user and their groups
        uid = os.getuid()
        user = pwd.getpwuid(uid).pw_name
        user_groups = [g.gr_name for g in grp.getgrall() if user in g.gr_mem]

        # Check if the user is 'root' or running the script with 'sudo'
        if uid == 0:
            print("Error: This script should not be run as root or with sudo.")
            sys.exit(1)

        # Check if the user is a member of the 'www-data' group
        if 'www-data' in user_groups:
            print("The user '{}' is a member of the 'www-data' group.".format(user))

if __name__ == "__main__":
    SudoPrivileges.check_user_and_abort_if_root_or_sudo()
