FROM python:3.9-slim

WORKDIR /app

# Install ngrok and dependencies
RUN apt-get update && apt-get install -y wget unzip curl jq
RUN wget https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.zip
RUN unzip ngrok-v3-stable-linux-amd64.zip
RUN mv ngrok /usr/local/bin

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# Start both Flask and ngrok
COPY start.sh .
RUN chmod +x start.sh
CMD ["./start.sh"] 