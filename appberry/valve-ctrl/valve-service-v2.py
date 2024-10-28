import psycopg2
from datetime import datetime
import time
import os
import RPi.GPIO as GPIO
import logging

# Configure logging
logging.basicConfig(
    filename='/home/pi/watering_service.log',  # Path to log file
    level=logging.INFO,  # Log INFO level and above
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Database connection configuration
DB_CONFIG = {
    "dbname": os.getenv("POSTGRES_DB"),
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
    "host": os.getenv("POSTGRES_HOST"),
    "port": os.getenv("POSTGRES_PORT", "5432"),
}

# GPIO setup
GPIO.setmode(GPIO.BCM)  # Use Broadcom pin-numbering
GPIO.setwarnings(False)


def start_watering(relay_port, device_id, device_name):
    """Activates the relay on the specified port."""
    GPIO.setup(relay_port, GPIO.OUT)
    GPIO.output(relay_port, GPIO.HIGH)
    logging.info(f"Watering started  {device_id} {device_name} on relay port {relay_port} .")


def stop_watering(relay_port, device_id, device_name):
    """Deactivates the relay on the specified port."""
    GPIO.output(relay_port, GPIO.LOW)
    logging.info(f"Watering stopped  {device_id} {device_name} on relay port {relay_port} .")


def update_status(cursor, task_id, status):
    """Updates the status of a schedule task."""
    cursor.execute("UPDATE schedule SET status = %s WHERE id = %s", (status, task_id))


def process_tasks():
    """Main loop to check and process scheduled tasks."""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()

        while True:
            now = datetime.now()

            # Check for pending tasks to start
            cursor.execute(
                """
                SELECT s.id, d.relay_port, s.start_date, s.end_date,d.name as device_name,d.id as device_id FROM schedule s 
                JOIN device d ON s.fk_device_schedule = d.id
                WHERE s.status = 'pending' AND s.start_date <= %s
            """,
                (now,),
            )
            pending_tasks = cursor.fetchall()

            for task in pending_tasks:
                task_id, relay_port, start_date, end_date, device_id, device_name = task
                start_watering(relay_port, device_id, device_name)
                update_status(cursor, task_id, "running")
                conn.commit()

            # Check for running tasks to stop
            cursor.execute(
                """
                SELECT s.id, d.relay_port,d.name as device_name,d.id as device_id FROM schedule s 
                JOIN device d ON s.fk_device_schedule = d.id
                WHERE s.status in ('running','pending') AND s.end_date <= %s
            """,
                (now,),
            )
            running_tasks = cursor.fetchall()

            for task in running_tasks:
                task_id, relay_port, device_id, device_name = task
                stop_watering(relay_port, device_id, device_name)
                update_status(cursor, task_id, "complete")
                conn.commit()
            
    except Exception as e:
        logging.info(f"Error: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()
        GPIO.cleanup()


if __name__ == "__main__":
    logging.info("Starting watering service...")
    while (True):  
        process_tasks()
        time.sleep(60) # Sleep for 60 seconds before next check
