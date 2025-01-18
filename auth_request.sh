#!/bin/bash

curl -v 'https://developer.api.autodesk.com/authentication/v2/token' \
  -X 'POST' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'client_id=test' \
  -d 'client_secret=test' \
  -d 'grant_type=client_credentials' \
  -d 'scope=data:read'
