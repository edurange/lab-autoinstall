#!/bin/bash
set -euo pipefail

echo "WARNING: This will reset machine identity."
echo "Intended for cloned instances before first use."
echo
read -p "Type 'RESET' to continue: " confirm
[[ "$confirm" == "RESET" ]] || { echo "Aborted."; exit 1; }

echo
read -p "Enter new hostname: " NEW_HOSTNAME
[[ -n "$NEW_HOSTNAME" ]] || { echo "Hostname cannot be empty"; exit 1; }

echo "Stopping services..."
systemctl stop ssh || true
systemctl stop NetworkManager || true

echo "Setting hostname..."
hostnamectl set-hostname "$NEW_HOSTNAME"

sed -i "s/^127\.0\.1\.1.*/127.0.1.1\t$NEW_HOSTNAME/" /etc/hosts || true

echo "Resetting SSH host keys..."
rm -f /etc/ssh/ssh_host_*

echo "Resetting systemd machine-id..."
truncate -s 0 /etc/machine-id
rm -f /var/lib/dbus/machine-id

echo "Resetting NetworkManager identity..."
rm -f /etc/NetworkManager/system-connections/*.nmconnection
rm -f /var/lib/NetworkManager/*.lease
rm -f /var/lib/NetworkManager/*.state

if command -v cloud-init >/dev/null 2>&1; then
  echo "Resetting cloud-init state..."
  cloud-init clean --logs --machine-id
fi

echo
echo "Identity reset complete."
echo "Reboot REQUIRED to regenerate identities."
