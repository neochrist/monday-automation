from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import logging
import requests
import os
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app, origins=["*"])

# Monday.com configuration
MONDAY_API_TOKEN = os.environ.get('MONDAY_API_TOKEN')
MONDAY_API_URL = "https://api.monday.com/v2"
MONDAY_BOARD_ID = os.environ.get('MONDAY_BOARD_ID')

# Add TEST_MODE to environment
TEST_MODE = os.environ.get('TEST_MODE', 'false').lower() == 'true'

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy"}), 200

@app.route('/register_webhook', methods=['POST'])
def register_webhook():
    """Register webhook with BuildingConnected"""
    try:
        data = request.json
        auth_token = data.get('auth_token')
        
        if not auth_token:
            return jsonify({"error": "No auth token provided"}), 400

        # Get ngrok URL from environment or request
        ngrok_url = os.environ.get('NGROK_URL', '')
        if not ngrok_url:
            tunnels = requests.get('http://localhost:4040/api/tunnels').json()
            ngrok_url = tunnels['tunnels'][0]['public_url']

        # Register webhook with BuildingConnected
        headers = {
            "Authorization": f"Bearer {auth_token}",
            "Content-Type": "application/json"
        }
        
        webhook_data = {
            "callbackUrl": f"{ngrok_url}/webhook",
            "events": ["opportunity.state.changed"]
        }

        logger.info(f"Registering webhook with callback URL: {webhook_data['callbackUrl']}")
        
        response = requests.post(
            "https://developer.api.autodesk.com/webhooks/v1/systems/buildingconnected/events/opportunity.state.changed/hooks",
            headers=headers,
            json=webhook_data
        )
        
        if response.status_code == 201:
            return jsonify({"status": "success", "webhook_url": webhook_data['callbackUrl']}), 201
        else:
            logger.error(f"Failed to register webhook: {response.status_code} {response.text}")
            return jsonify({"error": f"Failed to register webhook: {response.text}"}), response.status_code

    except Exception as e:
        logger.error(f"Error registering webhook: {str(e)}")
        return jsonify({"error": str(e)}), 500

def create_monday_item(opportunity_data):
    """Create a new item in Monday.com board"""
    query = """
    mutation ($boardId: Int!, $itemName: String!, $columnValues: JSON!) {
        create_item (
            board_id: $boardId,
            item_name: $itemName,
            column_values: $columnValues
        ) {
            id
        }
    }
    """
    
    variables = {
        "boardId": int(MONDAY_BOARD_ID),
        "itemName": opportunity_data.get('companyName', 'Unknown Company'),
        "columnValues": json.dumps({
            "email": {"email": opportunity_data.get('email', '')},
            "text": f"{opportunity_data.get('firstName', '')} {opportunity_data.get('lastName', '')}",
            "text1": opportunity_data.get('officeAddress', ''),
            "text2": opportunity_data.get('client', ''),
            "text3": opportunity_data.get('location', ''),
            "date4": opportunity_data.get('bidDueDate', ''),
            "long_text": opportunity_data.get('description', '')
        })
    }
    
    headers = {
        "Authorization": MONDAY_API_TOKEN,
        "Content-Type": "application/json"
    }
    
    response = requests.post(MONDAY_API_URL, json={"query": query, "variables": variables}, headers=headers)
    
    if response.status_code == 200:
        result = response.json()
        if result.get('data', {}).get('create_item', {}).get('id'):
            return result['data']['create_item']['id']
    return None

def upload_files_to_monday(item_id, files):
    """Upload files to Monday.com item"""
    for file_url in files:
        # Download file from BuildingConnected
        file_response = requests.get(file_url)
        if file_response.status_code == 200:
            # Upload to Monday.com
            query = """
            mutation ($file: File!) {
                add_file_to_column (
                    item_id: %s,
                    column_id: "files",
                    file: $file
                ) {
                    id
                }
            }
            """ % item_id
            
            files = {
                'query': (None, query),
                'variables[file]': (os.path.basename(file_url), file_response.content)
            }
            
            headers = {
                "Authorization": MONDAY_API_TOKEN
            }
            
            response = requests.post(MONDAY_API_URL, headers=headers, files=files)
            if response.status_code != 200:
                logger.error(f"Failed to upload file {file_url}")

@app.route('/webhook', methods=['POST'])
def handle_webhook():
    """Handle incoming webhooks from BuildingConnected"""
    data = request.json
    logger.info("Received webhook payload:")
    logger.info(json.dumps(data, indent=2))
    
    if data.get('state') == 'BIDDING' or data.get('submissionState') == 'BIDDING':
        # If in test mode, return success without creating Monday.com item
        if TEST_MODE:
            logger.info("Test mode: Skipping Monday.com integration")
            return jsonify({
                "status": "test_success",
                "message": "Webhook received successfully in test mode"
            }), 200
            
        # Create item in Monday.com
        item_id = create_monday_item(data)
        if item_id:
            # Upload files if available
            if 'files' in data:
                upload_files_to_monday(item_id, data['files'])
            return jsonify({"status": "created", "monday_item_id": item_id}), 200
        else:
            return jsonify({"status": "error", "message": "Failed to create Monday.com item"}), 500
    
    return jsonify({"status": "received"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
