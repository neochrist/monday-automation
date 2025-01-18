# BuildingConnected to Monday.com Integration

## Overview
This project creates an automated system that listens for changes in BuildingConnected opportunities and automatically creates corresponding entries in Monday.com when an opportunity's state changes to "BIDDING".

## Components
1. Flask Application (Backend Server)
2. ngrok (Tunnel Service)
3. BuildingConnected Webhook
4. Monday.com API Integration

## Detailed Process Flow

### 1. Initial Setup
- Docker container starts up with:
  - Flask application
  - ngrok service
  - Required environment variables (tokens, IDs)

### 2. Webhook Registration
1. Flask server starts on port 8080
2. ngrok creates a public URL pointing to our Flask server
3. System automatically registers this URL with BuildingConnected's webhook service
4. BuildingConnected now knows where to send notifications

### 3. Webhook Processing
When an opportunity in BuildingConnected changes state:
1. BuildingConnected sends a POST request to our ngrok URL
2. ngrok forwards this to our Flask application
3. Flask processes the webhook data

### 4. Business Logic
The application checks:
1. Is the state "BIDDING"?
2. Is this a duplicate entry?
3. Are all required fields present?

### 5. Monday.com Integration
If all checks pass, the system:
1. Creates a new item in Monday.com board
2. Maps the following fields:
   - Email
   - First Name + Last Name
   - Company Name
   - Office Address
   - Client
   - Complete Location
   - Bid Due Date
   - Description
3. Handles file attachments:
   - Downloads files from BuildingConnected
   - Uploads them to Monday.com

## Technical Details

### Environment Variables Required 