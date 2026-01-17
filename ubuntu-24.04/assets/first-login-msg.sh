#!/bin/sh
cat << 'MSG'

Welcome! This system was installed using a default sysadmin account.
Please create your own user before starting work.

  1. Create a user account:
      sudo adduser <newuser>

  2. Add the user to the 'sudo' group for administrative privileges:
      sudo usermod -aG sudo <newuser>

  3. Verify the changes:
      id <newuser>
      groups <newuser>
    ... should include your new username, and the group 'sudo'

  4. Enable and start the ssh server:
      sudo systemctl enable --now ssh.service

After completing these steps, you can remove this message by running:
  sudo rm /etc/profile.d/first-login-msg.sh

MSG