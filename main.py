from src.sensor.simulated import SimulatedSensor
from config import config
import time

def main():
    sensor = SimulatedSensor(device_id=config.sensor.device_id)
    
    while True:
        data = sensor.generate_data()
        print(f"Generated: {data}")
        # TODO: Send to MQTT publisher
        time.sleep(config.sensor.interval)


if __name__ == "__main__":
    main()
