from src.sensor.simulated import SimulatedSensor
from src.mqtt_publisher.aws import AWSMQTTPublisher
from config import config
import time

def main():
    sensor = SimulatedSensor(device_id=config.sensor.device_id)
    
    with AWSMQTTPublisher() as publisher:
        while True:
            data = sensor.read_data()
            print(f"Generated: {data}")
            
            if publisher.publish(data):
                print("✅ Published to MQTT")
            else:
                print("❌ Failed to publish")
                
            time.sleep(config.sensor.interval)

if __name__ == "__main__":
    main()
