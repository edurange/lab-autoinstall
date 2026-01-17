#!/bin/bash
cat << 'OVERRIDE_EOF' > /etc/systemd/system/getty@tty1.service.d/override.conf
[Unit]
After=systemd-update-utmp-runlevel.service apport.service
Wants=systemd-update-utmp-runlevel.service apport.service
OVERRIDE_EOF

rm -f /etc/systemd/system/cleanup-getty-override.service
rm -f /etc/systemd/system/multi-user.target.wants/cleanup-getty-override.service
rm -f /usr/local/sbin/cleanup-getty-override.sh