#!/bin/bash
# Diagnostic script to identify SSH disconnection issues

echo "=================================================="
echo "SSH Disconnection Diagnostic Tool"
echo "=================================================="
echo ""

# Check Docker daemon configuration
echo "1. Checking Docker daemon configuration..."
if [ -f /etc/docker/daemon.json ]; then
    echo "   ✓ Docker daemon.json found:"
    cat /etc/docker/daemon.json | sed 's/^/   /'
else
    echo "   ⚠ No /etc/docker/daemon.json found (using defaults)"
fi
echo ""

# Check iptables rules for SSH
echo "2. Checking iptables rules for SSH (port 22)..."
if command -v iptables &> /dev/null; then
    SSH_RULES=$(sudo iptables -L INPUT -n -v | grep -E "22|ssh" || echo "   No SSH-specific rules found")
    echo "$SSH_RULES" | sed 's/^/   /'
    
    # Check if SSH rule is at the top
    FIRST_RULE=$(sudo iptables -L INPUT -n --line-numbers | head -3 | tail -1)
    if echo "$FIRST_RULE" | grep -q "22"; then
        echo "   ✓ SSH rule appears to be prioritized"
    else
        echo "   ⚠ SSH rule may not be prioritized (Docker rules might be first)"
    fi
else
    echo "   ⚠ iptables command not found"
fi
echo ""

# Check Docker network configuration
echo "3. Checking Docker networks..."
docker network ls 2>/dev/null | sed 's/^/   /'
echo ""

# Check for port conflicts
echo "4. Checking for port conflicts..."
PORTS=(22 8000 3306 6379 8080 8081 8082)
for port in "${PORTS[@]}"; do
    if command -v netstat &> /dev/null; then
        result=$(netstat -tuln 2>/dev/null | grep ":$port " || echo "")
    elif command -v ss &> /dev/null; then
        result=$(ss -tuln 2>/dev/null | grep ":$port " || echo "")
    else
        result=""
    fi
    
    if [ -n "$result" ]; then
        echo "   Port $port: IN USE"
        echo "$result" | sed 's/^/     /'
    else
        echo "   Port $port: available"
    fi
done
echo ""

# Check system resources
echo "5. Checking system resources..."
if command -v free &> /dev/null; then
    echo "   Memory:"
    free -h | sed 's/^/     /'
fi
echo ""

if command -v nproc &> /dev/null; then
    CORES=$(nproc)
    echo "   CPU Cores: $CORES"
    echo "   ⚠ Spark workers configured for: ${SPARK_WORKER_CORES:-4} cores each"
    echo "   ⚠ Total Spark cores requested: $(( ${SPARK_WORKER_CORES:-4} * 2 ))"
fi
echo ""

# Check Docker container status
echo "6. Checking Docker container status..."
if docker ps -a 2>/dev/null | grep -q "CONTAINER"; then
    docker ps -a | sed 's/^/   /'
else
    echo "   No containers running"
fi
echo ""

# Recommendations
echo "=================================================="
echo "Recommendations:"
echo "=================================================="
echo ""
echo "If SSH disconnects when starting docker-compose:"
echo ""
echo "1. Preserve SSH rules BEFORE starting:"
echo "   sudo ./scripts/preserve-ssh.sh"
echo ""
echo "2. Reduce Spark worker resources in docker-compose.yml:"
echo "   Set SPARK_WORKER_MEMORY and SPARK_WORKER_CORES environment variables"
echo "   Example: export SPARK_WORKER_MEMORY=1G SPARK_WORKER_CORES=2"
echo ""
echo "3. Configure Docker daemon (if needed):"
echo "   sudo mkdir -p /etc/docker"
echo "   sudo tee /etc/docker/daemon.json > /dev/null <<EOF"
echo "   {"
echo "     \"iptables\": true,"
echo "     \"ip-forward\": true"
echo "   }"
echo "   EOF"
echo "   sudo systemctl restart docker"
echo ""
echo "4. Start services with resource limits:"
echo "   SPARK_WORKER_MEMORY=1G SPARK_WORKER_CORES=2 ./scripts/start.sh"
echo ""




