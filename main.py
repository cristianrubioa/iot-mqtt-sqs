from src.sensor.simulated import SimulatedSensor
from src.mqtt_publisher.aws import AWSMQTTPublisher
from config import config

def main():
    sensor = SimulatedSensor(device_id=config.sensor.device_id)
    
    with AWSMQTTPublisher() as publisher:
        while True:
            data = sensor.read_data()
            print(f"Generated: {data}")
            
            if publisher.publish(data):
                print("Published to MQTT successfully\n")
            else:
                print("Failed to publish to MQTT\n")

if __name__ == "__main__":
    main()
