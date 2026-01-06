#!/bin/bash
# Preserve SSH rules in iptables before Docker starts
# This prevents Docker from blocking SSH connections

set -e

echo "Preserving SSH rules in iptables..."

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo "This script must be run as root (use sudo)"
    echo "Run: sudo ./scripts/preserve-ssh.sh"
    exit 1
fi

# Ensure SSH rules are at the top of INPUT chain (before Docker rules)
# This ensures SSH traffic is allowed even if Docker modifies iptables
iptables -C INPUT -p tcp --dport 22 -j ACCEPT 2>/dev/null || \
    iptables -I INPUT 1 -p tcp --dport 22 -j ACCEPT

# Also ensure SSH is allowed in FORWARD chain
iptables -C FORWARD -p tcp --dport 22 -j ACCEPT 2>/dev/null || \
    iptables -I FORWARD 1 -p tcp --dport 22 -j ACCEPT

# Save iptables rules (if iptables-persistent is installed)
if command -v netfilter-persistent &> /dev/null; then
    netfilter-persistent save
elif command -v iptables-save &> /dev/null; then
    iptables-save > /etc/iptables/rules.v4 2>/dev/null || true
fi

echo "SSH rules preserved successfully!"
echo "You can now safely start docker-compose"




