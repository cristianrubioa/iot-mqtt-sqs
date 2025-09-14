from src.sensor.simulated import SimulatedSensor
from src.mqtt_publisher.aws import AWSMQTTPublisher
from src.sqs_client.aws import AWSSQSClient
from config import config

def main():
    sensor = SimulatedSensor(device_id=config.sensor.device_id)
    sqs_client = AWSSQSClient()
    
    with AWSMQTTPublisher() as mqtt_publisher:
        while True:
            data = sensor.read_data()
            print(f"Generated: {data}")
            
            # Publish to services
            services = [
                ("MQTT", mqtt_publisher.publish),
                ("SQS", sqs_client.send_message)
            ]
            
            for service_name, publish_func in services:
                success = publish_func(data)
                status = "successfully" if success else "failed"
                print(f"{service_name}: {status}")

            print()

if __name__ == "__main__":
    main()
