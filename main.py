import threading
import time
from src.sensor.simulated import SimulatedSensor
from src.mqtt_publisher.aws import AWSMQTTPublisher
from src.sqs_client.aws import AWSSQSClient
from config import config

def producer_thread():
    """Producer: generates and sends sensor data to IoT Core only"""
    sensor = SimulatedSensor(device_id=config.sensor.device_id)
    
    with AWSMQTTPublisher() as mqtt_publisher:
        while True:
            data = sensor.read_data()
            print(f"[PRODUCER] Generated: {data}")
            
            success = mqtt_publisher.publish(data)
            status = "successfully" if success else "failed"
            print(f"[PRODUCER] MQTT: {status}")
            print()

def consumer_thread():
    """Consumer: reads and processes SQS messages"""
    sqs_client = AWSSQSClient()
    print("[CONSUMER] SQS Consumer started")
    
    while True:
        messages = sqs_client.receive_messages()
        
        if not messages:
            time.sleep(5)
            continue
            
        for message in messages:
            try:
                import json
                body = json.loads(message["Body"])
                print(f"[CONSUMER] Received: {body}")
                
                receipt_handle = message["ReceiptHandle"]
                if sqs_client.delete_message(receipt_handle):
                    print("[CONSUMER] Message processed and deleted")
                    
            except Exception as e:
                print(f"[CONSUMER] Error: {e}")

def main():
    # Start both threads
    producer = threading.Thread(target=producer_thread, daemon=True)
    consumer = threading.Thread(target=consumer_thread, daemon=True)
    
    producer.start()
    consumer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down...")


if __name__ == "__main__":
    main()
