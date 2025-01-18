# Sample webhook payloads
SAMPLE_BIDDING_WEBHOOK = {
    "state": "BIDDING",
    "company": "Test Construction Corp",
    "email": "contact@testconstruction.com",
    "firstName": "John",
    "lastName": "Builder",
    "companyName": "Test Construction Corp",
    "officeAddress": "123 Build Street, Construction City, CC 12345",
    "client": "Major Development Inc",
    "location": "456 Project Avenue, Development Town, DT 67890",
    "bidDueDate": "2024-02-01",
    "description": "New construction project for commercial building",
    "files": [
        "https://example.com/file1.pdf",
        "https://example.com/file2.pdf"
    ]
}

SAMPLE_PENDING_WEBHOOK = {
    "state": "PENDING",
    "companyName": "Test Construction Corp",
    "description": "Status update to pending"
}