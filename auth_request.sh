#!/bin/bash

curl -v 'https://developer.api.autodesk.com/authentication/v2/token' \
  -X 'POST' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'client_id=rQ1P4LrSWmDSRnZhxjpT1JNAWwbjUfjo6o6ULGDQioh4lw6x' \
  -d 'client_secret=5GpD9K40Zr9OdPB5' \
  -d 'grant_type=client_credentials' \
  -d 'scope=data:read'
