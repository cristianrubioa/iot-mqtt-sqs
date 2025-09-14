# iot-mqtt-sqs
Python-based MQTT data server sending sensor data to AWS IoT and SQS.


## Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│ SimulatedSensor │───▶│ AWSMQTTPublisher │───▶│   AWS IoT Core  │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

- **SimulatedSensor**: Generates realistic sensor data with configurable intervals
- **AWSMQTTPublisher**: Handles secure MQTT connection with automatic reconnection
- **AWS IoT Core**: Receives and processes sensor data in the cloud

## Development

- **Python 3.11.9+** required
- Uses **uv** for dependency management
- **Pydantic** for configuration and data validation
- **paho-mqtt** for MQTT client functionality


## Setup

### 1. AWS IoT Core Certificates

You need to create AWS IoT certificates for secure connection:

1. **Go to AWS IoT Core Console**
   - Navigate to: AWS Console → IoT Core

2. **Create a Device**
   - Click "Connect" → "Connect one device"
   - Name: `your-device-name`
   - Click "Next" → "Auto-generate a new certificate"

3. **Download Certificates**
   - Download all 4 files:
     - `device-certificate.pem.crt` (Device certificate)
     - `private.pem.key` (Private key)
     - `public.pem.key` (Public key - optional)
     - `AmazonRootCA1.pem` (Root CA)

4. **Create `certs/` folder**
   ```bash
   mkdir certs
   # Move downloaded files to certs/ folder
   ```

5. **Activate Certificate**
   - Click "Activate" on the certificate
   - AWS will automatically attach the necessary IoT policies

### 2. Environment Configuration

1. **Copy environment template**
   ```bash
   cp .env.example .env
   ```

2. **Update `.env` with your values**
   - `AWS_MQTT__ENDPOINT`: Your IoT endpoint from AWS Console
   - Certificate paths in `certs/` folder
   - Other configuration as needed

### 3. Install Dependencies

```bash
# Using uv (recommended)
uv sync

# Or using pip
pip install -r requirements.txt
```

### 4. Run

```bash
python main.py
```

## Configuration

All settings are configured via environment variables in `.env`:

```bash
# AWS MQTT Configuration
AWS_MQTT__ENDPOINT=your-iot-endpoint.iot.us-east-1.amazonaws.com
AWS_MQTT__PORT=8883
AWS_MQTT__TOPIC=sdk/test/python
AWS_MQTT__QOS=1
AWS_MQTT__CLIENT_ID=basicPubSub
...
```

## Data Format

The sensor publishes JSON data in this format:

```json
{
  "device_id": "sensor-001",
  "timestamp": "2025-09-14T06:40:23.125288Z",
  "temperature": 23.09,
  "humidity": 40.94
}
```


## Security Note

**⚠️ Never commit certificates or `.env` files to version control!**
They contain sensitive credentials and are already excluded in `.gitignore`.


## Features

- 🌡️ **Simulated sensor data** (temperature & humidity)
- 📡 **AWS IoT Core MQTT** publishing with SSL/TLS
- 🔄 **Automatic reconnection** on network failures
- ⚙️ **Configurable QoS levels** (0, 1, 2)
- 🛡️ **Secure certificate-based authentication**
- 📊 **Structured JSON data** with Pydantic models
