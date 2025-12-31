#!/bin/sh
set -e

echo "Starting MinIO server..."

# Start MinIO in the background
minio server /data --console-address ":9001" &
MINIO_PID=$!

# Wait for MinIO to be ready
echo "Waiting for MinIO to be ready..."
sleep 5

# Check if this is first run (bucket doesn't exist)
if ! mc ls local/beer-dataset >/dev/null 2>&1; then
    echo "First run detected - setting up beer-dataset bucket..."
    
    # Configure mc client
    mc alias set local http://localhost:9000 ${MINIO_ROOT_USER} ${MINIO_ROOT_PASSWORD}
    
    # Create bucket
    echo "Creating beer-dataset bucket..."
    mc mb local/beer-dataset
    
    # Copy files
    echo "Uploading beer dataset files..."
    mc cp --recursive /import/ local/beer-dataset/
    
    # Set public read access (anonymous download)
    echo "Setting public read access (anonymous/no credentials)..."
    mc anonymous set public local/beer-dataset
    
    echo "✅ Setup complete! Beer dataset is ready for anonymous read access."
else
    echo "✅ Bucket already exists, skipping setup."
fi

# Keep MinIO running in foreground
wait $MINIO_PID

