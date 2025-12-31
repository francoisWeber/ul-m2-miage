#!/bin/sh
set -e

echo "Starting MinIO server..."

# Start MinIO in the background
minio server /data --console-address ":9001" &
MINIO_PID=$!

# Wait for MinIO to be ready
echo "Waiting for MinIO to be ready..."
sleep 5

# Configure mc client
mc alias set local http://localhost:9000 ${MINIO_ROOT_USER} ${MINIO_ROOT_PASSWORD}

# Check if bucket exists, create if needed
if ! mc ls local/beer-dataset >/dev/null 2>&1; then
    echo "Creating beer-dataset bucket..."
    mc mb local/beer-dataset
    
    echo "Uploading beer dataset files..."
    mc cp --recursive /import/ local/beer-dataset/
    
    echo "Setting public read access..."
    mc anonymous set public local/beer-dataset
    
    echo "✅ Bucket setup complete!"
else
    echo "✅ Bucket already exists."
fi

# Always ensure admin user exists (idempotent)
echo "Ensuring admin user exists: ${MINIO_ADMIN_USER}..."
if mc admin user info local ${MINIO_ADMIN_USER} >/dev/null 2>&1; then
    echo "   Admin user already exists."
else
    echo "   Creating admin user..."
    mc admin user add local ${MINIO_ADMIN_USER} ${MINIO_ADMIN_PASSWORD}
    mc admin policy attach local readwrite --user ${MINIO_ADMIN_USER}
    echo "   ✅ Admin user created with read-write access."
fi

echo ""
echo "✅ MinIO is ready!"
echo "   - Students: anonymous read-only access to beer-dataset"
echo "   - Admins: '${MINIO_ADMIN_USER}' user with read-write access"

# Keep MinIO running in foreground
wait $MINIO_PID

