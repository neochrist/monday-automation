#!/bin/bash

# Start Flask in the background
python app/app.py &

# Wait for Flask to start
sleep 5
echo "Flask started"

# Start ngrok in the background
ngrok http 8080 &
echo "ngrok started"

# Wait for ngrok to start
sleep 5

# Get the ngrok URL and register webhook
NGROK_URL=$(curl -s http://localhost:4040/api/tunnels | jq -r '.tunnels[0].public_url')
echo "ngrok URL: $NGROK_URL"

# Register webhook with BuildingConnected
echo "Registering webhook..."
curl -X POST "http://localhost:8080/register_webhook" \
    -H "Content-Type: application/json" \
    -d "{\"auth_token\": \"$AUTODESK_TOKEN\"}"

# Keep the container running
tail -f /dev/null 